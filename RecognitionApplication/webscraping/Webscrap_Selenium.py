from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import os
import time
import re


path = 'D:\\ChromeDriver\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'

# Initialize the Chrome WebDriver using the Service object
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

# Navigate to the website
website = 'https://digitalcollections.aucegypt.edu/digital/collection/p15795coll20/search'
driver.get(website)

# Optional: Wait for the page to load
time.sleep(3)


# Find all book links on the page
book_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/digital/collection/p15795coll20/id/')]")
book_urls = [link.get_attribute('href') for link in book_links]

# Remove duplicates
book_urls = list(set(book_urls))


# Custom sorting function to extract the 'rec' number from the URL
def get_rec_number(url):
    match = re.search(r'/rec/(\d+)', url)
    if match:
        return int(match.group(1))
    return 0  # Return 0 if no match is found, just in case

# Sort the URLs based on the 'rec' number
sorted_book_urls = sorted(book_urls, key=get_rec_number)

# Now `sorted_book_urls` will have the URLs sorted by the 'rec' number in ascending order


# Function to download images
def download_image(url, image_name, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Extract the file extension
    ext = url.split('.')[-1].split('?')[0]
    new_image_name = f"{image_name}.{ext}"
    image_path = os.path.join(folder, new_image_name)

    # Check if the image already exists and modify the name if necessary
    counter = 1
    while os.path.exists(image_path):
        new_image_name = f"{image_name}{counter}.{ext}"
        image_path = os.path.join(folder, new_image_name)
        counter += 1
        
    response = requests.get(url)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {new_image_name}")



# Loop through each book URL and find images
for url in sorted_book_urls:
    driver.get(url)
    # Wait for the page to load fully
    time.sleep(4)

    #Get Book name
    try:
        Book_name = driver.find_element(By.XPATH, "//h1[contains(@class, 'ItemTitle-primaryTitle')]").text
    except:
        print("h1 element not found. No Book Name found")
        Book_name = "Unknown_Book_Name"
        
    # Collect all image URLs on the book page
    while True:
        #Get Page name
        try:
            page_name = driver.find_element(By.XPATH, "//h2[contains(@class, 'ItemTitle-secondaryTitle')]").text
        except:
            print("h2 element not found. No Page Name found")
            page_name = "Unknown_Page_Name"
        
        image_elements = driver.find_elements(By.XPATH, "//img[not(contains(@src, 'thumbnail')) and contains(@src, 'p15795coll20')]")
        image_urls = [img.get_attribute('src') for img in image_elements]
        
        # Download each image
        for image_url in image_urls:
            image_name = f"{Book_name}_{page_name}"
            download_image(image_url, image_name, 'downloaded_images')
        
        # Try to find the "Next" button to navigate to the next page, if available
        try:
            next_button = driver.find_element(By.XPATH, "//button[@title='Next']")
            # Check if the button is disabled
            if next_button and next_button.get_attribute('disabled') is None:
                next_button.click()
                time.sleep(1)  # Wait for the next page to load
            else:
                break  # No more pages
        except:
            break  # No "Next" button found, exit the loop

# Close the driver
driver.quit()