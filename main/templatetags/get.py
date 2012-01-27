from django import template

register = template.Library()

def getitem(d, key):
    return d.get(key, '')
register.filter(getitem)
