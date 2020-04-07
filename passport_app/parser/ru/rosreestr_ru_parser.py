import requests
from bs4 import BeautifulSoup
from passport_app.parser.captcha_solver import solve_captcha


def rosreestr_ru_parser(cn):
    result = {}
    page = requests.get("https://rosreestr.ru/wps/portal/online_request")
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        href = soup.find("base")['href']
        img_src = href+soup.find("img", {"id": "captchaImage2"})['src']
        print (img_src)
        # solve_captcha(img_src)
        # result['p_text'] = p_text

    # print(result)
    return result

