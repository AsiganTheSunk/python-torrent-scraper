from configparser import ConfigParser

class CustomConfigParser():
    def __init__(self, ini_file='./scraperengine.ini'):
        self.ini_file = ini_file
        self.config_parser = ConfigParser()
        self.config_parser.read(self.ini_file)

    def get_section_map(self, section):
        dict1 = {}
        options = self.config_parser.options(section)
        for option in options:
            try:
                dict1[option] = self.config_parser.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None

        return dict1

    # print(self.get_section_map('WebScrapers'))

    def set_section_key(self, section, key, value):
        self.config_parser.set(section, key, value)
        try:
            # Writing the configuration file
            with open(self.ini_file, 'w+') as configfile:
                self.config_parser.write(configfile)
        except Exception as err:
            print(err)



