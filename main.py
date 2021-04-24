# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from core.web.search.data_struct.websearch_instance import WebSearchInstance
from core.constants.fileflags import FileFlags
from core.net.network_agent import NetworkAgent
from core.tracker_scraper import TrackerScraper

if __name__ == '__main__':
    network_agent = NetworkAgent()
    if network_agent.network_status():
        # Move Size Limit to Other Place, not Withing the Search, or apply other
        # filters based on the current place we are searching.
        web_search_instance = WebSearchInstance(
            title='Mortal Kombat',
            year='2021', quality='1080p',
            search_type=FileFlags.FILM_DIRECTORY_FLAG,
            upper_size_limit='4000', lower_size_limit='1000')

        tracker_scraper = TrackerScraper()
        magnet_dataframe = tracker_scraper.scrap(web_search_instance)
        print(magnet_dataframe)

    # scraper_engine = ScraperEngine()
    # # torrent_funk = TorrentFunkScraper(scraper_engine.logger)
    # kat_scraper = GranTorrentScraper(scraper_engine.logger)
    # with open('./test/static/GranTorrent.html', encoding='utf-8') as file:
    #     kat_scraper.get_raw_data(file)
    #
    # with open('./test/static/GranTorrentTorrent.html', encoding='utf-8') as file:
    #     kat_scraper.get_magnet_link(file)
