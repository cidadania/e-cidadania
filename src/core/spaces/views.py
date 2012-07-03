# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2012 Cidadania S. Coop. Galega
#
# This file is part of e-cidadania.
#
# e-cidadania is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# e-cidadania is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with e-cidadania. If not, see <http://www.gnu.org/licenses/>.

"""
These are the views that control the spaces, meetings and documents.
"""

import datetime
import itertools
import hashlib

# Generic class-based views
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView

# Decorators. the first is a wrapper to convert function-based decorators
# to method decorators that can be put in subclass methods.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

# Response types
from django.shortcuts import render_to_response, get_object_or_404, redirect

# Some extras
from django.contrib import messages
from django.template import RequestContext
from django.contrib.syndication.views import Feed
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

# e-cidadania data models
from core.spaces.models import Space, Entity, Document, Event, Intent
from apps.ecidadania.news.models import Post
from core.spaces.forms import SpaceForm, DocForm, EventForm, EntityFormSet, \
    RoleForm
from apps.ecidadania.proposals.models import Proposal, ProposalSet
from apps.ecidadania.staticpages.models import StaticPage
from apps.ecidadania.debate.models import Debate

#
# RSS FEED
#

class SpaceFeed(Feed):

    """
    Returns a space feed with the content of various applications. In the future
    this function must detect applications and returns their own feeds.
    """

    def get_object(self, request, space_url):
        current_space = get_object_or_404(Space, url=space_url)
        return current_space

    def title(self, obj):
        return _("%s feed") % obj.name

    def link(self, obj):
        return obj.get_absolute_url()
    
    def description(self, obj):
        return _("All the recent activity in %s ") % obj.name

    def items(self, obj):
        results = itertools.chain(
            Post.objects.all().filter(space=obj).order_by('-pub_date')[:10],
            Proposal.objects.all().filter(space=obj).order_by('-pub_date')[:10],
            Event.objects.all().filter(space=obj).order_by('-pub_date')[:10],
        ) 
        
        return sorted(results, key=lambda x: x.pub_date, reverse=True)

#
# INTENT VIEWS
#

@login_required
def add_intent(request, space_url):
     """
     Returns a page where the logged in user can click on a "I want to
     participate" button, which after sends an email to the administrator of
     the space with a link to approve the user to use the space.
     
     :attributes:  space, intent, token
     :rtype: Multiple entity objects.
     :context: space_url, heading
     """
     space = get_object_or_404(Space, url=space_url)
     try:
         intent = Intent.objects.get(user=request.user, space=space)
         heading = _("Access has been already authorized")
     except Intent.DoesNotExist:
         token = hashlib.md5("%s%s%s" % (request.user, space,
                             datetime.datetime.now())).hexdigest()
         intent = Intent(user=request.user, space=space, token=token)
         intent.save()
         subject = _("New participation request")
         body = _("User {0} wants to participate in space {1}.\n \
                  Please click on the link below to approve.\n {2}"\
                  .format(request.user.username, space.name, intent.get_approve_url()))
         heading = _("Your request is being processed.")
         send_mail(subject=subject, message=body,
                   from_email="noreply@ecidadania.org",
                   recipient_list=[space.author.email])


     return render_to_response('space_intent.html', \
             {'space_name': space.name, 'heading': heading}, \
                               context_instance=RequestContext(request))


class ValidateIntent(DetailView):

    """
    Validate the user petition to join a space. This will add the user to the
    users list in the space, allowing him participation. This function checks if
    the user visiting the token url is admin of the space. If he or she is an
    admin proceeds with the validation.

    .. versionadded: 0.1.5
    """
    context_object_name = 'get_place'
    template_name = 'spaces/validate_intent.html'
    status = _("The requested intent does not exist!")

    def get_object(self):
        space_object = get_object_or_404(Space, url=self.kwargs['space_url'])

        if self.request.user in space_object.admins.all() \
        or self.request.user in space_object.mods.all() \
        or self.request.user.is_staff or self.request.user.is_superuser:
            try:
                intent = Intent.objects.get(token=self.kwargs['token'])
                intent.space.users.add(intent.user)
                self.status = _("The user has been authorized to participate \
                in space \"%s\"." % space_object.name)
                messages.success(self.request, _("Authorization successful"))

            except Intent.DoesNotExist:
                self.status  = _("The requested intent does not exist!")

            return space_object

    def get_context_data(self, **kwargs):
        context = super(ValidateIntent, self).get_context_data(**kwargs)
        context['status'] = self.status
        context['request_user'] = Intent.objects.get(token=self.kwargs['token']).user
        return context


# SPACE VIEWS
#

# Please take in mind that the create_space view can't be replaced by a CBV
# (class-based view) since it manipulates two forms at the same time. Apparently
# that creates some trouble in the django API. See this ticket:
# https://code.djangoproject.com/ticket/16256
@permission_required('spaces.add_space')
def create_space(request):

    """
    Returns a SpaceForm form to fill with data to create a new space. There
    is an attached EntityFormset to save the entities related to the space. Only
    site administrators are allowed to create spaces.
    
    :attributes: - space_form: empty SpaceForm instance
                 - entity_forms: empty EntityFormSet
    :rtype: Space object, multiple entity objects.
    :context: form, entityformset
    """
    space_form = SpaceForm(request.POST or None, request.FILES or None)
    entity_forms = EntityFormSet(request.POST or None, request.FILES or None,
                                 queryset=Entity.objects.none())
    
    if request.method == 'POST':
        if space_form.is_valid() and entity_forms.is_valid():
            space_form_uncommited = space_form.save(commit=False)
            space_form_uncommited.author = request.user
                
            new_space = space_form_uncommited.save()
            space = get_object_or_404(Space, name=space_form_uncommited.name)

            ef_uncommited = entity_forms.save(commit=False)
            for ef in ef_uncommited:
                ef.space = space
                ef.save()
            # We add the created spaces to the user allowed spaces
    
            space.admins.add(request.user)
            #messages.success(request, _('Space %s created successfully.') % space.name)
            return redirect('/spaces/' + space.url)
    
    return render_to_response('spaces/space_form.html',
                              {'form': space_form,
                               'entityformset': entity_forms},
                              context_instance=RequestContext(request))
#    else:
#        return render_to_response('not_allowed.html',
#                                  context_instance=RequestContext(request))
                                  

class ViewSpaceIndex(DetailView):

    """
    Returns the index page for a space. The access to spaces is restricted and
    filtered in the get_object method. This view gathers information from all
    the configured modules in the space.
    
    :attributes: space_object, place
    :rtype: Object
    :context: get_place, entities, documents, proposals, publication
    """
    context_object_name = 'get_place'
    template_name = 'spaces/space_index.html'
    
    def get_object(self):
        space_url = self.kwargs['space_url']
        space_object = get_object_or_404(Space, url=space_url)

        
        if space_object.public == True or self.request.user.is_staff or \
        self.request.user.is_superuser:
            if self.request.user.is_anonymous():
                messages.info(self.request, _("Hello anonymous user. Remember \
                                              that this space is public to view, but \
                                              you must <a href=\"/accounts/register\">register</a> \
                                              or <a href=\"/accounts/login\">login</a> to participate."))
            return space_object

        if self.request.user.is_anonymous():
            messages.info(self.request, _("You're an anonymous user. \
                          You must <a href=\"/accounts/register\">register</a> \
                          or <a href=\"/accounts/login\">login</a> to access here."))
            self.template_name = 'not_allowed.html'
            return space_object

        # Check if the user is in the admitted users of the space
        for u in space_object.users.all():
            if self.request.user == u:
                return space_object

        # Check if the user is an admin
        for u in space_object.admins.all():
            if self.request.user == u:
                return space_object

        # Check if the user is a moderator
        for u in space_object.mods.all():
            if self.request.user == u:
                return space_object

        messages.warning(self.request, _("You're not registered to this space."))
        self.template_name = 'not_allowed.html'
        return space_object

    # Get extra context data
    def get_context_data(self, **kwargs):
        context = super(ViewSpaceIndex, self).get_context_data(**kwargs)
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['entities'] = Entity.objects.filter(space=place.id)
        context['documents'] = Document.objects.filter(space=place.id)
        context['proposalsets'] = ProposalSet.objects.filter(space=place.id)
        context['proposals'] = Proposal.objects.filter(space=place.id).order_by('-pub_date')
        context['publication'] = Post.objects.filter(space=place.id).order_by('-pub_date')[:10]
        context['page'] = StaticPage.objects.filter(show_footer=True).order_by('-order')
        context['messages'] = messages.get_messages(self.request)
        context['debates'] = Debate.objects.filter(space=place.id).order_by('-date')
        context['event'] = Event.objects.filter(space=place.id).order_by('-event_date')
        return context
        

# Please take in mind that the change_space view can't be replaced by a CBV
# (class-based view) since it manipulates two forms at the same time. Apparently
# that creates some trouble in the django API. See this ticket:
# https://code.djangoproject.com/ticket/16256
@permission_required('spaces.change_space')
def edit_space(request, space_url):

    """
    Returns a form filled with the current space data to edit. Access to
    this view is restricted only to site and space administrators. The filter
    for space administrators is given by the change_space permission and their
    belonging to that space.
    
    :attributes: - place: current space intance.
                 - form: SpaceForm instance.
                 - form_uncommited: form instance before commiting to the DB,
                   so we can modify the data.
    :param space_url: Space URL
    :rtype: HTML Form
    :context: form, get_place
    """
    place = get_object_or_404(Space, url=space_url)

    if request.user in place.admins.all():
        form = SpaceForm(request.POST or None, request.FILES or None, instance=place)
        entity_forms = EntityFormSet(request.POST or None, request.FILES or None,
                                 queryset=Entity.objects.all().filter(space=place))

        if request.method == 'POST':
            if form.is_valid() and entity_forms.is_valid():
                form_uncommited = form.save(commit=False)
                form_uncommited.author = request.user
            
                new_space = form_uncommited.save()
                space = get_object_or_404(Space, name=form_uncommited.name)
            
                ef_uncommited = entity_forms.save(commit=False)
                for ef in ef_uncommited:
                    ef.space = space
                    ef.save()
            
                messages.success(request, _('Space edited successfully'))
                return redirect('/spaces/' + space.url + '/')

        return render_to_response('spaces/space_form.html', {'form': form,
                    'get_place': place, 'entityformset': entity_forms},
                    context_instance=RequestContext(request))
            
    return render_to_response('not_allowed.html', context_instance=RequestContext(request))


class DeleteSpace(DeleteView):

    """
    Returns a confirmation page before deleting the space object completely.
    This does not delete the space related content. Only the site administrators
    can delete a space.
    
    :rtype: Confirmation
    """
    context_object_name = 'get_place'
    success_url = '/'

    @method_decorator(permission_required('spaces.delete_space'))
    def dispatch(self, *args, **kwargs):
        return super(DeleteSpace, self).dispatch(*args, **kwargs)

    def get_object(self):
        space = get_object_or_404(Space, url = self.kwargs['space_url'])
        if self.request.user in space.admins.all():
            return space
        else:
            self.template_name = 'not_allowed.html'
            return space
      

class GoToSpace(RedirectView):

    """
    Sends the user to the selected space. This view only accepts GET petitions.
    GoToSpace is a django generic :class:`RedirectView`.
    
    :Attributes: **self.place** - Selected space object
    :rtype: Redirect
    """
    def get_redirect_url(self, **kwargs):
        self.place = get_object_or_404(Space, name = self.request.GET['spaces'])
        return '/spaces/%s' % self.place.url


class ListSpaces(ListView):

    """
    Return a list of spaces in the system (except private ones) using a generic view.
    The users associated to a private spaces will see it, but not the other private
    spaces. ListSpaces is a django generic :class:`ListView`.
    
    :rtype: Object list
    :contexts: object_list
    """
    paginate_by = 10
    
    def get_queryset(self):
        current_user = self.request.user
        public_spaces = Space.objects.all().filter(public=True)
        all_spaces = Space.objects.all()
        
        if not current_user.is_anonymous():
            user_spaces = []
            for space in all_spaces:
                if current_user in space.users.all() \
                    or current_user in space.admins.all() \
                    or current_user in space.mods.all():
                    user_spaces.append(space)
                    public_spaces._result_cache(space)

            return public_spaces
            
        return public_spaces


class EditRole(UpdateView):

    """
    This view allows the administrator to edit the roles for every user in the
    platform.

    .. versionadded: 0.1.5
    """

    form_class = RoleForm
    model = Space
    template_name = 'spaces/user_groups.html'

    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return '/spaces/' + self.space.name

    def get_object(self):
        cur_space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return cur_space

    def get_context_data(self, **kwargs):
        context = super(EditRole, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

    @method_decorator(permission_required('spaces.change_space'))
    def dispatch(self, *args, **kwargs):
        return super(EditRole, self).dispatch(*args, **kwargs)


#
# DOCUMENTS VIEWS
#

class AddDocument(FormView):

    """
    Upload a new document and attach it to the current space.
    
    :rtype: Object
    :context: form, get_place
    """
    form_class = DocForm
    template_name = 'spaces/document_form.html'
    
    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return '/spaces/' + self.space.url

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        form_uncommited = form.save(commit=False)
        form_uncommited.space = self.space
        form_uncommited.author = self.request.user
        form_uncommited.save()
        #print form.cleaned_data
        return super(AddDocument, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(AddDocument, self).get_context_data(**kwargs)
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = self.space
        return context
        
    @method_decorator(permission_required('spaces.add_document'))
    def dispatch(self, *args, **kwargs):
        return super(AddDocument, self).dispatch(*args, **kwargs)
        

class EditDocument(UpdateView):

    """
    Returns a DocForm filled with the current document data.
    
    :rtype: HTML Form
    :context: doc, get_place
    """
    model = Document
    template_name = 'spaces/document_form.html'

    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return '/spaces/' + self.space.name

    def get_object(self):
        cur_doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        return cur_doc
        
    def get_context_data(self, **kwargs):
        context = super(EditDocument, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context
        
    @method_decorator(permission_required('spaces.change_document'))
    def dispatch(self, *args, **kwargs):
        return super(EditDocument, self).dispatch(*args, **kwargs)
        

class DeleteDocument(DeleteView):

    """
    Returns a confirmation page before deleting the current document.
    
    :rtype: Confirmation
    :context: get_place
    """
        
    def get_object(self):
        return get_object_or_404(Document, pk = self.kwargs['doc_id'])
    
    def get_success_url(self):
        current_space = self.kwargs['space_url']
        return '/spaces/{0}'.format(current_space)
        
    def get_context_data(self, **kwargs):
        context = super(DeleteDocument, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

    @method_decorator(permission_required('spaces.delete_document'))
    def dispatch(self, *args, **kwargs):
        return super(DeleteDocument, self).dispatch(*args, **kwargs)



class ListDocs(ListView):

    """
    Returns a list of documents attached to the current space.
    
    :rtype: Object list
    :context: object_list, get_place
    """
    paginate_by = 25
    context_object_name = 'document_list'

    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        objects = Document.objects.all().filter(space=place.id).order_by('pub_date')

        cur_user = self.request.user
        if cur_user in place.admins or \
           cur_user in place.mods or \
           cur_user in place.users:
            return objects
        
        if self.request.user.is_anonymous():
            self.template_name = 'not_allowed.html'
            return objects

        self.template_name = 'not_allowed.html'
        return objects

    def get_context_data(self, **kwargs):
        context = super(ListDocs, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context
        
        
#
# EVENT VIEWS
#

class AddEvent(FormView):

    """
    Returns an empty MeetingForm to create a new Meeting. Space and author fields
    are automatically filled with the request data.
    
    :rtype: HTML Form
    :context: form, get_place
    """
    form_class = EventForm
    template_name = 'spaces/event_form.html'

    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return '/spaces/' + self.space.url + '/'

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        form_uncommited = form.save(commit=False)
        form_uncommited.event_author = self.request.user
        form_uncommited.space = self.space
        form_uncommited.save()
        return super(AddEvent, self).form_valid(form) 

    def get_context_data(self, **kwargs):
        context = super(AddEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

    @method_decorator(permission_required('spaces.add_event'))
    def dispatch(self, *args, **kwargs):
        return super(AddEvent, self).dispatch(*args, **kwargs)


class ViewEvent(DetailView):
    
    """
    View the content of a event.
    
    :rtype: Object
    :context: event, get_place
    """
    context_object_name = 'event'
    template_name = 'spaces/event_detail.html'

    def get_object(self):
        space_url = self.kwargs['space_url']

        if self.request.user.is_anonymous():
            self.template_name = 'not_allowed.html'
            return get_object_or_404(Space, url = space_url)

        return get_object_or_404(Event, pk = self.kwargs['event_id'])

    def get_context_data(self, **kwargs):
        context = super(ViewEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

    @method_decorator(permission_required('spaces.view_event'))
    def dispatch(self, *args, **kwargs):
        return super(ViewEvent, self).dispatch(*args, **kwargs)


class EditEvent(UpdateView):

    """
    Returns a MeetingForm filled with the current Meeting data to be edited.
    
    :rtype: HTML Form
    :context: event, get_place
    """
    model = Event
    template_name = 'spaces/event_form.html'

    def get_object(self):
        cur_event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return cur_event
        
    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return '/spaces/' + self.space.name
    
    def get_context_data(self, **kwargs):
        context = super(EditEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context
        
    @method_decorator(permission_required('spaces.change_event'))
    def dispatch(self, *args, **kwargs):
        return super(EditEvent, self).dispatch(*args, **kwargs)
        
      
class DeleteEvent(DeleteView):

    """
    Returns a confirmation page before deleting the Meeting object.
   
    :rtype: Confirmation
    :context: get_place
    """

    def get_object(self):
        return get_object_or_404(Event, pk = self.kwargs['event_id'])

    def get_success_url(self):
        current_space = self.kwargs['space_url']
        return '/spaces/{0}'.format(current_space)
   
    def get_context_data(self, **kwargs):
        context = super(DeleteEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

    @method_decorator(permission_required('spaces.delete_event'))
    def dispatch(self, *args, **kwargs):
        return super(AddEvent, self).dispatch(*args, **kwargs)



class ListEvents(ListView):

    """
    List all the events attached to a space.
    
    :rtype: Object list
    :context: event_list, get_place
    """
    paginate_by = 25
    context_object_name = 'event_list'

    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        objects = Event.objects.all().filter(space=place.id).order_by\
            ('event_date')
        return objects

    def get_context_data(self, **kwargs):
        context = super(ListEvents, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

#
# NEWS RELATED
#

class ListPosts(ListView):

    """
    Returns a list with all the posts attached to that space. It's similar to
    an archive, but without classification or filtering.
    
    :rtype: Object list
    :context: post_list
    """
    paginate_by = 10
    context_object_name = 'post_list'
    template_name = 'news/news_list.html'
    
    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        
        if settings.DEBUG:
            messages.set_level(self.request, messages.DEBUG)
        return Post.objects.all().filter(space=place).order_by('-pub_date')
    
    def get_context_data(self, **kwargs):
        context = super(ListPosts, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['messages'] = messages.get_messages(self.request)
        return context
    
    
