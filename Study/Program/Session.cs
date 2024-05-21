using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;

namespace Study
{
    public class Session
    {

        private readonly Tracker _eyeTracker;
        private readonly Guid _id;
        public SnippetImage[] Snippets;
        private int _index;

        private int NrSnippets;

        private readonly Dictionary<string, string> _generalInfo;
        //private readonly Dictionary<int, List<string>> _snippetQuestions;
        private static readonly bool saveAfterSnippet = false; // CONFIG: Set to true to save results after each snippet
        public bool useScreenshots = false; // CONFIG: Set to true to save screenshots
        public bool WarmUpDone;
        
        public Session()
        {
            _id = Guid.NewGuid();
            FileHandling.SetTrialDirName("Trial_" + _id);
            _eyeTracker = new Tracker(_id);

            _generalInfo = new Dictionary<string, string>();
            Snippets = FileHandling.LoadImages();
            //_snippetQuestions = FileHandling.LoadSnippetQuestionLines();
            NrSnippets = Snippets.Length;
            if (saveAfterSnippet){
                FileHandling.Log("Results_" + _id + ".csv", "Number;Task;Time;TimeOut;SubjectID");
                LogGeneralInfoPart();
            }
        }

        public void AddInfo(string header, string value)
        {
            _generalInfo.Add(header, value);
        }

        public void LogGeneralInfo()
        {
            var fileName = "GeneralInfo_" + _id + ".csv";
            var header = new StringBuilder();
            var values = new StringBuilder();
            foreach (var key in _generalInfo.Keys)
            {
                header.Append(key + ";");
                values.Append(_generalInfo[key] + ";");
            }
            header.Append("EyeXScreenWidth;EyeXScreenHeight;");
            values.Append(_eyeTracker.GetScreenWidth().ToString() + ";" + _eyeTracker.GetScreenHeight() + ";");
            header.Append("SubjectID");
            values.Append(_id);
            FileHandling.Log(fileName, header.ToString());
            FileHandling.Log(fileName, values.ToString());
            FileHandling.StopLogging();
        }

        public void LogGeneralInfoPart()
        {
            var fileName = "GeneralInfo_" + _index + "_" + _id + ".csv";
            var header = new StringBuilder();
            var values = new StringBuilder();
            foreach (var key in _generalInfo.Keys)
            {
                header.Append(key + ";");
                values.Append(_generalInfo[key] + ";");
            }
            header.Append("EyeXScreenWidth;EyeXScreenHeight;");
            values.Append(_eyeTracker.GetScreenWidth().ToString() + ";" + _eyeTracker.GetScreenHeight() + ";");
            header.Append("SubjectID");
            values.Append(_id);
            FileHandling.Log(fileName, header.ToString());
            FileHandling.Log(fileName, values.ToString());
            FileHandling.StopLogging();
        }

        public void StartRecordingSnippet()
        {
            _eyeTracker.Run(Snippets[_index].Name, _index, _id);
        }

        public void StartRecordingFixationCross()
        {
            _eyeTracker.Run("FixationCross_" + _index, _index, _id);
        }

        /*public List<string> GetSnippetQuestions(int snippetId) {
            return _snippetQuestions[snippetId];
        }*/

        public string GetCurrentImagePath()
        {
            return Snippets[_index].GetPathToImage();
        }

        public string GetPreviousImageName()
        {
            return Snippets[_index - 1].Name;
        }

        public int GetPreviousSnippetId()
        {
            return _index - 1;
        }

        public void CalibrateTracker()
        {
            _eyeTracker.Calibrate();
        }


        public void StopRecording()
        {
            _eyeTracker.Stop();
            FileHandling.StopLogging();
        }


        public void SnippetDone(string result, string description, long time, bool timeout, Bitmap screenshot) //TODO maybe move saving here
        {
            Snippets[_index].Output = result;
            // Snippets[_index].Description = description;
            Snippets[_index].Time = time;
            Snippets[_index].TimeOut = timeout;
            if (useScreenshots) {
                FileHandling.SaveScreenshot(Snippets[_index].Name /*+ "_Trial" + _index + "_" + _id*/, screenshot);
            }
            if (saveAfterSnippet) {
                FileHandling.Log("Results_" + _id + ".csv", _index + ";" + Snippets[_index].Name + ";" + Snippets[_index].Time + ";" + Snippets[_index].TimeOut + ";" + _id);
                LogGeneralInfoPart();
            }
            _index += 1;
        }

        public bool NextSnippetAvailable()
        {
            return _index < NrSnippets;
        }

        public void LogResultsAndTimes()
        {
            if (!saveAfterSnippet) {
                var log = "";
                for (var i = 0; i < NrSnippets; ++i)
                {
                    log = log + i + ";" + Snippets[i].Name + ";" + Snippets[i].Output + ";" + Snippets[i].Time + ";" + Snippets[i].TimeOut + ";" + _id + "\n";
                    // log = log + i + ";" + Snippets[i].Name + ";" + Snippets[i].Output + ";" + Snippets[i].Description + ";" + Snippets[i].Time + ";" + Snippets[i].TimeOut + ";" + _id + "\n";
                }
                var fileName = "Results_" + _id + ".csv";
                FileHandling.Log(fileName, "Number;Task;Answer_Out;Time;TimeOut;SubjectID");
                // FileHandling.Log(fileName, "Number;Snippet;Answer_Out;Answer_Desc;Time;TimeOut;SubjectID");
                FileHandling.Log(fileName, log);

                log = "";
                var snippetInfos = new List<(string Name, string Type, int Difficulty, int CommentContribution)>();

                foreach (var snippet in Snippets)
                {
                    string taskName = snippet.Name.Substring(0, snippet.Name.Length - 2);
                    string taskType = snippet.Name.Substring(snippet.Name.Length - 2);

                    if (taskName == "Warm")
                        continue;

                    int difficulty = 0;
                    int commentContribution = 0;

                    snippetInfos.Add((taskName, taskType, difficulty, commentContribution));
                }

                snippetInfos.Sort((a, b) =>
                {
                    int numA = int.Parse(a.Name.Substring(4)); // Extract numeric part
                    int numB = int.Parse(b.Name.Substring(4));

                    return numA.CompareTo(numB);
                });

                foreach (var snippet in snippetInfos)
                {
                    log = log + snippet.Name + ";" + snippet.Type + ";" + snippet.Difficulty + ";" + snippet.CommentContribution + "\n";
                }

                fileName = "Ratings_" + _id + ".csv";
                FileHandling.Log(fileName, "Task;Type;Difficulty;Comment Contribution");
                FileHandling.Log(fileName, log);
            }
            FileHandling.StopLogging();
        }
    }
}
