using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SkypeMessagesExporter
{
    public class Channel
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public int LastMessageId { get; set; }

        public Channel(int id, string name, int lastMessageId = 0)
        {
            Id = id;
            Name = name;
            LastMessageId = lastMessageId;
        }
    }
}
