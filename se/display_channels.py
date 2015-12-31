class Display_Channels:
    def execute(self, skype_database, limit):
        skype_database.refresh()
        channels = skype_database.get_channels(limit)
    
        print("{:^10}|{:^15}| {}".format("id", "last activity", "name"))
        print("{:-<10}+{:-<15}+{:-<40}".format("-", "-", "-"))

        for channel in channels:
            print("{id:^10}|{last_activity:^15}| {display_name:.40}".format(**channel))