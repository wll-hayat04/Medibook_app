from django import template

register = template.Library()

# Exemple de filtre : convertir du texte en majuscules
@register.filter
def upper(value):
    return value.upper()
