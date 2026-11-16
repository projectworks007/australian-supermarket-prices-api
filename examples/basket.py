"""Price the same basket at Coles and Woolworths (or more stores) and show which one is cheapest.

Usage:
    RAPIDAPI_KEY=your-key python basket.py "weet-bix 575g" "vegemite 380g" "nescafe blend 43 150g"
    RAPIDAPI_KEY=your-key python basket.py --stores=coles,woolworths,aldi "butter 250g" "rolled oats 750g"

One call per item per store (3 items at 2 stores = 6 calls). Name the pack size ("575g", "2l", "380g"): only a
product with that size counts as a match, and multipacks are skipped unless you ask for one ("6 x 375ml"),
so the totals compare like with like. A store that misses an item is left out of the ranking.
ALDI sells mostly its own brands: use generic names ("butter 250g") when you include it.
"""
import re
import sys

from search import has_size, label, search

DEFAULT_STORES = ["coles", "woolworths"]
SIZE = re.compile(r"\d+(?:\.\d+)?\s*(?:kg|g|ml|l|litres?|pack)\b", re.I)
MULTIPACK = re.compile(r"\d+\s*x\s*\d+", re.I)


def like_for_like(item, results):
    """The first result that carries every pack size named in the item."""
    sizes = SIZE.findall(item)
    for product in results:
        name = label(product)
        if MULTIPACK.search(name) and not MULTIPACK.search(item):
            continue
        if all(has_size(name, size) for size in sizes):
            return product
    return None


def main():
    items = [a for a in sys.argv[1:] if not a.startswith("--")]
    chosen = [a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--stores=")]
    stores = chosen[0] if chosen else DEFAULT_STORES
    if not items:
        sys.exit(__doc__)
    totals = {store: 0.0 for store in stores}
    missing = {store: 0 for store in stores}
    for item in items:
        print(f"\n{item}")
        for store in stores:
            product = like_for_like(item, search(store, item, limit=8)["results"])
            if not product:
                missing[store] += 1
                print(f"  {store:<11} no like-for-like match")
                continue
            totals[store] += product["price"]
            offer = "  (on special)" if product.get("isOnSpecial") else ""
            print(f'  {store:<11} ${product["price"]:.2f}  {label(product)}{offer}')
    print(f"\nBasket total ({len(items)} items)")
    complete = sorted((total, store) for store, total in totals.items() if not missing[store])
    for total, store in complete:
        print(f"  {store:<11} ${total:.2f}")
    for store in stores:
        if missing[store]:
            print(f"  {store:<11} {missing[store]} item(s) not matched, left out")


if __name__ == "__main__":
    main()
