namespace SkypeMessagesExporter
{
    class Program
    {
        static void Main(string[] args)
        {
            ProgramMenu programMenu = new ProgramMenu();
            programMenu.ShowHelp();
            programMenu.ReadCommand();
        }
    }
}