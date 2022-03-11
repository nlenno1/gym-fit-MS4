// Tab View Control
$('.profile-menu-button').click(function(){
    section = this.id.slice(0, -7)
    $('#' + section).show();
    $(".profile-section").not($('#' + section)).hide();
    $("#visible-section-name").html(section.replace(/-/g, " ").toUpperCase());
})
$(document).ready(function(){
    $('#personal-details').show();
})