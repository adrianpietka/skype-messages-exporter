import time

class Export_Messages:
    def execute(self, settings, skype_database, api):
        while(True):            
            print("> listen at {}".format(time.strftime("%H:%M:%S")))

            if (skype_database.refresh()):
                channels = settings.channels
                messages = skype_database.get_new_messages(channels, settings.messages_limit)
                try:
                    api.save_messages(messages)
                    print(">> exported {} messages".format(len(messages)))
                    settings.set_last_message_for_channel(messages)
                except Exception as e:
                    print(">> can't export messages: {}".format(str(e)))
            else:
                print(">> can't create copy of skype database from: {}".format(settings.skype_database_original))

            time.sleep(settings.cycle_time)
            print("")