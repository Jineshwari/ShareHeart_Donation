from django.db import connection
from django.http import HttpResponse  
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .forms import NGOForm, UserForm
from .models import  User, DonorInfo, Voucher
from django.contrib import messages  # Import messages for user feedback
from django.contrib.auth.decorators import login_required
import random
from django.shortcuts import render
from django.http import JsonResponse




def home(request):
    return render(request, 'home.html')

def home2(request):
    return render(request, 'home2.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def donate(request):
    if request.method == 'POST':
        # Get donation quantities
        books = int(request.POST.get('books', 0))
        shoes = int(request.POST.get('shoes', 0))
        stationary = int(request.POST.get('stationary', 0))
        clothes = int(request.POST.get('clothes', 0))
        food = int(request.POST.get('food', 0))
        toys = int(request.POST.get('toys', 0))

        # Get donor information
        name = request.POST.get('name')
        donor_id = request.POST.get('donor')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        pick_up = request.POST.get('pick_up')

        # Get or create User
        user, created = User.objects.get_or_create(user_id=donor_id)
        
        # Create DonorInfo
        donor_info = DonorInfo.objects.create(
            books=books,
            shoes=shoes,
            stationary=stationary,
            clothes=clothes,
            food=food,
            toys=toys,
            name=name,
            donor=user,
            phone=phone,
            address=address,
            pin=pin,
            pick_up=pick_up
        )
        
        # Redirect to a success page
        return redirect('home2')
    
    return render(request, 'donate.html')
    


def donate2(request):
    return render(request, 'donate2.html')

def donate3(request):
    return render(request, 'donate3.html')

def rewards(request):
    vouchers = Voucher.objects.all()  # Fetch all vouchers from the database
    user_data = None  # Initialize variable to hold user data
    message = ""  # Initialize message for redemption feedback

    if request.method == "POST":
        if 'user_id' in request.POST:  # Check if user ID is submitted
            user_id = request.POST.get('user_id')  # Get user ID from form input
            print(f"User ID entered: {user_id}")  # Debugging line

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        u.user_id,
                        COUNT(di.donor_id) * 100 AS redeemable_points
                    FROM 
                        user u
                    LEFT JOIN 
                        home_donorinfo di ON u.user_id = di.donor_id
                    WHERE 
                        u.user_id = %s
                    GROUP BY 
                        u.user_id;
                """, [user_id])  # Pass user ID as parameter

                user_data = cursor.fetchone()  # Fetch single result

            print(f"Query Result: {user_data}")  # Debugging line to check what is returned

        elif 'redeem' in request.POST:  # Check if a voucher is being redeemed
            selected_voucher_id = request.POST.get('voucher_id')
            print(f"Voucher ID selected for redemption: {selected_voucher_id}")  # Debugging line
            
            try:
                selected_voucher = Voucher.objects.get(voucher_id=selected_voucher_id)

                # Generate a random redemption code
                redemption_code = f"CODE-{random.randint(1000, 9999)}"
                
                # Create a message for the user
                message = f"Use this code at checkout: {redemption_code}"
            
            except Voucher.DoesNotExist:
                message = "Selected voucher does not exist."

    return render(request, 'rewards.html', {'vouchers': vouchers, 'user_data': user_data, 'message': message})


def user_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            # Retrieve the user based on user_id
            user = User.objects.get(user_id=user_id)

            # Check if the password matches
            if user.password == password:  # Compare plain text passwords
                # Assuming you want to log in the user, you can set session variables
                request.session['user_id'] = user.user_id
                return JsonResponse({'status': 'success', 'redirect': '/'})  # Redirect to home or any other page
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid password'})
        
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})

    return render(request, 'user_login.html')  # Adjust the template name as needed




def ngo_login(request):
    return render(request, 'ngo_login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the existing user table
            messages.success(request, 'User registration successful!')
            return redirect('home2')  # Redirect to the success page
        else:
            messages.error(request, 'There was an error in your registration. Please try again.')
    else:
        form = UserForm()
    
    return render(request, 'user_register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NGOForm

def ngo_register(request):
    if request.method == 'POST':
        form = NGOForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the existing ngo table
            messages.success(request, 'NGO registration successful!')
            return redirect('home2')  # Redirect to the success page
        else:
            messages.error(request, 'There was an error in your registration. Please try again.')
    else:
        form = NGOForm()
    
    return render(request, 'ngo_register.html', {'form': form})


def success_view(request):
    return HttpResponse('Registration successful!')


def account(request):
    # Execute the SQL JOIN query
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                u.first_name AS user_name, 
                d.pick_up AS pickup_date, 
                d.phone AS phone_number,
                u.house_no AS house,
                u.city AS u_city  
            FROM 
                user u
            JOIN 
                home_donorinfo d ON u.user_id = d.donor_id  
            WHERE 
                d.pick_up >= CURDATE();  
        """)
        
        # Fetch all results from the query
        pickups = cursor.fetchall()

    # Pass the fetched data to the template
    return render(request, 'account.html', {'pickups': pickups})


# Catch-all dynamic view
def dynamic_page(request, page):
    return HttpResponse(f"You have navigated to: {page}")


