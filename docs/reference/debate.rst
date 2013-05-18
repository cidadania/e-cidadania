:mod:`apps.ecidadania.debate` --- Debates
=========================================

:mod:`debate.admin` --- Administration
--------------------------------------

.. automodule:: apps.ecidadania.debate.admin

.. autoclass:: DebateAdmin(admin.ModelAdmin)
    :members:

.. autoclass:: NoteAdmin(admin.ModelAdmin)
    :members:
    
:mod:`debate.models` --- Data models
------------------------------------

.. automodule:: apps.ecidadania.debate.models

.. autoclass:: Debate(models.Model)
    :members:

.. autoclass:: Note(models.Model)
    :members:

:mod:`debate.forms` --- Forms
-----------------------------

.. automodule:: apps.ecidadania.debate.forms

.. autoclass:: DebateForm(ModelForm)
    :members:

.. autoclass:: NoteForm(ModelForm)
    :members:
    
:mod:`debate.views` --- Views
-----------------------------

.. automodule:: apps.ecidadania.debate.views

.. autofunction:: add_new_debate(request, space_name)

.. autofunction:: create_note(request, space_name)

.. autofunction:: update_note(request, space_name)

.. autofunction:: delete_note(request, space_name)

.. autoclass:: ViewDebate(DetailView)
    :members:

.. autoclass:: ListDebates(ListView)
    :members:
