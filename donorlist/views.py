from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from donorlist.helpers import geocode, get_latitude, get_longitude, miles
from .forms import ProfileUpdateForm, EmailSendForm
from django.contrib import messages
from django.db.models import Q
from django.core.mail import EmailMessage


# Defines view for default call to home
def home(request):
	return render(request, 'donorlist/home.html')

# Register a new user
def registeruser(request):
	# If request is a 'GET', return the registeruser template
	if request.method == 'GET':
		return render(request, 'donorlist/registeruser.html', {'form':UserCreationForm()})
	# If request is a 'POST', validate data and submit user to database
	else:
		# Check that user entered matching password twice
		if request.POST['password1'] == request.POST['password2']:
			# Attempt to insert user into database or return IntegrityError
			try:
				# Create instance of a user object
				user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
				# Save user object into database
				user.save()
				# After someone signs up, log them in
				login(request, user)
				# After logging them in, redirect over to the updateprofile.html page; need to return the redirect
				return redirect('updateprofile')
			# Handle username that is already taken
			except IntegrityError:
				# Reload the registration page with an error notification
				return render(request, 'donorlist/registeruser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
		else:
			# If passwords don't match, send them the signup form again but tell them passwords don't match
			return render(request, 'donorlist/registeruser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

# Login in an existing user
def loginuser(request):
	# If request is a 'GET', return the user login template
	if request.method == 'GET':
		return render(request, 'donorlist/loginuser.html', {'form':AuthenticationForm()})
	# If request is a 'POST', validate user data and log user in
	else:
		# Check whether the username and password entered are valid
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		# If user does not exist or password invalid, notify user and return login form again
		if user is None:
			return render(request, 'donorlist/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
		else:
			# Log the user in
			login(request, user)
			# After logging them in, redirect user to the homepage
			return redirect('home')

# Log out a user that is currently signed in
@login_required
def logoutuser(request):
	# Check for POST to prevent browser from prematurely logging user out
	if request.method == 'POST':
		# Log user out
		logout(request)
		# Redirect user to home page after logout
		return redirect('home')

@login_required
def updateprofile(request):
	# If request method is POST, proceed to validate new profile details
	if request.method == 'POST':
		# Pass POST request data to ProfileUpdateForm
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		# Set up context appropriately
		context = {
			'p_form': p_form
		}
		# Check that the profile updates are valid
		if p_form.is_valid():
			# Save the updated profile information without commiting it
			new_profile = p_form.save(commit = False)
			# Fetch geocoding information given user's city
			city_results = geocode(new_profile.city)
			# Set the updated profile's latitute accordingly
			new_profile.latitude = get_latitude(city_results)
			# Set the updated profile's longitude accordingly
			new_profile.longitude = get_longitude(city_results)
			# Save the updated profile to the database
			new_profile.save()
			# Record success message
			messages.success(request, f'Your Profile has been Updated Successfully')
			# Redirect back to profile update page
			return redirect('updateprofile')
	# If request method is GET, return profile update form and don't edit database
	else:
		# Pass current user profile data to ProfileUpdateForm
		p_form = ProfileUpdateForm(instance=request.user.profile)
		# Set up context accordingly
		context = {
			'p_form': p_form
		}
	# Return update profile templat
	return render(request, 'donorlist/updateprofile.html', context)

# Show user their top blood donor options
@login_required
def viewdonors(request):
	# Pull donor matches
	donor_context = pull_donor_matches(request)
	return render(request, 'donorlist/viewdonors.html', donor_context)

@login_required
def email_donors(request):
	# Create EmailSendForm instance
	e_form = EmailSendForm()
	# Construct email context for template
	email_context = {"status_message": "", "e_form": e_form}
	# If request method is POST, proceed to process donor request emails
	if request.method == "POST":
		# Pass POST request data to EmailSendForm
		e_form = EmailSendForm(request.POST)
		# Check that the email is vlaid
		if e_form.is_valid():
			# Pull matched donors
			donor_list = pull_donor_matches(request)['donors']
			# Strip out donor emails from donor_list
			donor_emails = [donor["email_address"] for donor in donor_list]
			email = EmailMessage('Blood Donation Request', e_form.cleaned_data["mail_body"], to=donor_emails)
			# Send email, making sure not to crash the server if a user has submitted an invalid email address
			email.send(fail_silently=True)
			# Set status message to let users know that emails were successfully sent
			email_context['status_message'] = "Emails successfully sent!"
			# Reload the website with the updated email context
			return render(request, "donorlist/emaildonors.html", email_context)
		else:
			# If the form is invalid, set the status message accordingly
			email_context['status_message'] = "We were unable to process your request. Please try again later"
			return render(request, "donorlist/emaildonors.html", email_context)
	# If here, it's a GET request, so render email form template
	return render(request, "donorlist/emaildonors.html", email_context)

# Blood match DB pull
def pull_donor_matches(request):
	# Load in user details
	user = request.user
	# Load in user's bloodtype
	bloodtype = user.profile.blood_type
	# Store acceptable matches given an user's bloodtype
	matches = {}
	matches['ab+'] = ['o-', 'o+', 'a-', 'a+', 'b-', 'b+', 'ab-', 'ab+']
	matches['ab-'] = ['ab-', 'a-', 'b-', 'o-', 'x', 'x', 'x', 'x']
	matches['a+'] = ['o-', 'o+', 'a-', 'a+', 'x', 'x', 'x', 'x']
	matches['a-'] = ['o-', 'a-', 'x', 'x', 'x', 'x', 'x', 'x']
	matches['b+'] = ['o-', 'o+', 'b-', 'b+', 'x', 'x', 'x', 'x']
	matches['b-'] = ['o-', 'b-', 'x', 'x', 'x', 'x', 'x', 'x']
	matches['o+'] = ['o-', 'o+', 'x', 'x', 'x', 'x', 'x', 'x']
	matches['o-'] = ['o-', 'x', 'x', 'x', 'x', 'x', 'x', 'x']

	# Get valid matches given user's bloodtype
	validmatches = matches[bloodtype]

	# Q object for more complex queries
	q = Q()
	# Loop through valid matches
	for match in validmatches:
		# Update query to include current valid match
		q |= Q(blood_type__icontains = match)
	# Filter donors based on query constructed above
	donors = Profile.objects.filter(q)
	# Get donors within 50 miles, excluding the user themselves.
	wanted_donors = [donor.id for donor in donors if miles(user.profile.latitude, user.profile.longitude, donor.latitude, donor.longitude) < 50 and donor.user != user]
	# Filter out these donors
	donors = donors.filter(user__in=wanted_donors)
	# List of donors
	donor_list = []
	# Loop through filtered donors
	for donor in donors.iterator():
		# Dictionary into which we'll translate a donor instance
		context_object = {}
		# Loop through the fields of the donor instance
		for value in donor.fields:
			# Set the values of our custom object attributes accordingly
			context_object[value] = getattr(donor, value)
		# Convert blood type to upper case
		context_object['blood_type'] = context_object['blood_type'].upper()
		# Calculate distance between logged in user and current donor
		dist = miles(user.profile.latitude, user.profile.longitude, donor.latitude, donor.longitude)
		# Only need one decimal place
		distance = float("{:.1f}".format(dist))
		# Set the distance attribute to the calculated and transformed distance value
		context_object['distance'] = distance
		# Add to list of donors
		donor_list.append(context_object)

	# Sort donors by distance from user (from lowest to largest)
	donor_list = sorted(donor_list, key=lambda x: x['distance'])
	donor_context = {'donors': donor_list}
	return donor_context
