using System;
using System.Collections.Generic;

namespace SkypeMessagesExporter.ProgramMenuItem
{
    class ShowChannels : IProgramMenuItem
    {
        public string Help()
        {
            return Command() + " - display used channels from Skype database";
        }

        public string Command()
        {
            return "show channels";
        }

        public void Execute()
        {
            SkypeDatabase skypeDatabase = new SkypeDatabase();

            try
            {
                List<Channel> channels = skypeDatabase.GetChannels();

                foreach(Channel channel in channels)
                {
                    Console.WriteLine("#" + channel.Id + ": " + channel.Name);
                }
            }
            catch (Exception exception)
            {
                Console.WriteLine(exception.ToString());
            }
        }
    }
}
