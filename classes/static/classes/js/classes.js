$(document).ready(function() {
    // Submit form on change of selection in select elements
    $('#date-picker').change(function(){
        $('#date-form').submit();
    });

    $('#category-filter-select').change(function(){
        $('#date-form').submit();
    });
});