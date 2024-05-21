using System;

namespace Study
{
    public abstract class Question
    {
        public string Name;
        public string Text;
        public QuestionType Type;

        public enum QuestionType
        {
            Free, Int, Select, Combo
        }

        protected Question(string name, string text, QuestionType type)
        {
            Name = name;
            Text = text;
            Type = type;
        }

        public class IntQuestion : Question
        {
            public int LowerBorder;
            public int UpperBorder;
            public string WidthString;
            public IntQuestion(string name, string text, QuestionType type, string[] values) : base(name, text, type)
            {
                if (values.Length < 2)
                {
                    throw new ArgumentOutOfRangeException();
                }
                LowerBorder = Convert.ToInt32(values[0]);
                UpperBorder = Convert.ToInt32(values[1]);
                WidthString = values[2];
            }
        }


        public class FreeQuestion : Question
        {
            public bool Mandatory;
            public string WidthString;
            public FreeQuestion(string name, string text, QuestionType type, string[] values) : base(name, text, type)
            {
                if (values[0] == "MAN")
                {
                    Mandatory = true;
                }
                WidthString = values[1];
            }

        }

        public class SelectQuestion : Question
        {
            public string[] SelectionValues;
            public SelectQuestion(string name, string text, QuestionType type, string[] values) : base(name, text, type)
            {
                SelectionValues = values;
            }
        }

        public class ComboQuestion : Question
        {
            public string[] ComboValues;

            public ComboQuestion(string name, string text, QuestionType type, string[] values) : base(name, text,
                type)
            {
                ComboValues = values;
            }
        }


    }


}
