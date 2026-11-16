"""Search one Australian supermarket and print name, price, unit price and special for each product.

Usage:
    RAPIDAPI_KEY=your-key python search.py coles "milk 2l"
    RAPIDAPI_KEY=your-key python search.py woolworths coffee --specials
    RAPIDAPI_KEY=your-key python search.py iga "milk 2l" --postcode=3000
    RAPIDAPI_KEY=your-key python search.py harris-farm bananas --location=Broadway

Stores: coles, woolworths, aldi, iga, harris-farm. No dependencies (Python 3.8+).
Free key (50 calls a month):
https://rapidapi.com/highbrowfame/api/australian-supermarket-prices-api-coles-woolworths-aldi
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HOST = "australian-supermarket-prices-api-coles-woolworths-aldi.p.rapidapi.com"
BASE = "https://" + HOST


def search(store, query, limit=10, only_specials=False, **store_options):
    """Returns the API answer: {"site": ..., "count": n, "results": [...], "notes": [...], "problems": [...]}.

    store_options: postcode="3000" or storeId="32600" for IGA, location="Broadway" for Harris Farm.
    """
    params = {"store": store, "query": query, "limit": limit}
    if only_specials:
        params["onlySpecials"] = "true"
    params.update({key: value for key, value in store_options.items() if value})
    request = urllib.request.Request(
        BASE + "/grocery-au/search?" + urllib.parse.urlencode(params),
        headers={"x-rapidapi-key": os.environ["RAPIDAPI_KEY"], "x-rapidapi-host": HOST},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def has_size(name, size):
    """True when the name carries the pack size as a whole token: '2L' matches '2 l' and '2 Litres', not 'A2 Light'."""
    plain = lambda text: text.lower().replace("litres", "l").replace("litre", "l")
    parts = re.findall(r"[0-9.]+|[a-z]+", plain(size))
    pattern = r"(?<![a-z0-9.])" + r" *".join(re.escape(part) for part in parts) + r"(?![a-z0-9])"
    return bool(parts) and re.search(pattern, plain(name)) is not None


def label(product):
    """Product name with its pack size: Coles and IGA keep the size in a field of its own."""
    name = product["name"]
    size = (product.get("size") or product.get("packageSize") or product.get("packSize") or "").strip()
    return name if not size or has_size(name, size) else f"{name} {size}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    options = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if len(args) < 2:
        sys.exit(__doc__)
    store, query = args[0], " ".join(args[1:])
    answer = search(store, query, only_specials="--specials" in sys.argv, **options)
    print(f'{answer["count"]} products for "{query}" at {store}')
    for p in answer["results"]:
        was = f' (was ${p["wasPrice"]:.2f})' if (p.get("wasPrice") or 0) > p["price"] else ""
        unit = f'  {p["unitPriceText"]}' if p.get("unitPriceText") else ""
        offer = f'  [{p["promotion"]}]' if p.get("promotion") else ""
        print(f'  ${p["price"]:.2f}{was}{unit}  {label(p)}{offer}')
    for note in answer.get("notes", []):
        print("  note:", note)
    for problem in answer.get("problems", []):
        print("  problem:", problem.get("error"))


if __name__ == "__main__":
    main()
