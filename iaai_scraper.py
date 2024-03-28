import time
import random
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from selenium.common.exceptions import NoSuchElementException

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def slow_scroll_to(driver, x, y, duration=1):
    """
    Slowly scrolls the page to the specified coordinates (x, y) over the given duration.
    """
    current_x = driver.execute_script("return window.scrollX;")
    current_y = driver.execute_script("return window.scrollY;")
    distance_x = x - current_x
    distance_y = y - current_y
    start_time = time.time()
    while time.time() - start_time <= duration:
        elapsed_time = time.time() - start_time
        progress = min(1, elapsed_time / duration)
        target_x = current_x + distance_x * progress
        target_y = current_y + distance_y * progress
        driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", target_x, target_y)
        time.sleep(random.uniform(0.5, 3))  # Adjust the sleep duration for smoother scrolling

def solve_captcha(captcha_image_path):
    """
    Solve CAPTCHA using 2Captcha API.
    """
    api_key = 'your_2captcha_api_key'  # Replace with your actual 2Captcha API key
    solver = TwoCaptcha(api_key)
    
    captcha_id = solver.normal(captcha_file=captcha_image_path)

    # Poll 2Captcha API until solution is received
    while True:
        try:
            solution_response = solver.get_result(captcha_id)
            if solution_response['status'] == 1:
                captcha_solution = solution_response['code']
                return captcha_solution
            elif solution_response['status'] == 0:
                time.sleep(5)  # Wait for a few seconds before checking again
        except Exception as e:
            print(f"Error occurred while solving CAPTCHA: {e}")

def check_for_captcha(driver):
    """
    Check if a CAPTCHA is present on the page.
    """
    try:
        driver.find_element(By.ID, "main-iframe")  # Replace "captcha-id" with the actual ID of the CAPTCHA element
        return True
    except NoSuchElementException:
        return False

def search_iaai_website(search_query, max_mileage=100000, max_pages=3, min_delay=2, max_delay=5, min_page_load_delay=3, max_page_load_delay=7):
    try:
        # Set up the Chrome driver
        chrome_path = '/opt/homebrew/bin/chromedriver'
        chrome_service = ChromeService(executable_path=chrome_path)
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={get_random_user_agent()}')  # Rotate User-Agent
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        overall_index = 0

        # Visit the first page
        page_url = f'https://iaai.com/Search?searchkeyword={search_query}&page=1'
        driver.get(page_url)

        # Check for CAPTCHA upon opening the website
        if check_for_captcha(driver):
            print("CAPTCHA detected upon opening the website.")
            # Handle the CAPTCHA (e.g., solve it using 2Captcha)
            # captcha_solution = solve_captcha(captcha_image_path)  # Replace with the path to the CAPTCHA image
            # Once the CAPTCHA is solved, proceed with further actions
        else:
            print("No CAPTCHA detected upon opening the website.")
            # Proceed with further actions

        for page_number in range(1, max_pages + 1):
            print("URL: ", driver.current_url)
            # Wait for a random time delay before processing the page
            delay = random.uniform(min_delay, max_delay)
            time.sleep(delay)

            # Handle the cookie prompt (click "I understand")
            try:
                cookie_prompt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
                cookie_prompt.click()
            except:
                print("Cookie prompt not found or could not be clicked.")

            # Wait for the interfering element (cookie banner) to become invisible
            wait = WebDriverWait(driver, 10)
            wait.until(EC.invisibility_of_element_located((By.ID, "onetrust-pc-btn-handler")))

            # Generate a random delay after loading the page
            page_load_delay = random.uniform(min_page_load_delay, max_page_load_delay)
            time.sleep(page_load_delay)

            # Refresh the current page
            driver.refresh()

            # Check if a CAPTCHA is present after refreshing the page
            if check_for_captcha(driver):
                print("CAPTCHA detected after refreshing the page.")
                # Handle the CAPTCHA (e.g., solve it using 2Captcha)
                # captcha_solution = solve_captcha(captcha_image_path)  # Replace with the path to the CAPTCHA image
                # Once the CAPTCHA is solved, proceed with further actions
            else:
                print("No CAPTCHA detected after refreshing the page.")
                # Proceed with further actions

        # Close the browser when done
        driver.quit()

    except Exception as e:
        print(f"Error: {e}")

# Example usage
search_query = 'Intact Airbags Clear Run Drive Public'
max_mileage = 10000000  # Set the maximum mileage threshold
max_pages = 4  # Set the maximum number of pages to search
min_delay = 3  # Minimum delay between page loads (in seconds)
max_delay = 7  # Maximum delay between page loads (in seconds)
min_page_load_delay = 1  # Minimum additional delay after loading each page (in seconds)
max_page_load_delay = 3  # Maximum additional delay after loading each page (in seconds)
search_iaai_website(search_query, max_mileage, max_pages, min_delay, max_delay, min_page_load_delay, max_page_load_delay)
