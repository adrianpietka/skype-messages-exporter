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

    skype_database.refresh()
    channels = skype_database.get_channels(args.limit)
    
    print("{:^10}|{:^15}| {}".format("id", "last activity", "name"))
    print("{:-<10}+{:-<15}+{:-<40}".format("-", "-", "-"))

    for channel in channels:
        print("{id:^10}|{last_activity:^15}| {display_name:.40}".format(**channel))

except Exception as e:
    print(str(e))