using System;
using System.Collections.Generic;
using SkypeMessagesExporter.ProgramMenuItem;

namespace SkypeMessagesExporter
{
    class ProgramMenu
    {
        List<IProgramMenuItem> ProgramMenuItems = new List<IProgramMenuItem>();

        public ProgramMenu()
        {
            ProgramMenuItems.Add(new StartExportMessages());
            ProgramMenuItems.Add(new ShowChannels());
            ProgramMenuItems.Add(new ShowConfiguration());
            ProgramMenuItems.Add(new ExitProgram());
        }

        public void ShowHelp()
        {
            Console.WriteLine("Possibility commands:");
            
            foreach (IProgramMenuItem item in ProgramMenuItems)
            {
                Console.WriteLine("  " + item.Help());
            }
        }

        public void ReadCommand()
        {
            Console.Write("$: ");
            string enteredCommand = Console.ReadLine();
            ExecuteCommand(enteredCommand);
            ReadCommand();
        }

        public void ExecuteCommand(string enteredCommand)
        {
            bool unknownCommand = true;

            ProgramMenuItems.ForEach(delegate(IProgramMenuItem item)
            {
                if (item.Command() == enteredCommand)
                {
                    unknownCommand = false;
                    item.Execute();
                }
            });

            if (unknownCommand)
            {
                Console.WriteLine("Unknown command \"" + enteredCommand + "\". Try again.");
            }
        }
    }
}
