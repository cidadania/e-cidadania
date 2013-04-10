:mod:`apps.ecidadania.proposals` --- Proposals
==============================================

:mod:`proposals.admin` --- Administration
-----------------------------------------

.. automodule:: apps.ecidadania.proposals.admin

.. autoclass:: ProposalAdmin(admin.ModelAdmin)
    :members:

:mod:`proposals.models` --- Data models
---------------------------------------

.. automodule:: apps.ecidadania.proposals.models

.. autoclass:: BaseProposalAbstractModel(models.Model)
    :members:

.. autoclass:: Category(BaseClass)
    :members:

.. autoclass:: Proposal(models.Model)
    :members:

:mod:`proposals.forms` --- Forms
--------------------------------

.. automodule:: apps.ecidadania.proposals.forms

.. autoclass:: ProposalForm(ModelForm)
    :members:

:mod:`proposals.views` --- Views
--------------------------------

.. automodule:: apps.ecidadania.proposals.views.proposals

.. autoclass:: ListProposals(ListView)
    :members:
    
.. autoclass:: DeleteProposal(DeleteView)
    :members:
    
.. autoclass:: AddProposal(FormView)
    
.. autoclass:: EditProposal(UpdateView)

.. automodule:: apps.ecidadania.proposals.views.common

.. autoclass:: ViewProposal(DetailView)
    :members: