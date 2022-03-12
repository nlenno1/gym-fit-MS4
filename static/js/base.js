/* Open Mobile Menu */
function openNav() {
  document.getElementById("mobileNav").style.height = "100%";
}
/* Close Mobile Menu */
function closeNav() {
  document.getElementById("mobileNav").style.height = "0%";
}

// Popovers taken from Boostrap Documentation (https://getbootstrap.com/docs/5.0/components/popovers/)
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})

var option = {
  autohide: true,
  delay: 5000,
}

window.onload = (event) => {
  // Initialize toasts 
  var toastElList = [].slice.call(document.querySelectorAll('.toast'))
  var toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl, option).show()
  })
}

// Date formatting taken from Stack Overflow (https://stackoverflow.com/questions/32378590/set-date-input-fields-max-date-to-today)
var datePickerMinValue = new Date().toISOString().split("T")[0];
$('#date-picker').attr('min', datePickerMinValue)

// Adding css to allauth templates through JS 
$(".allauth-form-inner-content .text-center a").each(function() {
  $(this).addClass("btn btn-dark");
});
$(".allauth-form-inner-content .text-center input:submit").each(function() {
  $(this).addClass("btn btn-dark blue-button");
});
$(".allauth-form-inner-content .text-center button:submit").each(function() {
  $(this).addClass("btn btn-dark blue-button");
});

// Confirm Delete taken from https://stackoverflow.com/questions/37398416/django-delete-confirmation
$(document).on('click', '.confirm-delete', function(){
  return confirm('Are you sure you want to delete this?');
})

// Confirm Delete taken from https://stackoverflow.com/questions/37398416/django-delete-confirmation
$(document).on('click', '.confirm-remove', function(){
  return confirm('Are you sure you want to remove this?');
})

// Confirm Cancellation 
$(document).on('click', '.confirm-cancel', function(){
  return confirm('Are you sure you want to cancel this booking?');
})