using System.Linq;
using System.Windows;

namespace Study
{
    public partial class ProgQuestions
    {
        private readonly App _app;
        private readonly QuestionWindow _questionWindow;


        public ProgQuestions(App app)
        {
            InitializeComponent();
            _app = app;
            _questionWindow = new QuestionWindow(app, GridQuest, NextButton, "progQuestions");
        }



        private void Button_Click(object sender, RoutedEventArgs e)
        {
            var invalidQuestions = _questionWindow.CheckIfEntriesOkay();
            if (invalidQuestions.Count == 0)
            {
                _questionWindow.AddAnswersToInfo();

                _app.ChangeWindow(App.WindowType.Calibrate);
            }
            else
            {
                _questionWindow.FalseInputCount++;
                var errorMessage = invalidQuestions.Aggregate(Properties.Resources.QuestionErrorMessage, (current, questions) => current + (questions.Text + "\n"));
                MessageBox.Show(errorMessage, Properties.Resources.QuestionErrorTitle, MessageBoxButton.OK);
            }
        }

    }
}
