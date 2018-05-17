from torrentscraper.scraper_engine import ScraperEngine


class TorrentScraper():
    def __init__(self, webscraper_dict=None):
        self.name = self.__class__.__name__
        self.scraper_engine = ScraperEngine(webscraper_dict)

    def scrap(self, websearch, top=15):
        p2p_instance_list = []
        try:
            p2p_instance_list = self.scraper_engine.search(websearch)
        except Exception as err:
            print(self.name, err)
        dataframe = self.scraper_engine.create_magnet_dataframe(p2p_instance_list)
        dataframe = self.scraper_engine.unique_magnet_dataframe(dataframe)
        dataframe = self.scraper_engine.get_dataframe(dataframe, top)
        return dataframe