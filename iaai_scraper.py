import requests
from bs4 import BeautifulSoup

def search_iaai_website(search_query, max_mileage=100000, max_pages=3):
    try:
        # Create a session to handle cookies and maintain state
        session = requests.Session()

        # Specify the search endpoint on the IAAI website
        iaai_search_url = 'https://iaai.com/Search'

        # Set headers to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://iaai.com',  # Add the referer if necessary
            # Add other headers as needed based on the website's requirements
        }

        overall_index = 0  # Counter for the overall index across pages

        # Specify the search parameters, including the search query
        params = {
            'searchkeyword': search_query,
            # Add other parameters as needed based on the website's requirements
        }

        # Send a GET request to the IAAI website using the session, headers, and parameters
        response = session.get(iaai_search_url, params=params, headers=headers)

        # Print the final URL after the request
        print("Final URL:", response.url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find and print information related to vehicles on the current page
            vehicle_infos = soup.find_all('h4', class_='heading-7 rtl-disabled')
            mileage_elements = soup.find_all('span', class_='data-list__value rtl-disabled')  # Replace with the actual class for mileage
            location_elements = soup.find_all('span', {'class': 'data-list__value text-truncate', 'title': True})  # Replace with the actual class and title for location
            location_elements_with_branch = [location for location in location_elements if "branch" in location.get('title', '').lower()]

            for index, (vehicle_info, mileage_element, location_element) in enumerate(zip(vehicle_infos, mileage_elements, location_elements_with_branch), start=1):
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
                                trimmed_location = location_element.text.replace('Branch:', '').strip()
                                print(f"Location: Branch: {trimmed_location}")
                            
                                print(f"Mileage: {mileage_numeric} miles")
                                print(vehicle_info.text.strip())
                                print("-" * 50)
                    
                    except ValueError:
                        print(f"\nError: Unable to convert mileage to integer for Vehicle {index}. Mileage: {mileage_text}")

        else:
            print(f"\nError: Unable to search the IAAI website. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"\nError: {e}")

# Example usage
search_query = 'Intact Airbags Clear Run Drive Public'
max_mileage = 10000000  # Set the maximum mileage threshold
max_pages = 10000  # Set the maximum number of pages to search
search_iaai_website(search_query, max_mileage, max_pages)

