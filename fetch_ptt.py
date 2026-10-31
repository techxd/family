import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.ptt.cc"
START_URL = "https://www.ptt.cc/bbs/DC_SALE/index.html"
HEADERS = {"User-Agent": "Mozilla/5.0"}
COOKIES = {"over18": "1"}


def extract_price_from_text(text: str) -> str:
    if not text:
        return ""
    block_match = re.search(
        r"[【\[](?:交易價格|希望價格|欲售價格|售價|價格)[】\]]\s*(?:[（(][^）)\n]*[）)])?\s*[:：]?\s*([\s\S]*?)(?=\n\s*[【\[]|\n--|\Z)",
        text,
    )
    if block_match:
        block = block_match.group(1).strip()
        lines = [
            re.sub(r"^[（(]請務必填寫[^）)]*[）)]\s*", "", line.strip())
            for line in block.splitlines()
            if line.strip()
        ]
        lines = [l for l in lines if l]
        if lines:
            combined = " / ".join(lines[:2])
            return combined[:60]

    patterns = [
        r"(?:交易價格|希望價格|欲售價格|售價)\s*[:：]\s*([^\n\r]+)",
    ]
    for pat in patterns:
        match = re.search(pat, text)
        if match:
            price_line = match.group(1).strip()
            if price_line:
                return price_line[:60]
    return ""


def extract_price_from_title(title: str) -> str:
    match = re.search(r"(?:\$|NT\$?|售)\s*(\d{1,3}(?:,\d{3})+|\d{3,6})\s*元?", title, re.IGNORECASE)
    if match:
        return f"${match.group(1)}"
    return ""


def fetch_article_price(item: dict) -> dict:
    price = extract_price_from_title(item["title"])
    try:
        resp = requests.get(item["url"], headers=HEADERS, cookies=COOKIES, timeout=8)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            main_content = soup.find(id="main-content")
            if main_content:
                body_price = extract_price_from_text(main_content.get_text())
                if body_price:
                    price = body_price
    except Exception:
        pass
    item["price"] = price if price else "請洽內文"
    return item


def main():
    current_url = START_URL
    articles = []
    seen_urls = set()

    for page in range(5):
        if not current_url:
            break
        resp = requests.get(current_url, headers=HEADERS, cookies=COOKIES, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        main_container = soup.select_one(".r-list-container")
        if not main_container:
            break

        page_entries = []
        for child in main_container.children:
            if getattr(child, "name", None) != "div":
                continue
            classes = child.get("class", [])
            if "r-list-sep" in classes:
                break
            if "r-ent" in classes:
                page_entries.append(child)

        # Reverse so newer posts on the same page appear first
        for ent in reversed(page_entries):
            title_div = ent.select_one(".title a")
            if not title_div:
                continue
            title = title_div.get_text(strip=True)
            href = title_div.get("href", "")
            if not href:
                continue

            # Filter only titles containing '[售' or '[賣' and exclude '徵' or '換'
            if not re.search(r"\[\s*[售賣]", title):
                continue
            if "徵" in title or "換" in title:
                continue

            full_url = BASE_URL + href if href.startswith("/") else href
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            date_div = ent.select_one(".meta .date")
            date_str = date_div.get_text(strip=True) if date_div else ""

            articles.append({
                "title": title,
                "date": date_str,
                "url": full_url,
                "price": "請洽內文",
            })

        # Find previous page link ("‹ 上頁")
        prev_link = None
        for btn in soup.select(".btn-group-paging a"):
            if "上頁" in btn.get_text():
                href = btn.get("href")
                if href:
                    prev_link = BASE_URL + href if href.startswith("/") else href
                break
        current_url = prev_link

    with ThreadPoolExecutor(max_workers=25) as executor:
        articles = list(executor.map(fetch_article_price, articles))

    output_data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(articles),
        "articles": articles,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully fetched {len(articles)} articles and saved to data.json")


if __name__ == "__main__":
    main()
