from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Medicine, Purchase
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    """ Function for displaying main page of Medical Store. """

    # Getting all the medicines from the database
    medicines = Medicine.objects.all()

    # Storing all the medicines available inside context variable
    context = {
        "medicines" : medicines.order_by('name')
    }

    # Editing response headers so as to ignore cached versions of pages
    response = render(request, "MedicalStore/medicines.html", context)
    return responseHeadersModifier(response)

def search(request):
    """Function for displaying the search filtered medicines available in the database."""

    # If the user submits a search query
    if request.method == "POST":

        # Extracting the search query from post request
        searchQuery = request.POST["searchQuery"]

        # Getting the search results, i.e.,all the medicines containing
        # the search query as a substring
        searchFilteredMedicines = Medicine.objects.filter(name__contains = searchQuery)

        # Storing the search results inside the context variable
        context = {
            "medicines" : searchFilteredMedicines.order_by('name')
        }

        # Editing response headers so as to ignore cached versions of pages
        response = render(request, "MedicalStore/medicines.html", context)
        return responseHeadersModifier(response)

    # Redirecting if the request method is get as searching requires some input
    elif request.method == "GET":

        # Editing response headers so as to ignore cached versions of pages
        response = HttpResponseRedirect(reverse('MedicalStore:index'))
        return responseHeadersModifier(response)

    # Redirecting if the request method neither post nor get as searching requires some input
    else:

        # Editing response headers so as to ignore cached versions of pages
        response = HttpResponseRedirect(reverse('MedicalStore:index'))
        return responseHeadersModifier(response)

def responseHeadersModifier(response):
    """Funtion to edit response headers so that no cached versions can be viewed. Returns the modified response."""
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response


def buy_medicine(request, medicine_id):
    if request.session.get('isLoggedIn', False):
        if request.method == 'POST':
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            buyer_name = request.session.get('Name', 'Anonymous User')
            buyer_email = request.session.get('userEmail', 'anonymous@example.com')
            # Get selected address from form
            address = request.POST.get('address', 'N/A')
            quantity = 1  # Assuming the user buys one quantity of the medicine
            total_price = medicine.price * quantity

            if medicine.quantity >= quantity:
                medicine.quantity -= quantity
                medicine.save()

                # Create a purchase record with address information
                purchase = Purchase.objects.create(
                    medicine=medicine,
                    buyer_name=buyer_name,
                    buyer_email=buyer_email,
                    quantity=quantity,
                    total_price=total_price,
                    address=address
                )

                success_message = f"Thank you, {buyer_name}! You have successfully purchased {quantity} {medicine.name}."
                return render(request, 'MedicalStore/medicines.html', {'purchase': purchase, 'success_message': success_message})
            else:
                messages.error(
                    request, f"Sorry, {medicine.name} is out of stock.")
                return redirect('MedicalStore:index')
        else:
            # Redirect to the medicine list page if it's not a POST request
            return redirect('MedicalStore:index')
    else:
        messages.error(request, 'You need to be logged in to make a purchase.')
        return redirect('login')

def purchase_history(request):
    # Check if the user is authenticated using session variable
    if request.session.get('isLoggedIn', False):
        purchases = Purchase.objects.filter(
            buyer_email=request.session.get('userEmail')).order_by('-purchase_date')
        return render(request, 'MedicalStore/purchase_history.html', {'purchases': purchases})
    else:
        return redirect('login')
