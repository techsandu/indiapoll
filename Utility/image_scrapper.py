import requests
from  bs4 import BeautifulSoup
import os, requests, lxml, re, json, urllib.request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}
params = {
    "q": "Swaraj,CPIM",  # search query
    "tbm": "isch",  # image results
    "hl": "en",  # language of the search
    "gl": "us",  # country where search comes from
    "ijn": "0"  # page number
}

html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
soup = BeautifulSoup(html.text, "lxml")
def getHighData():
    google_images = []
    all_script_tags = soup.select("script")

    # # https://regex101.com/r/48UZhY/4
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))

    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # https://regex101.com/r/pdZOnW/3
    matched_google_image_data = re.findall(r'\[\"GRID_STATE0\",null,\[\[1,\[0,\".*?\",(.*),\"All\",',
                                           matched_images_data_json)

    # https://regex101.com/r/NnRg27/1
    matched_google_images_thumbnails = ", ".join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(", ")

    thumbnails = [
        bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in
        matched_google_images_thumbnails
    ]

    # removing previously matched thumbnails for easier full resolution image matches.
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
                                                       removed_matched_google_images_thumbnails)

    full_res_images = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in
        matched_google_full_resolution_images
    ]

    for index, (metadata, thumbnail, original) in enumerate(
            zip(soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images), start=1):
        google_images.append({
            "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
            "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
            "source": metadata.select_one(".fxgdke").text,
            "thumbnail": thumbnail,
            "original": original
        })

        # Download original images
        print(f'Downloading {index} image...')

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(original, f'Bs4_Images/original_size_img_{index}.jpg')

    return google_images
def getImageData():
    print("Started")
    poli = ["M.Swaraj,CPIM","K.Babu,INC"]
    for poli_name in poli:
        print(poli_name)
        try:
            search_query = f"image of {poli_name}"
            search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"
            response = requests.get(search_url)
            if response.status_code ==200:
                soup = BeautifulSoup(response.text,'html.parser')
                img_tags = soup.findAll('img')
                if img_tags:
                    print("we done")
                    img_url = img_tags[1]['src']
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        print("we gi=ot image")
                    else:
                        print("no image data")
                else:
                    print("no images")
            print(poli_name)
        except Exception as e:
            print(f"Failed to load {poli_name}")

if __name__ == '__main__':
    print("start")
    getHighData()