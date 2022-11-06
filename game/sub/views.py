from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from .forms import UserLoginForm, UserRegisterForm, SubscriptionForm
from .models import Subscription
from .tasks import new_subscription_notice


def user_registration(request):
    """
    Function for render registration.html
    :param request: WSGIRequest
    :return: render sub/registration.html
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вдала реєстрація')
            return redirect('home')
        else:
            messages.error(request, 'Помилка реєстрації')
    else:
        form = UserRegisterForm()
    return render(request, 'sub/registration.html', {"form": form})


def user_login(request):
    """
    Function for render login.html
    :param request: WSGIRequest
    :return: render sub/login.html
    """
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Помилка авторизації')
    else:
        form = UserLoginForm()
    return render(request, 'sub/login.html', {"form": form})


def user_logout(request):
    """
    Function for render login.html
    :param request: WSGIRequest
    :return: redirect('home')
    """
    logout(request)
    return redirect('home')


class Home(ListView):
    """
    Display a list of Subscriptions.
    :model:`Subscription`
    :context_object_name:`subscriptions`
    :template_name:`sub/subscriptions.html`
    """
    model = Subscription
    template_name = 'sub/subscriptions.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return Subscription.objects.filter(user_id=self.request.user.id)


class EditSubscription(UpdateView):
    """
    Display a Subscription edit page.
    :model:`Subscription`
    :context_object_name:`subscription`
    :fields: 'team_name'
    :template_name:`sub/edit_subscription.html`
    """
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'sub/subscription_edit.html'
    context_object_name = 'subscriptions'

    def get_form_kwargs(self):
        kwargs = super(EditSubscription, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class AddSubscription(CreateView):
    """
    Display an SubscriptionForm
    :form_class:`SubscriptionForm`
    :template_name:`sub/subscription_add.html`
    """
    form_class = SubscriptionForm
    template_name = 'sub/subscription_add.html'

    def get_form_kwargs(self):
        kwargs = super(AddSubscription, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save()
        new_subscription_notice.delay(form.current_user.email, form.cleaned_data['team_name'])
        return super().form_valid(form)


class RemoveSubscription(DeleteView):
    """
    Display an Subscription remove page.
    :model:`Subscription`
    :success_url:`subscriptions`
    :error_url: `article_delete_error`
    """
    model = Subscription
    success_url = reverse_lazy('home')
    error_url = reverse_lazy('subscription_delete_error')

    def get_error_url(self):
        if self.error_url:
            return self.error_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No error URL to redirect to. Provide a error_url.")

    def get_success_url(self):
        if self.error_url:
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No success URL to redirect to. Provide a success_url.")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        error_url = self.get_error_url()

        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except models.ProtectedError:
            return HttpResponseRedirect(error_url)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


def subscription_delete_error(request):
    """
    Function for render subscription_delete_error.html
    :param request: WSGIRequest
    :return: render sub/subscription_delete_error.html
    """
    return render(request, template_name='sub/subscription_delete_error.html')
