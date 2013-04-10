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

from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.comments import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.forms import CommentForm
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db import connection
from django.forms.models import modelformset_factory, inlineformset_factory

from apps.ecidadania.debate import url_names as urln
from apps.ecidadania.debate.models import Debate, Note, Row, Column
from apps.ecidadania.debate.forms import DebateForm, UpdateNoteForm, \
    NoteForm, RowForm, ColumnForm, UpdateNotePosition
from core.spaces.models import Space
from core.permissions import has_space_permission, has_all_permissions, \
    has_operation_permission
from helpers.cache import get_or_insert_object_in_cache


@permission_required('debate.add_debate')
def add_new_debate(request, space_url):

    """
    Create a new debate. This function returns two forms to create
    a complete debate, debate form and phases formset.

    .. versionadded:: 0.1.5

    :attributes: debate_form, row_formset, column_formset
    :context: form, rowform, colform, get_place, debateid
    """
    place = get_object_or_404(Space, url=space_url)

    if has_space_permission(request.user, place, allow=['admins']) \
            or has_all_permissions(request.user):

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
            if debate_form.is_valid() and row_formset.is_valid() \
                    and column_formset.is_valid():
                debate_form_uncommited = debate_form.save(commit=False)
                debate_form_uncommited.space = place
                debate_form_uncommited.author = request.user

                saved_debate = debate_form_uncommited.save()
                debate_instance = get_object_or_404(Debate,
                    pk=current_debate_id)

                row = row_formset.save(commit=False)
                for form in row:
                    form.debate = debate_instance
                    form.save()

                column = column_formset.save(commit=False)
                for form in column:
                    form.debate = debate_instance
                    form.save()

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
    return render_to_response('not_allowed.html',
                              context_instance=RequestContext(request))


@permission_required('debate.change_debate')
def edit_debate(request, space_url, debate_id):

    pk = debate_id
    place = get_object_or_404(Space, url=space_url)

    if has_operation_permission(request.user, place, 'debate.change_debate',
                                allow=['admins', 'mods']):

        RowFormSet = inlineformset_factory(Debate, Row, extra=1)
        ColumnFormSet = inlineformset_factory(Debate, Column, extra=1)

        instance = Debate.objects.get(pk=debate_id)
        debate_form = DebateForm(request.POST or None, instance=instance)
        row_formset = RowFormSet(request.POST or None, instance=instance, prefix="rowform")
        column_formset = ColumnFormSet(request.POST or None, instance=instance, prefix="colform")

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
    return render_to_response('not_allowed.html',
                              context_instance=RequestContext(request))


def get_debates(request):

    """
    Get all debates and serve them through JSON.
    """
    data = [debate.title for debate in Debate.objects.order_by('title')]
    return render_to_response(json.dumps(data), content_type='application/json')


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

    if request.method == "POST" and request.is_ajax:
        if has_operation_permission(request.user, place, 'note.add_note',
        allow=['admins', 'mods', 'users']):
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
            msg = "The petition was not POST."

    return HttpResponse(json.dumps(msg), mimetype="application/json")


def update_note(request, space_url):

    """
    Updated the current note with the POST data. UpdateNoteForm is an incomplete
    form that doesn't handle some properties, only the important for the note
    editing.
    """

    place = get_object_or_404(Space, url=space_url)

    if request.method == "GET" and request.is_ajax:
        note = get_object_or_404(Note, pk=request.GET['noteid'])
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

    if request.method == "POST" and request.is_ajax:
        if has_operation_permission(request.user, place, 'note.change_note',
        allow=['admins', 'mods']) or request.user == note.author:
            note = get_object_or_404(Note, pk=request.POST['noteid'])
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
            msg = "There was some error in the petition."
    return HttpResponse(msg)


def update_position(request, space_url):

    """
    This view saves the new note position in the debate board. Instead of
    reloading all the note form with all the data, we use the partial form
    "UpdateNotePosition" which only handles the column and row of the note.
    """
    note = get_object_or_404(Note, pk=request.POST['noteid'])
    position_form = UpdateNotePosition(request.POST or None, instance=note)
    place = get_object_or_404(Space, url=space_url)

    if request.method == "POST" and request.is_ajax:
        if has_operation_permission(request.user, place, 'note.change_note',
        allow=['admins', 'mods']) or request.user == note.author:
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
            msg = "There was some error in the petition."

    return HttpResponse(msg)


def delete_note(request, space_url):

    """
    Deletes a note object.
    """
    note = get_object_or_404(Note, pk=request.POST['noteid'])
    place = get_object_or_404(Space, url=space_url)

    if has_operation_permission(request.user, place, 'note.delete_note',
    allow=['admins', 'mods']) or note.author == request.user:
        ctype = ContentType.objects.get_for_model(Note)
        all_comments = Comment.objects.filter(is_public=True,
                is_removed=False, content_type=ctype,
                object_pk=note.id).all()
        for i in range(len(all_comments)):
            all_comments[i].delete()
        note.delete()
        return HttpResponse("The note has been deleted.")

    else:
        return HttpResponse("You're not the author of the note. Can't delete.")


class ViewDebate(DetailView):
    """
    View a debate.

    :context: get_place, notes, columns, rows
    """
    context_object_name = 'debate'
    template_name = 'debate/debate_view.html'

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

    def get_queryset(self):
        key = self.kwargs['space_url']
        current_space = get_or_insert_object_in_cache(Space, key, url=key)
        debates = Debate.objects.filter(space=current_space)

        # Here must go a validation so a user registered to the space
        # can always see the debate list. While an anonymous or not
        # registered user can't see anything unless the space is public

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

    def get_success_url(self):
        space = self.kwargs['space_url']
        return '/spaces/%s' % (space)

    def get_object(self):
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        if has_operation_permission(self.request.user, space, 'debate.delete_debate', allow=['admins', 'mods']):
            return get_object_or_404(Debate, pk=self.kwargs['debate_id'])
        else:
            self.template_name = 'not_allowed.html'

    def get_context_data(self, **kwargs):

        """
        Get extra context data for ViewDebate view.
        """
        context = super(DeleteDebate, self).get_context_data(**kwargs)
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = space
        return context
