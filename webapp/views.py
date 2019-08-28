from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# This file makes the client app logic


def index(request):
	return render(request, 'webapp/home.html',context={"userConnected":request.user})

def register(request):

	# If you are already inside the registration page and are submitting your form, the logic happens here.
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New account created: {username}")
			login(request, user)
			messages.info(request, f"You are now logged in as: {username}")
			return redirect("main:index")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")

	# Render the registration page and pass it the premade Django form
	form = UserCreationForm
	return render(request,
				  "webapp/register.html",
				  context={"form":form})
				  
				  
def login_request(request):

	# If you are already inside the login page and are submitting your form, the logic happens here.
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as: {username}")
				return redirect("main:index")
			else:
				messages.error(request,"Invalid username or password")
		else:
			messages.error(request,"Invalid username or password")
	
	# Render the login page and pass it the premade Django form
	form = AuthenticationForm()
	return render(request,
				  "webapp/login.html",
				  {"form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "Logged out succesfully!")
	return redirect("main:index")