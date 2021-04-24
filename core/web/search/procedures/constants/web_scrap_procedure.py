from enum import Enum, unique
from core.web.search.procedures.data_types.web_scrap_procedure import WebScrapProcedure


# Todo: Changing lambda for named functions avoids crash while using processes
# def call_torrent_file(o, a1, a2, a3, job_name):
#     return o.torrent_file(a1, a2, a3, job_name)
#
#
# def call_torrent_link(o, a1, a2, a3, job_name):
#     return o.torrent_link(a1, a2, a3, job_name)
#
#
# def call_magnet_link(o):
#     return o.magnet_link(a1, a2, a3, job_name)


@unique
class WebScrapProcedure(Enum):
    TORRENT_FILE = WebScrapProcedure(lambda o, resource_index, resource_link, raw_data:
                                     o.torrent_file(resource_index, resource_link, raw_data))
    TORRENT_LINK = WebScrapProcedure(lambda o, resource_index, resource_link, raw_data:
                                     o.torrent_link(resource_index, resource_link, raw_data))
    MAGNET_LINK = WebScrapProcedure(lambda o, resource_index, resource_link, raw_data:
                                    o.magnet_link(resource_index, resource_link, raw_data))

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif not name.startswith("_"):
            value = self.__dict__['_value_']
            return getattr(value, name)
        raise AttributeError(name)
