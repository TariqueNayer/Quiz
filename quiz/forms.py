from django import forms

class CategoryQuizForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)

        for question in questions:
            field_name = f"question_{question.id}"

            # MCQ question
            if all([
                question.option_a,
                question.option_b,
                question.option_c,
                question.option_d,
            ]):
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text,
                    widget=forms.RadioSelect,
                    choices=[
                        ("a", question.option_a),
                        ("b", question.option_b),
                        ("c", question.option_c),
                        ("d", question.option_d),
                    ],
                )

            # Text-based question
            else:
                self.fields[field_name] = forms.CharField(
                    label=question.text,
                    widget=forms.Textarea(attrs={"rows": 3}),
                    required=False,
                )