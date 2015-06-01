using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Configuration;
using System.Data.SQLite;

namespace SkypeMessagesExporter
{
    // ta klasa do totalnej refaktoryzacji -> SkypeDatabaseConnector
    // wydzielic pobieranie danych do -> SkypeDatabaseRepository(SkypeDatabaseConnector)
    public class SkypeDatabase
    {
        string skypeDatabaseFile = ConfigurationManager.AppSettings["SkypeDatabaseFile"];
        string skypeDatabaseConnection = ConfigurationManager.AppSettings["SkypeDatabaseConnection"];
        string tempDatabaseFile = ConfigurationManager.AppSettings["TempDatabaseFile"];

        SQLiteConnection dbConnection;

        private SQLiteConnection GetConnectionToDatabase()
        {
            return dbConnection;
        }

        private string PrepareQueryForGettingNewMessages(ChannelList channelList)
        {
            string channelsConditions = "";

            channelList.GetAll().ForEach(delegate(Channel channel)
            {
                channelsConditions += " OR (m.convo_id = " + channel.Id + " AND m.id > " + channel.LastMessageId + ")";
            });

            // limit wrzucic do konfiga
            return "SELECT m.id, m.convo_id, c.displayname as convo_name, m.author, m.timestamp, m.body_xml "
                 + "FROM Messages m JOIN Conversations c ON (c.id = m.convo_id) WHERE 1 != 1"
                 + channelsConditions + " ORDER BY m.id ASC LIMIT 30";
        }

        public SkypeDatabase()
        {
            try
            {
                dbConnection = new SQLiteConnection(skypeDatabaseConnection);
                dbConnection.Open();
            }
            catch (Exception exception)
            {
                Console.WriteLine(exception.Message);
            }
        }

        public void RefreshDatabase()
        {
            if (File.Exists(skypeDatabaseFile))
            {
                File.Copy(skypeDatabaseFile, tempDatabaseFile, true);
            }
            else
            {
                throw new Exception("[SkypeDatabase] Database with messages from Skype does not exists");
            }
        }

        public List<Message> GetNewMessages(ChannelList channelList)
        {
            List<Message> messages = new List<Message>();
            // polaczenie powinno byc nawiazane wczesniej,
            // teraz uzywac GetConnection() -> if (!connection) Connect() else dbConnection
            SQLiteCommand command = new SQLiteCommand(PrepareQueryForGettingNewMessages(channelList), GetConnectionToDatabase());
            SQLiteDataReader result = command.ExecuteReader();

            while (result.Read())
            {
                Console.WriteLine("- #" + Convert.ToInt32(result["id"].ToString()));

                Message message = new Message(
                    Convert.ToInt32(result["id"].ToString()),
                    Convert.ToInt32(result["convo_id"].ToString()),
                    Convert.ToString(result["convo_name"].ToString()),
                    Convert.ToString(result["author"].ToString()),
                    Convert.ToString(result["timestamp"].ToString()),
                    Convert.ToString(result["body_xml"].ToString())
                );

                messages.Add(message);
            }

            return messages;
        }

        public List<Channel> GetChannels()
        {
            string queryToGetChannels = "SELECT id, displayname FROM Conversations ORDER BY displayname";
            List<Channel> channels = new List<Channel>();
            SQLiteCommand command = new SQLiteCommand(queryToGetChannels, GetConnectionToDatabase());
            SQLiteDataReader result = command.ExecuteReader();

            while (result.Read())
            {
                Channel channel = new Channel(
                    Convert.ToInt32(result["id"].ToString()),
                    Convert.ToString(result["displayname"].ToString())
                );

                channels.Add(channel);
            }

            return channels;
        }

    }
}