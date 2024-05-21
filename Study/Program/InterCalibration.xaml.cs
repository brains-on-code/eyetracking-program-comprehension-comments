using System.Windows;

namespace Study
{
    /// <summary>
    /// Interaction logic for InterCalibration.xaml
    /// </summary>
    public partial class InterCalibration
    {
        private readonly App _app;

        public InterCalibration(App app)
        {
            _app = app;
            InitializeComponent();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            _app.ChangeWindow(App.WindowType.Calibrate);
        }
    }
}
