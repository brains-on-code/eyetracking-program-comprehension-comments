using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;

namespace Study
{
    public class FileHandling
    {
        // Config Variables
        private static readonly string ExperimentName = "Effect_of_Comments";   // CONFIG: Enter the name of your study
        private static readonly bool useImageCombinations = true;  // CONFIG: Set to true if you want to use imageCombinations.csv

        // Paths
        private static string DirName;
        public static readonly string ImageDirectoryPath = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\")) + "Resources\\Images\\";
        private static readonly string ImageCombinationsFile = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\")) + "Resources\\imageCombinations.csv";
        private static readonly string QuestionsPath = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\")) + "Resources\\Questions\\";
        private static readonly string SnippeQuestionsFile = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\")) + "Resources\\Questions\\snippetQuestions.csv";
        private static readonly string ResultMailFile = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\..\\")) + "\\" + ExperimentName + "\\"+  "Mails\\ResultMails.txt";
        private static readonly string AgainMailFile = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\..\\")) + "\\" + ExperimentName + "\\" + "Mails\\AgainMails.txt";

        public const string Png = ".png";
        private static StreamWriter _writer;
        private static string _fileName = "";


        public static void Log(string fileName, string text)
        {
            var path = DirName + "\\" + fileName;
            if (!_fileName.Equals(path))
            {
                Directory.CreateDirectory(DirName + "\\");
                _writer?.Close();
                _writer = File.AppendText(path);
                _fileName = path;
            }

            _writer.WriteLine(text);

        }

        public static void SetTrialDirName(string name)
        {

            DirName = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..\\..\\..\\")) + "Results\\" + ExperimentName + "\\" + name;
        }

        public static SnippetImage[] LoadImages()
        {
            string[] snippetNames = new string[0];

            if (useImageCombinations) {
                // read the header row into an array
                using (StreamReader reader = new StreamReader(FileHandling.ImageCombinationsFile))
                {
                    string line = reader.ReadLine();
                    string[] warmup = { "WarmUp" };
                    string[] snippets = line.Split(',');
                    string[] allSnippets = warmup.Concat(snippets).ToArray();
                    snippetNames = allSnippets;
                }
                // delete the header row from the file
                List<string> lines = File.ReadAllLines(FileHandling.ImageCombinationsFile).Skip(1).ToList();
                File.WriteAllLines(FileHandling.ImageCombinationsFile, lines);
            } else {
                String[] fileNames = Directory.GetFiles(ImageDirectoryPath);
                foreach (String fileName in fileNames)
                {
                    string snippetName = fileName.Replace(ImageDirectoryPath, "").Replace(Png, "");
                    snippetNames.Append(snippetName);
                }
            }

            SnippetImage[] snippetImages = new SnippetImage[snippetNames.Length];

            for (int i = 0; i < snippetNames.Length; i++)
            {
                snippetImages[i] = new SnippetImage() { Name = snippetNames[i] };

            }

            return snippetImages;

        }

        public static void SaveScreenshot(String fileName, Bitmap screenshot)
        {
            Console.WriteLine("naming Directory");
            string ScreenshotDirectory = DirName + "\\Screenshots\\";
            Console.WriteLine("creating directory");
            if (!Directory.Exists(ScreenshotDirectory))
            {
                Directory.CreateDirectory(ScreenshotDirectory);
                Console.WriteLine("created Directory");
            }
            Console.WriteLine("saving image");
            using (var copiedScreenshot = new Bitmap(screenshot))
            {

                Console.WriteLine("saving image");
                var path = ScreenshotDirectory + fileName + ".txt";
                path = ScreenshotDirectory + fileName + ".jpg";
                copiedScreenshot.Save(path);
                Console.WriteLine("saved image");
            }
        }

        public static string[] LoadQuestionLines(string fileName)
        {
            var fileText = File.ReadAllText(QuestionsPath + fileName + ".csv");
            fileText = fileText.Replace("\r\n", "\n");
            return fileText.Split('\n');
        }


        public static void StopLogging()
        {
            _writer.Close();
            _fileName = "";
        }

        public static void AddResultMail(string mailAddress)
        {
            AddMailToFile(ResultMailFile, mailAddress);
        }

        public static void AddAgainMail(string mailAddress)
        {
            AddMailToFile(AgainMailFile, mailAddress);
        }

        private static void AddMailToFile(string filePath, string mailAddress)
        {
            var file = File.AppendText(filePath);
            file.WriteLine(mailAddress);
            file.Close();
        }
    }
}