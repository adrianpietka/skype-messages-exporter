using System;

namespace SkypeMessagesExporter.ProgramMenuItem
{
    class ShowConfiguration : IProgramMenuItem
    {
        public string Help()
        {
            return Command() + " - display configuration values";
        }

        public string Command()
        {
            return "show configuration";
        }

        public void Execute()
        {
            Console.WriteLine("TODO it! :-)");
        }
    }
}
