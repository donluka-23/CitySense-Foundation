import { Recorder, attachDiagnostics, readCamera } from './diagnostics.mjs';

export const BASELINE = '0e0440a28b2d1c82a70aa545c3e8bf3479e0cea0';
const presetNames = ['overview', 'waterfront', 'central', 'street'];
const conditions = ['2d', 'detail', '3d'];

export function configuration(params, presets) {
  const preset = params.get('preset') ?? 'waterfront';
  const condition = params.get('condition') ?? '2d';
  const motion = params.get('motion') ?? 'immediate';
  const durationMs = Number(params.get('duration') ?? 400);
  const buildings = params.get('buildings') ?? (condition === '3d' ? 'on' : 'off');
  const pixelRatio = params.has('dpr') ? Number(params.get('dpr')) : null;
  if (!presetNames.includes(preset) || !Object.hasOwn(presets.locations, preset)) throw new Error('Invalid preset');
  if (!conditions.includes(condition)) throw new Error('Invalid condition');
  if (!['immediate', 'short'].includes(motion)) throw new Error('Invalid transition mode');
  if (!Number.isFinite(durationMs) || durationMs < 0 || params.get('duration') === '') throw new Error('Invalid duration');
  if (!['on', 'off'].includes(buildings)) throw new Error('Invalid building visibility');
  if (pixelRatio !== null && (!Number.isFinite(pixelRatio) || pixelRatio <= 0)) throw new Error('Invalid DPR');
  const camera = { center: [...presets.locations[preset].center], ...presets.locations[preset].cameras[condition] };
  return { preset, condition, motion, durationMs, buildings: buildings === 'on', pixelRatio, camera };
}

export function applyCamera(map, config, reducedMotion, commandId) {
  // Native handlers interrupt these native transitions. No timer moves the camera.
  const duration = config.motion === 'immediate' || reducedMotion ? 0 : config.durationMs;
  const data = { stage1cCommand: commandId };
  if (!duration) map.jumpTo(config.camera, data);
  else map.easeTo({ ...config.camera, duration, essential: false }, data);
  return duration;
}

export function extrusionInventory(style) {
  return style.layers.filter(layer => layer.type === 'fill-extrusion').map(layer => ({
    id: layer.id, minzoom: layer.minzoom ?? 0, maxzoom: layer.maxzoom ?? 24,
    suppliedVisibility: layer.layout?.visibility ?? 'visible',
    heightExpressionPresent: layer.paint?.['fill-extrusion-height'] !== undefined,
  }));
}

export function setBuildingVisibility(map, layers, enabled) {
  for (const layer of layers) map.setLayoutProperty(layer.id, 'visibility', enabled ? layer.suppliedVisibility : 'none');
}

export function runOptions(options = {}) {
  const allowed = {
    deviceClass: ['unclassified', 'physical-desktop', 'desktop-emulation', 'physical-mobile'],
    inputDevice: ['unclassified', 'mouse', 'trackpad', 'touch'],
    cacheState: ['unclassified', 'warm', 'cold'],
    networkProfile: ['unknown', 'unthrottled', 'throttled'],
    powerMode: ['unknown', 'normal', 'low-power'],
    purpose: ['gestures', 'transition', 'mixed'],
  };
  const result = { deviceClass: 'unclassified', inputDevice: 'unclassified', cacheState: 'unclassified',
    networkProfile: 'unknown', powerMode: 'unknown', purpose: 'gestures',
    displayHz: null, repetition: 1, durationMs: 30000 };
  for (const [key, values] of Object.entries(allowed)) if (Object.hasOwn(options, key)) {
    if (!values.includes(options[key])) throw new Error(`Invalid ${key}`);
    result[key] = options[key];
  }
  for (const key of ['displayHz', 'repetition', 'durationMs']) if (Object.hasOwn(options, key)) result[key] = options[key];
  if (result.displayHz !== null && (!Number.isFinite(result.displayHz) || result.displayHz <= 0)) throw new Error('Invalid displayHz');
  if (!Number.isSafeInteger(result.repetition) || result.repetition < 1) throw new Error('Invalid repetition');
  // Bounds recording memory and timer lifetime, not navigation or camera movement.
  if (!Number.isFinite(result.durationMs) || result.durationMs < 1000 || result.durationMs > 120000) throw new Error('Recording duration must be 1000–120000 ms');
  return result;
}

export function rendererInformation(map) {
  const gl = map.getCanvas().getContext('webgl2');
  if (!gl) return { context: 'unavailable' };
  const debug = gl.getExtension('WEBGL_debug_renderer_info');
  return { context: 'webgl2', vendor: gl.getParameter(gl.VENDOR), renderer: gl.getParameter(gl.RENDERER),
    version: gl.getParameter(gl.VERSION), unmaskedRenderer: debug ? gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : null };
}

export async function startPage() {
  const element = id => document.getElementById(id);
  const status = message => { element('status').textContent = message; };
  const recorder = new Recorder();
  const state = { stage: '1C', baseline: BASELINE, status: 'initializing', provider: 'MapTiler',
    style: 'streets-v4', suppliedStyleSha256: null, presetsSha256: null,
    sdkVersion: null, styleSpecVersion: null, projection: 'mercator', nativeLabels: true,
    keyPresent: false, keyRejected: false, providerExtrusions: [],
    buildingGeometryPresence: 'Not visually verified', styleLoadedAtMs: null, firstIdleAtMs: null,
    userAssessedNavigationQuality: null, visualAcceptance: 'pending' };
  let map = null, adapter = null, config = null, presets = null;
  let idle = false, quietSince = performance.now(), runDefaults = runOptions(), commandId = 0;
  const startup = performance.now();
  const ready = () => !!map && state.styleLoadedAtMs !== null && idle && map.isStyleLoaded()
    && map.areTilesLoaded() && !map.isMoving() && document.fonts.status === 'loaded'
    && performance.now() - quietSince >= 750 && !recorder.errors.length && !recorder.contextLosses;
  const environment = () => {
    const rect = element('map').getBoundingClientRect();
    return { userAgent: navigator.userAgent, hardwareConcurrency: navigator.hardwareConcurrency ?? null,
      devicePixelRatio, renderingPixelRatio: map?.getPixelRatio() ?? null,
      pageViewport: [innerWidth, innerHeight], mapViewport: [rect.width, rect.height],
      canvasPixels: map ? [map.getCanvas().width, map.getCanvas().height] : null,
      visible: !document.hidden, focused: document.hasFocus(), renderer: map ? rendererInformation(map) : null };
  };
  const diagnostic = () => ({
    ...state, exportedAtUtc: new Date().toISOString(), ready: ready(), environment: environment(),
    configuration: config, actualCamera: map ? readCamera(map) : null,
    inputSettings: map ? { dragPan: map.dragPan.isEnabled(), scrollZoom: map.scrollZoom.isEnabled(),
      dragRotate: map.dragRotate.isEnabled(), keyboard: map.keyboard.isEnabled(),
      minZoom: map.getMinZoom(), maxZoom: map.getMaxZoom(), minPitch: map.getMinPitch(), maxPitch: map.getMaxPitch(),
      nativeDefaults: 'Unmodified sensitivity, inertia, north snapping and zoom/pitch bounds; no maxBounds' } : null,
    activeRun: recorder.active, runs: recorder.runs,
    errors: recorder.errors, contextLosses: recorder.contextLosses, contextRestorations: recorder.restorations,
    limitations: [
      'Input-to-camera-render is a software proxy, not measured visual latency.',
      'Map render intervals are callback intervals, not GPU FPS or presentation timing.',
      'Only originalEvent-matched camera updates qualify inputs; unmatched/coalesced inputs are reported.',
      'Native smoothing/inertia may reuse an event; each input qualifies only once.',
      'Browser event timestamps exclude unknown hardware/OS delay and can be coalesced.',
      'Remote style/tile content is live; SHA-256 is a retrieval fingerprint, not an immutable release.',
      'User quality/acceptance is separate and pending. No performance budget is auto-certified.',
    ],
  });
  function recordControls(recording) {
    for (const id of ['preset', 'condition', 'buildings', 'motion', 'duration']) element(id).disabled = recording;
    element('record').textContent = recording ? 'Stop recording' : 'Record 30s';
  }
  function startRun(options = {}) {
    if (!adapter) throw new Error('Renderer unavailable');
    const pending = controlsConfiguration();
    if (JSON.stringify(pending) !== JSON.stringify(config)) throw new Error('Apply the selected settings before recording');
    const chosen = runOptions({ ...runDefaults, repetition: Number(element('repetition').value), ...options });
    const run = adapter.start(chosen); recordControls(true);
    status(`Recording run ${run.id}, repetition ${run.repetition}. Hold the final camera still for at least 2 seconds before completion.`);
    return run.id;
  }
  window.stage1c = { diagnostic, startRun,
    finishRun: () => adapter?.finish(),
    setTestConditions: options => { runDefaults = runOptions({ ...runDefaults, ...options }); return runDefaults; },
    applyCamera: () => apply(),
  };
  element('export').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(diagnostic(), null, 2) + '\n'], { type: 'application/json' }));
    const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'stage-1c-navigation.json'; anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  const guard = callback => {
    try { return callback(); }
    catch { status('Action unavailable. Check selected settings, apply them, wait for idle/tiles, and focus the visible map before recording.'); return null; }
  };
  element('record').addEventListener('click', () => guard(() => recorder.active ? adapter.finish() : startRun()));
  element('controls').addEventListener('submit', event => { event.preventDefault(); guard(apply); });
  element('stop').addEventListener('click', () => map?.stop());
  element('condition').addEventListener('change', () => { element('buildings').checked = element('condition').value === '3d'; });
  function controlsConfiguration() {
    return configuration(new URLSearchParams({ preset: element('preset').value, condition: element('condition').value,
      motion: element('motion').value, duration: element('duration').value,
      buildings: element('buildings').checked ? 'on' : 'off',
      ...(config?.pixelRatio !== null && config?.pixelRatio !== undefined ? { dpr: String(config.pixelRatio) } : {}) }), presets);
  }
  function apply() {
    if (!map || state.styleLoadedAtMs === null) throw new Error('Wait for style load');
    const next = controlsConfiguration();
    if (recorder.active && JSON.stringify(next) !== JSON.stringify(config)) throw new Error('Finish recording before changing conditions');
    config = next; setBuildingVisibility(map, state.providerExtrusions, config.buildings);
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const effective = config.motion === 'immediate' || reduced ? 0 : config.durationMs;
    const id = ++commandId;
    recorder.command(id, config.camera, config.motion, config.durationMs, effective);
    applyCamera(map, config, reduced, id);
    status(`${config.preset} / ${config.condition}; ${effective ? `${effective} ms native candidate` : 'immediate'}; provider 3D ${config.buildings ? 'requested' : 'hidden'}.${!state.providerExtrusions.length ? ' No supplied extrusion layer; 3D validation unavailable.' : ''}`);
  }
  async function fingerprint(text) {
    const bytes = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return [...new Uint8Array(bytes)].map(value => value.toString(16).padStart(2, '0')).join('');
  }
  try {
    const [presetResponse, configResponse] = await Promise.all([fetch('/presets.json', { cache: 'no-store' }), fetch('/config.json', { cache: 'no-store' })]);
    if (!presetResponse.ok || !configResponse.ok) throw new Error('Local configuration unavailable');
    const presetText = await presetResponse.text(); presets = JSON.parse(presetText);
    state.presetsSha256 = await fingerprint(presetText);
    config = configuration(new URLSearchParams(location.search), presets);
    for (const name of presetNames) {
      const option = document.createElement('option'); option.value = name; option.textContent = name; element('preset').append(option);
    }
    element('preset').value = config.preset; element('condition').value = config.condition;
    element('buildings').checked = config.buildings; element('motion').value = config.motion; element('duration').value = config.durationMs;
    const provider = await configResponse.json();
    state.keyPresent = provider.keyPresent; state.keyRejected = provider.keyRejected;
    if (!provider.keyPresent) {
      state.status = 'blocked-configuration'; status('MapTiler browser key unavailable or rejected. Configure it in the server terminal and restart. No substitute map.'); return;
    }
    const library = await import('/vendor/maplibre-gl.mjs');
    state.sdkVersion = library.getVersion();
    if (state.sdkVersion !== '6.13.0') throw new Error('Existing SDK version mismatch');
    library.setWorkerUrl('/vendor/maplibre-gl-worker.mjs');
    let response;
    try {
      response = await fetch(`https://api.maptiler.com/maps/streets-v4/style.json?key=${encodeURIComponent(provider.maptilerPublicKey)}`, { signal: AbortSignal.timeout(30000) });
    } catch { recorder.error('provider-style-network-cors-timeout'); throw new Error('Provider style unavailable'); }
    if (!response.ok) { recorder.error('provider-style-http', response.status); throw new Error('Provider style unavailable'); }
    const styleText = await response.text(), style = JSON.parse(styleText);
    state.suppliedStyleSha256 = await fingerprint(styleText); state.styleSpecVersion = style.version;
    state.providerExtrusions = extrusionInventory(style);
    style.projection = { type: 'mercator' }; // Canonical Stage 1B geography; no terrain or free flight.
    map = new library.Map({ container: 'map', style, ...config.camera, attributionControl: false,
      ...(config.pixelRatio === null ? {} : { pixelRatio: config.pixelRatio }) });
    window.stage1c.map = map;
    map.addControl(new library.NavigationControl({ visualizePitch: true }), 'top-right');
    map.addControl(new library.AttributionControl({ compact: false }), 'bottom-right');
    map.addControl({
      onAdd() {
        this.element = document.createElement('a'); this.element.className = 'maplibregl-ctrl provider-logo';
        this.element.href = 'https://www.maptiler.com/'; this.element.target = '_blank'; this.element.rel = 'noopener noreferrer';
        const logo = document.createElement('img'); logo.src = 'https://api.maptiler.com/resources/logo.svg'; logo.alt = 'MapTiler';
        logo.addEventListener('error', () => { recorder.error('provider-attribution-logo'); status('Attribution logo failed. Reload after fixing resource access.'); });
        this.element.append(logo); return this.element;
      }, onRemove() { this.element.remove(); },
    }, 'bottom-left');
    const invalidateReady = () => { idle = false; quietSince = performance.now(); };
    for (const event of ['dataloading', 'sourcedata', 'movestart', 'moveend', 'resize']) map.on(event, invalidateReady);
    map.once('load', () => {
      state.styleLoadedAtMs = performance.now() - startup; state.status = 'loaded-not-visually-accepted';
      setBuildingVisibility(map, state.providerExtrusions, config.buildings);
      for (const id of ['preset', 'condition', 'buildings', 'motion', 'duration', 'apply', 'stop', 'record']) element(id).disabled = false;
      status('Map loaded. Wait for idle, then drag/zoom/rotate. Set test conditions through window.stage1c before recording.');
    });
    map.on('idle', () => { idle = true; state.firstIdleAtMs ??= performance.now() - startup; });
    adapter = attachDiagnostics(map, recorder, { environment, configuration: () => ({ ...config,
      sdkVersion: state.sdkVersion, suppliedStyleSha256: state.suppliedStyleSha256,
      presetsSha256: state.presetsSha256, projection: 'mercator',
      reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches }), ready,
      onRunFinished: run => {
        recordControls(false); status(`Run ${run.id} complete: ${run.metrics.matchedInputCount} matched inputs, ${run.metrics.unmatchedInputCount} unmatched. ${run.machineMeasurementClass}; visual acceptance pending.`);
      },
    });
    map.on('error', () => { state.status = 'rendering-error'; status('Resource/render error recorded. Fix access and reload; do not accept this run.'); });
    map.getCanvas().addEventListener('webglcontextlost', () => { state.status = 'context-lost'; status('WebGL context lost. Reload for a new measurement session.'); });
    window.addEventListener('pagehide', () => { adapter?.dispose(); map?.remove(); }, { once: true });
  } catch {
    state.status = 'blocked-initialization'; recorder.error('initialization');
    // Errors may contain provider URLs/keys. Never publish their raw text.
    status('Initialization failed. Check URL settings, SDK, WebGL2 and provider access locally; exported errors are sanitized.');
  }
}

if (typeof document !== 'undefined' && document.getElementById('map')) startPage();
