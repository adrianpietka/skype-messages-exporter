using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Serialization;
using System.Net;
using RestSharp;
using System.Configuration;

namespace SkypeMessagesExporter
{
    class ExportMessages
    {
        List<Message> Messages;
        ChannelList ChannelList;

        public ExportMessages(ChannelList channelList, List<Message> messages)
        {
            ChannelList = channelList;
            Messages = messages;
        }

        public void Export()
        {
            if (Messages.Count() > 0)
            {
                SendRequest();
            }
            else
            {
                Console.WriteLine("[ExportMessages] No messages to sent");
            }
        }

        private void SendRequest()
        {
            Console.WriteLine(ConfigurationManager.AppSettings["WebServiceHost"]);
            Console.WriteLine("Anulowano proces exportu - ExportMessages.cs sprawdz");
            return;

            // host i uri wrzucic do konfiga
            var client = new RestClient(ConfigurationManager.AppSettings["WebServiceHost"]);
            var request = new RestRequest("update/", Method.POST);
            request.AddParameter("text/json", GetMessagesAsJson(), ParameterType.RequestBody);

            IRestResponse response = client.Execute(request);
            if (response.StatusCode.Equals(HttpStatusCode.OK))
            {
                ChannelList.SetActualFromMessages(Messages);
                ChannelList.Save();

                Console.WriteLine("[ExportMessages] Exported " + Messages.Count() + " new message(s)");

                Messages = new List<Message>();
            }
            else
            {
                Console.WriteLine("[ExportMessages] Error. Can't export " + Messages.Count() + " message(s)");
            }
        }

        private string GetMessagesAsJson()
        {
            return SimpleJson.SerializeObject(Messages.ToArray());
        }
    }
}
