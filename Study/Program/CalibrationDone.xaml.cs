using System.Windows;

namespace Study
{
    public partial class CalibrationDone
    {
        private readonly App _app;

        public CalibrationDone(App app)
        {
            InitializeComponent();
            _app = app;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            _app.ChangeWindow(App.WindowType.Instructions);
        }

    }
}