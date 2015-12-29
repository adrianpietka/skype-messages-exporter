import os.path
import json

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