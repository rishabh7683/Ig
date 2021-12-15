from django import template

register = template.Library()


@register.filter(name='gvspace')
def gvspace(num):
    snum=num.replace(',',', ')
    return snum
