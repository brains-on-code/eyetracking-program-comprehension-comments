using System;
using System.Windows.Forms;

namespace Study
{
    public partial class FixationCross
    {
        private readonly App _app;
        private readonly Timer _timer;

        public FixationCross(App app)
        {
            InitializeComponent();
            _app = app;
            _timer = new Timer {Interval = 5000}; 
            _timer.Tick += Timer_Tick;
            _timer.Start();
            _app.GetSession().StartRecordingFixationCross();
        }


        private void Timer_Tick(object sender, EventArgs e)
        {
            _timer.Stop();
            _app.GetSession().StopRecording();
            _app.ChangeWindow(_app.GetSession().WarmUpDone ? App.WindowType.Snippet : App.WindowType.WarmUp);
            
        }
     
    }
}
