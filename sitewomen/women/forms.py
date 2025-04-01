from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Husband, Women


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'is_published', 'cat', 'husband', 'tags']
        widget = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols':60, 'rows':10}),
        }
        labels = {'slug': 'URL'}

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем", label="Муж")

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title


