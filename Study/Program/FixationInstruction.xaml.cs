using System.Windows;

namespace Study
{
    public partial class FixationInstruction
    {
        private readonly App _app;
        public FixationInstruction(App app)
        {
            InitializeComponent();
            _app = app;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            _app.ChangeWindow(App.WindowType.FixationCross);
        }
    }
}

