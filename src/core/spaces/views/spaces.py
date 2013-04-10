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

from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from core.spaces import url_names as urln
from core.spaces.models import Space, Entity, Document, Event
from core.spaces.forms import SpaceForm, EntityFormSet, RoleForm
from core.permissions import has_space_permission, has_all_permissions
from apps.ecidadania.news.models import Post
from apps.ecidadania.proposals.models import Proposal, ProposalSet
from apps.ecidadania.staticpages.models import StaticPage
from apps.ecidadania.debate.models import Debate
from apps.ecidadania.voting.models import Poll, Voting
from helpers.cache import get_or_insert_object_in_cache

from operator import itemgetter

# Please take in mind that the create_space view can't be replaced by a CBV
# (class-based view) since it manipulates two forms at the same time. Apparently
# that creates some trouble in the django API. See this ticket:
# https://code.djangoproject.com/ticket/16256


@permission_required('spaces.add_space')
def create_space(request):

    """
    Returns a SpaceForm form to fill with data to create a new space. There
    is an attached EntityFormset to save the entities related to the space.
    Only site administrators are allowed to create spaces.

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
            # space.admins.add(request.user)
            space_form.save_m2m()

            return HttpResponseRedirect(reverse(urln.SPACE_INDEX,
                kwargs={'space_url': space.url}))

    return render_to_response('spaces/space_form.html',
                              {'form': space_form,
                               'entityformset': entity_forms},
                              context_instance=RequestContext(request))


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
        # Makes sure the space ins't already in the cache before hitting
        # the database
        space_url = self.kwargs['space_url']
        space_object = get_or_insert_object_in_cache(Space, space_url,
            url=space_url)

        if space_object.public or has_all_permissions(self.request.user):
            if self.request.user.is_anonymous():
                messages.info(self.request, _("Hello anonymous user. Remember \
                    that this space is public to view, but you must \
                    <a href=\"/accounts/register\">register</a> or \
                    <a href=\"/accounts/login\">login</a> to participate."))
            return space_object

        # Check if the user is in the admitted user groups of the space
        if has_space_permission(self.request.user, space_object,
                                allow=['admins', 'mods', 'users']):
            return space_object

        # If the user does not meet any of the conditions, it's not allowed to
        # enter the space
        if self.request.user.is_anonymous():
            messages.info(self.request, _("You're an anonymous user. You must \
                <a href=\"/accounts/register\">register</a> or \
                <a href=\"/accounts/login\">login</a> to access here."))
        else:
            messages.warning(self.request, _("You're not registered to this \
            space."))

        self.template_name = 'not_allowed.html'
        return space_object

    # Get extra context data
    def get_context_data(self, **kwargs):
        context = super(ViewSpaceIndex, self).get_context_data(**kwargs)
        # Makes sure the space ins't already in the cache before hitting the
        # databass
        place_url = self.kwargs['space_url']
        place = get_or_insert_object_in_cache(Space, place_url, url=place_url)
        '''posts_by_score = Comment.objects.filter(is_public=True) \
            .values('object_pk').annotate(score=Count('id')).order_by('-score')'''
        posts_by_score = Comment.objects.filter(is_public=True) \
            .values('object_pk').annotate(score=Count('id')).order_by('-score')
        post_ids = [int(obj['object_pk']) for obj in posts_by_score]
        top_posts = Post.objects.filter(space=place.id).in_bulk(post_ids)
        # print top_posts.values()[0].title
        # o_list = Comment.objects.annotate(ocount=Count('object_pk'))
        comment_list = {}
        most_commented = []
        for proposal in Proposal.objects.filter(space=place.id):
            comment_list[proposal.pk]=Comment.objects.filter(object_pk=proposal.pk).count()
        for p in dict(sorted(comment_list.items(), key = itemgetter(1))):
            most_commented.append(Proposal.objects.filter(pk=p))
        
        highlighted = {}
        highlight = []
        for i in Proposal.objects.filter(space=place.id):
            highlighted[i.pk] = i.support_votes.count
        for p in dict(sorted(highlighted.items(), key = itemgetter(1))):
            highlight.append(Proposal.objects.filter(pk=p))
        
        context['entities'] = Entity.objects.filter(space=place.id)
        context['documents'] = Document.objects.filter(space=place.id)
        context['proposalsets'] = ProposalSet.objects.filter(space=place.id)
        context['proposals'] = Proposal.objects.filter(space=place.id) \
                                                    .order_by('-pub_date')
        context['publication'] = Post.objects.filter(space=place.id) \
                                                    .order_by('-pub_date')[:5]
        context['mostviewed'] = Post.objects.filter(space=place.id) \
                                                    .order_by('-views')[:5]
        # context['mostcommented'] = [top_posts.get(id,None) for id in post_ids]
        context['mostcommented'] = filter(None, map(lambda x: top_posts.get(x, None), post_ids))
        context['mostcommentedproposal'] = most_commented
        context['highlightedproposal'] = highlight

        # context['mostcommented'] = sorted(o_list,
        #     key=lambda k: k['ocount'])[:10]
        # print sorted(o_list, key=lambda k: k['ocount'])[:10]
        context['page'] = StaticPage.objects.filter(show_footer=True) \
                                                    .order_by('-order')
        context['messages'] = messages.get_messages(self.request)
        context['debates'] = Debate.objects.filter(space=place.id) \
                                                    .order_by('-date')
        context['event'] = Event.objects.filter(space=place.id) \
                                                .order_by('-event_date')
        context['votings'] = Voting.objects.filter(space=place.id)
        context['polls'] = Poll.objects.filter(space=place.id)
        # True if the request.user has admin rights on this space
        context['user_is_admin'] = (self.request.user in place.admins.all()
            or self.request.user in place.mods.all()
            or self.request.user.is_staff or self.request.user.is_superuser)
        context['polls'] = Poll.objects.filter(space=place.id)
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

    if has_space_permission(request.user, place, allow=['admins']):
        form = SpaceForm(request.POST or None, request.FILES or None,
            instance=place)
        entity_forms = EntityFormSet(request.POST or None, request.FILES
            or None, queryset=Entity.objects.all().filter(space=place))

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

                form.save_m2m()
                return HttpResponseRedirect(reverse(urln.SPACE_INDEX,
                    kwargs={'space_url': space.url}))

        return render_to_response('spaces/space_form.html', {'form': form,
                    'get_place': place, 'entityformset': entity_forms},
                    context_instance=RequestContext(request))

    return render_to_response('not_allowed.html',
        context_instance=RequestContext(request))


class DeleteSpace(DeleteView):

    """
    Returns a confirmation page before deleting the space object completely.
    This does not delete the space related content. Only the site
    administrators can delete a space.

    :rtype: Confirmation
    """
    context_object_name = 'get_place'
    success_url = '/'

    @method_decorator(permission_required('spaces.delete_space'))
    def dispatch(self, *args, **kwargs):
        return super(DeleteSpace, self).dispatch(*args, **kwargs)

    def get_object(self):
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        if self.request.user in space.admins.all():
            return space
        else:
            self.template_name = 'not_allowed.html'
            return space


# class GoToSpace(RedirectView):

#     """
#     Sends the user to the selected space. This view only accepts GET petitions.
#     GoToSpace is a django generic :class:`RedirectView`.

#     :Attributes: **self.place** - Selected space object
#     :rtype: Redirect
#     """
#     def get_redirect_url(self, **kwargs):
#         self.place = get_object_or_404(Space,name = self.request.GET['spaces'])
#         return '/spaces/%s' % self.place.url


class ListSpaces(ListView):

    """
    Return a list of spaces in the system (except private ones) using a generic
    view. The users associated to a private spaces will see it, but not the
    other private spaces. ListSpaces is a django generic :class:`ListView`.

    :rtype: Object list
    :contexts: object_list
    """
    paginate_by = 10

    public_spaces = Space.objects.filter(public=True)
    all_spaces = Space.objects.all()

    def get_queryset(self):

        # I think I should explain this mess. What we want to obtain here is:
        # a list of public spaces in case the user is anonymous, or a list of
        # the public spaces plus the spaces the user is registered to if the
        # user is logged in.
        # To do the second, we create a set of PK objects, and outside of the
        # 'for' loop we make a queryset for those PK objects, after that we
        # combine the data of the user spaces and public ones with the '|'
        # operand.
        current_user = self.request.user
        user_spaces = set()

        if not current_user.is_anonymous():
            for space in self.all_spaces:
                if has_space_permission(current_user, space,
                                        allow=['users', 'admins', 'mods']):
                    user_spaces.add(space.pk)
            user_spaces = Space.objects.filter(pk__in=user_spaces)
            return self.public_spaces | user_spaces

        return self.public_spaces

    def get_context_data(self, **kwargs):
        context = super(ListSpaces, self).get_context_data(**kwargs)
        context['all_spaces'] = self.all_spaces
        context['public_spaces'] = self.public_spaces
        return context


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
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def get_object(self):
        cur_space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return cur_space

    def get_context_data(self, **kwargs):
        context = super(EditRole, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context

    @method_decorator(permission_required('spaces.change_space'))
    def dispatch(self, *args, **kwargs):
        return super(EditRole, self).dispatch(*args, **kwargs)
