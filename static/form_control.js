var $incomeCountEl = $('#income-count');

function addIncome() {
    var incomeCount = $incomeCountEl.val();
    var newCount = parseInt(incomeCount) + 1;

    var $newSection = $('<fieldset class="pure-group" id="in'+newCount.toString()+'"><input type="text" class="pure-input-1" name="income'+newCount.toString()+'" placeholder="Income"><div class="input-icon"><i>$</i><input type="number" class="pure-input-1" name="income-value'+newCount.toString()+'" placeholder="Amount"></div></fieldset>');

    $('#in'+incomeCount.toString()).after($newSection);
    $incomeCountEl.val(newCount);
    $incomeCountEl.attr('value', newCount);
}

$(document).ready(function() {
    $incomeCountEl.val(2);
    $incomeCountEl.attr('value', '2');
    $('#income-plus').click(function(){addIncome();});
});




