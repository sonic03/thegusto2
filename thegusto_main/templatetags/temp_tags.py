from django import template
import os

register = template.Library()

@register.filter
def url_to_name(pdf_url):
    name = pdf_url.split('.pdf')[0]
    name = name.replace('_',' ').replace('.','')
    return name