from django import template

register = template.Library()


def mul(value, arg):
    return value * arg


register.filter('mul', mul)
