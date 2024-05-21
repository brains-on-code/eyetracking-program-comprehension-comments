using System.Windows;

namespace Study
{
    public partial class SnippetsFinished
    {
        private readonly App _app;

        public SnippetsFinished(App app)
        {
            InitializeComponent();
            _app = app;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            _app.End();
        }

    }
}
