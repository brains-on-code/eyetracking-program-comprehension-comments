using System.Windows;

namespace Study
{
    public partial class StudentQuestions
    {
        private readonly App _app;
        private readonly QuestionWindow _questionWindow;


        public StudentQuestions(App app)
        {
            InitializeComponent();
            _app = app;
            _questionWindow = new QuestionWindow(app,GridQuest,NextButton, "studentQuestions");
        }



        private void Button_Click(object sender, RoutedEventArgs e)
        {
            var invalidQuestions = _questionWindow.CheckIfEntriesOkay();
            if (invalidQuestions.Count == 0)
            {
                _questionWindow.AddAnswersToInfo();
 
                _app.ChangeWindow(App.WindowType.ProgQuestions);
            }
            else
            {
                _questionWindow.InvalidQuestionsGiven(invalidQuestions);
            }
        }

    }
}
