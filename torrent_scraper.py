from torrentscraper.scraper_engine import ScraperEngine

class TorrentScraper():
    def __init__(self):
        self.scraper_engine = ScraperEngine()

    def scrap(self, websearch, top=15):
        try:
            p2p_instance_list = self.scraper_engine.search(websearch)
            dataframe = self.scraper_engine.create_magnet_dataframe(p2p_instance_list)
            dataframe = self.scraper_engine.unique_magnet_dataframe(dataframe)
            dataframe = self.scraper_engine.get_dataframe(dataframe, top)
            return dataframe
        except:
            pass