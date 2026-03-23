from django import template
register = template.Library()


@register.inclusion_tag('show_roles.html')
def show_roles(obj):
    return {'roles': obj.roles.all()}

@register.inclusion_tag('show_stats.html')
def show_stats(obj):

    return {'attack': obj.attack, 'defense': obj.defense, "hp": obj.hp}

@register.filter
def hp_percent(obj):

    hp = round((obj.current_hp / obj.max_hp) * 100, 1)

    return hp if hp > 0 else 0