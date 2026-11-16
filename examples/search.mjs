// Search one Australian supermarket from Node.js 18+ (no dependencies).
//
//   RAPIDAPI_KEY=your-key node search.mjs coles "milk 2l"
//   RAPIDAPI_KEY=your-key node search.mjs woolworths coffee --specials
//   RAPIDAPI_KEY=your-key node search.mjs iga "milk 2l" --postcode=3000
//
// Stores: coles, woolworths, aldi, iga, harris-farm. Free key (50 calls a month):
// https://rapidapi.com/highbrowfame/api/australian-supermarket-prices-api-coles-woolworths-aldi

const HOST = 'australian-supermarket-prices-api-coles-woolworths-aldi.p.rapidapi.com';
const BASE = `https://${HOST}`;

// storeOptions: { postcode: '3000' } or { storeId: '32600' } for IGA, { location: 'Broadway' } for Harris Farm.
export async function search(store, query, { limit = 10, onlySpecials = false, ...storeOptions } = {}) {
    const params = new URLSearchParams({ store, query, limit: String(limit), ...storeOptions });
    if (onlySpecials) params.set('onlySpecials', 'true');
    const response = await fetch(`${BASE}/grocery-au/search?${params}`, {
        headers: { 'x-rapidapi-key': process.env.RAPIDAPI_KEY, 'x-rapidapi-host': HOST },
        signal: AbortSignal.timeout(120_000),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);
    return response.json(); // { site, count, results: [...], notes: [...], problems: [...] }
}

// Product name with its pack size: Coles and IGA keep the size in a field of its own.
export function label(product) {
    const size = (product.size ?? product.packageSize ?? product.packSize ?? '').trim();
    const parts = size.toLowerCase().match(/[0-9.]+|[a-z]+/g) ?? [];
    if (!parts.length) return product.name;
    // The size as a whole token: "2 l" is found in "Milk 2L", not in "A2 Light Milk".
    const token = new RegExp(`(?<![a-z0-9.])${parts.map((part) => part.replace('.', '[.]')).join(' *')}(?![a-z0-9])`, 'i');
    return token.test(product.name) ? product.name : `${product.name} ${size}`;
}

const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));
if (args.length >= 2) {
    const [store, ...words] = args;
    const flags = process.argv.slice(2).filter((a) => a.startsWith('--') && a.includes('='));
    const storeOptions = Object.fromEntries(flags.map((a) => a.slice(2).split('=')));
    const answer = await search(store, words.join(' '), { onlySpecials: process.argv.includes('--specials'), ...storeOptions });
    console.log(`${answer.count} products for "${words.join(' ')}" at ${store}`);
    for (const p of answer.results) {
        const was = p.wasPrice > p.price ? ` (was $${p.wasPrice.toFixed(2)})` : '';
        const unit = p.unitPriceText ? `  ${p.unitPriceText}` : '';
        const offer = p.promotion ? `  [${p.promotion}]` : '';
        console.log(`  $${p.price.toFixed(2)}${was}${unit}  ${label(p)}${offer}`);
    }
    for (const note of answer.notes ?? []) console.log('  note:', note);
}
