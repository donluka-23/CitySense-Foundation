import { resolveTest, styles, labelExpression } from './comparison.mjs';
const params = new URLSearchParams(location.search);
const status = document.getElementById('status');
const exportButton = document.getElementById('evidence');
const startupStarted = performance.now();
const state = {
  stage: '1B', status: 'initializing', renderReady: false, screenshotCaptured: false,
  sdkVersion: null, styleSpecVersion: null, styleRevision: null, styleSha256: null,
  styleLoadMs: null, firstFullyLoadedFrameMs: null, firstIdleMs: null, stableVisibleTilesMs: null,
  errorCount: 0, errors: [], webglContextLosses: 0, labelLayersModified: [],
  heightPolicy: 'Provider 3D only; height lineage/accuracy unverified. No added geometry.',
  provider3dLayerCount: null, disabledExtrusionLayers: [], customData: false,
};
// Local diagnostics only. Vendor requests/accounting remain unchanged.
window.mapStage1b = { state };
window.mapStage1 = window.mapStage1b;
function report(message) { status.textContent = message; }
function fail(phase, httpStatus = null) {
  state.errorCount++; state.renderReady = false; state.status = 'blocked';
  state.errors.push({ phase, httpStatus });
  report(`${state.provider || 'Test'} blocked: ${phase}${httpStatus ? ` (HTTP ${httpStatus})` : ''}; no provider substitution.`);
}
function asset(tagName, url) {
  return new Promise((resolve, reject) => {
    const tag = document.createElement(tagName);
    if (tagName === 'link') { tag.rel = 'stylesheet'; tag.href = url; } else tag.src = url;
    tag.onload = resolve; tag.onerror = () => reject(new Error('Local SDK/CSS asset unavailable; run npm ci'));
    document.head.append(tag);
  });
}
async function hash(text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map(x => x.toString(16).padStart(2, '0')).join('');
}
function camera(map) {
  const c = map.getCenter();
  return { center: [c.lng, c.lat], zoom: map.getZoom(), bearing: map.getBearing(), pitch: map.getPitch() };
}
function download(value, name) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2) + '\n'], { type: 'application/json' }));
  const anchor = document.createElement('a'); anchor.href = url; anchor.download = name; anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function diagnostic() {
  const map = window.mapStage1b.map;
  const mapRect = document.getElementById('map').getBoundingClientRect();
  const entries = performance.getEntriesByType('resource');
  // Aggregate only: URLs, headers, raw style data and credentials never enter exports.
  const providers = entries.filter(e => {
    try { return ['api.maptiler.com', 'api.mapbox.com', 'tiles.openfreemap.org', 'events.mapbox.com'].includes(new URL(e.name).hostname); }
    catch { return false; }
  });
  return {
    ...state, exportedAt: new Date().toISOString(), screenshotCaptured: false,
    screenshotCaptureTimestamp: null, visualFindings: 'Not inspected by diagnostic code',
    actualCamera: map ? camera(map) : null,
    pageViewport: { width: innerWidth, height: innerHeight, dpr: devicePixelRatio },
    mapViewport: { width: mapRect.width, height: mapRect.height },
    fontsStatus: document.fonts.status,
    observedResourceEntries: entries.length, observedProviderEntries: providers.length,
    observableTransferBytes: entries.reduce((n, e) => n + (e.transferSize || 0), 0),
    networkCaveat: 'Resource Timing can omit worker requests and cross-origin sizes; not billable counts.',
    browser: navigator.userAgent, deviceTestClass: 'Unclassified; operator must declare desktop emulation or physical device',
    observableJsHeapBytes: performance.memory?.usedJSHeapSize ?? null,
    memoryCaveat: 'Optional nonstandard JS heap across page; excludes GPU/native/worker memory.',
    projection: 'mercator', interactionResponsiveness: 'Not measured',
    firstMeaningfulRender: 'Not measured; firstFullyLoadedFrameMs is an event-based proxy requiring visual corroboration',
  };
}
window.mapStage1b.diagnostic = diagnostic;
exportButton.addEventListener('click', () => {
  if (state.mode === 'compare') {
    const panes = [...document.querySelectorAll('iframe')].map(frame => frame.contentWindow.mapStage1b?.diagnostic());
    download({ stage: '1B', exportedAt: new Date().toISOString(), mode: 'compare', screenshotCaptured: false,
      parentViewport: [innerWidth, innerHeight], panes, caveat: 'Three concurrent maps; not a single-map performance benchmark' }, 'stage-1b-comparison.json');
  } else download(diagnostic(), `stage-1b-${state.provider}-${state.preset}-${state.condition}-${state.language}.json`);
});
async function start() {
  const presetResponse = await fetch('/presets.json', { cache: 'no-store' });
  if (!presetResponse.ok) throw new Error('Preset file unavailable; restart the updated server');
  const presetText = await presetResponse.text();
  const test = resolveTest(params, JSON.parse(presetText));
  Object.assign(state, test, { requestedCamera: test.camera, presetsSha256: await hash(presetText) });
  exportButton.disabled = false;
  if (test.mode === 'compare') {
    document.getElementById('map').hidden = true;
    const grid = document.getElementById('comparison'); grid.hidden = false;
    for (const provider of ['maptiler', 'mapbox', 'openfreemap']) {
      const query = new URLSearchParams(params);
      query.set('mode', 'single'); query.set('provider', provider); query.set('style', styles[provider]);
      const frame = document.createElement('iframe'); frame.title = `${provider} ${styles[provider]} basemap`;
      frame.src = `/?${query}`; grid.append(frame);
    }
    state.status = 'comparison';
    report('Stage 1B: A MapTiler | B Mapbox | C OpenFreeMap. Equal panes; reload to reset matching cameras. Compare mobile and performance in single mode.');
    return;
  }
  const configResponse = await fetch('/config.json', { cache: 'no-store' });
  if (!configResponse.ok) throw new Error('Provider configuration unavailable');
  const config = await configResponse.json();
  let library, style, options = {};
  report(`${test.provider} / ${test.style} | ${test.preset} ${test.condition} ${test.language} | initializing`);
  if (test.provider === 'mapbox') {
    if (!config.mapboxPublicToken?.startsWith('pk.')) {
      fail('configuration required: set MAPBOX_PUBLIC_ACCESS_TOKEN to an authorized pk. public token'); return;
    }
    await asset('link', '/vendor/mapbox-gl.css'); await asset('script', '/vendor/mapbox-gl.js');
    library = window.mapboxgl; library.accessToken = config.mapboxPublicToken;
    style = 'mapbox://styles/mapbox/standard';
    options.config = { basemap: { lightPreset: 'day', show3dObjects: test.condition === '3d' } };
    options.projection = 'mercator';
    if (test.language !== 'native') options.language = test.language;
  } else {
    if (test.provider === 'maptiler' && !config.maptilerPublicKey) {
      fail('configuration required: set MAPTILER_API_KEY to an authorized browser key'); return;
    }
    await asset('link', '/vendor/maplibre-gl.css');
    library = await import('/vendor/maplibre-gl.mjs');
    library.setWorkerUrl('/vendor/maplibre-gl-worker.mjs');
    const url = test.provider === 'openfreemap' ? 'https://tiles.openfreemap.org/styles/liberty'
      : `https://api.maptiler.com/maps/streets-v4/style.json?key=${encodeURIComponent(config.maptilerPublicKey)}`;
    let response;
    try { response = await fetch(url, { signal: AbortSignal.timeout(30000) }); }
    catch { fail('provider style fetch failed (network/CORS/timeout)'); return; }
    if (!response.ok) { fail('provider style unavailable', response.status); return; }
    const text = await response.text();
    state.styleSha256 = await hash(text); style = JSON.parse(text); state.styleSpecVersion = style.version;
    state.provider3dLayerCount = style.layers.filter(layer => layer.type === 'fill-extrusion').length;
    state.providerExtrusionLayers = style.layers.filter(layer => layer.type === 'fill-extrusion').map(layer => ({
      id: layer.id, minzoom: layer.minzoom ?? 0,
      suppliedVisibility: layer.layout?.visibility ?? 'visible',
      heightExpressionPresent: layer.paint?.['fill-extrusion-height'] !== undefined,
    }));
    for (const layer of style.layers) {
      if (layer.type === 'fill-extrusion' && test.condition !== '3d') {
        layer.layout = { ...layer.layout, visibility: 'none' };
        state.disabledExtrusionLayers.push(layer.id);
      }
      // Native preserves provider label composition. Requested languages use existing name fields.
      // Match only name-bearing text expressions; preserve numeric road shields.
      if (test.language !== 'native' && layer.type === 'symbol' && layer.layout?.['text-field']
          && /name(?::|_|\b)/.test(JSON.stringify(layer.layout['text-field']))
          && ['place', 'poi', 'transportation_name', 'water_name', 'park', 'waterway',
            'mountain_peak', 'aerodrome_label'].includes(layer['source-layer'])) {
        layer.layout['text-field'] = labelExpression(test.language);
        state.labelLayersModified.push(layer.id);
      }
    }
    if (test.condition === '3d' && !state.provider3dLayerCount) state.provider3dStatus = 'Unavailable in supplied style; no extrusion layer added';
    else state.provider3dStatus = test.condition === '3d' ? 'Provider extrusion layers retained with original visibility/minzoom; Batumi presence unverified' : 'Extrusions disabled';
    state.languageSelectionStatus = test.language === 'native' ? 'Provider default expressions preserved'
      : state.labelLayersModified.length ? 'Existing name-field fallback applied; translations/glyphs unverified'
        : 'Requested language adaptation unavailable: no recognized name layers; provider defaults retained';
  }
  state.sdkVersion = library.version || library.getVersion?.(); state.engineVersion = state.sdkVersion;
  const started = performance.now(); state.mapInitializedAt = new Date().toISOString();
  state.status = 'loading';
  const map = new library.Map({ container: 'map', style, ...test.camera, ...options, attributionControl: false });
  window.mapStage1b.map = map;
  map.addControl(new library.AttributionControl({ compact: false }), 'bottom-right');
  map.addControl(new library.NavigationControl(), 'top-right');
  if (test.provider === 'maptiler') {
    map.addControl({
      onAdd() {
        this.element = document.createElement('a'); this.element.className = 'maplibregl-ctrl';
        this.element.href = 'https://www.maptiler.com/'; this.element.target = '_blank'; this.element.rel = 'noopener noreferrer';
        const logo = document.createElement('img'); logo.src = 'https://api.maptiler.com/resources/logo.svg';
        logo.alt = 'MapTiler logo'; this.element.append(logo);
        logo.addEventListener('error', () => fail('attribution logo unavailable'));
        return this.element;
      },
      onRemove() { this.element.remove(); },
    }, 'bottom-left');
  }
  let quietSince = performance.now(); let idleSinceChange = false;
  const invalidate = () => { quietSince = performance.now(); idleSinceChange = false; state.renderReady = false; };
  map.on('dataloading', invalidate); map.on('sourcedata', invalidate); map.on('movestart', invalidate);
  map.on('moveend', invalidate); map.on('resize', invalidate);
  map.on('error', event => {
    const status = event.error?.status;
    fail('SDK resource/render error', Number.isInteger(status) ? status : null);
  });
  map.getCanvas().addEventListener('webglcontextlost', () => { state.webglContextLosses++; fail('WebGL context lost'); });
  map.getCanvas().addEventListener('webglcontextrestored', () => { state.contextRestoredAt = new Date().toISOString(); invalidate(); });
  map.once('load', async () => {
    state.styleLoadMs = Math.round(performance.now() - started);
    const loadedStyle = map.getStyle(); state.styleSpecVersion = loadedStyle.version;
    if (!state.styleSha256) state.styleSha256 = await hash(JSON.stringify(loadedStyle));
    if (test.provider === 'mapbox') state.provider3dStatus = test.condition === '3d'
      ? 'Standard show3dObjects enabled; local buildings/models and height lineage unverified'
      : 'Standard show3dObjects disabled';
    if (test.provider === 'mapbox') state.languageSelectionStatus = test.language === 'native'
      ? 'Provider default language behavior; not forced Georgian'
      : 'SDK language requested; local translations/glyphs unverified';
  });
  map.on('render', () => {
    if (state.firstFullyLoadedFrameMs === null && map.isStyleLoaded() && map.areTilesLoaded()) {
      state.firstFullyLoadedFrameMs = Math.round(performance.now() - started);
    }
  });
  map.on('idle', () => {
    if (state.firstIdleMs === null) state.firstIdleMs = Math.round(performance.now() - started);
    idleSinceChange = true;
  });
  const timer = setInterval(() => {
    const ready = state.styleLoadMs !== null && state.styleSha256 !== null && idleSinceChange
      && map.isStyleLoaded() && map.areTilesLoaded() && !map.isMoving()
      && document.fonts.status === 'loaded' && performance.now() - quietSince >= 750
      && state.errorCount === 0 && state.webglContextLosses === 0;
    state.renderReady = ready;
    if (ready) {
      state.status = 'ready-for-manual-inspection';
      if (state.stableVisibleTilesMs === null) state.stableVisibleTilesMs = Math.round(performance.now() - started);
      if (state.startupToStableMs === undefined) state.startupToStableMs = Math.round(performance.now() - startupStarted);
      const languageWarning = state.languageSelectionStatus?.startsWith('Requested language adaptation unavailable') ? ' Language adaptation unavailable.' : '';
      report(`${test.provider} / ${test.style} | ${test.preset} ${test.condition} ${test.language} | tiles + idle + fonts ready; errors 0.${languageWarning} Inspect map/attribution before screenshot.`);
    } else if (!state.errorCount) report(`${test.provider} / ${test.style} | ${test.preset} ${test.condition} ${test.language} | waiting for stable tiles, idle and fonts; no visual validation yet.`);
  }, 250);
  map.once('remove', () => clearInterval(timer));
}
start().catch(error => {
  // Only our configuration errors are exposed; SDK/fetch errors can contain credentials.
  const safe = /^(Unsupported|Invalid|Style does|Clean 2D|center |Preset file|Local SDK|Provider configuration)/.test(error.message)
    ? error.message : 'initialization failed (SDK, WebGL, style or configuration)';
  fail(safe);
});
