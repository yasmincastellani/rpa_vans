from bs4 import BeautifulSoup
import requests


class CatalogoVans:
    def __init__(self):
        self.__url_knu_skool_black = "https://www.vans.com.br/tenis-knu-skool-black-true-white/p/1002002760001U"
        self.__url_base_1 = "https://www.vans.com.br/_next/data/"
        self.__url_base_2 = "/tenis-knu-skool-black-true-white/p/1002002760001U.json?n1=tenis-knu-skool-black-true-white&sku=1002002760001U"

        self.__target_number_1 = "37"
        self.__target_number_2 = "38"

    def scrape(self) -> list[dict]:
        url_token = self.__search_id()
        tamanhos = self.__separate_sizes(
        self.__concat_urls(url_token))
        return self.__filter_sizes(tamanhos)

    def __search_id(self) -> str:
        response = requests.get(self.__url_knu_skool_black)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        paragraphs = soup.find_all("script")
        for p in paragraphs:
            if p.get("src") != None:
                if "_buildManifest.js" in p["src"]:
                    url_token_complete = p["src"]
                    url_token_complete_str = str(url_token_complete)
                    url_token_parts = url_token_complete_str.split("/")
                    url_token_dirt = url_token_parts[-2]
                    url_token = url_token_dirt.replace(" ", " ")
                    return url_token

    def __concat_urls(self, url_token: str) -> str:
        return self.__url_base_1 + url_token + self.__url_base_2

    def __separate_sizes(self, url: str) -> dict:
        response_status = requests.get(url)
        response_dict = response_status.json()

        dict_pageprops = response_dict["pageProps"]
        dict_products = dict_pageprops["product"]
        variants_options = dict_products["variantOptions"]
        return variants_options

    def __filter_sizes(self, variants_options: dict) -> list[dict]:
        list_shoes = []
        for obj in variants_options:
            shoes_size = obj["displayText"]
            if shoes_size == self.__target_number_1 or shoes_size == self.__target_number_2:
                shoes_available = obj["sellable"]
                info_shoes = {"size": shoes_size,
                              "disponível": shoes_available}
                list_shoes.append(info_shoes)
        return list_shoes


def output(data: list[dict]):
    for v in data:
        print(v)


if __name__ == "__main__":
    vans_catalog = CatalogoVans().scrape()
    output(vans_catalog)


