using System.Linq;
using System.Windows;

namespace Study
{
    public partial class GeneralQuestions
    {
        private readonly App _app;
        private readonly QuestionWindow _questionWindow;


        public GeneralQuestions(App app)
        {
            InitializeComponent();
            _app = app;
            _questionWindow = new QuestionWindow(app, GridQuest, NextButton, "generalQuestions");
        }



        private void Button_Click(object sender, RoutedEventArgs e)
        {
            var invalidQuestions = _questionWindow.CheckIfEntriesOkay();
            if (invalidQuestions.Count == 0)
            {
                _questionWindow.AddAnswersToInfo();

                _app.ChangeWindow(_questionWindow.StudentSelected()
                    ? App.WindowType.StudentQuestions
                    : App.WindowType.ProgQuestions);
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


