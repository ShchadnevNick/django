from django import template
from women import views

register = template.Library()

@register.inclusion_tag('women/list_categories.html')
def get_categories(cat_selected=0):
    cats = views.cats_db
    return {'cats': cats, 'cat_selected':cat_selected}
