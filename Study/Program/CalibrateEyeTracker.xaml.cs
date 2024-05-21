using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms;

namespace Study
{
    public partial class CalibrateEyeTracker
    {
        private readonly App _app;
        public CalibrateEyeTracker(App app)
        {
            InitializeComponent();
            _app = app;
        }

        private async void Button_Click(object sender, RoutedEventArgs e)
        {
            Button.IsEnabled = false;
            _app.GetSession().CalibrateTracker();
            await PutTaskDelay();

            _app.GetSession().AddInfo("ActualScreenWidth", Screen.PrimaryScreen.Bounds.Width.ToString());
            _app.GetSession().AddInfo("ActualScreenHeight", Screen.PrimaryScreen.Bounds.Height.ToString());

            _app.ChangeWindow(App.WindowType.CalibrationDone);

        }

        private static async Task PutTaskDelay()
        {
            await Task.Delay(3000);
        }
    }

}

