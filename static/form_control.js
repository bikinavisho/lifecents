var $incomeCountEl = $('#income-count');
var $expenseCountEl = $('#expense-count');

function addIncome() {
    var incomeCount = $incomeCountEl.val();
    var newCount = parseInt(incomeCount) + 1;

    var $newSection = $('<fieldset class="pure-group" id="in'+newCount.toString()+'"><input type="text" class="pure-input-1" name="income'+newCount.toString()+'" placeholder="Income"><div class="input-icon"><i>$</i><input type="number" class="pure-input-1" name="income-value'+newCount.toString()+'" placeholder="Amount"></div></fieldset>');

    $('#in'+incomeCount.toString()).after($newSection);
    $incomeCountEl.val(newCount);
    $incomeCountEl.attr('value', newCount);
}

function addExpense() {
    var expenseCount = $expenseCountEl.val();
    var newCount = parseInt(expenseCount) + 1;

    var $newSection = $('<fieldset class="pure-group" id="ex'+newCount.toString()+'"><input type="text" class="pure-input-1" name="expense'+newCount.toString()+'" placeholder="Expense"><div class="input-icon"><i>$</i><input type="number" class="pure-input-1" name="expense-value'+newCount.toString()+'" placeholder="Amount"></div></fieldset>');

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

});




