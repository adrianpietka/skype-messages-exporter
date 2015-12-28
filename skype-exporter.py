import json
import sys
import time
import signal
import requests
import shutil
import sqlite3

settings_file = "config.json"

api_url = "http://localhost:5757"

skype_database_original = "C:\\Users\\Adrian\\AppData\\Roaming\\Skype\\pietka.adrian\\main.db"
skype_database_temp = "skype.db"

cycle_time = 5
messages_limit = 30

class Settings:
    settings_file = ""

    channels = []

    def __init__(self, file_path):
        self.settings_file = file_path
        self.load()

    def load(self):
        data = json.load(open(self.settings_file, "r"))
        self.channels = data["channels"]

    def save(self):
        json.dump({"channels": self.getChannels()}, open(self.settings_file, "w"))

    def getChannels(self):
        return self.channels

    def setUpdateLastMessageIdForChannel(self, messages):
        for message in messages:
            self.channels[str(message["ConversationId"])] = message["Id"]

        self.save()

class MessageExporter:
    success_status = 200

    def exportAsJson(self, messages):
        try:
            payload = json.dumps(messages)
            headers = {"content-type": "application/json"}
            response = requests.post(api_url, data = payload, headers = headers)
            return response.status_code == self.success_status
        except:
            return False

class SkypeDatabase:
    def refresh(self):
        try:
            shutil.copyfile(skype_database_original, skype_database_temp)
            return True
        except:
            return False

    def getNewMessages(self, channels):
        messages = []

        channelsQuery = ""
        channelsId = list(channels.keys())
        for channelId in channelsId:
            channelsQuery = channelsQuery + "OR (m.convo_id = " + str(channelId) +  " AND m.id > " + str(channels[channelId]) + ")";
        
        connection = sqlite3.connect(skype_database_temp)
        result = connection.cursor()
        result.execute(
            "SELECT m.id, m.author, m.timestamp, m.body_xml, m.convo_id, c.displayname as convo_name "
            "FROM Messages m JOIN Conversations c ON (c.id = m.convo_id) "
            "WHERE 1 != 1 {}"
            "ORDER BY m.id ASC "
            "LIMIT {}".format(channelsQuery, messages_limit)
        )

        for row in result.fetchall():
            messages.append({
                "Id": row[0],
                "Author": row[1],
                "Date": row[2],
                "Content": row[3] if row[3] else "",
                "ConversationId": row[4],
                "ConversationName": row[5]})

        connection.close()

        return messages

class Listener:
    def listen(self, settings, skypeDatabase, messageExporter):
        while(True):            
            print("> listen at {}".format(time.strftime("%H:%M:%S")))

            if (not skypeDatabase.refresh()):
                print(">> can't create copy of skype database")
                continue

            channels = settings.getChannels()
            messages = skypeDatabase.getNewMessages(channels)
            
            if (messageExporter.exportAsJson(messages)):
                print(">> exported {} messages".format(len(messages)))
                settings.setUpdateLastMessageIdForChannel(messages)
            else:
                print(">> can't export messages")

            time.sleep(cycle_time)
            print("")

def signal_handler(signal, frame):
    print("\n> bye ;-(")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    settings = Settings(settings_file)
    skypeDatabase = SkypeDatabase()
    messageExporter = MessageExporter()
    listener = Listener()

    listener.listen(settings, skypeDatabase, messageExporter)