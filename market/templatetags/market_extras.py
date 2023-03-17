from django import template

register = template.Library()


def mul(value, arg):
    return value * arg


def detail_filename(value):
    return f'{value}_detail.html'


register.filter('mul', mul)
register.filter('detail_filename', detail_filename)
