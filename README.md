# Django Stash Tag

A Django template tag that allows for markup to be stashed and
dynamically applied *without* needing to create a separate partial or
template tag file.

## Installation

Install Django Stash Tag:

```
pip install django-stash-tag
```

After you've installed the tag, add `django_stash_tag` to
`INSTALLED_APPS` in your `settings.py` file:

```
# settings.py

INSTALLED_APPS = (
    # …
    'django_stash_tag',
)
```

## Static Usage

The `stash` tag can be used to store static markup for reuse further
down the template. Using `stash_apply` you can render the stashed
markup.

First we load the tag and stash the markup with a name to stash it
under:

```
{% load stash %}

{% stash 'static_heading' %}
  <h1>User: {{user.name}}</h1>
{% endstash %}
```

We then apply the stash with `stash_apply` and provide the stash name
`static_heading` as a tag argument:

```
{% stash_apply 'static_heading' %}
```

This would result in rendering (`context.user` is `{'name': 'Ivan'}`):

```
<h1>User: Ivan</h1>
```

## Dynamic Usage

In most cases you probably need more dynamic control over the
paramaterization of the stashed markup. You can accomplish such
behavior through the use of template tag kwargs.

Again we load the tag and stash the markup. This time the context
variables that are referenced within the stashed content are not
defined in the template's context:

```
{% load stash %}

{% stash 'section_header' %}
  <header>
    <h3>{{title}} {{company}}</h2>
    <small>{{subtext}} {{company}}.</small>
  </header>
{% endstash %}
```

We then apply the stash with additional template kwargs pertaining to
the context variables referenced in the stashed content
(`context.company` set to `{'name': 'GitHub'}`):

```
{% stash_apply 'section_header'
    title='About'
    subtext='We will take you back to when it all began at'
%}

{# further down in the template #}

{% stash_apply 'section_header'
    title='Apply for a Position at'
    subtext='Make software development a better experience at'
%}
```

Which would then output:

```
<header>
  <h3>About GitHub</h2>
  <small>We will take you back to when it all began at GitHub.</small>
</header>

<!-- further down in template --> 

<header>
  <h3>Apply for a Position at GitHub</h2>
  <small>Make software development a better experience at GitHub.</small>
</header>
```

As demonstrted above you can use `stash_apply` as much as you
want once you've stashed the content in your template. You can use both
context variables already set on the template or dynamic variables set
though kwargs.
