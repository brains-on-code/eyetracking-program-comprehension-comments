using System.Windows;

namespace Study
{
    
    public partial class Instructions
    {
        private readonly App _app;
        public Instructions(App app)
        {
            InitializeComponent();
            _app = app;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            _app.ChangeWindow(App.WindowType.FixationInstructions);
        }
    }
}
