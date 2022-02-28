#!/usr/bin/env python3

############################################################################
# Apop idols website photo crawler
# Version: 2.0
# Created by: Peter S
# Github: peterspbr | Twitter: HSPeterSS | Discord: BountyMiyukiDX#3806
# Created on Sep 2, 2021
# Updated on Feb 19, 2022
# Github repository: https://github.com/peterspbr/apopidols-parser
###########################################################################

import requests
import os, sys

from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    soup = bs(requests.get(url).content, "html.parser")
    urls = []

    for img in tqdm(soup.find_all("a"), "[*] Extracting images"):
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
        else:
            print("[!] Invalid URL!")

    return urls

def download(url, pathname):
    # Check if output directory exsists. If not, create it
    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    response = requests.get(url, stream=True)

    file_size = int(response.headers.get("Content-Length", 0))

    filename = os.path.join(pathname, url.split("/")[-1])

    progress = tqdm(response.iter_content(1024), f"[*] Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))

def main(url, path):
    print('''
Apop idols crawler V2.0\n
Created and maintained by Peter S. Github: peterspbr
Updated on Feb 19, 2022\n
Downloading {0} images\n
    '''.format(path))

    imgs = get_all_images(url)

    for img in imgs:
        download(img, path)

def usage_banner():
    print('''Usage:
    Download by idol name:
        {0} -a <idol name>
        [!] The name must be as follows: surname_name. Example: hirokawa_nanase

    Download by group name:
        {0} -g <group_name>
        [!] The name must be as follows: idol_group. Example: luce_twinkle_wink

    Download all images:
        {0} -e folder_name

    Show this help message:
        {0} -h'''
    .format(sys.argv[0]))

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        usage_banner()
    else:
        if sys.argv[1] == "-a":
            for i in range(1, 37233):
                main("https://apopidols.org/artist/{0}/?&page={1}".format(sys.argv[2], str(i)), str(sys.argv[2]))
        elif sys.argv[1] == "-g":
            for i in range(1, 37233):
                main("https://apopidols.org/group/{0}/?&page={1}".format(sys.argv[2], str(i)), str(sys.argv[2]))
        elif sys.argv[1] == "-e":
            for i in range(1, 37233):
                main("https://apopidols.org/?&page=" + str(i), sys.argv[2])
        elif sys.argv[1] == "-h":
            usage_banner()
