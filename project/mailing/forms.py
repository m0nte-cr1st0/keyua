from django import forms

from .models import ContactForm


class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactFormForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['onchange'] = "uploadFile()"
        self.fields['text'].widget.attrs['onkeyup'] = "textAreaAdjust(this)"
        self.fields['nda'].widget.attrs['id'] = 'checkbox1'