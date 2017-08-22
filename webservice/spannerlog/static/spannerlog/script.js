
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// pre-submit callback 
function showRequest(formData, jqForm, options) { 
    // formData is an array; here we use $.param to convert it to a string to display it 
    // but the form plugin does this for you automatically when it submits the data 
    var queryString = $.param(formData); 
 
    // jqForm is a jQuery object encapsulating the form element.  To access the 
    // DOM element for the form do this: 
    // var formElement = jqForm[0]; 
 
    console.log(formData);
 
    // here we could return false to prevent the form from being submitted; 
    // returning anything other than false will allow the form submit to continue 
    return true; 
} 

// post-submit callback 
function handleResponse(responseText, statusText, xhr, $form)  { 
    // for normal html responses, the first argument to the success callback 
    // is the XMLHttpRequest object's responseText property 
 
    // if the ajaxForm method was passed an Options Object with the dataType 
    // property set to 'xml' then the first argument to the success callback 
    // is the XMLHttpRequest object's responseXML property 
 
    // if the ajaxForm method was passed an Options Object with the dataType 
    // property set to 'json' then the first argument to the success callback 
    // is the json data object returned by the server 
 
    console.log(responseText);
    console.log(xhr);

    var schema = xhr.responseJSON

    // Remove table dummy from results set
    var index = schema.indexOf("dummy");
    if (index > -1) {
      schema.splice(index, 1);
    }

    // Empty divs
    $('#database').empty();

    // Add selector for available tables to display
    $('#database').append(`
      <h4 class="red">Tables:</h4>
      <div class="col-sm-2" style="margin-bottom: 15px;">
          <label for="tables" class="label">&mdash; Displayed Table &mdash;</label>
          <select id="tables" name="tables" data-placeholder="tables" class="chosen-select" title="tables">
          </select>
      </div>
      <div id="table-active-container"></div>
      `);

    // Add available tables to select
    $.each(schema, function(index, tableName){
      $('#tables').append('<option value="' + tableName + '">' + capitalizeFirstLetter(tableName) + '</option>');
    });

    // Select table Q if defined. Otherwise, choose the first one
    if ($.inArray("q", schema)) {
      $("#tables").val("q");
    } else {
      $("#tables").val(schema[0]);
    }

    // Add listener to table selector
    $("#tables").change(renderTable);

    // Render selected table
    renderTable();

    $('#loading').hide();
    $('.corenlp_error').remove();  // Clear error messages
    $('#database').show();
} 

function renderTable() {
  var tableName = $("#tables").val()
  console.log("Rendering table " + tableName)

  // Empty div
  $('#table-active-container').empty();

  $('#table-active-container').append('<table id="table-active" class="table table-bordered"></table>');
}

function handleError(data) {
    DATA = data;
    var alertDiv = $('<div/>').addClass('alert').addClass('alert-danger').addClass('alert-dismissible').addClass('corenlp_error').attr('role', 'alert')
    var button = $('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>');
    var message = $('<span/>').text(data.responseText);
    button.appendTo(alertDiv);
    message.appendTo(alertDiv);
    $('#loading').hide();
    alertDiv.appendTo($('#errors'));
    $('#submit').prop('disabled', false);
}

// ----------------------------------------------------------------------------
// MAIN
// ----------------------------------------------------------------------------

/**
 * MAIN()
 *
 * The entry point of the page
 */
$(document).ready(function() {

  // Submit on clicking the 'submit' button
  $('#submit').click(function() {
    // Get the program to run    
    currentQuery = $('#text').val();
    if (currentQuery.trim() == '') {
      currentQuery = 'Q(s[x]) <- Articles(_,s,_,_,_,_), NER<s>(x, "ORGANIZATION").';
      $('#text').val(currentQuery);
    }
  });

  var options = { 
      dataType:  'json',  // dataType identifies the expected content type of the server response 
      // target:        '#output1',   // target element(s) to be updated with server response 
      beforeSubmit:  showRequest,  // pre-submit callback 
      success:       handleResponse,  // post-submit callback 
      error:         handleError

      // other available options: 
      //url:       url         // override for form's 'action' attribute 
      //type:      type        // 'get' or 'post', override for form's 'method' attribute 
      //dataType:  null        // 'xml', 'script', or 'json' (expected server response type) 
      //clearForm: true        // clear all form fields after successful submit 
      //resetForm: true        // reset the form after successful submit 

      // $.ajax options can be used here too, for example: 
      //timeout:   3000 
  }; 
  // bind form using 'ajaxForm' 
  $('#form_execute').ajaxForm(options); 

});