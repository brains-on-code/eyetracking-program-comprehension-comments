using System;
using System.Windows;

namespace Study
{
    public partial class Intersnippet
    {
        private readonly App _app;
        public Intersnippet(App app)
        {
            _app = app;
            InitializeComponent();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            if (Input.Text == "X" || Input.Text == "x")
            {
                _app.GetSession().LogResultsAndTimes();
                _app.GetSession().LogGeneralInfo();
                _app.ChangeWindow(App.WindowType.SnippetsFinished);
            }
            else
            {
                _app.ChangeWindow(App.WindowType.FixationCross);
            }
        }
    }
}
