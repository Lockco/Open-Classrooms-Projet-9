from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from followers.forms import CustomUserChangeForm, FollowForm
from followers.models import UserFollows
import json


def signup(request: HttpRequest) -> HttpResponse:
	"""permet à un nouvel utilisateur de s'inscrire en créant un compte utilisateur"""

	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('reviews:home')
	else:
		form = UserCreationForm()
	return render(request, 'followers/signup.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
	"""permet à un utilisateur existant de se connecter à son compte"""

	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				auth.login(request, user)
				return redirect('reviews:home')
	form = AuthenticationForm()
	return render(request, 'followers/login.html', {'form': form})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
	"""permet à l'utilisateur de voir et modifier son propre profil"""

	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('followers:profile')
	else:
		form = CustomUserChangeForm(instance=request.user)
	return render(request, 'followers/profile.html', {'form': form})


@login_required(login_url='followers:login')
def logout_view(request: HttpRequest) -> HttpResponse:
	"""permet à l'utilisateur de se déconnecter de son compte"""

	logout(request)
	return redirect('reviews:home')


@login_required(login_url='followers:login')
def search_user(request: HttpRequest) -> HttpResponse:
	"""Permet de rechercher un utilisateur dans la base de données en utilisant une requête AJAX"""

	if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
		q = request.GET.get('term', '')
		users = User.objects.filter(username__icontains=q)
		results = []
		for user in users:
			user_json = {'id': user.id, 'label': user.username, 'value': user.username}
			results.append(user_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)


@login_required(login_url='followers:login')
def follow_user(request: HttpRequest) -> HttpResponse:
	""": permet à l'utilisateur de suivre d'autres utilisateurs"""

	if request.method == 'POST':
		form = FollowForm(request.POST)
		if form.is_valid():
			followed_username = form.cleaned_data['username']
			try:
				followed_user = User.objects.get(username=followed_username)
				follow = UserFollows(user=request.user, followed_user=followed_user)
				follow.save()
				return redirect('followers:follow')
			except User.DoesNotExist:
				form.add_error('username', 'Utilisateur non trouvé')
	else:
		form = FollowForm()
	follows = UserFollows.objects.filter(user=request.user)
	follow_by = UserFollows.objects.filter(followed_user_id=request.user.id)
	followed_users = [follow.followed_user for follow in follows]
	return render(request, 'followers/follow_form.html',
	              {'followed_users': followed_users, 'form': form, 'follow_by': follow_by}
	              )


@login_required
def unfollow(request: HttpRequest, user_id: int) -> HttpResponse:
	"""permet à l'utilisateur d'arrêter de suivre un autre utilisateur"""

	user_to_unfollow = User.objects.get(pk=user_id)
	request.user.follower.filter(followed_user=user_to_unfollow).delete()
	return redirect('followers:follow')
