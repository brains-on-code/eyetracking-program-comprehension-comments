using System;
using EyeXFramework;
using Tobii.EyeX.Framework;

namespace Study
{
    public class Tracker
    {
        private readonly EyeXHost _eyeXHost;
        private GazePointDataStream _stream;
        private bool _logggingStarted = false;
        private Guid id;


        public Tracker(Guid id)
        {
            _eyeXHost = new EyeXHost();
            this.id = id;
            _eyeXHost.Start();
        }


        public void Run(string snippetName, int trialNumber, Guid id)
        {
            Console.WriteLine(_eyeXHost.ScreenBounds);
            _stream = _eyeXHost.CreateGazePointDataStream(GazePointDataMode.LightlyFiltered);
            var fileName = "GazeData_" + id + ".csv";
            if (!_logggingStarted)
            {
                FileHandling.Log(fileName, "Time;Gaze.X;GazeY;SubjectID;Snippet;TrialNumber");
                _logggingStarted = true;
            }


            _stream.Next += (s, gazePointEventArgs) =>
            {
                FileHandling.Log(fileName, gazePointEventArgs.Timestamp + ";" + gazePointEventArgs.X + ";" + gazePointEventArgs.Y + ";" + id + ";" + snippetName + ";" + trialNumber);
            };
        }



        public void Stop()
        {
            _stream.Dispose();
        }

        public void Calibrate()
        {
            _eyeXHost.LaunchGuestCalibration();
        }

        public int GetScreenWidth()
        {
            return (int)_eyeXHost.ScreenBounds.Value.Width;
        }

        public int GetScreenHeight()
        {
            return (int)_eyeXHost.ScreenBounds.Value.Height;
        }
    }
}
