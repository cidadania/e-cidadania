/*
    debate_board_expired.js - Javascript containing the engine for the debate
                           system (expired).
                           
    License: GPLv3
    Copyright: 2013 Cidadania S. Coop. Galega
    Author: Oscar Carballal Prego <info@oscarcp.com>
*/

// We put here the strings for translation. This is meant to be translated by
// django jsi18n
var errorGetNote = gettext("Couldn't get note data.");
var comment = gettext('Comment');
var view = gettext('View');
var adviceMsg = gettext("Caution");
var advice = gettext("You are adding too much columns. We put no limit, \
    but too many columns will be a problem in smaller screens.");

/* Minor settings */
var alertIcon = 'http://ecidadania.org/static/assets/icons/alert.png';

function viewNote(obj) {
    /*
        editNote(obj) - This function detects the note the user clicked and raises
        a modal dialog, after that it checks the note in the server and returns
        it's data, prepopulating the fields.
    */
    var noteID = $(obj).parents('.note').attr('id');

    var request = $.ajax({
        url: "../update_note/",
        data: { noteid: noteID }
    });

    request.done(function(note) {
        $('h3#view-note-title').text(note.title);
        $('p#view-note-desc').html(note.message);
        $('span#view-note-author').text(note.author.name);

        var html = '';
        var comment_count = "<h5 class='note-comment-title'>" + comment + " (" + note.comments.length + ")</h5>";
        for(var i=0; i<note.comments.length; i++) {
            var item = note.comments[i];
            html += "<div class='comment-bubble' id='comment" + i +"'>" + "<p id='username' class='viewer'>"+ item.username + "</p>";
            html += "<p id='date' class='viewer-date'>"+ item.submit_date +"</p>";
            html += "<p id='comments" + i + "' class='viewer-comment'>" + item.comment +"</p><img src='/static/img/arrow-2.png' width='20' height='21'></div>";
        }
        $('div#comments').html(html);
        $('span#num-comments').html(comment_count);
        $('form#form_comments div.kopce').html(note.form_html);
   });

    request.fail(function (jqXHR, textStatus) {
        $('#view-current-note').modal('hide');
        $.gritter.add({
            title: errorMsg,
            text: errorGetNote + ' ' + textStatus,
            image: alertIcon
        });
    });
}
