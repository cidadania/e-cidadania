Style guide
===========

The style guide establish a series of rules to follow when coding in e-cidadania.
These rules are unbreakable. The style guide follows closely the `PEP8`_ document,
with some exceptions provided from the internal style guide at `Pocoo`_.

.. _PEP8: http://www.python.org/dev/peps/pep-0008
.. _Pocoo: http://www.pocoo.org//internal/styleguide/

Python
------

**Imports**
    Every import must be situated in the file header, below to the comment header.
    The python imports must precede any others, and the external librearies or
    third party modules must precede the application ones.

    *Example*::

        import os
        import sys

        from extlib import function

        from myapp.module import function

**Line width (columns)**
    The code must be between 80 and 120 columns, but we encourage that
    developers set them an 80 columns limit when possible.

**Long declarations**
    If a code line does not fit in 80 columns, try to reduce it declaring variables
    previously. If it still can not fit, you can divide the lines this way:

    *Parentheses*::

        website = models.URLField(_('Website'), verify_exists=True,
                                  max_length=200, null=True, blank=True,
                                  help_text=_('The URL will be checked'))

    *Declararations*::

        this_is_a_very_long(function_call, 'with many parameters') \
            .that_returns_an_object_with_an_attribute

        MyModel.query.filter(MyModel.scalar > 120) \
                     .order_by(MyModel.name.desc()) \
                     .limit(10)

    *Lists, tuples and dictionariess*::

        items = [
            'this is the first', 'set of items', 'with more items',
            'to come in this line', 'like this'
        ]

        dict = {
            ('mobile': phone),
            ('car': key),
            ('another': thing),
        }

**Indentation**
    Indentation must be *always* 4 spaces per level, no exceptions. You can not
    use tabs for indenting.

**Blank lines**
    Every classes and method must be separated by two blank lines. The code
    inside a class or method by one blank line.

    *Example*::

        class ListDocs(ListView):
            ----blank line----
            """
            List all documents stored whithin a space.
            """
            paginate_by = 25
            context_object_name = 'document_list'
            ----blank line----
            def get_queryset(self):
                place = get_object_or_404(Space, url=self.kwargs['space_name'])
                objects = Document.objects.all().filter(space=place.id).order_by('pub_date')
                return objects
            ----blank line----
            def get_context_data(self, **kwargs):
                context = super(ListDocs, self).get_context_data(**kwargs)
                context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
                return context
        ----blank line----
        ----blank line----
        def whatever(args):
            ----blank line----
            """
            A comment.
            """
            this_is_something = 0


HTML
----

**Columns**
    HTML code does not have a column limit, but it must be indented in a way we
    can locate easily every element inside the document. The indentation preceeds
    rendered results in application.

**Indentation**
    The X/HTML code must be indented with four spaces like python code, no exceptions.

    .. note:: There may be some old code that follows the old indentation
              rule (2 spaces per level). If you see it we would be glad to
              receive a path to solve it.

CSS
---

**Indentation**
    Indentation will be 4 spaces, always, like Python code.

    *Example*::

        body {
            background: #FAFAFA;
	          padding: 0;
	          margin: 0;
	          font-family: Verdana, "Lucida Sans", Arial;
	          font-size: 1em;
	          color: #000;
	          cursor: default;
        }

**Colors**
    Colors must be always written in hexadecimal. You are allowed to use three digits
    abbreviations.

**Font size**
    Font size must be declared in **em's** except for presentation requirement.


JavaScript
----------

The JavaScript code follows the same rules from the python code.
