using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SkypeMessagesExporter
{
    public class Message
    {
        public int Id { get; set; }
        public int ConversationId { get; set; }
        public string ConversationName { get; set; }
        public string Author { get; set; }
        public string Date { get; set; }
        public string Content { get; set; }
        
        public Message(int id, int conversationId, string conversationName, string author, string date, string content)
        {
            Id = id;
            ConversationId = conversationId;
            ConversationName = conversationName;
            Author = author;
            Date = date;
            Content = content;
        }

        public Message()
        {

        }
    }
}
