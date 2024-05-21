using System.Windows;

namespace Study
{
    public partial class MainWindow
    {
        private readonly App _app;

        public MainWindow(App app)
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
