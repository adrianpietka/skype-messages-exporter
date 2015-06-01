using System;
using System.IO;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace SkypeMessagesExporter
{
    public class ChannelList
    {
        private List<Channel> Channels = new List<Channel>();
        private string FileName;
        
        public ChannelList(string fileName)
        {
            Load(fileName);
        }

        public void Load(string fileName)
        {
            FileName = fileName;

            var reader = new StreamReader(File.OpenRead(FileName));
            while (!reader.EndOfStream)
            {
                var values = reader.ReadLine().Split(';');
                Channel channel = new Channel(
                    Convert.ToInt32(values[0]),
                    Convert.ToString(values[1]),
                    Convert.ToInt32(values[2])
                );

                Channels.Add(channel);
            }
            reader.Close();
        }

        public void Save()
        {
            StringBuilder content = new StringBuilder();

            Channels.ForEach(delegate(Channel channel)
            {
                content.AppendLine(
                    Convert.ToString(channel.Id) + ";" + channel.Name + ";" +
                    Convert.ToString(channel.LastMessageId)
                );
            });

            File.WriteAllText(FileName, content.ToString());
        }

        public void SetActualFromMessages(List<Message> messages)
        {
            messages.ForEach(delegate(Message message)
            {
                GetChannelById(message.ConversationId).LastMessageId = message.Id;
            });
        }

        public List<Channel> GetAll()
        {
            return Channels;
        }

        public Channel GetChannelById(int channelId)
        {
            return Channels.Find(channel => channel.Id.Equals(channelId));
        }
    }
}
