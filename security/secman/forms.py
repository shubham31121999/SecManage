from django import forms
from .models import CustomUser, MainProfile

class MainProfileForm(forms.ModelForm):
    class Meta:
        model = MainProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MainProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(user_type=2)