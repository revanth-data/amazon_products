
# import os
# import subprocess

# # Auto-install Playwright Chromium binaries on cloud startup
# os.system("playwright install chromium")
# os.system("playwright install-deps chromium")

# import streamlit as st

# import csv
# import json
# import os
# import random
# import time
# from concurrent.futures import ThreadPoolExecutor

# import pandas as pd
# from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright
# from playwright_stealth import Stealth

# # --- STREAMLIT PAGE CONFIG ---
# st.set_page_config(
#     page_title="Amazon Top 50-100 Multi-Page Extractor",
#     page_icon="🛒",
#     layout="wide"
# )

# st.title("🛒 Amazon India Multi-Page Rank & SEO Intelligence")
# st.caption("Scrape 50 to 100 products across pages to capture both Actual Search Order and Pure Organic SEO Ranks.")


# # --- PLAYWRIGHT SCRAPER TASK ---
# # def run_playwright_scraper(search_query, target_count=50):
# #     asins_meta = []  # Stores dicts with metadata discovered from search pages
# #     all_competitor_data = []

# #     with Stealth().use_sync(sync_playwright()) as p:
# #         browser = p.chromium.launch(
# #             headless=True,
# #             args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
# #         )

# #         context = browser.new_context(
# #             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
# #             viewport={"width": 1920, "height": 1080},
# #             locale="en-IN"
# #         )

# # --- UPDATE THIS SECTION IN YOUR app.py ---
# def run_playwright_scraper(search_query, target_count=50):
#     asins_meta = []
#     all_competitor_data = []

#     with sync_playwright() as p:
#         # Pass required sandbox and memory flags for Linux cloud hosting
#         browser = p.chromium.launch(
#             headless=True,
#             args=[
#                 "--no-sandbox",
#                 "--disable-setuid-sandbox",
#                 "--disable-dev-shm-usage",
#                 "--disable-gpu",
#                 "--disable-blink-features=AutomationControlled",
#             ]
#         )

#         context = browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
#             viewport={"width": 1920, "height": 1080},
#             locale="en-IN"
#         )
        

#         page = context.new_page()

#         # Phase 1: Paginate through Search Pages until target_count is reached
#         current_page = 1
#         seen_asins = set()
#         overall_rank_counter = 1
#         organic_seo_counter = 1

#         status_text = st.empty()

#         while len(asins_meta) < target_count and current_page <= 5:
#             status_text.text(f"Scanning Search Result Page {current_page}...")
#             url = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}&page={current_page}"
            
#             try:
#                 page.goto(url, wait_until="domcontentloaded")
                
#                 # Smooth scrolling to ensure all lazy-loaded DOM elements render
#                 for scroll in range(3):
#                     page.evaluate("window.scrollBy(0, 800)")
#                     time.sleep(0.5)

#                 time.sleep(random.uniform(2, 3))
#                 soup = BeautifulSoup(page.content(), "html.parser")
                
#                 cards_found_on_page = 0
#                 for card in soup.select("div[data-asin]"):
#                     asin = card.get("data-asin")
#                     if asin and len(asin) == 10 and asin not in seen_asins:
#                         seen_asins.add(asin)
#                         cards_found_on_page += 1

#                         # Identify if the listing is a Sponsored Ad
#                         card_str = str(card)
#                         is_sponsored = False
#                         if (
#                             card.select_one(".puis-sponsored-label-text, .s-sponsored-label-info-icon, .s-shopping-ad-attribute")
#                             or "sponsored" in card_str.lower()
#                             or "s-shopping-ad" in card_str.lower()
#                         ):
#                             is_sponsored = True

#                         # Calculate Organic SEO Rank
#                         if is_sponsored:
#                             organic_rank = "N/A (Paid Ad)"
#                             placement_label = "Sponsored Ad"
#                         else:
#                             organic_rank = organic_seo_counter
#                             placement_label = "Organic Result"
#                             organic_seo_counter += 1

#                         asins_meta.append({
#                             "ASIN": asin,
#                             "Overall_Page_Rank": overall_rank_counter,
#                             "Organic_SEO_Rank": organic_rank,
#                             "Placement_Type": placement_label,
#                             "Search_Page_Num": current_page
#                         })

#                         overall_rank_counter += 1
#                         if len(asins_meta) >= target_count:
#                             break

#                 if cards_found_on_page == 0:
#                     st.warning(f"No additional ASINs found on Page {current_page}. Stopping search pagination.")
#                     break

#                 current_page += 1

#             except Exception as e:
#                 st.error(f"Error fetching search page {current_page}: {e}")
#                 break

#         # Phase 2: Scrape Deep Product Details for Discovered ASINs
#         progress_bar = st.progress(0)

#         for idx, item in enumerate(asins_meta, 1):
#             asin = item["ASIN"]
#             status_text.text(f"Extracting product details {idx} of {len(asins_meta)} (ASIN: {asin})...")
#             prod_url = f"https://www.amazon.in/dp/{asin}"

#             try:
#                 page.goto(prod_url, wait_until="domcontentloaded")
#                 page.evaluate("window.scrollBy(0, 500)")
#                 time.sleep(random.uniform(1.5, 2.5))

#                 prod_soup = BeautifulSoup(page.content(), "html.parser")

#                 title = prod_soup.select_one("#productTitle")
#                 rating = prod_soup.select_one("i.a-icon-star span")
#                 reviews = prod_soup.select_one("#acrCustomerReviewText")

#                 # Selling Price Extraction
#                 price_el = prod_soup.select_one(".a-price[data-a-size='xl'] .a-price-whole, .a-price .a-price-whole")
#                 price_val = price_el.text.replace(",", "").strip().rstrip(".") if price_el else "N/A"

#                 # M.R.P. Extraction
#                 mrp_val = "N/A"
#                 mrp_el = prod_soup.select_one("span.a-basisPrice span.a-offscreen, .a-text-price[data-a-strike='true'] span.a-offscreen")

#                 if mrp_el:
#                     mrp_val = mrp_el.text.replace("₹", "").replace(",", "").strip()
#                 else:
#                     for text_node in prod_soup.find_all(string=True):
#                         if "m.r.p" in text_node.lower():
#                             parent_el = text_node.find_parent(["span", "td", "tr", "div"])
#                             if parent_el:
#                                 strike_price = parent_el.select_one(".a-offscreen")
#                                 if strike_price:
#                                     mrp_val = strike_price.text.replace("₹", "").replace(",", "").strip()
#                                     break

#                 if mrp_val != "N/A" and "/" in mrp_val:
#                     mrp_val = mrp_val.split("/")[0].strip()

#                 # Feature Bullets
#                 bullets = [
#                     li.text.strip()
#                     for li in prod_soup.select("#feature-bullets ul li span.a-list-item")
#                     if li.text.strip()
#                 ]

#                 # Technical Specifications Table
#                 specs = {}
#                 for row in prod_soup.select("#productDetails_techSpec_section_1 tr, #prodDetails tr"):
#                     th = row.select_one("th")
#                     td = row.select_one("td")
#                     if th and td:
#                         specs[th.text.strip().replace("\xa0", " ")] = td.text.strip().replace("\xa0", " ")

#                 all_competitor_data.append({
#                     "Overall_Page_Rank": item["Overall_Page_Rank"],
#                     "Organic_SEO_Rank": item["Organic_SEO_Rank"],
#                     "Placement_Type": item["Placement_Type"],
#                     "Search_Page_Num": item["Search_Page_Num"],
#                     "ASIN": asin,
#                     "Title": title.text.strip() if title else "N/A",
#                     "Price_INR": price_val,
#                     "MRP_INR": mrp_val,
#                     "Rating": rating.text.split()[0] if rating else "N/A",
#                     "Review_Count": reviews.text.strip() if reviews else "0",
#                     "Feature_Bullets": " | ".join(bullets),
#                     "Technical_Specifications": specs
#                 })

#             except Exception as e:
#                 st.warning(f"Failed to scrape detail page for ASIN {asin}: {e}")

#             progress_bar.progress(idx / len(asins_meta))

#         browser.close()
#         status_text.text("Extraction completed successfully!")
#         progress_bar.empty()

#     return all_competitor_data


# def process_json_to_df(data):
#     """Flattens nested dictionaries and dynamically formats dynamic spec columns."""
#     if not data:
#         return pd.DataFrame()

#     discovered_spec_keys = set()
#     for item in data:
#         specs = item.get("Technical_Specifications", {})
#         if isinstance(specs, dict):
#             discovered_spec_keys.update(specs.keys())

#     sorted_spec_keys = sorted(list(discovered_spec_keys))

#     rows = []
#     for item in data:
#         specs = item.get("Technical_Specifications", {})
#         if not isinstance(specs, dict):
#             specs = {}

#         row = {
#             "Overall_Page_Rank": item.get("Overall_Page_Rank"),
#             "Organic_SEO_Rank": item.get("Organic_SEO_Rank"),
#             "Placement_Type": item.get("Placement_Type"),
#             "Search_Page_Num": item.get("Search_Page_Num"),
#             "ASIN": item.get("ASIN"),
#             "Title": item.get("Title"),
#             "Price_INR": item.get("Price_INR"),
#             "MRP_INR": item.get("MRP_INR"),
#             "Rating": item.get("Rating"),
#             "Review_Count": item.get("Review_Count"),
#             "Feature_Bullets": item.get("Feature_Bullets")
#         }

#         for spec_key in sorted_spec_keys:
#             row[spec_key] = specs.get(spec_key, None)

#         rows.append(row)

#     return pd.DataFrame(rows)


# # --- STREAMLIT UI LAYOUT ---
# with st.sidebar:
#     st.header("Search Controls")
#     search_query = st.text_input("Enter Search Keyword", value="LED projector")
#     target_count = st.slider("Target Number of Products", min_value=20, max_value=100, value=50, step=10)
#     start_btn = st.button("🚀 Run Multi-Page Extractor", use_container_width=True)

# if start_btn:
#     if not search_query.strip():
#         st.error("Please enter a valid search keyword.")
#     else:
#         st.info(f"Extracting top **{target_count}** products for **'{search_query}'**...")

#         # Run Playwright inside a ThreadPoolExecutor to isolate the sync browser context
#         with ThreadPoolExecutor(max_workers=1) as executor:
#             future = executor.submit(run_playwright_scraper, search_query, target_count)
#             raw_data = future.result()

#         if raw_data:
#             df = process_json_to_df(raw_data)
#             st.session_state["scraped_df"] = df
#             st.session_state["query_name"] = search_query
#             st.success(f"Successfully scraped {len(df)} total products!")
#         else:
#             st.error("No products could be extracted.")

# # --- RESULTS DISPLAY AND DOWNLOAD ---
# if "scraped_df" in st.session_state:
#     df = st.session_state["scraped_df"]
#     query = st.session_state["query_name"]

#     st.subheader(f"Extracted Market Intelligence: *'{query}'*")
#     st.dataframe(df, use_container_width=True)

#     col1, col2 = st.columns(2)

#     # Download CSV Button
#     csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
#     col1.download_button(
#         label="📥 Download CSV Dataset",
#         data=csv_bytes,
#         file_name=f"amazon_{query.replace(' ', '_')}_top{len(df)}.csv",
#         mime="text/csv",
#         use_container_width=True
#     )

#     # Download Excel Button
#     excel_file = f"amazon_{query.replace(' ', '_')}.xlsx"
#     with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
#         df.to_excel(writer, index=False, sheet_name="Market Intelligence")

#     with open(excel_file, "rb") as f:
#         col2.download_button(
#             label="📊 Download Excel Spreadsheet",
#             data=f,
#             file_name=excel_file,
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#             use_container_width=True
#         )


import csv
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="Amazon Top 50-100 Multi-Page Extractor",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Amazon India Multi-Page Rank & SEO Intelligence")
st.caption("Scrape products across pages to capture both Actual Search Order and Pure Organic SEO Ranks.")

# Rotation of Realistic User Agents to prevent blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
    }

# --- LIGHTWEIGHT HTTP SCRAPER FUNCTION ---
def run_http_scraper(search_query, target_count=50):
    asins_meta = []
    all_competitor_data = []

    current_page = 1
    seen_asins = set()
    overall_rank_counter = 1
    organic_seo_counter = 1

    session = requests.Session()
    status_text = st.empty()

    # Phase 1: Search Page Pagination
    while len(asins_meta) < target_count and current_page <= 5:
        status_text.text(f"Scanning Search Page {current_page}...")
        url = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}&page={current_page}"
        
        try:
            response = session.get(url, headers=get_headers(), timeout=10)
            if response.status_code != 200:
                st.warning(f"Page {current_page} returned HTTP {response.status_code}. Stopping pagination.")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            cards_found_on_page = 0

            for card in soup.select("div[data-asin]"):
                asin = card.get("data-asin")
                if asin and len(asin) == 10 and asin not in seen_asins:
                    seen_asins.add(asin)
                    cards_found_on_page += 1

                    card_str = str(card)
                    is_sponsored = False
                    if (
                        card.select_one(".puis-sponsored-label-text, .s-sponsored-label-info-icon, .s-shopping-ad-attribute")
                        or "sponsored" in card_str.lower()
                        or "s-shopping-ad" in card_str.lower()
                    ):
                        is_sponsored = True

                    if is_sponsored:
                        organic_rank = "N/A (Paid Ad)"
                        placement_label = "Sponsored Ad"
                    else:
                        organic_rank = organic_seo_counter
                        placement_label = "Organic Result"
                        organic_seo_counter += 1

                    asins_meta.append({
                        "ASIN": asin,
                        "Overall_Page_Rank": overall_rank_counter,
                        "Organic_SEO_Rank": organic_rank,
                        "Placement_Type": placement_label,
                        "Search_Page_Num": current_page
                    })

                    overall_rank_counter += 1
                    if len(asins_meta) >= target_count:
                        break

            if cards_found_on_page == 0:
                break

            current_page += 1
            time.sleep(random.uniform(1.0, 2.0))

        except Exception as e:
            st.error(f"Error fetching page {current_page}: {e}")
            break

    # Phase 2: Product Detail Extraction
    progress_bar = st.progress(0)

    for idx, item in enumerate(asins_meta, 1):
        asin = item["ASIN"]
        status_text.text(f"Extracting product details {idx} of {len(asins_meta)} (ASIN: {asin})...")
        prod_url = f"https://www.amazon.in/dp/{asin}"

        try:
            prod_resp = session.get(prod_url, headers=get_headers(), timeout=10)
            if prod_resp.status_code == 200:
                prod_soup = BeautifulSoup(prod_resp.content, "html.parser")

                title = prod_soup.select_one("#productTitle")
                rating = prod_soup.select_one("i.a-icon-star span")
                reviews = prod_soup.select_one("#acrCustomerReviewText")

                price_el = prod_soup.select_one(".a-price[data-a-size='xl'] .a-price-whole, .a-price .a-price-whole")
                price_val = price_el.text.replace(",", "").strip().rstrip(".") if price_el else "N/A"

                mrp_val = "N/A"
                mrp_el = prod_soup.select_one("span.a-basisPrice span.a-offscreen, .a-text-price[data-a-strike='true'] span.a-offscreen")
                if mrp_el:
                    mrp_val = mrp_el.text.replace("₹", "").replace(",", "").strip()

                bullets = [
                    li.text.strip()
                    for li in prod_soup.select("#feature-bullets ul li span.a-list-item")
                    if li.text.strip()
                ]

                specs = {}
                for row in prod_soup.select("#productDetails_techSpec_section_1 tr, #prodDetails tr"):
                    th = row.select_one("th")
                    td = row.select_one("td")
                    if th and td:
                        specs[th.text.strip().replace("\xa0", " ")] = td.text.strip().replace("\xa0", " ")

                all_competitor_data.append({
                    "Overall_Page_Rank": item["Overall_Page_Rank"],
                    "Organic_SEO_Rank": item["Organic_SEO_Rank"],
                    "Placement_Type": item["Placement_Type"],
                    "Search_Page_Num": item["Search_Page_Num"],
                    "ASIN": asin,
                    "Title": title.text.strip() if title else "N/A",
                    "Price_INR": price_val,
                    "MRP_INR": mrp_val,
                    "Rating": rating.text.split()[0] if rating else "N/A",
                    "Review_Count": reviews.text.strip() if reviews else "0",
                    "Feature_Bullets": " | ".join(bullets),
                    "Technical_Specifications": specs
                })

            time.sleep(random.uniform(0.5, 1.2))

        except Exception as e:
            st.warning(f"Failed to fetch details for ASIN {asin}: {e}")

        progress_bar.progress(idx / len(asins_meta))

    status_text.text("Extraction completed successfully!")
    progress_bar.empty()

    return all_competitor_data


def process_json_to_df(data):
    if not data:
        return pd.DataFrame()

    discovered_spec_keys = set()
    for item in data:
        specs = item.get("Technical_Specifications", {})
        if isinstance(specs, dict):
            discovered_spec_keys.update(specs.keys())

    sorted_spec_keys = sorted(list(discovered_spec_keys))

    rows = []
    for item in data:
        specs = item.get("Technical_Specifications", {})
        if not isinstance(specs, dict):
            specs = {}

        row = {
            "Overall_Page_Rank": item.get("Overall_Page_Rank"),
            "Organic_SEO_Rank": item.get("Organic_SEO_Rank"),
            "Placement_Type": item.get("Placement_Type"),
            "Search_Page_Num": item.get("Search_Page_Num"),
            "ASIN": item.get("ASIN"),
            "Title": item.get("Title"),
            "Price_INR": item.get("Price_INR"),
            "MRP_INR": item.get("MRP_INR"),
            "Rating": item.get("Rating"),
            "Review_Count": item.get("Review_Count"),
            "Feature_Bullets": item.get("Feature_Bullets")
        }

        for spec_key in sorted_spec_keys:
            row[spec_key] = specs.get(spec_key, None)

        rows.append(row)

    return pd.DataFrame(rows)


# --- STREAMLIT UI ---
with st.sidebar:
    st.header("Search Controls")
    search_query = st.text_input("Enter Search Keyword", value="lumio projector")
    target_count = st.slider("Target Number of Products", min_value=20, max_value=100, value=20, step=10)
    start_btn = st.button("🚀 Run Multi-Page Extractor", use_container_width=True)

if start_btn:
    if not search_query.strip():
        st.error("Please enter a valid search keyword.")
    else:
        st.info(f"Extracting top **{target_count}** products for **'{search_query}'**...")
        raw_data = run_http_scraper(search_query, target_count)

        if raw_data:
            df = process_json_to_df(raw_data)
            st.session_state["scraped_df"] = df
            st.session_state["query_name"] = search_query
            st.success(f"Successfully scraped {len(df)} products!")
        else:
            st.error("No products extracted.")

if "scraped_df" in st.session_state:
    df = st.session_state["scraped_df"]
    query = st.session_state["query_name"]

    st.subheader(f"Extracted Market Intelligence: *'{query}'*")
    st.dataframe(df, use_container_width=True)

    csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="📥 Download CSV Dataset",
        data=csv_bytes,
        file_name=f"amazon_{query.replace(' ', '_')}.csv",
        mime="text/csv"
    )
