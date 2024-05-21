using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Markup;
using ComboBox = System.Windows.Controls.ComboBox;
using HorizontalAlignment = System.Windows.HorizontalAlignment;
using ListBox = System.Windows.Controls.ListBox;
using RadioButton = System.Windows.Controls.RadioButton;
using TextBox = System.Windows.Controls.TextBox;

namespace Study
{
    class QuestionGrid
    {
        private readonly App _app;
        private const int GapBetwQuestions = 30;
        private const int QuestionsFontSize = 22;
        public readonly Dictionary<string, Question> Questions;
        public readonly Dictionary<string, TextBox> TextBoxes;
        public readonly Dictionary<string, ListBox> ListBoxes;
        public readonly Dictionary<string, ComboBox> ComboBoxes;
        private readonly Grid _grid;

        public QuestionGrid(Grid grid, string filename)
        {
            _grid = grid;
            var questionLines = FileHandling.LoadQuestionLines(filename);
            Questions = new Dictionary<string, Question>();
            TextBoxes = new Dictionary<string, TextBox>();
            ListBoxes = new Dictionary<string, ListBox>();
            ComboBoxes = new Dictionary<string, ComboBox>();

            foreach (var question in questionLines)
            {
                CreateQuestion(question.Split(';'));
            }
            AddQuestionsToGrid();
        }

        public QuestionGrid(App app, Grid grid)
        {
            _app = app;
            _grid = grid;
            Questions = new Dictionary<string, Question>();
            TextBoxes = new Dictionary<string, TextBox>();
            ListBoxes = new Dictionary<string, ListBox>();
            ComboBoxes = new Dictionary<string, ComboBox>();

            // Add standard questions
            CreateQuestion(new[] {"Out", "What is the output of the code snippet?", "Free", "MAN", "?"});
            //CreateQuestion(new[] {"Desc", "Describe what the code snippet does?", "Free", "MAN", "?" });

            AddQuestionsToGrid();
        }


        private void CreateQuestion(string[] questionLine)
        {
            Question.QuestionType type;
            if (!Enum.TryParse(questionLine[2], out type))
            {
                throw new ArgumentOutOfRangeException();
            }
            var name = questionLine[0];
            var text = questionLine[1];
            if (type == Question.QuestionType.Int)
            {
                Questions.Add(name, new Question.IntQuestion(name, text, type,GetParams(questionLine)));
            }
            else if (type == Question.QuestionType.Select)
            {
                Questions.Add(name, new Question.SelectQuestion(name, text, type, GetParams(questionLine)));
            }
            else if (type == Question.QuestionType.Free)
            {
                Questions.Add(name, new Question.FreeQuestion(name, text, type, GetParams(questionLine)));
            }
            else if (type == Question.QuestionType.Combo)
            {
                Questions.Add(name, new Question.ComboQuestion(name, text, type, GetParams(questionLine)));
            }
        }



        private void AddQuestionsToGrid()
        {
            var index = 0;
            foreach (var question in Questions.Values)
            {
                _grid.RowDefinitions.Add(new RowDefinition());
                AddTextBlockToGrid(question.Text, index * 2 + 2, 0);

                if (index < Questions.Count - 1)
                {
                    _grid.RowDefinitions.Add(new RowDefinition() { Height = new GridLength(GapBetwQuestions) });
                }

                if (question.Type == Question.QuestionType.Free )
                {
                    AddTextBoxToGrid(question.Name, index * 2 + 2, 2, ((Question.FreeQuestion)question).WidthString);
                } else if (question.Type == Question.QuestionType.Int)
                {
                    AddTextBoxToGrid(question.Name, index * 2 + 2, 2, ((Question.IntQuestion)question).WidthString);
                }
                else if (question.Type == Question.QuestionType.Select)
                {
                    AddSelectionToGrid(question.Name, index * 2 + 2, 2, ((Question.SelectQuestion)question).SelectionValues);
                }
                else if (question.Type == Question.QuestionType.Combo)
                {
                    AddComboToGrid(question.Name, index * 2 + 2, 2, ((Question.ComboQuestion)question).ComboValues);
                }

                index++;
            }



        }

        private void AddComboToGrid(string name, int row, int column, string[] values)
        {
            var comboBox = new ComboBox();
            double maxWidth = 0;
            foreach (var value in values)
            {
                var item = new ComboBoxItem
                {
                    Content = value,
                    FontSize = QuestionsFontSize
                };
                item.Measure(new Size(double.PositiveInfinity, Double.PositiveInfinity));
                var temp = item.DesiredSize.Width;
                if (temp > maxWidth)
                {
                    maxWidth = temp;
                }
                comboBox.Items.Add(item);
            }

            comboBox.FontSize = QuestionsFontSize;
            comboBox.Name = name;
            comboBox.HorizontalAlignment = HorizontalAlignment.Left;
            comboBox.Text = "Bitte wählen";
            comboBox.Measure(new Size(Double.PositiveInfinity, Double.PositiveInfinity));
            comboBox.Width =  comboBox.DesiredSize.Width + maxWidth;


            Grid.SetRow(comboBox, row);
            Grid.SetColumn(comboBox, column);
            _grid.Children.Add(comboBox);
            ComboBoxes.Add(name, comboBox);
        }

        private void AddSelectionToGrid(string name, int row, int column, string[] values)
        {
            var listBox = new ListBox();
            foreach (var value in values)
            {
                var button = new RadioButton
                {
                    Content = value,
                    FontSize = QuestionsFontSize,
                    VerticalContentAlignment = VerticalAlignment.Center,
                    Margin = new Thickness(30, 0, 0, 0)
                };
                button.Checked += (sender, args) => listBox.SelectedItem = sender;
                listBox.Items.Add(button);

            }
            listBox.ItemsPanel = (ItemsPanelTemplate)XamlReader.Parse("<ItemsPanelTemplate xmlns=\"http://schemas.microsoft.com/winfx/2006/xaml/presentation\"><StackPanel Orientation=\"Horizontal\"/></ItemsPanelTemplate>");
            listBox.BorderThickness = new Thickness(0);
            listBox.FontSize = QuestionsFontSize;
            listBox.Name = name;

            Grid.SetRow(listBox, row);
            Grid.SetColumn(listBox, column);
            _grid.Children.Add(listBox);
            ListBoxes.Add(name, listBox);
        }


        private void AddTextBoxToGrid(string name, int row, int column, string widthString)
        {
            var textBox = new TextBox
            {
                FontSize = QuestionsFontSize,
                Name = name,
                HorizontalAlignment = HorizontalAlignment.Left,
                Width = 500

            };
            if (widthString != "?")
            {
                var textBlock = new TextBlock
                {
                    Text = widthString,
                    FontSize = QuestionsFontSize
                };
                textBlock.Height = textBlock.FontSize * textBlock.FontFamily.LineSpacing;
                textBlock.Measure(new Size(Double.PositiveInfinity, Double.PositiveInfinity));
                textBox.Width = textBlock.DesiredSize.Width;
            }
            textBox.MaxHeight = textBox.FontSize * textBox.FontFamily.LineSpacing;
            Grid.SetRow(textBox, row);
            Grid.SetColumn(textBox, column);
            _grid.Children.Add(textBox);
            TextBoxes.Add(name, textBox);
        }

        private void AddTextBlockToGrid(string text, int row, int column)
        {
            var textBlock = new TextBlock
            {
                Text = text,
                FontSize = QuestionsFontSize,
                TextWrapping = TextWrapping.Wrap
            };
            Grid.SetRow(textBlock, row);
            Grid.SetColumn(textBlock, column);
            _grid.Children.Add(textBlock);
        }


        private static string[] GetParams(string[] questionLine)
        {
            var result = new string[questionLine.Length - 3];
            Array.Copy(questionLine, 3, result, 0, questionLine.Length - 3);
            return result;
        }


        public List<Question> CheckIfEntriesOkay()
        {
            var invalidQuestions = new List<Question>();
            foreach (var textBox in TextBoxes.Values)
            {
                var question = Questions[textBox.Name];
                var text = textBox.Text;
                switch (question.Type)
                {
                    case Question.QuestionType.Free:
                        var freeQuestion = (Question.FreeQuestion)question;
                        if (freeQuestion.Mandatory && text == "")
                        {
                            invalidQuestions.Add(question);
                        }
                        break;
                    case Question.QuestionType.Int:
                        if (!IntQuestionOkay(question, text))
                        {
                            invalidQuestions.Add(question);
                        }
                        break;
                }
            }

            foreach (var listBox in ListBoxes.Values)
            {
                if (listBox.SelectedItem == null)
                {
                    invalidQuestions.Add(Questions[listBox.Name]);
                }
            }

            foreach (var comboBox in ComboBoxes.Values)
            {
                if (comboBox.SelectedItem == null)
                {
                    invalidQuestions.Add(Questions[comboBox.Name]);
                }

            }

            return invalidQuestions;
        }

        private static bool IntQuestionOkay(Question question, string text)
        {
            if (text == "") return false;
            var intQuestion = (Question.IntQuestion)question;
            int number;
            if (int.TryParse(text, out number))
            {
                if (number < intQuestion.LowerBorder || number > intQuestion.UpperBorder)
                {
                    return false;
                }
            }
            else
            {
                return false;
            }
            return true;
        }
    }

}
