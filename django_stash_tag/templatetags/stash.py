import re
from django import template

register = template.Library()
template.base.tag_re = re.compile(template.base.tag_re.pattern, re.DOTALL)


'''
Usage:
------

    {% stash 'contact_link' %}
      <a href='/v2/contacts/{{ contact_id }}'>{{ contact_name }}</a>
    {% endstash %}

    {% stash_apply 'contact_link'
        contact_name='Ian Jabour'
        contact_id=1
        orgrole=user.orgtype
    %}

    {% stash_apply 'contact_link'
        contact_name='Joe Schmoe'
        contact_id=2
        orgrole=user.orgtype
    %}


    {% stash 'header' %}
      <header>SimpleLegal</header>
    {% endstash %}

    {% stash_apply 'header' %}
'''


@register.tag
def stash(parser, token):
    nodelist = parser.parse(('endstash',))
    parser.delete_first_token()
    stash_name = with_prefix(token.split_contents()[1])

    return StashSetNode(stash_name, nodelist)


class StashSetNode(template.Node):
    def __init__(self, stash_name, nodelist):
        self.stash_name = stash_name
        self.nodelist = nodelist

    def render(self, context):
        context.push({self.stash_name: self.nodelist})
        return ''


@register.tag
def stash_apply(parser, token):
    token_contents = token.split_contents()
    stash_name = with_prefix(token.split_contents()[1])

    kwargs = {}

    if len(token_contents) > 2:
        raw_kwargs = [raw_kwarg.split('=')
                      for raw_kwarg in token_contents[2:]]

        kwargs = {raw_kwarg[0]: raw_kwarg[1] for raw_kwarg in raw_kwargs}

    return StashGetNode(stash_name, **kwargs)


class StashGetNode(template.Node):
    def __init__(self, stash_name, **kwargs):
        self.stash_name = stash_name
        self.kwargs = kwargs

    def render(self, context):
        nodelist = context.get(self.stash_name)
        with_vars = {
            key: template.base.Variable(value).resolve(context)
            for key, value in self.kwargs.items()
        }
        context.push(with_vars)
        return nodelist.render(context)


def with_prefix(stash_name):
    return '_stash__{0}'.format(stash_name)
