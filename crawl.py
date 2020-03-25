import os
from bs4 import BeautifulSoup
import requests


URL = "https://losslessplus.com/visit.php?job=viewresult&sid=5a9c9c50497cfdf68758b4e868955d2d"

resp = requests.get(URL)

soup = BeautifulSoup(resp.text, "html.parser")

for a in reversed(soup.find_all("a", class_="linkbai")):
    tenbai = a.text
    linkbai = requests.get(a.get("href"))
    linkbai_soup = BeautifulSoup(linkbai.text, "html.parser")
    download_link_0 = linkbai_soup.find(id="zoomtext").find(
        "div", class_="quote-content-2").a.get("href")
    download_link_1 = requests.get(
        download_link_0.replace("url.php", "url2.php"))
    download_link_1_soup = BeautifulSoup(download_link_1.text, "html.parser")
    content = download_link_1_soup.find(
        "meta", {"http-equiv": "refresh"}).get("content")
    local_file_name = tenbai + ".flac"
    drive_link = content.split("url=")[-1]
    print(drive_link)
    if not os.path.exists("download/" + local_file_name):
        with requests.get(drive_link, stream=True) as r:
            try:
                r.raise_for_status()
                with open("download/" + local_file_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            except Exception as e:
                print(e)
                print(tenbai)
                pass
