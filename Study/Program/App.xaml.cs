using System;
using System.Windows;

namespace Study
{
    public partial class App
    {
        private Window _currentWindow;
        private Session _session;

        public enum WindowType
        {
            Main, GeneralQuestions, Snippet, StartTrials,
            Finish, FixationCross,
            Instructions, Intersnippet,
            WarmUp, Calibrate, FinalQuestions,
            StudentQuestions, Information,
            ProgQuestions, Mail,
            FixationInstructions, CalibrationDone,
            SnippetsFinished,
            InterCalibration,
            SnippetQuestions
        }

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            _session = new Session();
            _currentWindow = GetWindow(WindowType.Main);
            _currentWindow.Show();
        }

        public void ChangeWindow(WindowType windowType)
        {
            var newWindow = GetWindow(windowType);
            newWindow.Show();
            _currentWindow.Close();
            _currentWindow = newWindow;
        }

        private Window GetWindow(WindowType windowType)
        {
            switch (windowType)
            {
                case WindowType.Main: return new MainWindow(this);
                case WindowType.GeneralQuestions: return new GeneralQuestions(this);
                case WindowType.StudentQuestions: return new StudentQuestions(this);
                case WindowType.ProgQuestions: return new ProgQuestions(this);
                case WindowType.InterCalibration: return new InterCalibration(this);
                case WindowType.Calibrate: return new CalibrateEyeTracker(this);
                case WindowType.CalibrationDone: return new CalibrationDone(this);
                case WindowType.Instructions: return new Instructions(this);
                case WindowType.FixationInstructions: return new FixationInstruction(this);
                case WindowType.FixationCross: return new FixationCross(this);
                case WindowType.WarmUp: return new WarmUpSnippet(this);
                case WindowType.StartTrials: return new Starting(this);
                case WindowType.Snippet: return new Snippet(this);
                case WindowType.SnippetQuestions: return new SnippetQuestions(this, _session.GetPreviousImageName(), _session.GetPreviousSnippetId());
                case WindowType.Intersnippet: return new Intersnippet(this);
                case WindowType.SnippetsFinished: return new SnippetsFinished(this);

                default:
                    throw new ArgumentOutOfRangeException(nameof(windowType), windowType, null);
            }
        }

        public Session GetSession()
        {
            return _session;
        }

        public void End()
        {
            _session.StopRecording();
            Shutdown();
        }
    }
}
