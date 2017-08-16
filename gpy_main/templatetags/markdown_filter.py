# Credit @ Jonathan Evan: http://www.jw.pe/blog/post/using-markdown-django-17/
from django import template
import markdown

register = template.Library()


@register.filter
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text, safe_mode='escape')
