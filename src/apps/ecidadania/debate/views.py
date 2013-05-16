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
These are the views that control the debates.
"""

import json
import datetime

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.comments import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.forms import CommentForm
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.forms.formsets import formset_factory, BaseFormSet
from django.db import connection
from django.forms.models import modelformset_factory, inlineformset_factory

from guardian.shortcuts import assign_perm

from apps.ecidadania.debate import url_names as urln
from apps.ecidadania.debate.models import Debate, Note, Row, Column
from apps.ecidadania.debate.forms import DebateForm, UpdateNoteForm, \
    NoteForm, RowForm, ColumnForm, UpdateNotePosition
from core.spaces.models import Space
from core.permissions import has_space_permission, has_all_permissions, \
    has_operation_permission
from helpers.cache import get_or_insert_object_in_cache


def add_new_debate(request, space_url):

    """
    Create a new debate. This function returns two forms to create
    a complete debate, debate form and phases formset.

    .. versionadded:: 0.1.5

    :attributes: debate_form, row_formset, column_formset
    :context: form, rowform, colform, get_place, debateid
    """
    place = get_object_or_404(Space, url=space_url)

    if (request.user.has_perm('admin_space', place) or
        request.user.has_perm('mod_space', place)):

        RowFormSet = inlineformset_factory(Debate, Row, extra=1)
        ColumnFormSet = inlineformset_factory(Debate, Column, extra=1)

        debate_form = DebateForm(request.POST or None)
        row_formset = RowFormSet(request.POST or None, prefix="rowform")
        column_formset = ColumnFormSet(request.POST or None, prefix="colform")

        # Get the last PK and add 1 to get the current PK
        try:
            last_debate_id = Debate.objects.latest('id')
            current_debate_id = last_debate_id.pk + 1
        except ObjectDoesNotExist:
            current_debate_id = 1

        if request.method == 'POST':
            if (debate_form.is_valid() and row_formset.is_valid() and
                column_formset.is_valid()):

                debate_form_uncommited = debate_form.save(commit=False)
                debate_form_uncommited.space = place
                debate_form_uncommited.author = request.user

                saved_debate = debate_form_uncommited.save()
                debate_instance = get_object_or_404(Debate, pk=current_debate_id)

                row = row_formset.save(commit=False)
                for form in row:
                    form.debate = debate_instance
                    form.save()

                column = column_formset.save(commit=False)
                for form in column:
                    form.debate = debate_instance
                    form.save()

                # Assign the permissions to the creator of the debate and the
                # space administrators
                assign_perm('view_debate', request.user, debate_instance)
                assign_perm('admin_debate', request.user, debate_instance)
                assign_perm('change_debate', request.user, debate_instance)
                assign_perm('delete_debate', request.user, debate_instance)

                return HttpResponseRedirect(reverse(urln.DEBATE_VIEW,
                    kwargs={'space_url': space_url,
                            'debate_id': str(debate_form_uncommited.id)}))

        return render_to_response('debate/debate_add.html',
                              {'form': debate_form,
                               'rowform': row_formset,
                               'colform': column_formset,
                               'get_place': place,
                                     'debateid': current_debate_id},
            context_instance=RequestContext(request))
    else:
        raise PermissionDenied


def edit_debate(request, space_url, debate_id):

    """
    """
    pk = debate_id
    place = get_object_or_404(Space, url=space_url)
    instance = Debate.objects.get(pk=debate_id)

    if (request.user.has_perm('admin_space', place) or
        request.user.has_perm('admin_debate', instance) or
        request.user == instance.author):

        RowFormSet = inlineformset_factory(Debate, Row, extra=1)
        ColumnFormSet = inlineformset_factory(Debate, Column, extra=1)

        debate_form = DebateForm(request.POST or None, instance=instance)
        row_formset = RowFormSet(request.POST or None, instance=instance,
                                                       prefix="rowform")
        column_formset = ColumnFormSet(request.POST or None, instance=instance,
                                                             prefix="colform")

        if request.method == 'POST':
            if debate_form.is_valid() and row_formset.is_valid() \
                    and column_formset.is_valid():
                debate_form_uncommited = debate_form.save(commit=False)
                debate_form_uncommited.space = place
                debate_form_uncommited.author = request.user

                saved_debate = debate_form_uncommited.save()
                debate_instance = get_object_or_404(Debate,
                    pk=debate_id)

                row = row_formset.save(commit=False)

                for form in row:
                    form.debate = instance
                    form.save()

                    column = column_formset.save(commit=False)
                    for form in column:
                        form.debate = instance
                        form.save()

                return HttpResponseRedirect(reverse(urln.DEBATE_VIEW,
                    kwargs={'space_url': space_url,
                            'debate_id': str(debate_form_uncommited.id)}))

        return render_to_response('debate/debate_add.html',
                                  {'form': debate_form,
                                   'rowform': row_formset,
                                   'colform': column_formset,
                                   'get_place': place,
                                           'debateid': debate_id},
                                  context_instance=RequestContext(request))
    else:
        raise PermissionDenied


# def get_debates(request):

#     """
#     Get all debates and serve them through JSON.
#     """
#     data = [debate.title for debate in Debate.objects.order_by('title')]
#     return render_to_response(json.dumps(data), content_type='application/json')


def create_note(request, space_url):

    """
    This function creates a new note inside the debate board. It receives the
    order from the createNote() AJAX function. To create the note first we
    create the note in the DB, and if successful we return some of its
    parameters to the debate board for the user. In case the petition had
    errors, we return the error message that will be shown by jsnotify.

    .. versionadded:: 0.1.5
    """
    note_form = NoteForm(request.POST or None)
    place = get_object_or_404(Space, url=space_url)

    if request.method == "POST" and request.is_ajax():
        debate = get_object_or_404(Debate, pk=request.POST['debateid'])

        # This is not the best approach, but I don't want to think in
        # another solution right now, we need this and we need it now
        if ((debate.private and request.user.has_perm('view_debate', debate)) or
            (not debate.private and request.user.has_perm('view_space', place))):

            if note_form.is_valid():
                note_form_uncommited = note_form.save(commit=False)
                note_form_uncommited.author = request.user
                note_form_uncommited.debate = get_object_or_404(Debate,
                    pk=request.POST['debateid'])
                note_form_uncommited.title = request.POST['title']
                note_form_uncommited.message = request.POST['message']
                note_form_uncommited.column = get_object_or_404(Column,
                    pk=request.POST['column'])
                note_form_uncommited.row = get_object_or_404(Row,
                    pk=request.POST['row'])
                note_form_uncommited.save()

                response_data = {}
                response_data['id'] = note_form_uncommited.id
                response_data['message'] = note_form_uncommited.message
                response_data['title'] = note_form_uncommited.title
                msg = "The note has been created."
                return HttpResponse(json.dumps(response_data),
                                mimetype="application/json")
            else:
                msg = "The note form didn't validate. This fields gave errors: " + str(note_form.errors)
        else:
            raise PermissionDenied
    else:
        msg = "The petition was not POST."

    return HttpResponse(json.dumps(msg), mimetype="application/json")


def update_note(request, space_url):

    """
    Updated the current note with the POST data. UpdateNoteForm is an incomplete
    form that doesn't handle some properties, only the important for the note
    editing.
    """

    # Shit double validation here due to the fact that we can't get the note ID
    # until the JS code sends us the GET or POST signals
    place = get_object_or_404(Space, url=space_url)

    if request.method == "GET" and request.is_ajax():
        note = get_object_or_404(Note, pk=request.GET['noteid'])
        debate = get_object_or_404(Debate, pk=note.debate.id)

        if (request.user.has_perm('admin_space', place) or
            request.user.has_perm('mod_space', place) or
            request.user.has_perm('admin_debate', debate) or
            request.user.has_perm('mod_debate', debate) or
            request.user == note.author):

            ctype = ContentType.objects.get_for_model(Note)
            latest_comments = Comment.objects.filter(is_public=True,
                is_removed=False, content_type=ctype, object_pk=note.id) \
                .order_by('-submit_date')[:5]
            form = CommentForm(target_object=note)

            response_data = {}
            response_data['title'] = note.title
            response_data['message'] = note.message
            response_data['author'] = {'name': note.author.username}
            response_data['comments'] = [{'username': c.user.username,
                'comment': c.comment,
                'submit_date': c.submit_date} for c in latest_comments]
            response_data["form_html"] = form.as_p()

            return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder),
                            mimetype="application/json")
        else:
            raise PermissionDenied

    if request.method == "POST" and request.is_ajax:
        note = get_object_or_404(Note, pk=request.POST['noteid'])
        debate = get_object_or_404(Debate, pk=note.debate.id)

        if (request.user.has_perm('admin_space', place) or
            request.user.has_perm('mod_space', place) or
            request.user.has_perm('admin_debate', debate) or
            request.user.has_perm('mod_debate', debate) or
            request.user == note.author):

            note_form = UpdateNoteForm(request.POST or None, instance=note)
            if note_form.is_valid():
                note_form_uncommited = note_form.save(commit=False)
                note_form_uncommited.title = request.POST['title']
                note_form_uncommited.message = request.POST['message']
                note_form_uncommited.last_mod_author = request.user

                note_form_uncommited.save()
                msg = "The note has been updated."
            else:
                msg = "The form is not valid, check field(s): " + note_form.errors
            return HttpResponse(msg)
        else:
            raise PermissionDenied
    return HttpResponse(msg)


def update_position(request, space_url):

    """
    This view saves the new note position in the debate board. Instead of
    reloading all the note form with all the data, we use the partial form
    "UpdateNotePosition" which only handles the column and row of the note.
    """
    place = get_object_or_404(Space, url=space_url)

    if request.method == "POST" and request.is_ajax:
        note = get_object_or_404(Note, pk=request.POST['noteid'])
        debate = get_object_or_404(Debate, pk=note.debate.id)
        position_form = UpdateNotePosition(request.POST or None, instance=note)

        if (request.user.has_perm('admin_space', place) or
            request.user.has_perm('mod_space', place) or
            request.user.has_perm('admin_debate', debate) or
            request.user.has_perm('mod_debate', debate) or
            request.user == note.author):

            if position_form.is_valid():
                position_form_uncommited = position_form.save(commit=False)
                position_form_uncommited.column = get_object_or_404(Column,
                                                pk=request.POST['column'])
                position_form_uncommited.row = get_object_or_404(Row,
                                                pk=request.POST['row'])
                position_form_uncommited.save()
                msg = "The note has been updated."
            else:
                msg = "There has been an error validating the form."
        else:
            raise PermissionDenied
    return HttpResponse(msg)


def delete_note(request, space_url):

    """
    Deletes a note object.
    """
    note = get_object_or_404(Note, pk=request.POST['noteid'])
    place = get_object_or_404(Space, url=space_url)

    if (request.user.has_perm('admin_space', place) or
        request.user.has_perm('mod_space', place) or
        request.user.has_perm('admin_debate', debate) or
        request.user.has_perm('mod_debate', debate) or
        request.user == note.author):

        ctype = ContentType.objects.get_for_model(Note)
        all_comments = Comment.objects.filter(is_public=True,
                is_removed=False, content_type=ctype,
                object_pk=note.id).all()
        for i in range(len(all_comments)):
            all_comments[i].delete()
        note.delete()
        return HttpResponse("The note has been deleted.")

    else:
        return PermissionDenied


class ViewDebate(DetailView):
    """
    View a debate.

    :context: get_place, notes, columns, rows
    """
    context_object_name = 'debate'
    template_name = 'debate/debate_view.html'

    def dispatch(self, request, *args, **kwargs):
        debate = get_object_or_404(Debate, pk=kwargs['debate_id'])
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if debate.private:
            if (request.user.has_perm('admin_space', place) or
                request.user.has_perm('mod_space', place) or
                request.user.has_perm('view_debate', debate)):
                return super(ViewDebate, self).dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            if request.user.has_perm('view_space', space):
                return super(ViewDebate, self).dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied

    def get_object(self):
        key = self.kwargs['debate_id']
        debate = get_or_insert_object_in_cache(Debate, key, pk=key)

        # Check debate dates
        if datetime.date.today() >= debate.end_date:
            self.template_name = 'debate/debate_expired_view.html'
            return debate
        elif datetime.date.today() < debate.start_date:
            self.template_name = 'debate/debate_outdated.html'
            return debate
            # We can't return none, if we do, the platform cannot show
            # the start and end dates and the title
            # return Debate.objects.none()

        return debate

    def get_context_data(self, **kwargs):
        context = super(ViewDebate, self).get_context_data(**kwargs)
        columns = Column.objects.filter(debate=self.kwargs['debate_id'])
        rows = Row.objects.filter(debate=self.kwargs['debate_id'])
        space_key = self.kwargs['space_url']
        current_space = get_or_insert_object_in_cache(Space, space_key,
                                                      url=space_key)
        debate_key = self.kwargs['debate_id']
        current_debate = get_or_insert_object_in_cache(Debate, debate_key,
                                                       pk=debate_key)
        notes = Note.objects.filter(debate=current_debate.pk)
        try:
            last_note = Note.objects.latest('id')
        except:
            last_note = 0

        context['get_place'] = current_space
        context['notes'] = notes
        context['columns'] = columns
        context['rows'] = rows
        if last_note == 0:
            context['lastnote'] = 0
        else:
            context['lastnote'] = last_note.pk

        return context


class ListDebates(ListView):
    """
    Return a list of debates for the current space.

    :context: get_place
    """
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            super(ListDebates, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        key = self.kwargs['space_url']
        current_space = get_or_insert_object_in_cache(Space, key, url=key)
        debates = Debate.objects.filter(space=current_space)
        return debates

    def get_context_data(self, **kwargs):
        context = super(ListDebates, self).get_context_data(**kwargs)
        key = self.kwargs['space_url']
        space = get_or_insert_object_in_cache(Space, key, url=key)
        context['get_place'] = space
        return context


class DeleteDebate(DeleteView):

    """
    Delete an existent debate. Debate deletion is only reserved to spaces
    administrators or site admins.
    """
    context_object_name = "get_place"

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])
        debate = get_object_or_404(Debate, pk=kwargs['debate_id'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space) or
            request.user.has_perm('admin_debate', debate) or
            request.user == debate.author):
            return super(DeleteDebate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        space = self.kwargs['space_url']
        return '/spaces/%s' % (space)

    def get_object(self):
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return get_object_or_404(Debate, pk=self.kwargs['debate_id'])

    def get_context_data(self, **kwargs):

        """
        Get extra context data for ViewDebate view.
        """
        context = super(DeleteDebate, self).get_context_data(**kwargs)
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = space
        return context
