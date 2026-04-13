"""
Cambodia Universities - Wikipedia Source
Since EMIS doesn't expose a public university API,
this scrapes Wikipedia's official MoEYS list.
"""

import json
import time
import requests
from bs4 import BeautifulSoup

OUTPUT_FILE = "cambodia_universities.json"
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_universities_in_Cambodia"

def scrape_wikipedia():
    print("[*] Fetching Wikipedia list of universities in Cambodia...")
    resp = requests.get(WIKI_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    universities = []
    tables = soup.find_all("table", class_="wikitable")

    type_labels = ["Public", "Private"]

    for i, table in enumerate(tables):
        utype = type_labels[i] if i < len(type_labels) else "Unknown"
        rows = table.find_all("tr")[1:]  # skip header
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 4:
                name_cell = cols[0]
                # Get clean English name (first line before Khmer script)
                full_text = name_cell.get_text(separator="\n", strip=True)
                name_en = full_text.split("\n")[0].strip()

                abbrev = cols[1].get_text(strip=True)
                established = cols[2].get_text(strip=True)
                location = cols[3].get_text(strip=True)

                # Get website if available
                website = ""
                if len(cols) >= 5:
                    link = cols[4].find("a", href=True)
                    if link:
                        website = link["href"]

                universities.append({
                    "name": name_en,
                    "abbreviation": abbrev,
                    "type": utype,
                    "established": established,
                    "location": location,
                    "website": website
                })

    output = {
        "source": WIKI_URL,
        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(universities),
        "universities": universities
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"[+] Done! Found {len(universities)} universities.")
    print(f"[+] Saved to: {OUTPUT_FILE}")
    return output

if __name__ == "__main__":
    scrape_wikipedia()