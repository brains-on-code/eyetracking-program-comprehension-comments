using System.Drawing.Printing;
using System.Linq;
using System.Windows;

namespace Study
{
    public partial class SnippetQuestions
    {
        private readonly App _app;
        private readonly QuestionWindow _questionWindow;


        public SnippetQuestions(App app, string filename, int snippetId)
        {
            InitializeComponent();
            _app = app;
            _questionWindow = new QuestionWindow(app, GridQuest, NextButton, filename, snippetId);
        }



        private void Button_Click(object sender, RoutedEventArgs e)
        {
            var invalidQuestions = _questionWindow.CheckIfEntriesOkay();
            if (invalidQuestions.Count == 0)
            {
                if (!_app.GetSession().WarmUpDone)
                {
                    _app.GetSession().WarmUpDone = true;
                    _questionWindow.LogResults();
                    _app.ChangeWindow(App.WindowType.StartTrials);
                    return;
                }

                _questionWindow.LogResults();
                if (_app.GetSession().NextSnippetAvailable())
                {
                    _app.ChangeWindow(App.WindowType.Intersnippet);
                }
                else
                {
                    _app.GetSession().LogResultsAndTimes();
                    _app.GetSession().LogGeneralInfo();
                    _app.ChangeWindow(App.WindowType.SnippetsFinished);
                }
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


