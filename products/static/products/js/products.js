// Disable input for amount of tokens if Unlimited Use selected 
$('#id_type').change(function () {
    if (this.value == "UU"){
        $("#id_amount_of_tokens").prop('disabled', true);
        $("#id_amount_of_tokens").val('');
    } else {
        $("#id_amount_of_tokens").prop('disabled', false);
    }
})  