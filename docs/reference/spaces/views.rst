:mod:`spaces.views` --- Views
=============================
 
Intent views
------------

.. automodule:: core.spaces.views.intent

.. autoclass:: ValidateIntent(DetailView)
    :members:

.. autofunction:: add_intent(request, space_url)


RSS views
---------
.. automodule:: core.spaces.views.rss

.. autoclass:: SpaceFeed(HTTPAuthFeed)
    :members:

News views
----------

.. automodule:: core.spaces.views.news    

.. autoclass:: ListPosts(ListView)
    :members:

.. autoclass:: RedirectArchive(RedirectView)
    :members:

.. autoclass:: YearlyPosts(YearArchiveView)
    :members:

.. autoclass:: MonthlyPosts(MonthArchiveView)
    :members:

Spaces views
------------
.. automodule:: core.spaces.views.spaces    

.. autoclass:: ListSpaces(ListView)
    :members:

.. autoclass:: ViewSpaceIndex(DetailView)
    :members:
    
.. autoclass:: DeleteSpace(DeleteView)
    :members:

.. autofunction:: edit_space(request, space_name)

.. autofunction:: create_space(request)

.. autofunction:: edit_roles(request, space_url)

.. autofunction:: search_user(request, space_url)

Document views
--------------

.. automodule:: core.spaces.views.documents    

.. autoclass:: AddDocument(FormView)

.. autoclass:: EditDocument(UpdateView)

.. autoclass:: DeleteDocument(DeleteView)
    :members:

.. autoclass:: ListDocs(ListView)
    :members:

Event views
-----------

.. automodule:: core.spaces.views.events
    
.. autoclass:: AddEvent(FormView)

.. autoclass:: EditEvent(UpdateView)

.. autoclass:: DeleteEvent(DeleteView)
    :members:

.. autoclass:: ViewEvent(DetailView)
    :members:

.. autoclass:: ListEvents(ListView)
    :members:

