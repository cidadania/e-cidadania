:mod:`core.spaces` --- Spaces/Processes
=======================================

:mod:`spaces.admin` --- Administration
--------------------------------------

.. automodule:: core.spaces.admin

.. autoclass:: EntityAdmin(admin.ModelAdmin)
    :members:

.. autoclass:: EntityInline(admin.TabularInline)
    :members:

.. autoclass:: SpaceAdmin(admin.ModelAdmin)
    :members:
    
.. autoclass:: DocumentAdmin(admin.ModelAdmin)
    :members:
    
.. autoclass:: EventAdmin(admin.ModelAdmin)
    :members:

:mod:`spaces.models` --- Data models
------------------------------------

.. automodule:: core.spaces.models

.. autoclass:: Space(models.Model)
    :members:

.. autoclass:: Entity(models.Model)
    :members:

.. autoclass:: Document(models.Model)
    :members:

.. autoclass:: Event(models.Model)
    :members:
    
:mod:`spaces.forms` --- Forms
-----------------------------

.. automodule:: core.spaces.forms

.. autoclass:: SpaceForm(ModelForm)
    :members:

.. autoclass:: DocForm(ModelForm)
    :members:
    
.. autoclass:: EventForm(ModelForm)
    :members:

:mod:`EntityFormSet` --- modelformset_factory

:mod:`spaces.views` --- Views
-----------------------------
 
General space views
...................

.. automodule:: core.spaces.views.intent

.. autoclass:: ValidateIntent(DetailView)
    :members:

.. autofunction:: add_intent(request, space_url)

.. automodule:: core.spaces.views.rss

.. autoclass:: SpaceFeed(HTTPAuthFeed)
    :members:

News views
..........

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
............

.. automodule:: core.spaces.views.spaces    

.. autoclass:: ListSpaces(ListView)
    :members:

.. autoclass:: ViewSpaceIndex(DetailView)
    :members:
    
.. autoclass:: DeleteSpace(DeleteView)
    :members:

.. autoclass:: EditRole(UpdateView)
    :members:

.. autofunction:: edit_space(request, space_name)

.. autofunction:: create_space(request)

Document views
..............

.. automodule:: core.spaces.views.documents    

.. autoclass:: AddDocument(FormView)

.. autoclass:: EditDocument(UpdateView)

.. autoclass:: DeleteDocument(DeleteView)
    :members:

.. autoclass:: ListDocs(ListView)
    :members:

Event views
...........

.. automodule:: core.spaces.views.events
    
.. autoclass:: AddEvent(FormView)

.. autoclass:: EditEvent(UpdateView)

.. autoclass:: DeleteEvent(DeleteView)
    :members:

.. autoclass:: ViewEvent(DetailView)
    :members:

.. autoclass:: ListEvents(ListView)
    :members:

