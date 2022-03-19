// Disable/Enable and control the value of the "amount of
// tokens" field due to the selection of the package type input
$('#id_type').change(function () {
    if (this.value == "UU"){
        $("#id_amount_of_tokens").prop('disabled', true);
        $("#id_amount_of_tokens").val('');
    } else {
        $("#id_amount_of_tokens").prop('disabled', false);
    }
});

$('document').ready(function () {
    if ($('#id_type')[0].value == "UU"){
        $("#id_amount_of_tokens").prop('disabled', true);
        $("#id_amount_of_tokens").val('');
    } else {
        $("#id_amount_of_tokens").prop('disabled', false);
    }
})