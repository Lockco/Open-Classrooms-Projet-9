from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView

from tickets.models import Ticket


class TicketHome(ListView):
	model = Ticket
	context_object_name = "tickets"


class TicketCreateForm(forms.ModelForm):
	"""formulaire pour créer un nouveau ticket"""

	title = forms.CharField(max_length=128, label="Titre")
	description = forms.CharField(required=False, label="Déscription", widget=forms.Textarea(attrs={'class': 'form-control'}))
	image = forms.ImageField(required=False, label="Image")  # Ajout du champ pour l'image

	class Meta:
		model = Ticket
		exclude = ['ticket']
		fields = ['title', 'description', 'image', ]


@login_required(login_url='followers:login')
def create_ticket(request: HttpRequest):
	"""permet à l'utilisateur de créer un nouveau ticket"""

	if request.method == 'POST':
		form = TicketCreateForm(request.POST, request.FILES)
		if form.is_valid():
			# Création du ticket
			ticket = Ticket.objects.create(
				title=form.cleaned_data['title'],
				description=form.cleaned_data['description'],
				user=request.user,
				image=form.cleaned_data['image']
			)
			ticket.save()
			if ticket.image:
				print("Image path: ", ticket.image.path)
			else:
				print("No image associated with this ticket.")
			return redirect(reverse('reviews:feed') + f'?created_ticket={ticket.id}')
	else:
		form = TicketCreateForm()
	return render(request, 'ticket_form.html', {'form': form})


@login_required(login_url='followers:login')
def edit_ticket(request: HttpRequest, ticket_id: int) -> HttpResponse:
	"""permet à l'utilisateur de modifier un ticket existant"""
	review = get_object_or_404(Ticket, pk=ticket_id)
	if request.method == 'POST':
		form = TicketCreateForm(request.POST, instance=review)
		if form.is_valid():
			form.save()
			return redirect('reviews:user_posts')
	else:
		form = TicketCreateForm(instance=review)
	return render(request, 'edit_ticket.html', {'form': form})
