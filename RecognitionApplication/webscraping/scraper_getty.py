import hashlib, io, requests, pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image


options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get("https://www.gettyimages.com/search/2/image?phrase=celebrity+photo+archive")
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")
driver.quit()

def gets_url(classes, location, source):
    results = []
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))
    return results

if __name__ == "__main__":
    returned_results = gets_url("fm5xLZr6E1NLQUhYh_xd", "img", "src")
    for b in returned_results:
        image_content = requests.get(b).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
        file_path = Path(r"D:\Internships_work\Library internship\Repos\presentation repo\RecognitionApplication\uploaded_images", hashlib.sha1(image_content).hexdigest()[:10] + ".png")
        image.save(file_path, "PNG", quality=80)