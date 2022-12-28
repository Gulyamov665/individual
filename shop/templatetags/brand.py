from django import template
from shop.models import Brand

register = template.Library()


@register.inclusion_tag('brands.html')
def brands():
    brands_list = Brand.objects.all()
    return {'brands': brands_list}
