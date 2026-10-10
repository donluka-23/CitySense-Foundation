// One manually invoked, bounded aggregate OSM audit, independent of CitySense ingestion.
// No provider tile extraction, synthetic state, contributor/contact data or database writes.
import { createHash } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';

const output = process.argv[2];
if (!output || process.argv.length !== 3) {
  console.error('Usage: node audit-coverage.mjs NEW_OUTPUT_DIRECTORY');
  process.exit(2);
}
const bounds = [41.61, 41.60, 41.67, 41.67]; // Overpass south,west,north,east.
const bbox = bounds.join(',');
const selections = [
  ['street_ways', `way[highway](${bbox})`],
  ['pedestrian_ways', `way[highway~"^(footway|path|pedestrian|steps)$"](${bbox})`],
  ['building_ways', `way[building][building!="no"](${bbox})`],
  ['building_relations', `rel[building][building!="no"](${bbox})`],
  ['building_ways_with_height_tag', `way[building][building!="no"][height](${bbox})`],
  ['building_ways_with_levels_tag', `way[building][building!="no"]["building:levels"](${bbox})`],
  ['building_ways_with_height_or_levels', `(way[building][building!="no"][height](${bbox});way[building][building!="no"]["building:levels"](${bbox});)`],
  ['building_parts', `way["building:part"](${bbox})`],
  ['coastline_ways', `way[natural=coastline](${bbox})`],
  ['park_ways', `way[leisure=park](${bbox})`],
  ['park_relations', `rel[leisure=park](${bbox})`],
  ['vegetation_ways', `(way[natural~"^(wood|grassland|scrub)$"](${bbox});way[landuse~"^(forest|grass|meadow|orchard)$"](${bbox});)`],
  ['tourism_attraction_objects', `nwr[tourism=attraction](${bbox})`],
  ['named_street_ways', `way[highway][name](${bbox})`],
  ['street_ways_with_name_en', `way[highway]["name:en"](${bbox})`],
  ['street_ways_with_name_ka', `way[highway]["name:ka"](${bbox})`],
  ['street_ways_with_georgian_in_name', `way[highway][name~"(ა|ბ|გ|დ|ე|ვ|ზ|თ|ი|კ|ლ|მ|ნ|ო|პ|ჟ|რ|ს|ტ|უ|ფ|ქ|ღ|ყ|შ|ჩ|ც|ძ|წ|ჭ|ხ|ჯ|ჰ)"](${bbox})`],
  ['attraction_objects_with_name_en', `nwr[tourism=attraction]["name:en"](${bbox})`],
  ['attraction_objects_with_name_ka', `nwr[tourism=attraction]["name:ka"](${bbox})`],
];
const labels = `(nwr[place=city][name](${bbox});nwr[tourism=attraction][name](${bbox});nwr[leisure=park][name](${bbox});nwr[natural=water][name](${bbox}););`;
const query = `[out:json][timeout:25][maxsize:67108864];\n`
  + selections.map(([, selection]) => `${selection};out count;`).join('\n')
  + '\n' + labels + '\n'
  + 'convert audit_label ::id=id(),osm_type=type(),name=t["name"],name_en=t["name:en"],name_ka=t["name:ka"],category=t["tourism"],leisure=t["leisure"],natural=t["natural"],place=t["place"];out;';
const directory = resolve(output);
await mkdir(dirname(directory), { recursive: true });
await mkdir(directory, { recursive: false }); // Fails if evidence directory already exists.
await writeFile(resolve(directory, 'query.overpassql'), query, { flag: 'wx' });
const receipt = {
  auditDateTbilisi: new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Tbilisi',
    year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date()),
  source: 'OpenStreetMap via public Overpass',
  endpoint: 'https://overpass-api.de/api/interpreter',
  attribution: '© OpenStreetMap contributors', license: 'ODbL-1.0',
  licenseUrl: 'https://www.openstreetmap.org/copyright',
  bboxSouthWestNorthEast: bounds, querySha256: createHash('sha256').update(query).digest('hex'),
  requestedAt: new Date().toISOString(), status: 'not_completed',
  interpretation: 'Source presence/tag audit only; not provider rendering, field completeness, measured height, pedestrian connectivity or suitability evidence',
  counts: {}, labels: [],
};
try {
  const response = await fetch(receipt.endpoint, {
    method: 'POST', redirect: 'error', signal: AbortSignal.timeout(45000),
    headers: { 'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'CitySense-Stage1-BatumiMapAudit/0.1 (manual bounded geographic coverage audit; no personal data)' },
    body: new URLSearchParams({ data: query }),
  });
  receipt.httpStatus = response.status;
  const reader = response.body.getReader();
  let bytes = 0; const chunks = [];
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    bytes += value.length;
    if (bytes > 262144) { await reader.cancel(); throw new Error('Response exceeds 256 KiB'); }
    chunks.push(Buffer.from(value));
  }
  const body = Buffer.concat(chunks);
  receipt.retrievedAt = new Date().toISOString();
  receipt.bytes = body.length;
  receipt.rawSha256 = createHash('sha256').update(body).digest('hex');
  if (!response.ok) {
    // This endpoint echoes only the fixed public query; keep a short parse diagnostic.
    receipt.upstreamDiagnostic = body.toString('utf8').replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').slice(-1800);
    throw new Error(`HTTP ${response.status}`);
  }
  const data = JSON.parse(body.toString('utf8'));
  if (data.remark) throw new Error('Overpass reported incomplete or failed execution');
  receipt.osmDatabaseTimestamp = data.osm3s?.timestamp_osm_base;
  const counts = data.elements.filter(e => e.type === 'count');
  if (counts.length !== selections.length) throw new Error('Unexpected count cardinality');
  for (let i = 0; i < selections.length; i++) {
    receipt.counts[selections[i][0]] = Object.fromEntries(
      Object.entries(counts[i].tags).map(([key, value]) => [key, Number(value)]));
  }
  const allowedTags = ['osm_type', 'name', 'name_en', 'name_ka', 'category', 'leisure', 'natural', 'place'];
  receipt.labels = data.elements.filter(e => e.type === 'audit_label').map(e => ({
    sourceId: `${e.tags.osm_type}/${e.id}`,
    ...Object.fromEntries(allowedTags.filter(k => k !== 'osm_type' && e.tags[k]).map(k => [k, e.tags[k]])),
  }));
  // Only the deliberately projected, nonpersonal response can enter the private raw archive.
  if (data.elements.some(e => !['count', 'audit_label'].includes(e.type)
      || (e.type === 'audit_label' && Object.keys(e.tags).some(k => !allowedTags.includes(k))))) {
    throw new Error('Unexpected raw element or tag');
  }
  await writeFile(resolve(directory, 'response.json'), body, { flag: 'wx' });
  receipt.status = 'completed';
} catch (error) {
  receipt.status = 'unavailable';
  receipt.error = error.message; // Fixed public endpoint, never includes a credential.
  process.exitCode = 1;
}
await writeFile(resolve(directory, 'coverage-summary.json'), JSON.stringify(receipt, null, 2) + '\n', { flag: 'wx' });
console.log(JSON.stringify({ status: receipt.status, counts: receipt.counts, labelCount: receipt.labels.length,
  evidencePath: resolve(directory, 'coverage-summary.json'), error: receipt.error }, null, 2));
