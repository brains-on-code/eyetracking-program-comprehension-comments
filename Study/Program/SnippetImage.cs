using System.Drawing;

namespace Study
{
    public class SnippetImage
    {
        public string Name;
        public bool Comments;   // CONFIG: Enter your independent variable
        public long Time;
        public string Output;
        // public string Description;
        public bool TimeOut;


        public string GetPathToImage()
        {
            // return FileHandling.ImageDirectoryPath + Name + "_" + Indentation + FileHandling.Png;
            return FileHandling.ImageDirectoryPath + Name + FileHandling.Png;
        }

    }
}
