# template tags file
import re
from django import template
register = template.Library()

@register.filter(name='twittertag')
def twittertag(token):
    return re.sub(r'\W(#(\w+))', r'<a href="https://twitter.com/#!/search/realtime/\2" target="_blank">\1</a>', token)    
twittertag.is_safe = True

# Use in your templates like this:
#<ul>
#  {% for t in tweets %}
#    <li>{{ t.text|urlize|twittertag }}</li>
#  {% endfor %}
#</ul>
