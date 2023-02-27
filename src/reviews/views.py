from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from followers.models import UserFollows
from reviews.models import Review
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import CharField, Value, Q, QuerySet
from tickets.models import Ticket
from django import forms

from tickets.views import TicketCreateForm


class ReviewHome(ListView):
	model = Review
	context_object_name = "reviews"


class ReviewCreateForm(forms.ModelForm):
	headline = forms.CharField(label='Titre', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
	body = forms.CharField(label='Description', required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
	RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
	rating = forms.ChoiceField(label='Note', widget=forms.RadioSelect(attrs={'class': 'rating'}),
	                           choices=RATING_CHOICES)
	image = forms.ImageField(label='Image', required=False)

	class Meta:
		model = Review
		exclude = ['ticket']
		fields = ['headline', 'body', 'rating', 'image']


@login_required(login_url='followers:login')
def create_review(request):
	"""permet à l'utilisateur de créer une critique en réponse à un ticket existant"""

	if request.method == 'POST':
		form = ReviewCreateForm(request.POST, request.FILES)
		if form.is_valid():
			# On crée un ticket
			ticket = Ticket.objects.create(
				title=form.cleaned_data['headline'],
				description=form.cleaned_data['body'],
				user=request.user,
				image=form.cleaned_data['image'],
				has_review=True
			)
			ticket.save()
			# On récupère le dernier ID de ticket
			ticket_id = ticket.id
			# On crée la critique en réponse au ticket créé
			review = Review.objects.create(
				ticket_id=ticket_id,
				rating=form.cleaned_data['rating'],
				user=request.user,
				headline=form.cleaned_data['headline'],
				body=form.cleaned_data['body'],
			)
			review.save()
			context = {'ticket': ticket, 'review': review}
			return redirect('reviews:home')
	else:
		form = ReviewCreateForm()
	return render(request, 'reviews/create_review.html', {'form': form})


@login_required(login_url='followers:login')
def reply_to_ticket(request: HttpRequest, ticket_id: int) -> HttpResponse:
	"""permet à l'utilisateur de répondre à un ticket spécifique en créant une nouvelle critique"""

	try:
		ticket = Ticket.objects.get(id=ticket_id)
	except Ticket.DoesNotExist:
		print("Le Ticket n'existe pas")
		return redirect('reviews:home')

	if request.method == 'POST':
		form = ReviewCreateForm(request.POST)
		if form.is_valid():
			review = form.save(commit=False)
			review.user = request.user
			review.ticket = ticket
			review.save()
			ticket.has_review = True
			ticket.save()
			return redirect('reviews:home')
		else:
			print('Problème avec le formulaire')
	else:
		form = ReviewCreateForm()
	return render(request, 'reviews/reply_to_ticket.html', {'form': form, 'ticket': ticket})


@login_required(login_url='followers:login')
def get_users_viewable_reviews(request) -> QuerySet[Review]:
	"""récupère une liste des critiques qui sont visibles pour l'utilisateur connecté."""

	# Récupération des critiques de l'utilisateur connecté
	user_reviews = Review.objects.filter(user=request.user)

	# Récupération des utilisateurs que l'utilisateur connecté suit
	followed_users = UserFollows.objects.filter(user=request.user)
	followed_users_ids = followed_users.values_list('followed_user__id', flat=True)

	# Récupération des critiques des utilisateurs que l'utilisateur connecté suit
	followed_users_reviews = Review.objects.filter(user__in=followed_users_ids)

	# Récupération des utilisateurs qui suivent l'utilisateur connecté
	follower_users = UserFollows.objects.filter(followed_user=request.user)
	follower_users_ids = follower_users.values_list('user__id', flat=True)

	# Récupération des critiques des utilisateurs qui suivent l'utilisateur connecté mais que lui ne suit pas
	follower_users_reviews = Review.objects.filter(user__in=follower_users_ids).exclude(user__in=followed_users_ids)

	# Union des trois querysets
	reviews = user_reviews | followed_users_reviews | follower_users_reviews
	return reviews


@login_required(login_url='followers:login')
def get_users_viewable_tickets(request):
	"""récupère une liste de tickets qui sont visibles pour l'utilisateur connecté"""

	# Récupération des utilisateurs que l'utilisateur connecté suit
	followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
	# Récupération des tickets de l'utilisateur connecté et des utilisateurs qu'il suit
	tickets = Ticket.objects.filter(Q(user=request.user) | Q(user__in=followed_users))
	return tickets


@login_required(login_url='followers:login')
def feed(request):
	"""affiche un flux de tous les posts (critiques et tickets) qui sont visibles pour l'utilisateur connecté"""

	reviews = get_users_viewable_reviews(request)
	# returns queryset of reviews
	reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

	tickets = get_users_viewable_tickets(request)
	# returns queryset of tickets
	tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

	# combine and sort the two types of posts
	posts = sorted(
		chain(reviews, tickets),
		key=lambda post: post.time_created,
		reverse=True
	)

	return render(request, 'reviews/feed.html', context={'posts': posts})


@login_required(login_url='followers:login')
def user_posts(request):
	"""affiche une liste de tous les posts (critiques et tickets) créés par l'utilisateur connecté"""

	reviews = Review.objects.filter(user=request.user).order_by('-time_created')
	tickets = Ticket.objects.filter(user=request.user).order_by('-time_created')
	if not reviews and not tickets:
		context = {'message': "Vous n'avez rien posté pour le moment"}
	else:
		context = {'reviews': reviews, 'tickets': tickets}
	return render(request, 'user_posts.html', context)


@login_required(login_url='followers:login')
def edit_review(request, review_id):
	"""permet à l'utilisateur de modifier une critique existante"""

	review = get_object_or_404(Review, pk=review_id)
	if request.method == 'POST':
		form = ReviewCreateForm(request.POST, instance=review)
		if form.is_valid():
			form.save()
			return redirect('reviews:user_posts')
	else:
		form = ReviewCreateForm(instance=review)
	return render(request, 'edit_review.html', {'form': form})


@login_required(login_url='followers:login')
def delete_review(request, id):
	"""permet à l'utilisateur de supprimer une critique existante"""

	review = get_object_or_404(Review, pk=id)
	ticket_id = review.ticket_id
	ticket = Ticket.objects.get(id=ticket_id)
	ticket.has_review = False
	ticket.save()
	review.delete()
	return redirect('reviews:user_posts')


@login_required(login_url='followers:login')
def edit_ticket(request, ticket_id):
	"""permet à l'utilisateur de modifier un ticket existant"""

	ticket = get_object_or_404(Ticket, pk=ticket_id)
	if request.method == 'POST':
		form = TicketCreateForm(request.POST, instance=ticket)
		if form.is_valid():
			form.save()
			return redirect('reviews:user_posts')
	else:
		form = TicketCreateForm(instance=ticket)
	return render(request, 'edit_ticket.html', {'form': form})


@login_required(login_url='followers:login')
def delete_ticket(request, id):
	"""permet à l'utilisateur de supprimer un ticket existant"""

	ticket = get_object_or_404(Ticket, pk=id)
	ticket.delete()
	return redirect('reviews:user_posts')
