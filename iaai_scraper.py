import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def search_iaai_website(search_query, max_mileage=100000, max_pages=3, delay=2):
    try:
        # Set up the Chrome driver
        chrome_path = '/opt/homebrew/bin/chromedriver'
        chrome_service = ChromeService(executable_path=chrome_path)
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument(f'user-agent={get_random_user_agent()}')  # Rotate User-Agent
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        overall_index = 0

        for page_number in range(1, max_pages + 1):
            # Build the URL for the current page
            page_url = f'https://iaai.com/Search?searchkeyword={search_query}&page={page_number}'

            # Open the page in the browser
            driver.get(page_url)

            # Wait for a short time (delay) before processing the page
            time.sleep(delay)

            # Extract and print information related to vehicles on the current page
            vehicle_infos = driver.find_elements(By.CLASS_NAME, 'heading-7.rtl-disabled')
            mileage_elements = driver.find_elements(By.CLASS_NAME, 'data-list__value.rtl-disabled')  # Replace with the actual class for mileage
            location_elements = driver.find_elements(By.CSS_SELECTOR, 'span.data-list__value.text-truncate[title]')  # Replace with the actual class and title for location

            for index, (vehicle_info, mileage_element, location_element) in enumerate(zip(vehicle_infos, mileage_elements, location_elements), start=1):
                if mileage_element:
                    # Extract the numeric part of the mileage
                    mileage_text = mileage_element.text.replace('Mileage:', '').replace('miles', '').replace(',', '').strip()

                    try:
                        if 'Not Actual' not in mileage_text and 'Not Required/Exempt' not in mileage_text and 'Inoperable Digital Dash' not in mileage_text:
                            mileage_numeric = int(''.join(filter(str.isdigit, mileage_text)))
                            if mileage_numeric <= max_mileage:
                                overall_index += 1  # Increment the overall index
                                print(f"\nVehicle {overall_index} Information:")

                                # Trim the location to only display "Branch:" and the name of the location
                                trimmed_location = location_element.get_attribute('title').replace('Branch:', '').strip()
                                print(f"Location: Branch: {trimmed_location}")

                                print(f"Mileage: {mileage_numeric} miles")
                                print(vehicle_info.text.strip())
                                print("-" * 50)

                    except ValueError:
                        print(f"\nError: Unable to convert mileage to integer for Vehicle {index}. Mileage: {mileage_text}")

        # Close the browser when done
        driver.quit()

    except Exception as e:
        print(f"Error: {e}")

# Example usage
search_query = 'Intact Airbags Clear Run Drive Public'
max_mileage = 10000000  # Set the maximum mileage threshold
max_pages = 10000  # Set the maximum number of pages to search
search_iaai_website(search_query, max_mileage, max_pages, delay=5)  # Set delay to 5 seconds

