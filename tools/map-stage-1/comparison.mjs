// Pure configuration logic, shared with the local verification checks.
export const styles = { maptiler: 'streets-v4', mapbox: 'standard', openfreemap: 'liberty' };
const legacyViews = {
  overview: { center: [41.633, 41.644], zoom: 12.5 },
  oldtown: { center: [41.645, 41.651], zoom: 16 },
  waterfront: { center: [41.638, 41.658], zoom: 16 },
  park: { center: [41.625, 41.646], zoom: 16 },
  south: { center: [41.612, 41.630], zoom: 16 },
  botanical: { center: [41.707, 41.694], zoom: 15 },
};
function number(params, key, fallback, min, max) {
  if (!params.has(key)) return fallback;
  const raw = params.get(key);
  const value = Number(raw);
  if (!raw.trim() || !Number.isFinite(value) || value < min || value > max) {
    throw new Error(`Invalid ${key}; allowed range ${min} to ${max}`);
  }
  return value;
}
export function resolveTest(params, presets) {
  const provider = params.get('provider') || 'openfreemap';
  if (!Object.hasOwn(styles, provider)) throw new Error('Unsupported provider');
  const style = params.get('style') || styles[provider];
  if (style !== styles[provider]) throw new Error('Style does not match selected provider');
  const language = params.get('lang') || 'native';
  if (!['native', 'en', 'ka'].includes(language)) throw new Error('Unsupported language');
  const mode = params.get('mode') || 'single';
  if (!['single', 'compare'].includes(mode)) throw new Error('Unsupported mode');
  const preset = params.get('preset') || 'overview';
  if (!Object.hasOwn(presets.locations, preset)) throw new Error('Unsupported preset');
  let center = [...presets.locations[preset].center];
  let source = presets.locations[preset].coordinateSource;
  const condition = params.get('condition') || (params.get('provider3d') === '1' ? '3d'
    : params.has('view') && Number(params.get('pitch')) > 0 ? 'detail' : '2d');
  if (!Object.hasOwn(presets.conditions, condition)) throw new Error('Unsupported condition');
  let camera = { ...presets.locations[preset].cameras[condition], center };
  if (params.has('view')) {
    const view = params.get('view');
    if (!Object.hasOwn(legacyViews, view) || params.has('preset')) throw new Error('Invalid legacy view/preset combination');
    camera = { ...camera, ...legacyViews[view] };
    source = { status: 'Legacy Stage 1 camera; not coordinate-verified for Stage 1B', view };
  }
  if (params.has('center')) {
    const values = params.get('center').split(',');
    if (values.length !== 2 || values.some(v => !v.trim() || !Number.isFinite(Number(v)))) throw new Error('center requires longitude,latitude');
    center = values.map(Number);
    if (Math.abs(center[0]) > 180 || Math.abs(center[1]) > 85.05112878) throw new Error('center exceeds Mercator coordinate bounds');
    camera.center = center;
    source = { status: 'User URL override; independently unverified' };
  }
  camera.zoom = number(params, 'zoom', camera.zoom, 0, 22);
  camera.pitch = number(params, 'pitch', camera.pitch, 0, 60);
  camera.bearing = number(params, 'bearing', camera.bearing, -180, 180);
  if (condition === '2d' && (camera.pitch !== 0 || camera.bearing !== 0)) throw new Error('Clean 2D requires pitch=0 and bearing=0');
  return { provider, style, language, mode, preset, condition, camera, coordinateSource: source };
}
export function labelExpression(language) {
  const fields = language === 'en' ? ['name:en', 'name_en', 'name:latin', 'name']
    : ['name:ka', 'name_ka', 'name'];
  return fields.reduceRight((fallback, field) => ['case',
    ['all', ['has', field], ['!=', ['get', field], '']], ['get', field], fallback], '');
}
