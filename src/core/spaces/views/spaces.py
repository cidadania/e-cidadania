# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Clione Software
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, \
    HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
from django.contrib.auth.models import User

from helpers.cache import get_or_insert_object_in_cache
from operator import itemgetter
from guardian.shortcuts import assign_perm, get_users_with_perms, remove_perm, get_perms
from guardian.core import ObjectPermissionChecker

from core.spaces import url_names as urln
from core.spaces.models import Space, Entity, Document, Event
from core.spaces.forms import SpaceForm, EntityFormSet, RoleForm
from apps.ecidadania.news.models import Post
from apps.ecidadania.proposals.models import Proposal, ProposalSet
from apps.ecidadania.staticpages.models import StaticPage
from apps.ecidadania.debate.models import Debate
from apps.ecidadania.voting.models import Poll, Voting
from e_cidadania.settings import DEBUG


# Please take in mind that the create_space view can't be replaced by a CBV
# (class-based view) since it manipulates two forms at the same time. Apparently
# that creates some trouble in the django API. See this ticket:
# https://code.djangoproject.com/ticket/16256
@login_required
def create_space(request):

    """
    Returns a SpaceForm form to fill with data to create a new space. There
    is an attached EntityFormset to save the entities related to the space.
    Every user in the platform is allowed to create spaces. Once it's created
    we assign the administration permissions to the user, along with some
    others for the sake of functionality.

    .. note:: Since everyone can have the ability to create spaces, instead
              of checking for the add_space permission we just ask for login.

    :attributes:           - space_form: empty SpaceForm instance
                           - entity_forms: empty EntityFormSet
    :permissions required: login_required
    :rtype:                Space object, multiple entity objects.
    :context:              form, entityformset
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

            # Assign permissions to the user so he can chenge everything in the
            # space
            assign_perm('view_space', request.user, space)
            assign_perm('change_space', request.user, space)
            assign_perm('delete_space', request.user, space)
            assign_perm('admin_space', request.user, space)

            if DEBUG:
                # This will tell us if the user got the right permissions for
                # the object
                un = request.user.username
                u = ObjectPermissionChecker(request.user)  # Avoid unnecesary queries for the permission checks
                print """Space permissions for user '%s':
                View: %s
                Change: %s
                Delete: %s
                Admin: %s
                Mod: %s
                """ % (un, u.has_perm('view_space', space),
                    u.has_perm('change_space', space),
                    u.has_perm('delete_space', space),
                    u.has_perm('admin_space', space),
                    u.has_perm('mod_space', space))

            return HttpResponseRedirect(reverse(urln.SPACE_INDEX,
                kwargs={'space_url': space.url}))

    return render_to_response('spaces/space_form.html',
                              {'form': space_form,
                               'entityformset': entity_forms},
                              context_instance=RequestContext(request))


class ViewSpaceIndex(DetailView):

    """
    Returns the index page for a space. The access to spaces is restricted and
    filtered in the dispatch method. This view gathers information from all
    the configured modules in the space and also makes some calculations to
    gather most commented posts, most interesting content, etc.


    :attributes:           - space_object/space/place: current space instance
    :permissions required: space.view_space
    :rtype:                Object
    :context: get_place, entities, documents, proposals, proposalsets,
              publication, mostviewed, mostcommented, mostcommentedproposal,
              page, messages, debates, events, votings, polls, participants.
    """
    context_object_name = 'get_place'
    template_name = 'spaces/space_index.html'

    def dispatch(self, request, *args, **kwargs):
        """
        We get the current space and user, first we check if the space is
        public, if so, we check if the user is anonymous and leave a message,
        after that we return the view. If the space is not public we check
        for the view permission of the object, if the user doesn't have it we
        return a 403. Since dispatch is run before anything, this checks are
        made before obtaining the object. If the user doesn't have the
        permission we return a 403 code, which is handled by
        django-guardian and returns a template.

        .. note:: Take in mind that the dispatch method takes **request** as a
                  parameter.
        """
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if space.public:
            if request.user.is_anonymous():
                messages.info(self.request, _("Hello anonymous user. Remember \
                    that this space is public to view, but you must \
                    <a href=\"/accounts/register\">register</a> or \
                    <a href=\"/accounts/login\">login</a> to participate."))

            return super(ViewSpaceIndex, self).dispatch(request, *args, **kwargs)

        if request.user.has_perm('view_space', space):
            return super(ViewSpaceIndex, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        # Makes sure the space ins't already in the cache before hitting
        # the database
        space_url = self.kwargs['space_url']
        space_object = get_or_insert_object_in_cache(Space, space_url, url=space_url)
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
            comment_list[proposal.pk] = Comment.objects.filter(object_pk=proposal.pk).count()
        for p in dict(sorted(comment_list.items(), key=itemgetter(1))):
            most_commented.append(Proposal.objects.filter(pk=p))

        highlighted = {}
        highlight = []
        for i in Proposal.objects.filter(space=place.id):
            highlighted[i.pk] = i.support_votes.count
        for p in dict(sorted(highlighted.items(), key=itemgetter(1))):
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
        context['participants'] = get_users_with_perms(place)
        return context


# Please take in mind that the change_space view can't be replaced by a CBV
# (class-based view) since it manipulates two forms at the same time. Apparently
# that creates some trouble in the django API. See this ticket:
# https://code.djangoproject.com/ticket/16256
def edit_space(request, space_url):

    """
    Returns a form filled with the current space data to edit. Access to
    this view is restricted only to site and space administrators. The filter
    for space administrators is given by the change_space and admin_space
    permission and their belonging to that space.

    :attributes:           - place: current space intance.
                           - form: SpaceForm instance.
                           - form_uncommited: form instance before commiting to
                             the DB, so we can modify the data.
    :permissions required: spaces.change_space, spaces.admin_space
    :param space_url:      Space URL
    :rtype:                HTML Form
    :context:              form, get_place, entityformset
    """
    place = get_object_or_404(Space, url=space_url)

    if (request.user.has_perm('change_space', place) and
        request.user.has_perm('admin_space', place)):
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

    else:
        raise PermissionDenied


class DeleteSpace(DeleteView):

    """
    Returns a confirmation page before deleting the space object completely.
    This does not delete the space related content. Only the site
    administrators or the space administrators can delete a space.

    :attributes:           space_url
    :permissions required: spaces.delete_space, spaces.admin_space
    :rtype:                Confirmation
    """
    context_object_name = 'get_place'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('delete_space', space) and
            request.user.has_perm('admin_space', space)):
            return super(DeleteSpace, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        space_url = self.kwargs['space_url']
        space = get_object_or_404(Space, url=space_url)
        return space


class ListSpaces(ListView):

    """
    Return a list of spaces in the system (except private ones) using a generic
    view. The users associated to a private spaces will see it, but not the
    other private spaces. ListSpaces is a django generic :class:`ListView`.

    .. note:: Permissions on this view are used only to filter the spaces list
              but the view itself is public.

    :attributes: space_url
    :permissions required: spaces.view_space
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
        all_spaces = Space.objects.all()
        public_spaces = Space.objects.filter(public=True)

        if not current_user.is_anonymous():
            for space in self.all_spaces:
                if current_user.has_perm('view_space', space):
                    user_spaces.add(space.pk)

            user_spaces = Space.objects.filter(pk__in=user_spaces)
            return self.public_spaces | user_spaces

        return self.public_spaces

    def get_context_data(self, **kwargs):
        context = super(ListSpaces, self).get_context_data(**kwargs)
        context['public_spaces'] = self.public_spaces
        return context


def edit_roles(request, space_url):

    """
    The edit_role function works to provide a way for space administrators to
    modify the users roles inside a space, at the space level.

    It basically works as an AJAX communication where the frontend sends to key
    values: userid and perm, containing the user ID and the permission code,
    which later we compare with the permissions dictionary. If the user has the
    permission we go to the next one and so on.

    There is a special perm code called "delete" that triggers the deletion of
    all the permissions for the current user on the current space.

    :ajax keys: userid, perm
    :returns: reponses
    :versionadded: 0.1.9
    """

    space = get_object_or_404(Space, url=space_url)
    perm_dict = {
        'admins': ['admin_space', 'view_space'],
        'mods': ['mod_space', 'view_space'],
        'users': ['view_space', ]
    }

    if request.user.has_perm('admin_space', space):
        if request.method == 'POST' and request.is_ajax():
            user = get_object_or_404(User, pk=request.POST['userid'])
            cur_user_perms = get_perms(user, space)

            if request.POST['perm'] == "delete":
                for p in cur_user_perms:
                    try:
                        remove_perm(p, user, space)
                    except:
                        return HttpResponseServerError(_("Couldn't delete user permissions."))
                return HttpResponse(_('Permissions deleted. User removed from space.'))

            else:
                try:
                    perm = perm_dict[request.POST['perm']]
                    for p in perm:
                        if p in cur_user_perms:
                            pass
                        else:
                            try:
                                assign_perm(p, user, space)
                            except:
                                return HttpResponseServerError(_("The permissions couldn't be assigned."))
                    return HttpResponse(_('Permissions assigned.'))
                except:
                    return HttpResponseBadRequest(_('Permission code not valid.'))
        else:
            space_users = get_users_with_perms(space, with_superusers=False)
            admins = set()
            mods = set()
            users = set()
            for user in space_users:
                if user.has_perm('admin_space', space):
                    admins.add(user)
                elif user.has_perm('mod_space', space):
                    mods.add(user)
                else:
                    # We omit the check for "view_space" because the space_users
                    # variable is already filtered to show only the users with permissions
                    # on that object and users shows all the users in the space.
                    users.add(user)

            return render_to_response('spaces/user_groups.html',
                {'get_place': space, 'user_admins': admins, 'user_mods': mods,
                 'user_users': users}, context_instance=RequestContext(request))
    else:
        raise PermissionDenied


def search_user(request, space_url):

    """
    Simple search user mechanishm, it makes a query to django with the strict
    user name, it it doesn't match, it returns an error.

    :ajax keys: uname
    :returns: user ID
    .. versionadded:: 0.1.9
    """
    space = get_object_or_404(Space, url=space_url)

    if request.user.has_perm('admin_space', space):
        if request.method == 'POST' and request.is_ajax():
            try:
                user = User.objects.get(username=request.POST['uname'])
                assign_perm('view_space', user, space)
                return HttpResponse(user.id)
            except:
                return HttpResponseNotFound(_('The user does not exist.'))
        else:
            return HttpResponseBadRequest(_("Wrong petition."))
    else:
        raise PermissionDenied
