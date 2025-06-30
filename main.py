from bs4 import BeautifulSoup
import requests


class CatalogoVans:
    def __init__(self):
        self.__url_knu_skool_black = "https://www.vans.com.br/tenis-knu-skool-black-true-white/p/1002002760001U"
        self.__url_base_concat = "https://www.vans.com.br/_next/data/"
        self.__url_base_knu_black_concat = "/tenis-knu-skool-black-true-white/p/1002002760001U.json?n1=tenis-knu-skool-black-true-white&sku=1002002760001U"
        self.__url_knu_skool_rhododendron_concat = "/tenis-knu-skool-rhododendron/p/1002002760039U.json?n1=tenis-knu-skool-rhododendron&sku=1002002760039U"
        self.__url_knu_skool_gray_concat = "/tenis-knu-skool-suede-gray/p/1002002760035U.json?n1=tenis-knu-skool-suede-gray&sku=1002002760035U"

        self.__target_number_1 = "37"
        self.__target_number_2 = "38"

    def scrape(self) -> list[dict]:
        url_token = self.__search_id()
        tamanhos = self.__separate_sizes(
            self.__concat_urls_shoes(url_token))
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

    def __concat_urls_shoes(self, url_token: str) -> str:
        url_black = self.__url_base_concat + url_token + self.__url_base_knu_black_concat
        url_rhododendron = self.__url_base_concat + \
            url_token + self.__url_knu_skool_rhododendron_concat
        url_gray = self.__url_base_concat + url_token + self.__url_knu_skool_gray_concat
        urls_shoes = [url_black, url_rhododendron, url_gray]

        return urls_shoes

    def __separate_sizes(self, urls: list) -> dict:
        variants_by_url = {}

        for url in urls:
            response = requests.get(url)
            response.raise_for_status()  # Lança erro se o status não for 200
            response_dict = response.json()
            variants = response_dict["pageProps"]["product"]["variantOptions"]
            variants_by_url[url] = variants
            response_status = requests.get(url)
            response_dict = response_status.json()

        return variants_by_url

    def __filter_sizes(self, variants_by_url: dict) -> list[dict]:
        list_shoes = []

        variants_black = list(variants_by_url.values())[0]
        variants_rhododendron = list(variants_by_url.values())[1]
        variants_gray = list(variants_by_url.values())[2]

        all_variants = variants_black + variants_rhododendron + variants_gray
        colors = ["black", "rhododendron", "gray"]
        variant_lists = list(variants_by_url.values())

        for color, variant_list in zip(colors, variant_lists):
            for obj in variant_list:
                shoes_size = obj["displayText"]
                if shoes_size == self.__target_number_1 or shoes_size == self.__target_number_2:
                    shoes_available = obj["sellable"]
                    info_shoes = {
                        "size": shoes_size,
                        "color": color,
                        "disponível": shoes_available
                }
                    
                    list_shoes.append(info_shoes)

        return list_shoes

def output(data: list[dict]):
    for v in data:
        print(v)

if __name__ == "__main__":
    vans_catalog = CatalogoVans().scrape()
    output(vans_catalog)
