/*
    role_edit.js - Javascript code describing all the functions for the role
    changes of the users.

    License: GPLv3
    Copyright: 2013 Cidadania S. Coop. Galega
    Author: Oscar Carballal Prego <info@oscarcp.com>
*/

var errorTitle = gettext("An error has ocurred.");
var errorMsg = gettext("Couldn't add/change user permissions.");
var saveTitle = gettext("Changes saved");
var saveMsg = gettext("The changes have been saved successfully.");

var alertIcon = 'http://ecidadania.org/static/assets/icons/alert.png';
var saveIcon = "http://files.softicons.com/download/toolbar-icons/crystal-office-icon-set-by-mediajon/png/48x48/checkmark.png";

function makeSortable() {
    /*
        makeSortable() - Makes every element with id starting by 'sortable'
        sortable through the connectedSortable class lists. It uses jQuery
        Sortable. This function has to be called whenever a new element is on
        the page (note, table column or row) to make the new elements sortable.
    */
    
    // Get all the div elements starting by sortable
    $("#users, #admins, #mods, #delete").sortable({
        connectWith: ".connectedSortable",
        cancel: ".disabled",
        cursor: "move",
        placeholder: "user-placeholder",
        start: function(e,ui) { 
            $(ui.placeholder).hide("slow"); // Remove popping
        },
        change: function(e,ui) {
            $(ui.placeholder).hide().show("normal");
        },
        stop: function(e,ui) {
            var userObj = ui.item;
            var userID = userObj.attr('id');
            var perm = userObj.parent().attr('id');

            $.ajax({
                type: "POST",
                url: ".", /* Send to the same url */
                data: {
                    userid: userID,
                    perm: perm,
                }
            }).done(function(jqXHR, textStatus) {
                $.gritter.add({
                    title: saveTitle,
                    text: saveMsg,
                    image: saveIcon
                });
            }).fail(function(jqXHR, textStatus) {
                $.gritter.add({
                    title: errorTitle,
                    text: errorMsg,
                    image: alertIcon
                });
            });
        }
    }).disableSelection();
}

$(document).ready(function() {
    // Activate sortables
    makeSortable();
});