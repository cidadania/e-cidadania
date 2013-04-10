# Obtained from: http://www.djangosnippets.org/snippets/133/
# Author: http://www.djangosnippets.org/users/SmileyChris/

from django.template import loader, Context, RequestContext, TemplateSyntaxError
from django.http import HttpResponse


def render_response(template_prefix=None, always_use_requestcontext=True):
    """
    Create a decorator which can be used as a shortcut to render templates to
    an HttpResponse.

    The decorated function must return either:
     * an HttpResponse object,
     * a string containing the template name (if doesn't start with '/' then
       will be combined with the template_prefix) or
     * a tuple comprising of:
         * a string or tuple containing the template name(s),
         * a dictionary to add to the Context or RequestContext and
         * (optionally) a list of context processors (if given, forces use of
           RequestContext).

    Example usage (in a views module)::

        from projectname.renderer import render_response
        render_response = render_response('app_name/')     # Template dir.

        @render_response
        app_view(request):
            ...
            return 'app_view_template.htm', dict(object=object)
"""
    def renderer(func):
        def _dec(request, *args, **kwargs):
            response = func(request, *args, **kwargs)

            if isinstance(response, HttpResponse):
                return response
            elif isinstance(response, basestring):
                template_name = response
                namespace = {}
                context_processors = None
            elif isinstance(response, (tuple, list)):
                len_tuple = len(response)
                if len_tuple == 2:
                    template_name, namespace = response
                    context_processors = None
                elif len_tuple == 3:
                    template_name, namespace, context_processors = response
                else:
                    raise TemplateSyntaxError('%s.%s function did not return a parsable tuple' % (func.__module__, func.__name__))
            else:
                raise TemplateSyntaxError('%s.%s function did not provide a template name or HttpResponse object' % (func.__module__, func.__name__))

            if always_use_requestcontext or context_processors is not None:
                context = RequestContext(request, namespace, context_processors)
            else:
                context = Context(namespace)

            if template_prefix:
                if isinstance(template_name, (list, tuple)):
                    template_name = map(correct_path, template_name)
                else:
                    template_name = correct_path(template_name)

            return HttpResponse(loader.render_to_string(template_name, context_instance=context))

        return _dec

    def correct_path(template_name):
        if template_name.startswith('/'):
            return template_name[1:]
        return '%s%s' % (template_prefix, template_name)

    return renderer
