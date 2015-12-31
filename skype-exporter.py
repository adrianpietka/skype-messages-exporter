import sys
import signal
import argparse
from se import *

if __name__ != "__main__":
    raise Exception("Can't execute script as a module")

def signal_handler(signal, frame):
    print("\n> bye ;-(")
    sys.exit(0)

try:
    parser = argparse.ArgumentParser(description="Export messages from Skype channels to a remote web service.")
    parser.add_argument("config_file", help="json config file")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    settings = Settings(args.config_file)
    skype_database = Skype_Database(settings.skype_database_original, "temp/skype.db")
    api = Api(settings.api_url)
    
    export_messages = Export_Messages()
    export_messages.execute(settings, skype_database, api)
except Exception as e:
    print(str(e))