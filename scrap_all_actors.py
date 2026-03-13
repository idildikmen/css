import pandas as pd
import os
from playwright.sync_api import sync_playwright
import re
import time

# SET UP:
START_INDEX = 143  # We change this step by step not to get blocked
BATCH_SIZE = 10
END_INDEX = START_INDEX + BATCH_SIZE
LINKS_FILE = 'eu_policies_with_feedback_links.csv'
RESULTS_FILE = 'stakeholder_analysis_final.csv'

# 1. Load the links
df_links = pd.read_csv(LINKS_FILE)
df_batch = df_links[START_INDEX:END_INDEX]

def scrape_stats_page(df_subset):
    all_results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        for index, row in df_subset.iterrows():
            url = row['correct_feedback_url']
            if pd.isna(url): continue

            print(f"[{index}] Scrapping stats from: {url}")
            row_data = {
                'index_ref': index, # Keep original index for matching
                'title': row['title'],
                'topic': row['topic'],
                'url': url,
                'total_feedback_check': row['feedback_count']
            }

            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
                stats_tab = page.get_by_role("tab", name="Statistics")
                stats_tab.wait_for(state="visible", timeout=10000)
                stats_tab.click()

                legend_selector = "g.highcharts-legend-item text"
                page.wait_for_selector(legend_selector, timeout=20000)
                labels = page.locator(legend_selector).all_text_contents()

                for text in labels:
                    match = re.search(r"^(.*?):\s*(\d+)\s*\(([\d.]+)%\)", text)
                    if match:
                        row_data[match.group(1).strip()] = int(match.group(2))
                
                print(f"   > Success.")
                all_results.append(row_data)
            except Exception as e:
                print(f"   > Error at {url}: {e}")
                all_results.append(row_data)
            
            time.sleep(2)
        browser.close()
    return pd.DataFrame(all_results)

# Run step by step:
print(f"Running batch: {START_INDEX} to {END_INDEX}...")
new_results_df = scrape_stats_page(df_batch)

# 2. Updating the main Results file
if os.path.exists(RESULTS_FILE):
    existing_df = pd.read_csv(RESULTS_FILE)
    updated_df = pd.concat([existing_df, new_results_df], ignore_index=True)
else:
    updated_df = new_results_df

# 3. Clean and Save
updated_df = updated_df.fillna(0)
updated_df.to_csv(RESULTS_FILE, index=False)

print(f"\nDone! Total records in {RESULTS_FILE}: {len(updated_df)}")
print(f"Next time, set START_INDEX to {END_INDEX}")