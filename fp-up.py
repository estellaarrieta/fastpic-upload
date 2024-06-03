import os
import re
from pprint import pprint
import requests
from lxml import html
from requests_toolbelt.multipart.encoder import MultipartEncoder

# https://new.fastpic.org/
# cookie "fp_sid"
FP_SID = ""


def get_upload_id():
    cookies = {}
    cookies["fp_sid"] = FP_SID
    r = requests.get('https://new.fastpic.org/', cookies = cookies)
    r = html.fromstring(r.content)
    script_el_text = r.xpath("//script[contains(text(), 'upload_id')]/text()")[0]
    match = re.search(r'"upload_id"\s*:\s*\'(.*?)\'', script_el_text)
    if match:
        upload_id = match.group(1)
        return upload_id.strip()

def upload_image_fastpic(file, file_name,  upload_id = '', thumb_size=350, jpeg_quality = 0, check_thumb="size", resize_to = "", thumb_text = '', is_anon = False):

    if os.path.exists(file):
        img_bytes = open(file, 'rb')
    else:
        img_bytes = file

    fields={
    'uploading': '1',
    'fp': 'not-loaded',
    'upload_id': upload_id,
    'check_thumb': str(check_thumb),
    'thumb_text': str(thumb_text),
    'thumb_size': str(thumb_size),
    'check_thumb_size_vertical': 'false',
    'check_orig_resize': 'false',
    'orig_resize': '1200',
    'check_resize_frontend': 'false',
    'check_optimization': 'false',
    'check_poster': 'false',
    'delete_after': '0',
    'file1': (file_name, img_bytes, 'image/jpeg')
}
    if resize_to:
        fields["check_orig_resize"] = 'true'
        fields["orig_resize"]= str(resize_to)
    if jpeg_quality:
        fields["jpeg_quality"] = jpeg_quality

    multipart_data = MultipartEncoder(fields)

    cookies = {}
    if not is_anon:
        cookies["fp_sid"] = FP_SID
        cookies["pp"] = '1'

    url = 'https://new.fastpic.org/v2upload/'
    response = requests.post(
        url,
        data=multipart_data,
        headers={'Content-Type': multipart_data.content_type},
        timeout=30,
        cookies = cookies
    )

    album_link = response.json()["album_link"]
    pprint(response.json())
    codes = html.fromstring(response.json()["codes"])
    pic_url_collection = {}
    pic_url_collection["album_link"] = album_link
    pic_url_collection['direct'] = codes.xpath('//li[1]//input/@value')[0]
    pic_url_collection['bb_thmub']  = codes.xpath('//li[2]//input/@value')[0]
    pic_url_collection['bb_big']  = codes.xpath('//li[3]//input/@value')[0]
    pic_url_collection['html_thumb']  = codes.xpath('//li[4]//input/@value')[0]
    pic_url_collection['md_thumb']  = codes.xpath('//li[5]//input/@value')[0]
    return pic_url_collection

if __name__ == "__main__":
    upload_id = get_upload_id()
    upload_image_fastpic("C:/Users/user/Pictures/2fe8879d5a237b3e6cc737f216c08e14.jpg", "cell.jpg", upload_id = upload_id)
    upload_image_fastpic("C:/Users/user/Pictures/2536369488_preview_ef94ff1d6f-2_1390x600.jpg", "raid.jpg", upload_id = upload_id)
