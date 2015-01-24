using System;

namespace SkypeMessagesExporter.ProgramMenuItem
{
    class ExitProgram : IProgramMenuItem
    {
        public string Help()
        {
            return Command() + " - close application";
        }

        public string Command()
        {
            return "exit";
        }

        public void Execute()
        {
            Environment.Exit(0);
        }
    }
}
