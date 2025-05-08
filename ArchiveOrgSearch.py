import unittest
import urllib.parse  # Added missing import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import re
import os  # Add this import

class ArchiveOrgSearch(unittest.TestCase):

    def setUp(self):
        # Create meta_data directory if it doesn't exist
        self.output_dir = "meta_data"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        options = Options()
        options.set_preference("general.useragent.override", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        # Uncomment for headless mode
        # options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)

    def test_search_in_Archive_org(self):
        driver = self.driver
        wait = WebDriverWait(driver, 30)
        base_url = "https://archive.org/details/tv"

        # 1) list all creators you want to scrape
        creators = ["wncn", "wkrc"] # can update this list based on preferences 

        for creator in creators:
            # 2) set up your params per‐creator
            params = {
                "q": "abortion",
                "and[]": f'creator:"{creator}"'
            }

            # 3) reset pagination + data container
            current_page = 1
            video_data = []

            # 4) hit the first page
            driver.get(f"{base_url}?{urllib.parse.urlencode(params)}")
            self.assertIn("TV", driver.title)

            # optional: grab total_results if you need it
            total_results = self.get_total_results(driver)
            print(f"[{creator}] total results: {total_results}")

            # 5) loop through pages exactly as before
            while True:
                print(f"[{creator}] processing page {current_page}")
                items = self.process_page(driver, wait)
                if not items:
                    break

                # 6) extract data, but tag with the loop's creator
                for row in self.extract_page_data(items):
                    row["Creator"] = creator
                    video_data.append(row)

                # 7) advance to next page
                current_page += 1
                next_url = f"{base_url}?{urllib.parse.urlencode(params)}&page={current_page}"
                driver.get(next_url)
                if not self.page_has_results(driver):
                    break
                time.sleep(1.5)

            # 8) save each creator's results separately
            df = pd.DataFrame(video_data)
            out_name = os.path.join(self.output_dir, f"{creator}_abortion.xlsx")
            df.to_excel(out_name, index=False)
            print(f"Saved {len(video_data)} entries for {creator} → {out_name}")

    def get_total_results(self, driver):
        try:
            results_text = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.results"))
            ).text
            
            # Improved regex pattern for different result formats
            match = re.search(r'(\d{1,3}(?:,\d{3})*)\s+(?:results|items)', results_text, re.I)
            if match:
                return int(match.group(1).replace(',', ''))
        except Exception as e:
            print(f"Error detecting total results: {e}")
        return None

    def page_has_results(self, driver):
        try:
            return bool(driver.find_elements(By.CSS_SELECTOR, "div.item-ia.hov"))
        except:
            return False

    def process_page(self, driver, wait):
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-ia.hov")))
            return driver.find_elements(By.CSS_SELECTOR, "div.item-ia.hov")
        except Exception as e:
            print(f"Error loading page: {e}")
            return []

    def extract_page_data(self, items):
        page_data = []
        for item in items:
            try:
                data_id = item.get_attribute("data-id")
                title = item.find_element(By.CSS_SELECTOR, "div.ttl").text.strip()
                
                page_data.append({
                    "Unique Identifier": data_id,
                    "URL": f"https://archive.org/details/{data_id}",
                    "Title": title,
                    "Creator": "x",
                    "All Time Views": self.extract_metric(item, "iconochive-eye"),
                    "Favorites": self.extract_metric(item, "iconochive-favorite"),
                    "Number of Quotes": self.extract_metric(item, "iconochive-quote"),
                    "Script": self.clean_script(item)
                })
            except Exception as e:
                print(f"Skipping item: {str(e)}")
        return page_data

    def extract_metric(self, item, icon_class):
        try:
            # Find the h1 element containing the specific icon class
            element = item.find_element(By.XPATH, f".//h1[contains(@class, 'stat')]//span[contains(@class, '{icon_class}')]/..")
            # Get the text content and extract the number
            text = element.text.strip()
            # Remove any non-numeric characters and return the number
            return re.sub(r'[^\d]', '', text) or "0"
        except Exception as e:
            print(f"Error extracting metric {icon_class}: {str(e)}")
            return "0"
    
    def clean_script(self, item):
        try:
            script_div = item.find_element(By.CSS_SELECTOR, "div.hidden-lists.SIN p.sin-detail")
            return re.sub(r'<[^>]+>', '', script_div.get_attribute("innerHTML"))
        except:
            return ""

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)