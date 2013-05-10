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
var confirmDelete = gettext('Are you sure?');
var userTitle = gettext('User added to users group');
var userMsg = gettext('The user has been successfully added to the users list.');
var userDel = gettext('Delete user');

var alertIcon = 'http://ecidadania.org/static/assets/icons/alert.png';
var saveIcon = "http://files.softicons.com/download/toolbar-icons/crystal-office-icon-set-by-mediajon/png/48x48/checkmark.png";

function searchUser() {
    /*
        searchUser() - Send an AJAX POST to the server in search of the strict
        username the user wrote. If the user doens't exist it returns a 404,
        if id exists, it adds it to the users list and gets the ID from the
        server in case you want to change it from column.
    */
    $("#user-search-btn").click(function(e) {
        e.preventDefault();
        var userName = $("#user-search").val();

        $.ajax({
            type: "POST",
            url: "../search_user/", /* Send to the same url */
            data: {
                uname: userName,
            }
        }).success(function(data, textStatus, jqXHR) {
            $.gritter.add({
                title: "User added to users group",
                text: "The user has been added successfully to the users list.",
                image: saveIcon,
                time: 4000
            });
            $("ul#users").append("<li id='" + data + "' class='ui-state-default'>" + userName + "<a href='#' class='pull-right delete' title='" + userDel + " " + userName + "'><i class='icon-remove'></i></a><li>");
        }).fail(function(jqXHR, textStatus) {
            $.gritter.add({
                title: errorTitle,
                text: errorMsg,
                image: alertIcon
            });
        });
    })
}

function deleteUserFromSpace() {
    /*
        deleteUserFromSpace() - Sends the deletion command to the backend along
        with the user ID for deleting all the permissions for that user in the
        current space.
    */

    $(".delete").click(function(event) {
        event.preventDefault();
        var answer = confirm(confirmDelete);
        var userID = $(this).parent().attr("id");
        var currentEl = $(this)

        if (answer) {
            $.ajax({
                type: "POST",
                url: ".", /* Send to the same url */
                data: {
                    userid: userID,
                    perm: "delete"
                }
            }).done(function(jqXHR, textStatus) {
                $.gritter.add({
                    title: saveTitle,
                    text: saveMsg,
                    image: saveIcon
                });
                currentEl.parent().remove();
            }).fail(function(jqXHR, textStatus) {
                $.gritter.add({
                    title: errorTitle,
                    text: errorMsg,
                    image: alertIcon
                });
            });
        };
    });
}

function changeUserPermissions() {
    /*
        changeUserPermission() - Handles the user permissions. It submits the
        ul ID to the server, and the server matches it with a set of permissions
        that will be given to the user.
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
    changeUserPermissions();
    deleteUserFromSpace();
    searchUser();
});