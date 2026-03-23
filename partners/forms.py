from django import forms

from partners.models import Partner
from common.models import Role


class PartnerForm(forms.ModelForm):
    attack = forms.IntegerField(min_value=1, max_value=40, error_messages={
        "required": "Please enter a number between 1 and 40"
    })
    defense = forms.IntegerField(min_value=1, max_value=40, error_messages={
        "required": "Please enter a number  between 1 and 40"
    })
    hp = forms.IntegerField(min_value=1, max_value=40, error_messages={
        "required": "Please enter a number  between 1 and 40"
    })

    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        error_messages={
            "required": "Please select one or more roles"
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        attack = cleaned_data.get("attack") or 1
        defense = cleaned_data.get("defense") or 1
        hp = cleaned_data.get("hp") or 1

        name = cleaned_data.get("name", "")
        title = cleaned_data.get("title", "")

        if attack + defense + hp > 40:
            raise forms.ValidationError(
                "The total number of stats must not exceed 40"
            )

        if name and title and name == title:
            raise forms.ValidationError('Partner name and title cannot be the same')


        return cleaned_data

    class Meta:
        model = Partner
        labels = {
            'character': "Select an existing character",
            'image_url': "Partner Image URL"
        }
        help_texts = {
            'image_url': "There will be default image if left empty",
            'character': "Character to receive support from this partner"
        }
        error_messages = {
            "name": {
                'max_length': "The Partner name is too long.",
                'required': "Please enter the name of your partner."
            },
            "title": {
                'max_length': "The Partner title is too long.",
                'required': "Please enter the title of your partner."
            },
            "description": {
                'required': "Please enter a description of your partner."
            },
            "character": {
                'required': "Please select a character."
            }
        }
        fields = [
            "name",
            "title",
            "attack",
            "defense",
            "hp",
            "roles",
            "description",
            "image_url",
            "character"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "name": "Partner name (e.g. Steward)",
            "title": "Partner title (e.g. The Rat)",
            "description": "Describe your Partner...",
            "image_url": "https://example.com/partner.png",
            "attack": "Attack Points (1–40)",
            "defense": "Defense Points (1–40)",
            "hp": "Hit Points (1–40)",
        }


        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.RadioSelect)):
                field.widget.attrs["class"] = "form-control"

        for field,text in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs["placeholder"] = text

class PartnerCreateForm(PartnerForm):
    ...


class PartnerEditForm(PartnerForm):
    slug = forms.CharField(disabled=True)
    creator_display = forms.CharField(disabled=True, required=False, label="Creator")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['creator_display'].initial = self.instance.creator.username

    class Meta(PartnerForm.Meta):
        fields = [
            "name",
            "title",
            "attack",
            "defense",
            "hp",
            "roles",
            "slug",
            "description",
            "image_url",
            "character",
            "creator_display"
        ]

class PartnerSearchForm(forms.Form):
    query = forms.CharField(max_length=100,label='',required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))