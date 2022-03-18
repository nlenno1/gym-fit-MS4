// Tab View Control
$('.profile-menu-button').click(function(){
    // When button is clicked, make the correct section visible 
    // and hide all others
    section = this.id.slice(0, -7);
    $('#' + section).show();
    $(".profile-section").not($('#' + section)).hide();
    $("#visible-section-name").html(section.replace(/-/g, " ").toUpperCase());
});
// Show personal details section on loading the page
$(document).ready(function(){
    $('#personal-details').show();
});