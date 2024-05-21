using System.Windows;

namespace Study
{
    public partial class Information
    {
        private readonly App _app;

        public Information(App app)
        {
            InitializeComponent();
            _app = app;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            _app.ChangeWindow(App.WindowType.GeneralQuestions);
        }
    }
}