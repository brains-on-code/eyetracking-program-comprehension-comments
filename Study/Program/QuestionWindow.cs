using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace Study
{
    class QuestionWindow
    {
        private const int GapToButton = 50;
        private readonly App _app;
        private readonly QuestionGrid _questiongrid;
        public int FalseInputCount;
        private readonly string _name;
        private readonly int _id;



        public QuestionWindow(App app, Grid gridQuest, Button nextButton, string fileName)
        {
            _name = fileName;
            _app = app;
            _questiongrid = new QuestionGrid(gridQuest, fileName);

            gridQuest.RowDefinitions.Add(new RowDefinition { Height = new GridLength(GapToButton) });
            gridQuest.RowDefinitions.Add(new RowDefinition());
            Grid.SetRow(nextButton, _questiongrid.Questions.Count * 2 + 2);
        }

        public QuestionWindow(App app, Grid gridQuest, Button nextButton, string fileName, int snippetId)
        {
            _name = fileName;
            _id = snippetId;
            _app = app;
            _questiongrid = new QuestionGrid(app, gridQuest);

            gridQuest.RowDefinitions.Add(new RowDefinition { Height = new GridLength(GapToButton) });
            gridQuest.RowDefinitions.Add(new RowDefinition());
            Grid.SetRow(nextButton, _questiongrid.Questions.Count * 2 + 2);
        }

        public void AddAnswersToInfo()
        {
            foreach (var textBox in _questiongrid.TextBoxes.Values)
            {
                _app.GetSession().AddInfo(textBox.Name, textBox.Text.Replace(";",""));
            }
            foreach (var listBox in _questiongrid.ListBoxes.Values)
            {
                _app.GetSession().AddInfo(listBox.Name, ((RadioButton)listBox.SelectedItems[0]).Content.ToString());
            }
            foreach (var comboBox in _questiongrid.ComboBoxes.Values)
            {
                _app.GetSession().AddInfo(comboBox.Name, ((ComboBoxItem)comboBox.SelectedItem).Content.ToString());
            }
            _app.GetSession().AddInfo("NrFalseInputs_" + _name, FalseInputCount.ToString());
            
        }

        public void LogResults()
        {
            _app.GetSession().Snippets[_id].Output = _questiongrid.TextBoxes.ElementAt(0).Value.Text.Trim();
            // _app.GetSession().Snippets[_id].Description = _questiongrid.TextBoxes.ElementAt(1).Value.Text.Trim();
        }

        public  List<Question> CheckIfEntriesOkay()
        {
            return _questiongrid.CheckIfEntriesOkay();
        }

        public bool StudentSelected()
        {
            if(_questiongrid.ListBoxes.ContainsKey("Job"))
            {
                var jobListBox = _questiongrid.ListBoxes["Job"];
                var job = (string) ((RadioButton) jobListBox.SelectedItem).Content;
                return job == "Student";
            }
            if (_questiongrid.ComboBoxes.ContainsKey("Job"))
            {
                var jobComboBox = _questiongrid.ComboBoxes["Job"];
                var job = (string)((ComboBoxItem)jobComboBox.SelectedItem).Content;
                return job == "Student";
            }
            return false;

        }

        public void InvalidQuestionsGiven(List<Question> invalidQuestions)
        {
            FalseInputCount++;
            var errorMessage = invalidQuestions.Aggregate(Properties.Resources.QuestionErrorMessage, (current, questions) => current + (questions.Text + "\n"));
            MessageBox.Show(errorMessage, Properties.Resources.QuestionErrorTitle, MessageBoxButton.OK);
        }
    }
}