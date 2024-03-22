import time
import random
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

def random_mouse_movement(driver):
    x, y = random.uniform(1, 50), random.uniform(1, 50)
    driver.execute_script(f"window.scrollBy({x}, {y})")

def retrieve_proxies():
    # Retrieve proxies from spys.me
    regex = r"[0-9]+(?:\.[0-9]+){3}:[0-9]+"
    c = requests.get("https://spys.me/proxy.txt")
    test_str = c.text
    a = re.finditer(regex, test_str, re.MULTILINE)
    with open("proxies_list.txt", 'w') as file:
        for i in a:
            print(i.group(), file=file)
            print(f"Proxy added: {i.group()}")

    # Retrieve proxies from free-proxy-list.net
    c = requests.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(c.content, 'html.parser')
    z = soup.find('textarea').get_text()
    x = re.findall(regex, z)
    with open("proxies_list.txt", "a") as myfile:
        for i in x:
            print(i, file=myfile)
            print(f"Proxy added: {i}")

def load_proxy_list(file_path='proxies_list.txt'):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def search_iaai_website(search_query, max_mileage=100000, max_pages=3, delay_range=(2, 5), use_proxy=False):
    if use_proxy:
        retrieve_proxies()  # Retrieve proxies if using proxy

    proxies = load_proxy_list() if use_proxy else None

    try:
        # Set up the Chrome driver in headless mode
        chrome_path = '/opt/homebrew/bin/chromedriver'
        chrome_service = ChromeService(executable_path=chrome_path)
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Enable headless mode
        chrome_options.add_argument(f'user-agent={get_random_user_agent()}')  # Rotate User-Agent

        if use_proxy and proxies:
            # Set up proxy if provided
            chrome_options.add_argument(f'--proxy-server={proxies[0]}')
            print(f"Using Proxy: {proxies[0]}")

        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        overall_index = 0

        for page_number in range(1, max_pages + 1):
            # Build the URL for the current page
            page_url = f'https://www.iaai.com/SalesList/iaaai?ToPage={page_number}&SearchResultsPerPage=25&IsSearch=True&Keyword={search_query}'

            # Open the page in the browser
            driver.get(page_url)

            # Wait for a short time (delay) before processing the page
            time.sleep(random.uniform(*delay_range))

            # Simulate random mouse movement
            random_mouse_movement(driver)

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
                        print(f"\nError: Unable to convert mileage to integer for Vehicle {index}. Mileage: {
