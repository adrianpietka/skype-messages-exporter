import json
import sys
import time
import signal
import requests
import shutil
import sqlite3
import argparse
import os.path

if __name__ != "__main__":
    raise Exception("Can't execute script as a module")

class Settings:
    config_file = ""

    channels = []

    def __init__(self, file_path):
        self.config_file = file_path
        self.load()

    def load(self):
        data = json.load(open(self.config_file, "r"))
        self.channels = data["channels"]

    def save(self):
        json.dump({"channels": self.get_channels()}, open(self.config_file, "w"))

    def get_channels(self):
        return self.channels

    def set_last_message_for_channel(self, messages):
        for message in messages:
            self.channels[str(message["conversation"]["id"])] = message["id"]

        self.save()

class Message_Exporter:
    success_status = 200

    def export_as_json(self, messages):
        try:
            payload = json.dumps(messages)
            headers = {"content-type": "application/json"}
            response = requests.post(api_url, data = payload, headers = headers)
            return response.status_code == self.success_status
        except:
            return False

class Skype_Database:
    def refresh(self):
        try:
            shutil.copyfile(skype_database_original, skype_database_temp)
            return True
        except:
            return False

    def get_new_messages(self, channels):
        messages = []

        channels_query = ""
        channels_id = list(channels.keys())
        for channel_id in channels_id:
            channels_query += " OR (m.convo_id = " + str(channel_id) +  " AND m.id > " + str(channels[channel_id]) + ")";
        
        connection = sqlite3.connect(skype_database_temp)
        result = connection.cursor()
        result.execute(
            "SELECT m.id, m.author, m.timestamp, m.body_xml, m.convo_id, c.displayname as convo_name "
            "FROM Messages m JOIN Conversations c ON (c.id = m.convo_id) "
            "WHERE 1 != 1 {}"
            "ORDER BY m.id ASC "
            "LIMIT {}".format(channels_query, messages_limit)
        )

        for row in result.fetchall():
            messages.append({
                "id": row[0],
                "author": row[1],
                "date": row[2],
                "content": row[3] if row[3] else "",
                "conversation": {"id": row[4], "name": row[5]}
                })

        connection.close()

        return messages

class Listener:
    def listen(self, settings, skype_database, message_exporter):
        while(True):            
            print("> listen at {}".format(time.strftime("%H:%M:%S")))

            if (not skype_database.refresh()):
                print(">> can't create copy of skype database")
                continue

            channels = settings.get_channels()
            messages = skype_database.get_new_messages(channels)
            
            if (message_exporter.export_as_json(messages)):
                print(">> exported {} messages".format(len(messages)))
                settings.set_last_message_for_channel(messages)
            else:
                print(">> can't export messages")

            time.sleep(cycle_time)
            print("")

def signal_handler(signal, frame):
    print("\n> bye ;-(")
    sys.exit(0)

try:
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Export messages from Skype channels to a remote web service.")
    parser.add_argument("config_file", help="json config file")
    args = parser.parse_args()

    if (not os.path.isfile(args.config_file)):
        raise Exception("> Can't load config file: {}".format(args.config_file))

    cycle_time = 5
    messages_limit = 30
    api_url = "http://localhost:5757"
    skype_database_temp = "skype.db"
    skype_database_original = "C:\\Users\\Adrian\\AppData\\Roaming\\Skype\\pietka.adrian\\main.db"

    settings = Settings(args.config_file)
    skype_database = Skype_Database()
    message_exporter = Message_Exporter()
    listener = Listener()

    listener.listen(settings, skype_database, message_exporter)
except Exception as e:
    print(str(e))