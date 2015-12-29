import shutil
import sqlite3

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
        
    def get_channels(self, limit):
        channels = []
 
        connection = sqlite3.connect(self.skype_database_temp)
        result = connection.cursor()
        result.execute(
            "SELECT id, displayname, last_activity_timestamp "
            "FROM Conversations "
            "WHERE last_activity_timestamp IS NOT NULL "
            "ORDER BY last_activity_timestamp DESC "
            "LIMIT {}".format(limit)
        )

        for row in result.fetchall():
            channels.append({
                "id": row[0],
                "display_name": format(row[1]),
                "last_activity": row[2]
            })

        connection.close()

        return channels