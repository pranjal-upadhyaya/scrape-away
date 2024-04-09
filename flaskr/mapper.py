from flaskr.miner import DataMiner

class Mapper(DataMiner):

    def __init__(self, url):
        self.linked_urls = {url}
        self.map = {"url": self.url}
        DataMiner.__init__(self, url)
        self.soup = self.fetch_and_parse(self.url)

    def mapper(self, soup, text_key = None, link_key = None, tag: str | None = None, attrs : dict = {}):
        new_soup = self.find_element(soup = soup, tag = tag, attrs = attrs)
        if text_key:
            text = self.extract_text(new_soup)
            self.map[text_key] = text
        if link_key:
            link = self.extract_link(new_soup)
            self.map[link_key] = link

    