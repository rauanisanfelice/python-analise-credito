from django import forms

class AnaliseForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    
    renda = forms.DecimalField(label='Qual é sua renda anual?',  max_digits=10, decimal_places=2, help_text="Informe sua renda anual.")
    idade = forms.IntegerField(label='Idade', max_value=100, min_value=1, help_text="Informe sua idade")
    emprestimo = forms.DecimalField(label='Você possui emprestimos? Quanto?', max_digits=10, decimal_places=2, required=False, help_text="Informe o valor de seu emprestimos caso possuir.")