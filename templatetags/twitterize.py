# template tags file
import re
from django import template
register = template.Library()

@register.filter(name='twitterize')
def twitterize(token):
    return re.sub(r'\W(@(\w+))', r'<a href="https://twitter.com/\2" target="_blank">\1</a>', token)
twitterize.is_safe = True

# Use in your templates like this:
#<ul>
#  {% for t in tweets %}
#    <li>{{ t.text|urlize|twitterize }}</li>
#  {% endfor %}
#</ul>
