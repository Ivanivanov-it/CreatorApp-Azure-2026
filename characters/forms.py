from django import forms

from characters.models import Character
from common.models import Role
from common.choices import CharacterType



class CharacterForm(forms.ModelForm):
    attack = forms.IntegerField(min_value=1,max_value=100,error_messages={
        "required": "Please enter a number  between 1 and 100"
    })

    defense = forms.IntegerField(min_value=1, max_value=100,error_messages={
        "required": "Please enter a number  between 1 and 100"
    })
    hp = forms.IntegerField(min_value=1, max_value=100,error_messages={
        "required": "Please enter a number  between 1 and 100"
    })


    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        error_messages={
            "required": "Please select one or more roles"
        }
    )
    type = forms.ChoiceField(
        choices=CharacterType.choices,
        widget=forms.RadioSelect,
        error_messages={
            "required": "Selecting character type is required"
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        attack = cleaned_data.get("attack") or 1
        defense = cleaned_data.get("defense") or 1
        hp = cleaned_data.get("hp") or 1

        print(cleaned_data)

        name = cleaned_data.get("name","")
        title = cleaned_data.get("title","")


        if attack + defense + hp > 100:
            raise forms.ValidationError(
                "The total number of stats must not exceed 100"
            )

        if name and title and name == title:
            raise forms.ValidationError('Character name and title cannot be the same')


        return cleaned_data


    class Meta:
        model = Character
        labels = {
            'image_url': "Character Image URL"
        }
        help_texts = {
            'image_url': 'There will be default image if left empty',
        }
        error_messages = {
            "name": {
                'max_length': "The Character name is too long.",
                'required': "Please enter the name of your character."
            },
            "title": {
                'max_length': "The Character title is too long.",
                'required': "Please enter the title of your character."
            },
            "description": {
                'required': "Please enter a description of your character."
            }
        }
        fields = [
            "name",
            "title",
            "type",
            "attack",
            "defense",
            "hp",
            "roles",
            "description",
            "image_url",
        ]




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "name": "Character name (e.g. Gilgamesh)",
            "title": "Character title (e.g. King of Kings)",
            "description": "Describe your character...",
            "image_url": "https://example.com/character.png",
            "attack" : "Attack Points (1–100)",
            "defense": "Defense Points (1–100)",
            "hp": "Hit Points (1–100)",
        }

        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.RadioSelect)):
                field.widget.attrs["class"] = "form-control"

        for field,text in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs["placeholder"] = text



class CharacterCreateForm(CharacterForm):
    ...

class CharacterEditForm(CharacterForm):
    slug = forms.CharField(disabled=True)
    creator_display = forms.CharField(disabled=True,required=False,label="Creator")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['creator_display'].initial = self.instance.creator.username

    class Meta(CharacterForm.Meta):
        fields = [
            "name",
            "title",
            "type",
            "attack",
            "defense",
            "hp",
            "roles",
            "slug",
            "description",
            "image_url",
            "creator_display"
        ]



class CharacterDeleteForm(CharacterForm):
    ...

class CharacterSearchForm(forms.Form):
    query = forms.CharField(max_length=100,label='',required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))