from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib  import messages
from django.conf import settings
from django.contrib.auth.models import User  # Ensure this is imported
from django.core.exceptions import ObjectDoesNotExist

User = settings.AUTH_USER_MODEL


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            new_user = form.save()

            # Retrieve cleaned data
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")  # UserCreationForm uses `password1`

            # Display a success message
            messages.success(request, f"Hey {username}, your account was created successfully!")

            # Authenticate and log in the new user
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect("Grocery:index")
            else:
                print(messages.error(request, "Account creation succeeded, but login failed. Please log in manually."))

    else:
        form = UserRegisterForm()  # Show an empty form for GET requests

    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)


# def login_view(request):
#     # Redirect to home if the user is already authenticated
#     if request.user.is_authenticated:
#         messages.info(request, "You are already logged in.")
#         return redirect("Grocery:index")
#
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#
#         if not email or not password:
#             messages.warning(request, "Both email and password are required.")
#             return render(request, "userauths/sign-in.html", {"email": email})
#
#         try:
#             # Retrieve user by email
#             user = User.objects.get(email=email)
#
#             # Authenticate using the username and password
#
#         except :
#             messages.warning(request, f"No user found with the email {email}.")
#             print("nousers found")
#             return render(request, "userauths/sign-in.html", {"email": email})
#
#         user = authenticate(request, email=email, password=password)
#
#         if user is not None:
#             login(request, user)
#             messages.success(request, "You are logged in successfully!")
#             print("success")
#             return redirect("Grocery:index")
#         else:
#             messages.warning(request, "Invalid password. Please try again.")
#             print("invalid password")
#
#     # Render the login page if not a POST request or after a failed login
#     return render(request, "userauths/sign-in.html")




def login_view(request):
    # Redirect to home if the user is already authenticated
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("Grocery:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.warning(request, "Both email and password are required.")
            return render(request, "userauths/sign-in.html", {"email": email})

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in successfully!")
            return redirect("Grocery:index")
        else:
            messages.warning(request, "Invalid email or password. Please try again.")

    # Render the login page if not a POST request or after a failed login
    return render(request, "userauths/sign-in.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You are logged out successfully!")
    return redirect("userauths:sign-in")