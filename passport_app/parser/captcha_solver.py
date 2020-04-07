# import cv2 as cv
# import pytesseract
# import requests
# from PIL import Image
# from io import StringIO
# # from io import BytesIO
# import urllib3

def solve_captcha(url):
    # conn = urllib3.connection_from_url(url)
    # resp = conn.request('GET', url)
    result = None
    # file_destination = "./temp_capttcha.png"
    # resp = requests.get(url)
    # if resp.status_code == 200:
    #     with open(file_destination, 'wb') as f: # Make sure to use wb are we are writing bytes
    #         f.write(resp.content)
    #     gray = cv.imread(file_destination)
    #     result = pytesseract.image_to_string(Image.fromarray(gray) )
    #
    # print("result = "+result)
    return result
