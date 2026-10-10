// All times below are software observations. No GPU FPS or visual latency is inferred.
export function distribution(values) {
  const sorted = values.filter(Number.isFinite).sort((a, b) => a - b);
  const percentile = q => sorted.length ? sorted[Math.ceil(q * sorted.length) - 1] : null;
  return { count: sorted.length, p50: percentile(0.5), p95: percentile(0.95),
    p99: percentile(0.99), max: sorted.at(-1) ?? null };
}

export function eventClock(timestamp, enteredAt, timeOrigin) {
  const at = timestamp > 1e12 ? timestamp - timeOrigin : timestamp;
  return Number.isFinite(at) && at >= 0 && at <= enteredAt + 1 ? at : null;
}

export function readCamera(map) {
  const center = map.getCenter();
  return { center: [center.lng, center.lat], zoom: map.getZoom(),
    bearing: map.getBearing(), pitch: map.getPitch(), roll: map.getRoll?.() ?? 0 };
}

export function cameraDifference(before, after, project) {
  const angle = (a, b) => Math.abs((((a - b + 180) % 360) + 360) % 360 - 180);
  const a = project(before.center), b = project(after.center);
  return { centerCssPixels: Math.hypot(a.x - b.x, a.y - b.y),
    zoom: Math.abs(after.zoom - before.zoom), bearing: angle(after.bearing, before.bearing),
    pitch: Math.abs(after.pitch - before.pitch), roll: angle(after.roll ?? 0, before.roll ?? 0) };
}

function changed(a, b) { return JSON.stringify(a) !== JSON.stringify(b); }

export class Recorder {
  constructor({ now = () => performance.now(), timeOrigin = performance.timeOrigin,
    capacity = 60000 } = {}) {
    this.now = now; this.timeOrigin = timeOrigin; this.capacity = capacity;
    this.runs = []; this.active = null; this.events = new WeakMap();
    this.errors = []; this.contextLosses = 0; this.restorations = 0;
  }
  start(context, camera, options = {}) {
    if (this.active) throw new Error('A run is already recording');
    const run = {
      id: this.runs.length + 1, startedAt: this.now(), finishedAt: null,
      conditions: structuredClone(context), repetition: options.repetition ?? 1,
      purpose: options.purpose ?? 'gestures', initialCamera: structuredClone(camera),
      finalCamera: null, inputs: [], renderIntervalsMs: [], activeRenderIntervalsMs: [],
      commands: [], stabilityWindows: [], settleObservations: [], zoomAnchors: [], longTasks: [],
      resourceActivity: 0, invalidReasons: [], warnings: [],
      userAssessment: null, visualAcceptance: 'pending',
    };
    this.runs.push(run); this.active = run; this.events = new WeakMap();
    this.lastCamera = structuredClone(camera); this.renderedCamera = structuredClone(camera);
    this.lastRender = null; this.lastActiveRender = null; this.lastInput = null;
    this.gesture = null; this.waiting = []; this.stabilityPending = null;
    if (!context.ready) this.invalidate('not-ready-at-start');
    if (context.deviceClass === 'unclassified') this.invalidate('device-class-unclassified');
    if (context.cacheState !== 'warm') this.warn('not-a-declared-warm-run');
    if (context.inputDevice === 'unclassified') this.warn('input-device-unclassified');
    return run;
  }
  add(list, value) {
    if (list.length >= this.capacity) { this.invalidate('diagnostic-buffer-overflow'); return false; }
    list.push(value); return true;
  }
  invalidate(reason) {
    if (this.active && !this.active.invalidReasons.includes(reason)) this.active.invalidReasons.push(reason);
  }
  warn(reason) {
    if (this.active && !this.active.warnings.includes(reason)) this.active.warnings.push(reason);
  }
  input(event, kind) {
    if (!this.active) return;
    const enteredAt = this.now();
    const inputAt = eventClock(event.timeStamp, enteredAt, this.timeOrigin);
    if (inputAt === null) this.invalidate('input-clock-incompatible');
    if (!this.gesture || this.gesture.kind !== kind || enteredAt - this.gesture.lastAt > 250) {
      this.gesture = { kind, onsetAt: inputAt, lastAt: enteredAt, rendered: false };
    }
    this.gesture.lastAt = enteredAt;
    const sample = { kind, inputAt, enteredAt, dispatchDelayMs: inputAt === null ? null : Math.max(0, enteredAt - inputAt),
      cameraChangeAt: null, renderAt: null, inputToCameraRenderProxyMs: null,
      cameraToRenderMs: null, gestureOnsetToRenderProxyMs: null };
    if (this.add(this.active.inputs, sample)) {
      this.events.set(event, { sample, gesture: this.gesture }); this.lastInput = sample;
    }
  }
  cameraChange(camera, originalEvent) {
    if (!this.active || !changed(camera, this.lastCamera)) return;
    this.cancelStability('interrupted-by-camera-change'); this.lastCamera = structuredClone(camera);
    const match = originalEvent && this.events.get(originalEvent);
    if (match && match.sample.cameraChangeAt === null) {
      match.sample.cameraChangeAt = this.now(); this.waiting.push(match);
    }
  }
  render(camera, moving) {
    if (!this.active) return;
    const at = this.now();
    if (this.lastRender !== null) this.add(this.active.renderIntervalsMs, at - this.lastRender);
    this.lastRender = at;
    const cameraChanged = changed(camera, this.renderedCamera);
    if (moving || cameraChanged) {
      if (this.lastActiveRender !== null) this.add(this.active.activeRenderIntervalsMs, at - this.lastActiveRender);
      this.lastActiveRender = at;
    } else this.lastActiveRender = null;
    // A resource-only render or a command without matching originalEvent cannot qualify an input.
    if (!cameraChanged) return;
    for (const { sample, gesture } of this.waiting) {
      sample.renderAt = at;
      sample.inputToCameraRenderProxyMs = sample.inputAt === null ? null : Math.max(0, at - sample.inputAt);
      sample.cameraToRenderMs = at - sample.cameraChangeAt;
      if (!gesture.rendered && gesture.onsetAt !== null) {
        sample.gestureOnsetToRenderProxyMs = at - gesture.onsetAt; gesture.rendered = true;
      }
    }
    this.waiting = []; this.renderedCamera = structuredClone(camera);
  }
  cancelStability(reason) {
    if (this.stabilityPending) { this.stabilityPending.status = reason; this.stabilityPending = null; }
  }
  movementEnded(camera) {
    if (!this.active) return null;
    this.cancelStability('superseded-by-another-endpoint');
    if (this.lastInput) this.add(this.active.settleObservations, {
      kind: this.lastInput.kind, lastInputEnteredAt: this.lastInput.enteredAt,
      moveEndAt: this.now(), sinceLastInputMs: this.now() - this.lastInput.enteredAt,
      caveat: 'Moveend observation; inspect sequence for interruption, inertia or programmatic movement',
    });
    const window = { at: this.now(), camera: structuredClone(camera), status: 'pending', drift: null, actualWindowMs: null };
    this.add(this.active.stabilityWindows, window); this.stabilityPending = window;
    return window;
  }
  completeStability(window, camera, project) {
    if (!this.active || this.stabilityPending !== window) return;
    window.actualWindowMs = this.now() - window.at;
    window.drift = cameraDifference(window.camera, camera, project); window.status = 'measured';
    this.stabilityPending = null;
  }
  command(id, target, mode, requestedDurationMs, effectiveDurationMs) {
    if (!this.active) return;
    this.add(this.active.commands, { id, target: structuredClone(target), mode, requestedDurationMs,
      effectiveDurationMs, startedAt: this.now(), endedAt: null, durationMs: null,
      endpointDifference: null, status: 'pending' });
  }
  commandEnded(id, camera, project) {
    const command = this.active?.commands.find(item => item.id === id && item.endedAt === null);
    if (!command) return;
    command.endedAt = this.now(); command.durationMs = command.endedAt - command.startedAt;
    command.endpointDifference = cameraDifference(command.target, camera, project);
    const d = command.endpointDifference;
    command.status = d.centerCssPixels <= 1 && d.zoom <= 0.001 && d.bearing <= 0.1 && d.pitch <= 0.1
      ? 'target-reached' : 'interrupted-or-target-not-reached';
  }
  error(phase, status = null) {
    // Callers pass fixed phase labels, never SDK exception messages or URLs.
    this.errors.push({ phase, httpStatus: Number.isInteger(status) ? status : null, at: this.now() });
    this.invalidate('rendering-or-resource-error');
  }
  finish(camera, reason = 'completed') {
    if (!this.active) return null;
    const run = this.active;
    this.cancelStability('recording-ended-before-stability-window');
    for (const command of run.commands) if (command.status === 'pending') command.status = 'recording-ended-before-command';
    run.finishedAt = this.now(); run.durationMs = run.finishedAt - run.startedAt;
    run.finalCamera = structuredClone(camera); run.finishReason = reason;
    if (reason !== 'completed') this.invalidate('recording-stopped-early');
    const matched = run.inputs.filter(x => x.renderAt !== null);
    run.metrics = {
      dispatchDelayMs: distribution(run.inputs.map(x => x.dispatchDelayMs)),
      inputToCameraRenderProxyMs: distribution(matched.map(x => x.inputToCameraRenderProxyMs)),
      gestureOnsetToRenderProxyMs: distribution(matched.map(x => x.gestureOnsetToRenderProxyMs)),
      cameraToRenderMs: distribution(matched.map(x => x.cameraToRenderMs)),
      activeRenderIntervalsMs: distribution(run.activeRenderIntervalsMs),
      allRenderIntervalsMs: distribution(run.renderIntervalsMs),
      byInputKind: Object.fromEntries([...new Set(run.inputs.map(x => x.kind))].map(kind => [kind,
        distribution(matched.filter(x => x.kind === kind).map(x => x.inputToCameraRenderProxyMs))])),
      matchedInputCount: matched.length, unmatchedInputCount: run.inputs.length - matched.length,
    };
    if (!matched.length) this.warn('no-matched-native-inputs');
    if (!run.stabilityWindows.some(x => x.status === 'measured')) this.warn('no-completed-stability-window');
    run.machineMeasurementClass = run.invalidReasons.length ? 'invalid-for-reference-comparison' : 'software-proxies-only';
    this.active = null; this.waiting = []; return run;
  }
}

export function attachDiagnostics(map, recorder, { environment, configuration, ready, onRunFinished }) {
  let downOnMap = false, finishTimer = null, stabilityTimer = null, zoomAnchor = null;
  const canvas = map.getCanvas(), cleanup = [];
  const listen = (target, event, callback) => {
    target.addEventListener(event, callback, { capture: true, passive: true });
    cleanup.push(() => target.removeEventListener(event, callback, true));
  };
  listen(window, 'mousedown', event => { downOnMap = canvas.contains(event.target); });
  listen(window, 'mouseup', () => { downOnMap = false; recorder.gesture = null; });
  listen(window, 'blur', () => { downOnMap = false; recorder.invalidate('window-blurred'); });
  listen(window, 'mousemove', event => {
    if (downOnMap && event.buttons) {
      if (zoomAnchor) { zoomAnchor.status = 'interrupted-by-other-input'; zoomAnchor = null; }
      recorder.input(event, event.ctrlKey || (event.buttons & 2) ? 'rotate-pitch' : 'drag');
    }
  });
  listen(canvas, 'wheel', event => {
    if (!event.deltaY && !event.deltaX) return;
    recorder.input(event, 'wheel');
    if (!recorder.active || map.getPitch() !== 0) return;
    const rect = canvas.getBoundingClientRect(), point = { x: event.clientX - rect.left, y: event.clientY - rect.top };
    if (!zoomAnchor || recorder.now() - zoomAnchor.lastWheelAt > 350) {
      if (zoomAnchor) zoomAnchor.status = 'superseded-by-next-wheel-sequence';
      const geo = map.unproject(point);
      zoomAnchor = { point, coordinate: [geo.lng, geo.lat], lastWheelAt: recorder.now(), status: 'pending', driftCssPixels: null };
      recorder.add(recorder.active.zoomAnchors, zoomAnchor);
    } else if (Math.hypot(point.x - zoomAnchor.point.x, point.y - zoomAnchor.point.y) > 0.5) {
      zoomAnchor.status = 'pointer-moved-during-wheel-sequence';
    }
    zoomAnchor.lastWheelAt = recorder.now();
  });
  listen(canvas, 'keydown', event => {
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', '+', '-', '='].includes(event.key)) {
      if (zoomAnchor) { zoomAnchor.status = 'interrupted-by-other-input'; zoomAnchor = null; }
      recorder.input(event, 'keyboard');
    }
  });
  listen(document, 'visibilitychange', () => { if (document.hidden) recorder.invalidate('hidden-tab'); });
  listen(window, 'error', () => recorder.error('browser-script-or-resource-error'));
  listen(window, 'unhandledrejection', () => recorder.error('browser-unhandled-rejection'));
  listen(window, 'resize', () => recorder.invalidate('viewport-or-dpr-changed'));
  listen(canvas, 'webglcontextlost', () => { recorder.contextLosses++; recorder.invalidate('webgl-context-lost'); });
  listen(canvas, 'webglcontextrestored', () => { recorder.restorations++; recorder.invalidate('webgl-context-restored'); });
  const handlers = {
    move: event => recorder.cameraChange(readCamera(map), event.originalEvent),
    render: () => {
      if (recorder.active && devicePixelRatio !== recorder.active.conditions.environment.devicePixelRatio) recorder.invalidate('viewport-or-dpr-changed');
      recorder.render(readCamera(map), map.isMoving());
    },
    movestart: () => {
      clearTimeout(stabilityTimer); recorder.cancelStability('interrupted-by-movement');
      // Maps need not render while idle. Never count the idle gap between gestures as an active frame stall.
      recorder.lastActiveRender = null;
    },
    moveend: event => {
      if (event.stage1cCommand) recorder.commandEnded(event.stage1cCommand, readCamera(map), point => map.project(point));
      if (zoomAnchor && event.originalEvent?.type === 'wheel') {
        if (zoomAnchor.status === 'pending') {
          const point = map.project(zoomAnchor.coordinate);
          zoomAnchor.driftCssPixels = Math.hypot(point.x - zoomAnchor.point.x, point.y - zoomAnchor.point.y);
          zoomAnchor.settleAfterLastWheelMs = recorder.now() - zoomAnchor.lastWheelAt;
          zoomAnchor.status = 'measured-flat-ground-anchor';
        }
        zoomAnchor = null;
      } else if (zoomAnchor && event.stage1cCommand) {
        zoomAnchor.status = 'interrupted-by-command'; zoomAnchor = null;
      }
      const window = recorder.movementEnded(readCamera(map));
      clearTimeout(stabilityTimer);
      if (window) stabilityTimer = setTimeout(() => recorder.completeStability(window, readCamera(map), point => map.project(point)), 2000);
    },
    dataloading: () => { if (recorder.active) recorder.active.resourceActivity++; },
    resize: () => recorder.invalidate('viewport-or-dpr-changed'),
    error: event => recorder.error('sdk-resource-or-render', event.error?.status),
  };
  for (const [event, handler] of Object.entries(handlers)) map.on(event, handler);
  let observer = null;
  const longTasks = entries => {
    if (!recorder.active) return;
    for (const entry of entries) if (entry.startTime >= recorder.active.startedAt) {
      recorder.add(recorder.active.longTasks, { startTime: entry.startTime, duration: entry.duration });
    }
  };
  if (globalThis.PerformanceObserver?.supportedEntryTypes?.includes('longtask')) {
    observer = new PerformanceObserver(list => longTasks(list.getEntries()));
    observer.observe({ type: 'longtask' });
  }
  const finish = reason => {
    clearTimeout(finishTimer); clearTimeout(stabilityTimer);
    if (observer) longTasks(observer.takeRecords());
    if (map.isMoving()) recorder.invalidate('camera-still-moving-at-finish');
    if (zoomAnchor) { zoomAnchor.status = 'recording-ended-before-wheel-settle'; zoomAnchor = null; }
    const run = recorder.finish(readCamera(map), reason); if (run) onRunFinished(run); return run;
  };
  return {
    start(options) {
      if (!ready()) throw new Error('Wait for complete tiles, idle and fonts with no errors');
      const context = { ...configuration(), ...options, environment: environment(), ready: ready(),
        startedAtUtc: new Date().toISOString(), longTaskObserverAvailable: !!observer };
      if (document.hidden || !document.hasFocus()) throw new Error('Focus the visible experiment tab first');
      const run = recorder.start(context, readCamera(map), options);
      zoomAnchor = null;
      finishTimer = setTimeout(() => finish('completed'), options.durationMs); return run;
    },
    finish: () => finish('operator-stopped'),
    dispose() {
      finish('page-disposed'); observer?.disconnect(); cleanup.forEach(fn => fn());
      for (const [event, handler] of Object.entries(handlers)) map.off(event, handler);
    },
  };
}
