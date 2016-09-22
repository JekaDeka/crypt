from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # exclude = ['author', 'updated', 'created', ]
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={'required': True, 'rows': 5, 'cols': 4,
                       'placeholder': 'Введите ваше сообщение'}
            ),
        }
