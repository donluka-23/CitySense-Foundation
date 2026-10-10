import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { configuration, applyCamera, extrusionInventory, setBuildingVisibility, runOptions } from '../navigation.mjs';
import { Recorder, attachDiagnostics, distribution, eventClock, cameraDifference } from '../diagnostics.mjs';

const presets = JSON.parse(await readFile(new URL('../../../docs/design/MAP_CAMERA_PRESETS.json', import.meta.url), 'utf8'));
const base = { center: [41.64, 41.65], zoom: 16, bearing: 0, pitch: 0, roll: 0 };
const moved = { ...base, center: [41.641, 41.65] };
const project = ([x, y]) => ({ x: x * 1000, y: y * 1000 });
function recording(options = {}) {
  let at = 100;
  const recorder = new Recorder({ now: () => at, timeOrigin: 1700000000000, ...options });
  recorder.start({ ready: true, deviceClass: 'physical-desktop', cacheState: 'warm', inputDevice: 'mouse' }, base);
  return { recorder, at: value => { at = value; } };
}

test('All twelve canonical cameras preserve exact supplied coordinates and parameters', () => {
  for (const preset of ['overview', 'waterfront', 'central', 'street']) for (const condition of ['2d', 'detail', '3d']) {
    const config = configuration(new URLSearchParams({ preset, condition }), presets);
    assert.deepEqual(config.camera, { center: presets.locations[preset].center, ...presets.locations[preset].cameras[condition] });
    assert.equal(config.buildings, condition === '3d');
  }
});

test('Invalid settings are rejected before renderer construction', () => {
  for (const query of ['preset=__proto__', 'condition=other', 'motion=orbit', 'duration=', 'duration=NaN', 'duration=-1', 'dpr=0', 'dpr=Infinity', 'buildings=true']) {
    assert.throws(() => configuration(new URLSearchParams(query), presets));
  }
});

test('Immediate and reduced-motion changes never call the animation API', () => {
  for (const [motion, reduced] of [['immediate', false], ['short', true]]) {
    const calls = [];
    const map = { jumpTo: (...args) => calls.push(args), easeTo: () => assert.fail('unexpected animation') };
    const config = configuration(new URLSearchParams({ motion }), presets);
    assert.equal(applyCamera(map, config, reduced, 7), 0);
    assert.deepEqual(calls, [[config.camera, { stage1cCommand: 7 }]]);
  }
});

test('Short transitions use the requested native candidate without flight or timer updates', () => {
  for (const duration of [150, 400, 650]) {
    const calls = [];
    const map = { easeTo: (...args) => calls.push(args), jumpTo: () => assert.fail('unexpected jump') };
    const config = configuration(new URLSearchParams({ motion: 'short', duration: String(duration) }), presets);
    assert.equal(applyCamera(map, config, false, 8), duration);
    assert.deepEqual(calls, [[{ ...config.camera, duration, essential: false }, { stage1cCommand: 8 }]]);
  }
});

test('Matched building-load controls preserve supplied visibility and style semantics', () => {
  const style = { layers: [
    { id: 'flat', type: 'fill' },
    { id: 'visible', type: 'fill-extrusion', minzoom: 15, paint: { 'fill-extrusion-height': ['get', 'height'] } },
    { id: 'hidden', type: 'fill-extrusion', layout: { visibility: 'none' } },
  ] };
  const before = structuredClone(style), calls = [], layers = extrusionInventory(style);
  const map = { setLayoutProperty: (...args) => calls.push(args) };
  setBuildingVisibility(map, layers, false); setBuildingVisibility(map, layers, true);
  assert.deepEqual(calls, [['visible', 'visibility', 'none'], ['hidden', 'visibility', 'none'],
    ['visible', 'visibility', 'visible'], ['hidden', 'visibility', 'none']]);
  assert.deepEqual(style, before); assert.equal(layers[0].minzoom, 15);
  assert.deepEqual(extrusionInventory({ layers: [] }), []);
});

test('Empty distributions are unavailable rather than invented zero measurements', () => {
  assert.deepEqual(distribution([]), { count: 0, p50: null, p95: null, p99: null, max: null });
  const d = distribution(Array.from({ length: 100 }, (_, index) => index + 1));
  assert.deepEqual(d, { count: 100, p50: 50, p95: 95, p99: 99, max: 100 });
});

test('Input clocks handle monotonic and epoch origins, and reject impossible timestamps', () => {
  assert.equal(eventClock(90, 100, 1700000000000), 90);
  assert.equal(eventClock(1700000000090, 100, 1700000000000), 90);
  assert.equal(eventClock(1000, 100, 1700000000000), null);
  assert.equal(eventClock(-1, 100, 1700000000000), null);
});

test('Only an originalEvent-matched camera change followed by a changed-camera render qualifies input', () => {
  const { recorder, at } = recording(); const event = { timeStamp: 95 };
  recorder.input(event, 'drag'); at(105); recorder.render(base, false);
  assert.equal(recorder.active.inputs[0].renderAt, null);
  at(110); recorder.cameraChange(moved, event); at(120); recorder.render(moved, true);
  at(130); recorder.cameraChange({ ...moved, zoom: 16.1 }, event); at(140); recorder.render({ ...moved, zoom: 16.1 }, true);
  const run = recorder.finish(moved);
  assert.equal(run.metrics.matchedInputCount, 1);
  assert.equal(run.inputs[0].dispatchDelayMs, 5);
  assert.equal(run.inputs[0].inputToCameraRenderProxyMs, 25);
  assert.equal(run.inputs[0].cameraToRenderMs, 10);
  assert.equal(run.inputs[0].renderAt, 120);
});

test('A programmatic camera change cannot certify unrelated input latency', () => {
  const { recorder, at } = recording(); recorder.input({ timeStamp: 95 }, 'wheel');
  at(110); recorder.cameraChange(moved); at(120); recorder.render(moved, true);
  const run = recorder.finish(moved);
  assert.equal(run.metrics.matchedInputCount, 0); assert.equal(run.metrics.unmatchedInputCount, 1);
  assert.equal(run.metrics.inputToCameraRenderProxyMs.p95, null);
});

test('Coalesced input is reported; gesture onset retains earlier waiting time', () => {
  const { recorder, at } = recording();
  recorder.input({ timeStamp: 95 }, 'drag'); at(110);
  const latest = { timeStamp: 105 }; recorder.input(latest, 'drag');
  at(120); recorder.cameraChange(moved, latest); at(130); recorder.render(moved, true);
  const run = recorder.finish(moved);
  assert.equal(run.metrics.unmatchedInputCount, 1);
  assert.equal(run.inputs[1].inputToCameraRenderProxyMs, 25);
  assert.equal(run.inputs[1].gestureOnsetToRenderProxyMs, 35);
});

test('Sample overflow invalidates the run rather than silently improving metrics', () => {
  const { recorder } = recording({ capacity: 1 });
  recorder.input({ timeStamp: 90 }, 'drag'); recorder.input({ timeStamp: 91 }, 'drag');
  assert.ok(recorder.finish(base).invalidReasons.includes('diagnostic-buffer-overflow'));
});

test('Stability uses a completed two-second endpoint window and circular bearing difference', () => {
  const { recorder, at } = recording(); const window = recorder.movementEnded(base);
  at(2100); recorder.completeStability(window, { ...base, bearing: 359.99 }, project);
  assert.equal(window.status, 'measured'); assert.equal(window.actualWindowMs, 2000);
  assert.ok(Math.abs(window.drift.bearing - 0.01) < 1e-8);
  assert.equal(window.drift.centerCssPixels, 0);
  assert.equal(cameraDifference(base, moved, project).centerCssPixels, 1);
  assert.equal(cameraDifference(base, { ...base, bearing: -720 }, project).bearing, 0);
});

test('Movement invalidates an unfinished stability window', () => {
  const { recorder, at } = recording(); const window = recorder.movementEnded(base);
  at(200); recorder.cameraChange(moved, null); at(2200); recorder.completeStability(window, moved, project);
  assert.equal(window.status, 'interrupted-by-camera-change'); assert.equal(window.drift, null);
});

test('Command endpoints distinguish completed and interrupted native transitions', () => {
  const { recorder, at } = recording();
  recorder.command(1, moved, 'short', 400, 400); at(500); recorder.commandEnded(1, moved, project);
  recorder.command(2, { ...base, zoom: 17 }, 'short', 400, 400); at(550); recorder.commandEnded(2, moved, project);
  const [completed, interrupted] = recorder.finish(moved).commands;
  assert.equal(completed.durationMs, 400); assert.equal(completed.status, 'target-reached');
  assert.equal(interrupted.status, 'interrupted-or-target-not-reached');
  assert.equal(interrupted.durationMs, 50);
});

test('Early completion and unavailable environment are explicitly invalid', () => {
  const { recorder } = recording(); recorder.invalidate('hidden-tab');
  const run = recorder.finish(base, 'operator-stopped');
  assert.deepEqual(run.invalidReasons, ['hidden-tab', 'recording-stopped-early']);
  assert.equal(run.visualAcceptance, 'pending'); assert.equal(run.userAssessment, null);
  assert.equal(run.machineMeasurementClass, 'invalid-for-reference-comparison');
});

test('Declared test conditions cannot smuggle arbitrary fields into exports', () => {
  const options = runOptions({ deviceClass: 'physical-desktop', inputDevice: 'trackpad', cacheState: 'warm', key: 'must-not-export' });
  assert.equal(options.inputDevice, 'trackpad'); assert.equal(Object.hasOwn(options, 'key'), false);
  assert.throws(() => runOptions({ deviceClass: 'invented' }));
  assert.throws(() => runOptions({ repetition: 0 }));
  assert.throws(() => runOptions({ durationMs: Infinity }));
});

test('Installed SDK exposes the exact camera, navigation, worker and projection APIs used', async () => {
  const sdk = await import('../../map-stage-1/node_modules/maplibre-gl/dist/maplibre-gl.mjs');
  assert.equal(sdk.getVersion(), '6.13.0');
  for (const method of ['jumpTo', 'easeTo', 'stop', 'getRoll', 'getPixelRatio', 'setLayoutProperty', 'getMinPitch']) {
    assert.equal(typeof sdk.Map.prototype[method], 'function', method);
  }
  assert.equal(typeof sdk.setWorkerUrl, 'function');
  assert.equal(typeof sdk.NavigationControl, 'function');
});

test('Browser wiring separates gesture intervals, measures a flat zoom anchor, and flags resize', () => {
  const saved = Object.fromEntries(['window', 'document', 'devicePixelRatio'].map(name => [name, Object.getOwnPropertyDescriptor(globalThis, name)]));
  const fakeWindow = new EventTarget(), fakeDocument = new EventTarget(), canvas = new EventTarget();
  fakeDocument.hidden = false; fakeDocument.hasFocus = () => true;
  canvas.contains = target => target === canvas;
  canvas.getBoundingClientRect = () => ({ left: 0, top: 0 });
  globalThis.window = fakeWindow; globalThis.document = fakeDocument; globalThis.devicePixelRatio = 1;
  let at = 100, camera = base;
  const handlers = new Map(), recorder = new Recorder({ now: () => at, timeOrigin: 0 });
  const map = {
    getCanvas: () => canvas, getCenter: () => ({ lng: camera.center[0], lat: camera.center[1] }),
    getZoom: () => camera.zoom, getBearing: () => camera.bearing, getPitch: () => camera.pitch,
    isMoving: () => false, project: coordinate => ({ x: coordinate[0], y: coordinate[1] }),
    unproject: point => ({ lng: point.x, lat: point.y }),
    on: (name, callback) => handlers.set(name, callback), off: name => handlers.delete(name),
  };
  let adapter;
  try {
    adapter = attachDiagnostics(map, recorder, { ready: () => true, environment: () => ({ devicePixelRatio: 1 }),
      configuration: () => ({}), onRunFinished: () => {} });
    adapter.start(runOptions({ deviceClass: 'physical-desktop', cacheState: 'warm', inputDevice: 'mouse' }));
    const wheel = new Event('wheel');
    Object.defineProperties(wheel, { timeStamp: { value: 95 }, deltaY: { value: 120 }, clientX: { value: 10 }, clientY: { value: 20 } });
    canvas.dispatchEvent(wheel); at = 110; camera = { ...base, zoom: 17 };
    handlers.get('move')({ originalEvent: wheel }); handlers.get('render')();
    at = 125; camera = { ...camera, zoom: 17.1 }; handlers.get('move')({ originalEvent: wheel }); handlers.get('render')();
    assert.deepEqual(recorder.active.activeRenderIntervalsMs, [15]);
    at = 200; handlers.get('moveend')({ originalEvent: wheel });
    assert.equal(recorder.active.zoomAnchors[0].driftCssPixels, 0);
    assert.equal(recorder.active.zoomAnchors[0].settleAfterLastWheelMs, 100);
    at = 2000; handlers.get('movestart')(); camera = moved; handlers.get('move')({}); handlers.get('render')();
    assert.deepEqual(recorder.active.activeRenderIntervalsMs, [15]);
    handlers.get('resize')();
    assert.ok(recorder.active.invalidReasons.includes('viewport-or-dpr-changed'));
  } finally {
    adapter?.dispose();
    for (const [name, descriptor] of Object.entries(saved)) {
      if (descriptor) Object.defineProperty(globalThis, name, descriptor); else delete globalThis[name];
    }
  }
});
