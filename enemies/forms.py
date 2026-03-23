from django import forms

from common.models import Role
from enemies.models import Enemy
from common.choices import CharacterType

class EnemyForm(forms.ModelForm):
    attack = forms.IntegerField(min_value=1,max_value=250,error_messages={
        "required": "Please enter a number  between 1 and 250"
    })
    defense = forms.IntegerField(min_value=1, max_value=250,error_messages={
        "required": "Please enter a number  between 1 and 250"
    })
    hp = forms.IntegerField(min_value=1, max_value=250,error_messages={
        "required": "Please enter a number  between 1 and 250"
    })

    weakness = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        error_messages={
            "required": "Selecting 1 or more enemy weaknesses is required"
        }
    )

    type = forms.ChoiceField(
        choices=CharacterType.choices,
        widget=forms.RadioSelect,
        error_messages={
            "required": "Selecting enemy type is required"
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        attack = cleaned_data.get("attack") or 1
        defense = cleaned_data.get("defense") or 1
        hp = cleaned_data.get("hp") or 1


        name = cleaned_data.get("name","")
        title = cleaned_data.get("title","")


        if attack + defense + hp > 250:
            raise forms.ValidationError(
                "The total number of stats must not exceed 250"
            )

        if name and title and name == title:
            raise forms.ValidationError('Enemy name and title cannot be the same')


        return cleaned_data


    class Meta:
        model = Enemy
        labels = {
            'image_url': "Enemy Image URL"
        }
        help_texts = {
            'image_url': 'There will be default image if left empty',
            'weakness': 'Your enemy will receive more damage from these roles'
        }
        error_messages = {
            "name": {
                'max_length': "The Enemy name is too long.",
                'required': "Please enter the name of your enemy."
            },
            "title": {
                'max_length': "The Enemy title is too long.",
                'required': "Please enter the title of your enemy."
            },
            "description": {
                'required': "Please enter a description of your enemy."
            }
        }
        fields = [
            "name",
            "title",
            "type",
            "attack",
            "defense",
            "hp",
            "weakness",
            "description",
            "image_url",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "name": "Enemy name (e.g. Thaemine)",
            "title": "Enemy title (e.g. Conqueror of Stars)",
            "description": "Describe your Enemy...",
            "image_url": "https://example.com/partner.png",
            "attack": "Attack Points (1–250)",
            "defense": "Defense Points (1–250)",
            "hp": "Hit Points (1–250)",
        }


        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.RadioSelect)):
                field.widget.attrs["class"] = "form-control"

        for field,text in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs["placeholder"] = text


class EnemyCreateForm(EnemyForm):
    ...

class EnemyEditForm(EnemyForm):
    slug = forms.CharField(disabled=True)
    creator_display = forms.CharField(disabled=True, required=False, label="Creator")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['creator_display'].initial = self.instance.creator.username

    class Meta(EnemyForm.Meta):
        fields = [
            "name",
            "title",
            "type",
            "attack",
            "defense",
            "hp",
            "weakness",
            "slug",
            "description",
            "image_url",
            "creator_display"
        ]

class EnemyDeleteForm(EnemyForm):
    ...

class EnemySearchForm(forms.Form):
    query = forms.CharField(max_length=100,label='',required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))