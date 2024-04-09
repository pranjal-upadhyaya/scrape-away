from flaskr.spider import Spider
from bs4 import BeautifulSoup
import re
import tldextract as tld

class DataMiner(Spider):

    def __init__(self, url):
        Spider.__init__(self, url)

    def fetch_and_parse(self, params: dict | None = None, data: dict | None = None, browsers: list | str = [], os : str | list = [], platform: str | list = [], response_language: str = 'en-US,en;q=0.5', timeout: int = 10):
        response_obj = self.send_request(params=params, data=data, browsers=browsers, os=os, platform=platform, response_language=response_language, timeout=timeout)
        if response_obj.get("content_type") == "text/html" and response_obj.get("response_data"):
            soup = BeautifulSoup(response_obj["response_data"], "lxml")
            return soup
        else:
            return None
    
    def pretify_soup(Self, soup: BeautifulSoup):

        return soup.prettify()
        
    def fetch_all_links(self, depth: int = 10, params: dict | None = None, data: dict | None = None, browsers: list | str = [], os : str | list = [], platform: str | list = [], response_language: str = 'en-US,en;q=0.5', timeout: int = 10):
        print(self.url)
        linked_urls = set()
        soup = self.fetch_and_parse(params=params, data=data, browsers=browsers, os=os, platform=platform, response_language=response_language, timeout=timeout)
        # self.linked_urls.add(self.url)
        linked_urls.add(self.url)
        if soup and depth > 0:
            links = soup.find_all('a')
            countdown = 5
            for link in links:
                if link["href"] not in self.linked_urls:
                    new_url = link["href"]
                    sanitized_url = tld.extract(new_url)
                    if sanitized_url.subdomain == sanitized_url.suffix == "":
                        continue
                    else:
                        countdown -= 1
                        # self.linked_urls.add(new_url)
                        linked_urls.add(new_url)
                        url_obj = DataMiner(new_url)
                        url_obj.fetch_all_linked_data(depth = depth -1, params=params, data=data, browsers=browsers, os=os, platform=platform, response_language=response_language, timeout=timeout)
                if countdown <= 0:
                    break
        return list(linked_urls)
        
    # def fetch_all_linked_data(self, seen: set = set(), data_obj: list = [], depth: int = 10, params: dict | None = None, data: dict | None = None, browsers: list | str = [], os : str | list = [], platform: str | list = [], response_language: str = 'en-US,en;q=0.5', timeout: int = 10):
        
    #     print(self.url)
    #     soup = self.fetch_and_parse(params=params, data=data, browsers=browsers, os=os, platform=platform, response_language=response_language, timeout=timeout)
    #     self.extract_text(soup)
    #     data_obj.append(self.response_obj)
    #     seen.add(self.url)
    #     if soup and depth > 0:
    #         links = soup.find_all('a')
    #         countdown = 5
    #         for link in links:
    #             if link["href"] not in seen:
    #                 new_url = link["href"]
    #                 sanitized_url = tld.extract(new_url)
    #                 if sanitized_url.subdomain == sanitized_url.suffix == "":
    #                     continue
    #                 else:
    #                     countdown -= 1
    #                     seen.add(new_url)
    #                     url_obj = DataMiner(new_url)
    #                     data_obj = url_obj.fetch_all_linked_data(seen=seen, data_obj=data_obj, depth = depth -1, params=params, data=data, browsers=browsers, os=os, platform=platform, response_language=response_language, timeout=timeout)
    #             if countdown <= 0:
    #                 break
    #     return data_obj
    
    @staticmethod
    def find_elements(soup: BeautifulSoup, tag, attrs : dict = {}, limit : int | None = None):
        elements = soup.find_all(name = tag, attrs=attrs, limit=limit)
        return elements
    
    @staticmethod
    def find_element(soup: BeautifulSoup, tag: str | None = None, attrs : dict = {}):
        element = soup.find(name = tag, attrs=attrs)
        return element
    
    @staticmethod
    def extract_text(element: BeautifulSoup):
        try:
            string = element.string
        except Exception as e:
            print(e)
            string = None
        return string
    
    @staticmethod
    def extract_link(element: BeautifulSoup):
        return element.get("href")

    def extract_raw_text(self, soup):
        # Extract text from paragraphs and headings
        if soup:
            paragraphs = soup.find_all('p')
            headings = soup.find_all(re.compile(r'^h[1-6]$'))
            text = ' '.join([tag.get_text() for tag in paragraphs + headings])
            text = " ".join(text.split())
            # self.response_obj["extracted_text"] = text
            return text
        else:
            # self.response_obj["extracted_text"] = None
            return None

    # def write_raw_to_csv(self):
    #     field_names = list(self.response_obj.keys())
    #     with open("scraped_data.csv", "w", encoding="utf-8", newline="") as csvfile:
    #         csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)
    #         csv_writer.writeheader()
    #         csv_writer.writerow(self.response_obj)
    #         csvfile.close()

    # def bulk_write_to_csv(self, depth: int = 10, params: dict | None = None, data: dict | None = None, browsers: list | str = [], os : str | list = [], platform: str | list = [], response_language: str = 'en-US,en;q=0.5', timeout: int = 10):
    #     data_obj = self.fetch_all_linked_data(data_obj=[], depth = depth -1, params=params, data=data, browsers=browsers, os=os, platform=platform, response_language=response_language, timeout=timeout)
    #     print("Acquired Data Object")
    #     field_names = list(self.response_obj.keys())
    #     with open("scraped_data.csv", "w", encoding="utf-8", newline="") as csvfile:
    #         csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)
    #         csv_writer.writeheader()
    #         csv_writer.writerows(data_obj)
    #         csvfile.close()