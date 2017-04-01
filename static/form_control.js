// Initialization of Socket
//var socket = io();

// Reference to the count of how many income/expense fields there are
var $incomeCountEl = $('#income-count');
var $expenseCountEl = $('#expense-count');

// Function which adds a new Income field
function addIncome() {
    var incomeCount = $incomeCountEl.val();
    var newCount = parseInt(incomeCount) + 1;

    var $newSection = $('<fieldset class="pure-group" id="in'+newCount.toString()+'"><input type="text" class="pure-input-1" name="income'+newCount.toString()+'" placeholder="Income"><div class="input-icon"><i>$</i><input type="number" class="pure-input-1" name="income-value'+newCount.toString()+'" placeholder="Amount" min="0" step="any"></div></fieldset>');

    $('#in'+incomeCount.toString()).after($newSection);
    $incomeCountEl.val(newCount);
    $incomeCountEl.attr('value', newCount);
}

// Function which adds a new Expense field
function addExpense() {
    var expenseCount = $expenseCountEl.val();
    var newCount = parseInt(expenseCount) + 1;

    var $newSection = $('<fieldset class="pure-group" id="ex'+newCount.toString()+'"><input type="text" class="pure-input-1" name="expense'+newCount.toString()+'" placeholder="Expense"><div class="input-icon"><i>$</i><input type="number" class="pure-input-1" name="expense-value'+newCount.toString()+'" placeholder="Amount" min="0" step="any"></div></fieldset>');

    $('#ex'+expenseCount.toString()).after($newSection);
    $expenseCountEl.val(newCount);
    $expenseCountEl.attr('value', newCount);
}

$(document).ready(function() {
    // Initialization of Counts
    $incomeCountEl.val(2);
    $incomeCountEl.attr('value', '2');
    $expenseCountEl.val(2);
    $expenseCountEl.attr('value', '2');

    // Set the Click Triggers and Handlers
    $('#income-plus').click(function(){addIncome();});
    $('#expense-plus').click(function(){addExpense();});

    // Previously existing database values are editable upon double click
    $('.editables').dblclick(function(){
        if($(this).prop('readonly') == true) {
            $(this).prop('readonly',false);
        }
        else {
            //Presumably data has been changed
            $(this).prop('readonly',true);

            //Get the data
            var csrf = $('#csrf').val();
            var thisValue = $(this).val();
            var type = "name";

            // Get id of this item
            var thisId = $(this).attr('id');
            var dbIdId;

            if(thisValue.includes('$')) {
                // The value was edited
                type = "value";
                // Get rid of the dollar sign before passing
                thisValue = thisValue.replace('$', '');
                // Get HTML id of db id
                dbIdId = thisId.replace('v', 'id');

            }
            else {
                // The name was edited
                // Get HTML id of db id
                dbIdId = thisId.replace('n', 'id');
            }
            // Get value of db id
            var dbId = $('#'+dbIdId).val();
            // Send gathered data to server
            socket.emit('json', {'msg': thisValue, 'type': type, 'db-id': dbId,'csrf': csrf});

        }
    });

    //Delete database entry upon click of X
    $('.x-out').click(function(){
        var confirmation = window.confirm("Are you sure you want to delete this entry?");
        if(confirmation) {
            // Get id of this item
            var thisId = $(this).attr('id');
            // Get id of db id item
            var dbIdId = thisId.concat('id');
            var dbId = $('#'+dbIdId).val();
            // Delete the database entry
            socket.emit('deletion', dbId);

            // Remove visually from page
            var $parentDiv1 = $(this).parent();
            var $parentDiv2 = $parentDiv1.parent();
            $parentDiv2.remove();
        }
    });

});


socket.on('connect', function() {
    console.log('user connected');
});

// Receive emit from server
socket.on('message', function(msg) {
    console.log('received message %s', msg);
});

// Receive emit from server
socket.on('json', function(data) {
    console.log('received message %s', data);
});


