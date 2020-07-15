import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):
          if "images" not in img_url:
            if "pthumb" not in img_url:
              urls.append(img_url)
    file = open("image_links.txt", "a")
    for i in urls:
        file.write(i+"\n")
    file.close()
    print("done")

for i in range(1,21):
  get_all_images("https://www.listal.com/sommer-ray/pictures/"+str(i))
