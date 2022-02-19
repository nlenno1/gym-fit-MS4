from django.shortcuts import render

def view_class_access_packages(request):
    """ A view to return the class access packages available"""

    return render(request, 'products/join_us.html')
