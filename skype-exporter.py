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
    def __init__(self, file_path):
        self.config_file = file_path
        self.load()

    def load(self):
        if (not os.path.isfile(self.config_file)):
            raise Exception("> Can't load config file: {}".format(self.config_file))
        
        data = json.load(open(self.config_file, "r"))
        self.channels = data["channels"]
        self.api_url = data["api_url"]
        self.messages_limit = int(data["messages_limit"])
        self.cycle_time = int(data["cycle_time"])
        self.skype_database_original = data["skype_database_original"]

    def save(self):
        json.dump({
            "channels": self.channels,
            "api_url": self.api_url,
            "messages_limit": self.messages_limit,
            "cycle_time": self.cycle_time,
            "skype_database_original": self.skype_database_original
            }, open(self.config_file, "w"))

    def set_last_message_for_channel(self, messages):
        for message in messages:
            self.channels[str(message["conversation"]["id"])] = message["id"]

        self.save()

class Message_Exporter:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def export_as_json(self, messages):
        payload = json.dumps(messages)
        headers = {"content-type": "application/json"}
        return requests.post(self.api_url, data = payload, headers = headers)

class Skype_Database:
    def __init__(self, original, temp):
        self.skype_database_original = original
        self.skype_database_temp = temp
        
    def refresh(self):
        try:
            shutil.copyfile(self.skype_database_original, self.skype_database_temp)
            return True
        except:
            return False

    def get_new_messages(self, channels, messages_limit):
        messages = []

        channels_query = ""
        channels_id = list(channels.keys())
        for channel_id in channels_id:
            channels_query += " OR (m.convo_id = " + str(channel_id) +  " AND m.id > " + str(channels[channel_id]) + ")";
        
        connection = sqlite3.connect(self.skype_database_temp)
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

            if (skype_database.refresh()):
                channels = settings.channels
                messages = skype_database.get_new_messages(channels, settings.messages_limit)
                try:
                    message_exporter.export_as_json(messages)
                    print(">> exported {} messages".format(len(messages)))
                    settings.set_last_message_for_channel(messages)
                except Exception as e:
                    print(">> can't export messages: {}".format(str(e)))
            else:
                print(">> can't create copy of skype database from: {}".format(settings.skype_database_original))

            time.sleep(settings.cycle_time)
            print("")

def signal_handler(signal, frame):
    print("\n> bye ;-(")
    sys.exit(0)

try:
    parser = argparse.ArgumentParser(description="Export messages from Skype channels to a remote web service.")
    parser.add_argument("config_file", help="json config file")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)

    settings = Settings(args.config_file)
    skype_database = Skype_Database(settings.skype_database_original, "skype.db")
    message_exporter = Message_Exporter(settings.api_url)
    listener = Listener()

    listener.listen(settings, skype_database, message_exporter)
except Exception as e:
    print(str(e))