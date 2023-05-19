from django import template
 
register = template.Library() # если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются :(

@register.filter(name='censor')
def multiply(value):
    if 'fuck' in str(value) or 'ass' in str(value) or 'fool' in str(value):
        return '****'
    else:
        return str(value)
































