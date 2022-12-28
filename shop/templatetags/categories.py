from django import template

from shop.models import Category

register = template.Library()


@register.inclusion_tag('categories.html')
def categories():
    categories_list = Category.objects.all()
    return {'categories': categories_list}
