import argparse
from se import *

if __name__ != "__main__":
    raise Exception("Can't execute script as a module")

try:
    parser = argparse.ArgumentParser(description="Display list of Skype channels.")
    parser.add_argument("config_file", help="json config file")
    parser.add_argument('-l', '--limit', type=int, default=25, help='display last X channels')
    args = parser.parse_args()
    
    settings = Settings(args.config_file)
    skype_database = Skype_Database(settings.skype_database_original, "temp/skype.db")

    display_channels = Display_Channels()
    display_channels.execute(skype_database, args.limit)
except Exception as e:
    print(str(e))