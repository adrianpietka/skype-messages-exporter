using System;
using System.Threading;
using System.Collections.Generic;

// http://msdn.microsoft.com/en-US/library/7a2f3ay4(v=vs.80).aspx
// puscic exportowanie na dwa watki:
// - MessageListenerWorker - wrzuc nowe wiadomosci do kolejki
// - MessageExporterWorker - exportuj partie wiadomosci z kolejki
// MessageQueue - semafor z kolejka wiadomosci do wysylania

namespace SkypeMessagesExporter.ProgramMenuItem
{
    class StartExportMessages : IProgramMenuItem
    {
        public string Help()
        {
            return Command() + " - running export messages to webservice";
        }

        public string Command()
        {
            return "start";
        }

        public void Execute()
        {
            bool keepRunning = true;
            int messageListenerInterval = 60 * 1000; // zmienic na 1 minute, a najlepiej z configa brac

            // channels.csv wrzucic do configa
            ChannelList channelList = new ChannelList("channels.csv");
            SkypeDatabase skypeDatabase = new SkypeDatabase();

            Console.WriteLine("Press Ctrl + C to exit.");
            Console.CancelKeyPress += delegate(object sender, ConsoleCancelEventArgs e)
            {
                keepRunning = false;
            };

            while (keepRunning)
            {
                try
                {
                    skypeDatabase.RefreshDatabase();
                    List<Message> newMessages = skypeDatabase.GetNewMessages(channelList);

                    // MessageQueue messageQueue = new MessageQueue();
                    // messageQueue.AddMessages(newMessages);
                    // przerobic to na kolejke newMessages na MessageQueue
                    // po updacie leci remove na element z kolejki
                    ExportMessages exportMessages = new ExportMessages(channelList, newMessages);
                    exportMessages.Export();
                }
                catch (Exception exception)
                {
                    Console.WriteLine(exception.ToString());
                }

                Thread.Sleep(messageListenerInterval);
            }
        }
    }
}
