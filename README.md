# Australian Supermarket Prices API: Coles, Woolworths, ALDI, IGA and Harris Farm

Live Australian grocery prices as clean JSON. Search **Coles, Woolworths, ALDI, IGA and Harris Farm** by keyword and get the product name, price, was-price, special, unit price, pack size, image and link, in AUD. One API, one key, the same core fields for every store.

**[Get a free key on RapidAPI (50 calls a month)](https://rapidapi.com/highbrowfame/api/australian-supermarket-prices-api-coles-woolworths-aldi)** and run the examples below in two minutes.

This repository holds ready-to-run examples in Python, Node.js and curl: a product search, a specials finder and a Coles vs Woolworths basket comparison.

## Quick start

```bash
curl --get "https://australian-supermarket-prices-api-coles-woolworths-aldi.p.rapidapi.com/grocery-au/search" \
  --data-urlencode "store=coles" \
  --data-urlencode "query=milk 2l" \
  --data-urlencode "limit=5" \
  -H "x-rapidapi-key: YOUR_KEY" \
  -H "x-rapidapi-host: australian-supermarket-prices-api-coles-woolworths-aldi.p.rapidapi.com"
```

| Parameter | Required | Meaning |
| --- | --- | --- |
| `store` | yes | `coles`, `woolworths`, `aldi`, `iga` or `harris-farm` |
| `query` | yes, unless `searchUrl` is given | What you would type into the store's search box, e.g. `milk 2l` |
| `limit` | no | Maximum products, 1 to 50 (default 20) |
| `onlySpecials` | no | `true` returns only products on special |
| `searchUrl` | no | Instead of `query`: a category, specials or product link of the store (Coles, Woolworths, ALDI) |
| `postcode`, `storeId` | no | IGA only: prices at the IGA store of that postcode or store number |
| `location` | no | Harris Farm only: the store whose prices to show, e.g. `Broadway` |

`GET /grocery-au/sites` lists the stores and their filters.

## Python: search a store

[`examples/search.py`](examples/search.py), no dependencies:

```bash
RAPIDAPI_KEY=your-key python examples/search.py coles "milk 2l"
```

```text
10 products for "milk 2l" at coles
  $3.40  $1.70 / 1L  Coles Full Cream Milk 2L
  $4.20 (was $4.70)  $2.10 / 1L  Devondale Full Cream Milk 2L  [Save $0.50]
  $3.40  $1.70 / 1L  Coles Lite Reduced Fat Milk 2L
  $7.30  $3.65 / 1L  a2 Milk Lactose Free Light Milk 2L
```

Node.js 18+ version: [`examples/search.mjs`](examples/search.mjs).

## Find the real specials

`onlySpecials=true` returns only products on special, and `wasPrice` tells you what the product cost before, so you can tell a real half-price deal from a yellow ticket. Ready for specials alerts, catalogue trackers and Black Friday checks.

```bash
RAPIDAPI_KEY=your-key python examples/search.py woolworths coffee --specials
```

```text
10 products for "coffee" at woolworths
  $26.00 (was $37.50)  $6.50 / 100G  Moccona Freeze Dried Instant Coffee Classic Medium Roast 400g  [Save $11.50]
  $10.00 (was $14.50)  $6.67 / 100G  Nescafe Blend 43 Instant Coffee Jar 150g  [Save $4.50]
  $4.00 (was $8.00)  $0.40 / 1EA  Nescafe Caramel Latte Coffee Sachets 10 pack  [Half Price]
```

## Coles vs Woolworths: compare a basket

[`examples/basket.py`](examples/basket.py) prices the same shopping list at each store. It only counts a product that carries the pack size you named, so the totals compare like with like:

```bash
RAPIDAPI_KEY=your-key python examples/basket.py "weet-bix 575g" "vegemite 380g" "nescafe blend 43 150g"
```

```text
weet-bix 575g
  coles       $5.00  Sanitarium Weet-bix Breakfast Cereal 575g
  woolworths  $3.50  Weet-Bix Breakfast Cereal 575g  (on special)

vegemite 380g
  coles       $6.00  Vegemite Spread 380g  (on special)
  woolworths  $7.70  Vegemite Spread 380g

nescafe blend 43 150g
  coles       $14.50  Nescafe Blend 43 Instant Coffee 150g
  woolworths  $10.00  Nescafe Blend 43 Instant Coffee Jar 150g  (on special)

Basket total (3 items)
  woolworths  $21.20
  coles       $25.50
```

Add ALDI, IGA or Harris Farm with `--stores=coles,woolworths,aldi`. ALDI sells mostly its own brands, so use generic names there ("butter 250g", "rolled oats 750g").

All outputs on this page are real answers from 16 November 2026.

## IGA and Harris Farm: prices per store

IGA and Harris Farm set their prices store by store, so you choose the store:

```bash
RAPIDAPI_KEY=your-key python examples/search.py iga "milk 2l" --postcode=3000
RAPIDAPI_KEY=your-key python examples/search.py harris-farm bananas --location=Broadway
```

The answer names the store it used (for the postcode above: the IGA on Flinders Street, Melbourne).

## What each product record holds

A real answer, shortened to two products: [`sample-response.json`](sample-response.json).

| Field | Meaning |
| --- | --- |
| `name`, `brand` | Product name and brand |
| `size`, `packageSize` or `packSize` | Pack size (the field name differs by store) |
| `price` | Current shelf price in AUD |
| `wasPrice`, `savings`, `isOnSpecial` | Previous price, the saving and whether the product is on special |
| `promotion` | Special text, e.g. "Half Price", "Save $2.50", "Pick any 2 for $8" |
| `unitPrice`, `unitMeasure`, `unitPriceText` | Price per litre, kg, 100 g or each |
| `department`, `category` | Where the store files the product |
| `isAvailable` | Availability |
| `image`, `url` | Product image and product page |
| `scrapedAt` | When the price was read |

Per store:

- **Woolworths**: also barcode, half-price flag, health star rating, allergens, ingredients, nutrition and in-store price.
- **Coles**: also aisle, multi-buy details, special type and purchase limits.
- **ALDI**: also Special Buys with their dates. ALDI prices are refreshed daily; the answer's `notes` say when.
- **IGA**: the store's own prices and specials with their start and end dates, plus barcode.
- **Harris Farm**: the chosen store's prices, plus barcode and tags. Refreshed daily; the first answer can take up to 30 seconds.

The same key also covers **Woolworths New Zealand**: `GET /grocery-nz/search?store=woolworths-nz&query=milk`.

## What people build with it

- Coles vs Woolworths vs ALDI price comparison apps and browser extensions
- Basket and cost-of-living trackers ("what does my weekly shop cost at each store?")
- Half-price and specials alerts on Slack, Discord or e-mail
- AI shopping assistants that need today's price, not last year's
- Meal planners and budgeting apps that price a recipe at the nearest store

## Plans

| Plan | Price | Calls per month |
| --- | --- | --- |
| Basic | free | 50 |
| Pro | $9.99 | 1,000 |
| Ultra | $29.99 | 3,000 |
| Mega | $99.99 | 10,000 |

Figures as shown on the [pricing page](https://rapidapi.com/highbrowfame/api/australian-supermarket-prices-api-coles-woolworths-aldi/pricing) on 16 November 2026; the pricing page always has the current ones.

## Other countries

- **United Kingdom**: [UK Supermarket Prices API: Tesco, Sainsbury's, Asda, Morrisons](https://rapidapi.com/highbrowfame/api/uk-supermarket-prices-tesco-sainsburys-asda-morrisons), with [code examples](https://github.com/projectworks007/uk-supermarket-prices-api)
- **New Zealand**: [New Zealand Supermarket Prices API: Woolworths (Countdown)](https://rapidapi.com/highbrowfame/api/new-zealand-supermarket-prices-api-woolworths-countdown)

## FAQ

**Do I need an account with the supermarkets?** No. One RapidAPI key covers all five stores.

**How fresh are the prices?** Coles, Woolworths and IGA are read when you call the API; ALDI and Harris Farm are refreshed daily. `scrapedAt` on every record shows exactly when.

**Can I search several stores in one call?** One store per call. `basket.py` shows how to loop over them.

**Can I get a whole category or the specials page?** Yes: pass the store's category or specials link as `searchUrl` instead of `query` (Coles, Woolworths, ALDI).

**A search returned nothing.** The answer's `problems` list says in plain words why, for example "Coles shows no products for this."

**Something missing?** Open an issue here or use the Discussions tab on the RapidAPI page.

## Start now

**[Subscribe to the free plan on RapidAPI](https://rapidapi.com/highbrowfame/api/australian-supermarket-prices-api-coles-woolworths-aldi)**, copy your key, and run `examples/search.py`. Fifty calls a month cost nothing; the Pro plan covers a daily basket tracker for $9.99.

---

The example code is MIT licensed. This project is independent and is not affiliated with Coles, Woolworths, ALDI, IGA or Harris Farm Markets. Maintained by highbrow_fame.
