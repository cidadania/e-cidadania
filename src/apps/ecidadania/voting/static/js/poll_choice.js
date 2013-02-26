var tdlength = 0;

function addChoice() {
    /*
        addTableColumn() - Create a new column ny creating a new sortable TD in
        all the rows.
    */
    var tableID = $('table').attr('id');
    var inputs = $('#' + tableID + ' input').length;
    var tdlength = $('#' + tableID + ' td').length;
    var criteriacount = $('#' + tableID + ' th[id^=poll-vcriteria]').length;
    var formCount = parseInt($('#id_choiceform-TOTAL_FORMS').val());

    if (criteriacount >= 10) return false;
    $('#' + tableID + ' tr:first').append("<th id='poll-vcriteria" + (criteriacount) +"' class='criteria-vtitle'><input id='id_form-" + (criteriacount+1) +"-choice_text' name='form-" + (criteriacount) + "-choice_text' type='text' maxlength='200'></th>");
    $('#' + tableID + ' tbody tr').each(function(){
        //var tdlength = $('#' + tableID + ' td').length;
        tdlength += 1;
    });
    $('#id_choiceform-TOTAL_FORMS').val(formCount + 1);
}


function removeChoice() {
    /*
        removeTableColumn() - Deletes the last column (all the last TDs).
    */
    var t = $('table');
    var formCount = parseInt($('#id_choiceform-TOTAL_FORMS').val());
    var columns = $('th[class=criteria-vtitle]', t).length;
    if (columns > 2) return false;
        $('#' + t + ' th:last-child, #' + t ).fadeOut("fast", function() {
            $(this).remove();
        $('#id_choiceform-TOTAL_FORMS').val(formCount - 1);

        });
    } 

/*function saveTable() {
    
        saveTable() - Saves the table data. Instead of using a standard form,
        we submite the data trough ajax post, and treat it as a form in the
        django view.
    
    $('#ajaxform').submit( function(e) {
        var tableID = $('table').attr('id');

        var xvalues = [];
      //  var xfields = $('th.criteria-vtitle :input');
      //  $.each(xfields, function(i, field){
      //      xvalues.push(field.value);
      //  });
        $('#id_columns').val(xvalues);
        var rows = $('#' + tableID + ' tbody tr');
        $.each(rows, function(i, field) {
            var rowID = this.attr('id');
            })
        });
}
*/
/*******************
    MAIN LOOP
********************/

$(document).ready(function() {
    // Activate javascript notifications.
    $('#jsnotify').notify();
    // Activate sortables
    // Show controls for some notes
 //   saveTable();
});

