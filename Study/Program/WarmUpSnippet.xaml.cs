using System;
using System.Diagnostics;
using System.Drawing;
using System.Windows;
using System.Windows.Forms;
using System.Windows.Media.Imaging;
using MessageBox = System.Windows.MessageBox;

namespace Study
{
    public partial class WarmUpSnippet
    {

        private readonly App _app;
        private readonly Timer _timer;
        private readonly Stopwatch _stopwatch;
        private bool _warned;
        private bool _timeout;

        // CONFIG
        public const int SnippetHeight = 1440;
        public const int SnippetWidth = 2560;
        private const int LastTimerInterval = 60000;
        private const int FirstTimerInterval = 240000;

        public WarmUpSnippet(App app)
        {
            _app = app;
            _stopwatch = new Stopwatch();

            _timer = new Timer { Interval = FirstTimerInterval };
            _timer.Tick += Timer_Tick;
            _timer.Start();

            Hide();
            InitializeComponent();


            var imagePath = _app.GetSession().GetCurrentImagePath();
            var bitImage = new BitmapImage(new Uri(imagePath));
            CodeImage.Source = bitImage;
            CodeImage.Height = SnippetHeight;
            CodeImage.Width = SnippetWidth;

            Show();
            _app.GetSession().StartRecordingSnippet();
            _stopwatch.Start();
        }


        private void Button_Click(object sender, RoutedEventArgs e)
        {
            Bitmap screenshot = null;
            if (_app.GetSession().useScreenshots)
            {
                screenshot = TakeScreenshot();
            }

            StopEverything();
            _app.GetSession().SnippetDone("", "", _stopwatch.ElapsedMilliseconds, _timeout, screenshot);
            ShowNextWindow();
        }

        private void StopEverything()
        {
            _app.GetSession().StopRecording();
            _timer.Stop();
            _stopwatch.Stop();
        }


        private void Timer_Tick(object sender, EventArgs e)
        {
            if (!_warned)
            {
                MessageBox.Show(Properties.Resources.TimeNearlyOutMessage, Properties.Resources.TimeNearlyOutTitle,
                    MessageBoxButton.OK);
                _timer.Interval = LastTimerInterval;
                _warned = true;
            }
            else
            {
                _timer.Stop();
                MessageBox.Show(Properties.Resources.TimeOutMessage, Properties.Resources.TimeOutTitle,
                    MessageBoxButton.OK);
                _timeout = true;
                Button_Click(null, null);
            }

        }

        private void ShowNextWindow()
        {
            _app.ChangeWindow(App.WindowType.SnippetQuestions);
        }

        private Bitmap TakeScreenshot()
        {
            int screenWidth = (int)Screen.PrimaryScreen.Bounds.Width;
            int screenHeight = (int)Screen.PrimaryScreen.Bounds.Height;

            // Console.WriteLine("Width: " + screenWidth + ", Height: " + screenHeight);

            Bitmap screenshot = new Bitmap(screenWidth, screenHeight, System.Drawing.Imaging.PixelFormat.Format32bppArgb);
            Graphics graphics = Graphics.FromImage(screenshot);
            graphics.CopyFromScreen(0, 0, 0, 0, Screen.PrimaryScreen.Bounds.Size);

            return screenshot;
        }
    }
}

      