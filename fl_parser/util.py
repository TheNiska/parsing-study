from requests import get


def get_html(url):
    with open('headers.txt', 'r', encoding='utf-8') as file:
        user_agent = file.readline()[:-1]
    headers = {'User-Agent': user_agent}

    html = get(url=url, headers=headers).text
    return html
