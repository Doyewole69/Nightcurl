from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.shortcuts import render, redirect
from unicodedata import name
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm, UserAddressForm
from .token import account_activation_token
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.models import User
import logging

# Create your views here.

from .forms import UserRegistrationForm, UserAddressForm

# Create your views here.

User = get_user_model()

class HomeView(TemplateView):
    template_name = 'nightcurlapp/index.html'



class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'nightcurlapp/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('nightcurlapp:dashboard')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save(commit=True)
            user.is_active = False 
            user.save()

            address = address_form.save(commit=False)
            address.user = user
            address.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('nightcurlapp/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = registration_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            messages.success(
                self.request,
                'Please confirm your email address to complete the registration to join Nightcurl.'
            )
            return HttpResponseRedirect(reverse_lazy('nightcurlapp:signup'))

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()
        return super().get_context_data(**kwargs)


    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, f'Thank you {user.first_name} for your email confirmation. Now you can login your account.'  f'Thank You For Joining Nightcurl. The Revolutionary Social Media Networ. ')
        return HttpResponseRedirect(reverse_lazy('nightcurlapp:transaction_report'))
    else:
        messages.error(request, 'Activation link is invalid.')
        return HttpResponseRedirect(reverse_lazy('nightcurlapp:realestatesignup'))
    
    
    
class UserLoginView(LoginView):
    template_name='nightcurlapp/login.html'
    redirect_authenticated_user = False


class LogoutView(RedirectView):
    pattern_name = 'nightcurlapp:home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)