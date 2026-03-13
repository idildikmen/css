import pandas as pd
from playwright.sync_api import sync_playwright
import time
import random

df = pd.read_csv('eu_policies_high_engagement.csv')

def get_detailed_links(df_subset):
    # We will work on a copy 
    df_work = df_subset.copy()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36")
        page = context.new_page()

        print(f"Starting extraction for {len(df_work)} policies...")

        for index, row in df_work.iterrows():
            url = row['initiative_url']
            print(f"[{index+1}/{len(df_work)}] Navigating to: {url}")
            
            try:
                # Navigate to the page
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Locate the link
                # Using .first in case there are multiple matches
                feedback_link = page.locator("a:has-text('View feedback received')").first
                
                # Wait for the page and item to exist
                feedback_link.wait_for(state="attached", timeout=10000)
                
                # Extract href
                href = feedback_link.get_attribute("href")
                
                if href:
                    full_url = "https://ec.europa.eu" + href if href.startswith('/') else href
                    print(f"   > Found: {full_url}")
                    df_work.at[index, "correct_feedback_url"] = full_url
                else:
                    print(f"   > No href found for {url}")
                    df_work.at[index, "correct_feedback_url"] = None

            except Exception as e:
                print(f"   > Error at {url}: {e}")
                df_work.at[index, "correct_feedback_url"] = None
            
            time.sleep(1) # Small delay

        browser.close()
    
    return df_work

# Execute the code:

#%%

# Select the next 15 rows (index 15 up to 30)
df_next_batch = df[130:] #We change this to start from where we left.

# Run the function for this specific batch
df_processed_batch = get_detailed_links(df_next_batch)

# Append to the existing CSV
# mode='a' is append
# header=False prevents writing the column names again

df_processed_batch.to_csv('eu_policies_with_feedback_links.csv', mode='a', header=False, index=False)

print(f"\nBatch 15-30 processed and appended to 'eu_policies_with_feedback_links.csv'")

check_len = pd.read_csv('eu_policies_with_feedback_links.csv')
print(f"Total rows now in CSV: {len(check_len)}")
