import requests
import json


def main():
    query = "python"
    url = f"https://api.hh.ru/vacancies?text={query}&area=26"
    response = requests.get(url=url)
    vacancies = json.loads(response.text)
    for item in vacancies["items"]:
        name = item["name"]
        descr = item["snippet"]["requirement"]
        if descr:
            descr = (descr.replace("<highlighttext>", "")
                          .replace("</highlighttext>", ""))
        print(f"{name:-^80}")
        print(descr)
        print(item["url"])
        print(item["alternate_url"])
        print()


if __name__ == "__main__":
    main()
