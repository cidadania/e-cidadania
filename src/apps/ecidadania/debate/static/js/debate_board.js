/*
    debate_board.js - Javascript containing the engine for the debate
                           system.
                           
    License: GPLv3
    Copyright: 2011 Cidadania S. Coop. Galega
    Author: Oscar Carballal Prego <info@oscarcp.com>
*/

// We put here the strings for translation. This is meant to be translated by
// django jsi18n
var newTitle = gettext('Write here your title');
var newMessage = gettext('Write here your message');
var editString = gettext('Edit');
var viewString = gettext('View');
var errorMsg = gettext('There has been an error.');
var errorMsg2 = gettext("Could't delete column or row.");
var errorCreate = gettext("Couldn't create note.");
var errorGetNote = gettext("Couldn't get note data.");
var errorSave = gettext("Couldn't save note.");
var errorSavePos = gettext("Couldn't save note position.");
var errorDelete = gettext("Couldn't delete note.");
var errorCRDelete = gettext("There must be at least one column or row in the table.");
var errorCRCreate = gettext("Couln't create row or column.");
var confirmDelete = gettext('Are you sure?');
var comment = gettext('Comment');
var view = gettext('View');
var edit = gettext('Edit');
var remove = gettext('Delete note');
var adviceMsg = gettext("Caution");
var advice = gettext("You are adding too much columns. We put no limit, \
    but too many columns will be a problem in smaller screens.");

/* Minor settings */
var alertIcon = 'http://ecidadania.org/static/assets/icons/alert.png';

/*
    NOTE FUNCTIONS
*/

function showControls() {
    /*
     showControls() - Hides the edit and delete controls from the notes. If the
     users hovers over a note created by himself, the note shows the controls.
     */
    $(".note").hover(function(){
            $(this).find(".deletenote").show();
            $(this).find("#edit-note").show();
            $(this).find("#view-note").show();
        },
        function() {
            $(this).find(".deletenote").hide();
            $(this).find("#edit-note").hide();
            $(this).find("#view-note").hide();
        }
    );
}

function createNote() {
    /*
        createNote() - Creates a new note related with the debate. Frist the
        function creates the note in the server and after that we create a "fake"
        note in the debate board with the data returned by the view. If for some
        reason the user creates the note and leaves it before moving or editing the
        note is positioned in position [1,1].
    */

    var request = $.ajax({
        type:"POST",
        url:"../create_note/",
        data:{
            debateid:$('#debate-number').text(),
            title: newTitle,
            message: newMessage,
            column:1,
            row:1
        }
    });

    request.done(function (note) {
        var newNote = $("#sortable-dispatcher").append("<div id='" + note.id + "' style='display:hidden;' class='note mine'>" +
            "<div class='handler'><span id='view-note' style='float:left;'>" +
            "<a href='#' class='nounderline' onclick='viewNote(this)' data-toggle='modal' data-target='#view-current-note' title='" + view + "'><i class='icon-eye-open' style='font-size:12px;''></i></a>" +
            "</span><div class='deletenote' style='float:right;'><a href='#' onclick='deleteNote(this)' id='deletenote' title='" + remove + "'><i class='icon-remove' style='font-size:12px;'></i></a></div>" +
            "<span id='edit-note' style='float:right;'>" +
            "<a href='#'' class='nounderline' onclick='editNote(this)' data-toggle='modal' data-target='#edit-current-note' title='" + edit + "'><i class='icon-pencil' style='font-size:12px;'></i></a>" +
            "</span></div><p class='note-text'>" + note.title + "</p>");
        newNote.show("slow");
        showControls();
    });

    request.fail(function (jqXHR, textStatus) {
        $.gritter.add({
            title: errorMsg,
            text: errorCreate + ' ' + textStatus,
            image: alertIcon
        });
    });
}

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

function editNote(obj) {
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
        $("input[name='notename']").val(note.title);
        wysieditor.data("wysihtml5").editor.setValue(note.message, true);
        // If for some reason the WYSIHTML5 editor fails, it will fallback
        // into a simple textarea that gets shown
        $("textarea#id_note_message").val(note.message);
        $("#last-edited-note").text(noteID);
    });

    request.fail(function (jqXHR, textStatus) {
        $('#edit-current-note').modal('hide');
        $.gritter.add({
            title: errorMsg,
            text: errorGetNote + ' ' + textStatus,
            image: alertIcon
        });
    });
}

function saveNote() {
    /*
        saveNote() - Saves the current edited note, only the title and message
        field, since the other fields are managed through makeSortable() or by
        django itself.
    */
    var noteID = $('#last-edited-note').text();

    var request = $.ajax({
        type: "POST",
        url: "../update_note/",
        data: {
            noteid: noteID,
            title: $("input[name='notename']").val(),
            message: $("textarea#id_note_message").val()
            //message: $("td#cke_contents_id_note_message .cke_show_borders").text()
        }
    });

    request.done(function(msg) {
        $('#edit-current-note').modal('hide');
        var newTitle = $("input[name='notename']").val();
        $("div#" + noteID + " > p").text(newTitle);
    });

    request.fail(function(jqXHR, textStatus) {
        $('#edit-current-note').modal('hide');
        $.gritter.add({
            title: errorMsg,
            text: errorSave + ' ' + textStatus,
            image: alertIcon
        });
    })
}

function deleteNote(obj) {
    /*
        deleteNote() - Delete a note making an AJAX call. This function is called
        through getClickedNote(). We locate the note ID, and post it to django,
        after that we hide the note from the board and when it's hidden we remove it
        from the DOM.
    */
    var noteID = $(obj).parents('.note').attr('id');
    var answer = confirm(confirmDelete);

    if (answer) {
        var request = $.ajax({
            type: "POST",
            url: "../delete_note/",
            data: { noteid: noteID }
        });

        request.done(function(msg) {
           $('#' + noteID).hide("normal", function() {
               $('#' + noteID).remove();
           });
        });

        request.fail(function(jqXHR, textStatus) {
            $.gritter.add({
                title: errorMsg,
                text: errorDelete + ' ' + textStatus,
                image: alertIcon
            });
        });
    }
}

function makeSortable() {
    /*
        makeSortable() - Makes every element with id starting by 'sortable'
        sortable through the connectedSortable class lists. It uses jQuery
        Sortable. This function has to be called whenever a new element is on
        the page (note, table column or row) to make the new elements sortable.
    */
    
    // Get all the div elements starting by sortable
    $("[id^=sortable]").sortable({
        connectWith: ".connectedSortable",
        cancel: ".disabled",
    	cursor: "move",
    	placeholder: "note-alpha",
    	start: function(e,ui) { 
            $(ui.placeholder).hide("slow"); // Remove popping
        },
        change: function(e,ui) {
            $(ui.placeholder).hide().show("normal");
        },
        stop: function(e,ui) {
            var noteObj = ui.item;
            var noteID = noteObj.attr('id');
            var position = noteObj.parent().attr('headers').split("-");

            $.ajax({
                type: "POST",
                url: "../update_position/",
                data: {
                    noteid: noteID,
                    column: position[0],
                    row: position[1]
                }
            }).fail(function(jqXHR, textStatus) {
                $.gritter.add({
                    title: errorMsg,
                    text: errorSavePos + ' ' + textStatus,
                    image: alertIcon
                });
            });
        }
    }).disableSelection();
}

/* DEBATE CREATION */

var tdlength = 0;

function addTableColumn() {
    /*
        addTableColumn() - Create a new column ny creating a new sortable TD in
        all the rows.
    */
    var tableID = $('table').attr('id');
    var inputs = $('#' + tableID + ' input').length;
    var tdlength = $('#' + tableID + ' td').length;
    var criteriacount = $('#' + tableID + ' th[id^=debate-vcriteria]').length;
    var formCount = parseInt($('#id_colform-TOTAL_FORMS').val());

    if (criteriacount >= 7) {
        $.gritter.add({
            title: adviceMsg,
            text: advice,
            image: alertIcon,
            sticky: true
        });
    };
    $('#' + tableID + ' tr:first').append("<th id='debate-vcriteria" + (criteriacount+1) + "' class='criteria-vtitle'><input id='" + tableID + "-criteria" + (inputs+1) + "' name='colform-" + (criteriacount) + "-criteria' type='text' class='small'></th>");
    $('#' + tableID + ' tbody tr').each(function(){
        //var tdlength = $('#' + tableID + ' td').length;
        $(this).append("<td id='sortable" + (tdlength) + "-" + tableID + "' class='connectedSortable'></td>").fadeIn("slow");
        tdlength += 1;
    });
    $('#id_colform-TOTAL_FORMS').val(formCount + 1);
    makeSortable();
}

function addTableRow() {
    /*
        addTableRow() - Creates a new row in the debate table, it has no limits
        no warnings and no validations. The validations are done by django
        in the form.
    */
    var tableID =$('table').attr('id');
    var criteriacount = $('#' + tableID + ' th[id^=debate-vcriteria]').length;
    var tdlength = $('#' + tableID + 'td').length;
    var formCount_row = parseInt($('#id_rowform-TOTAL_FORMS').val());

    var t = $('table');
    var numColumns = $('th[id^=debate-vcriteria]', t).length;
    var numRows = $('td[class=criteria-htitle]', t).length;
    if (numRows >= 10) return false;

    var tr = $('<tr>');
    tr.append("<td class='criteria-htitle'><div id='debate-ttitle'><input style='width:100px;' id='" + tableID + "-criteria" + (numRows) + "' name='rowform-" + (numRows) + "-criteria' type='text'></div></td>");
    $('#id_rowform-TOTAL_FORMS').val(formCount_row + 1);
    for (i=0; i<numColumns; i++) {
        tr.append('<td>');
    }
    t.append(tr);

}

function removeTableRow() {
    /*
        removeTableRow() - Deletes the last row, unless there is only one,
        in which case it will show up a message.
    */
    var t = $('table');
    var numRows = $('td[class=criteria-htitle]', t).length;
    var formCount_row = parseInt($('#id_rowform-TOTAL_FORMS').val());
    if (numRows < 2) {
        $.gritter.add({
            title: errorMsg2,
            text: errorCRDelete + ' ' + textStatus,
            image: alertIcon
        });
    };
    $('tbody tr:last-child').fadeOut("fast", function() {
        $(this).remove();
    $('#id_rowform-TOTAL_FORMS').val(formCount_row - 1);

    });

}

function removeTableColumn() {
    /*
        removeTableColumn() - Deletes the last column (all the last TDs).
    */
    var tableID = $('table').attr('id');
    var formCount = parseInt($('#id_colform-TOTAL_FORMS').val());
    var columns = $('#' + tableID+ ' tr:last td').length;
    if (columns > 2) {
        $('#' + tableID + ' th:last-child, #' + tableID + ' td:last-child').fadeOut("fast", function() {
            $(this).remove();
        $('#id_colform-TOTAL_FORMS').val(formCount - 1);

        });
    } 
    else {
        $.gritter.add({
            title: errorMsg2,
            text: errorCRDelete + ' ' + textStatus,
            image: alertIcon
        });
    }
}

function saveTable() {
    /*
        saveTable() - Saves the table data. Instead of using a standard form,
        we submite the data trough ajax post, and treat it as a form in the
        django view.
    */
    $('#ajaxform').submit( function(e) {
        var tableID = $('table').attr('id');

        var xvalues = [];
      //  var xfields = $('th.criteria-vtitle :input');
      //  $.each(xfields, function(i, field){
      //      xvalues.push(field.value);
      //  });
        $('#id_columns').val(xvalues);
        var sortable = [];
        var rows = $('#' + tableID + ' tbody tr');
        $.each(rows, function(i, field) {
            var rowID = this.attr('id');
            $(rowID + ' td').each(function() {
                sortable.push($(this).attr('id'));
            })
    //        alert('Estos son los sortables: ' + sortable[0]);
            $(this).val(sortable);
            sortable.length = 0;
        });
    });
}

/*******************
    MAIN LOOP
********************/

$(document).ready(function() {
    // Activate sortables
    makeSortable();
    // Show controls for some notes
    showControls();
    saveTable();
});

