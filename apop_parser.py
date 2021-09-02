#!/usr/bin/python3

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

    for img in tqdm(soup.find_all("a"), "Extracting images"):
        img_url = img.attrs.get("data-title-id")

        if not img_url:
            continue
        
        img_url = urljoin(url, "/static/img/" + img_url + ".jpg")

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass

        if is_valid(img_url):
            urls.append(img_url)

    return urls


def download(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    response = requests.get(url, stream=True)

    file_size = int(response.headers.get("Content-Length", 0))

    filename = os.path.join(pathname, url.split("/")[-1])

    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))


def main(url, path):
    imgs = get_all_images(url)

    for img in imgs:
        download(img, path)
    
if __name__ == "__main__":
    for i in range(1, 37233):
        main("https://apopidols.org/posts/?&page=" + str(i), 'idol')
