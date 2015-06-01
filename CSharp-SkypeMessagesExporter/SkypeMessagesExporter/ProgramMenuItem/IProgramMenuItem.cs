namespace SkypeMessagesExporter.ProgramMenuItem
{
    interface IProgramMenuItem
    {
        string Command();
        string Help();
        void Execute();
    }
}
