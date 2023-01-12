from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from app_users.forms import RegisterForm, UserEditForm, ProfileRedactForm
from app_users.models import Profile
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, FormView
from django.shortcuts import render


class AnotherLoginView(LoginView):
    template_name = 'users/login.html'


class AnotherLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = '/'


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            patronymic = form.cleaned_data.get('patronymic')
            phone_number = form.cleaned_data.get('phone_number')
            Profile.objects.create(
                user=user,
                patronymic=patronymic,
                phone_number=phone_number
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileView(TemplateView):
    model = Profile
    template_name = 'users/account.html'


class RedactProfileView(FormView):
    template_name = 'users/profile.html'
    form_class = ProfileRedactForm

    def get_success_url(self):
        pk = self.request.user.id
        success_url = f'/users/{pk}'
        return success_url

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        photo = form.cleaned_data.get('photo')
        password1 = form.cleaned_data.get('password1')
        phone_number = form.cleaned_data.get('phone_number')
        email = form.cleaned_data.get('email')
        last_name = name[0].title()
        first_name = name[1].title()
        patronymic = name[2].title()
        Profile.objects.filter(id=self.request.user.profile.id). \
            update(patronymic=patronymic, photo=photo, phone_number=phone_number)
        User.objects.filter(id=self.request.user.id). \
            update(first_name=first_name, last_name=last_name, email=email)
        user = User.objects.get(id=self.request.user.id)
        if password1 != '':
            user.set_password(password1)
            user.save()
        user = authenticate(username=self.request.user, password=password1)
        login(self.request, user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        form_kwargs = super(RedactProfileView, self).get_form_kwargs()

        form_kwargs.update({'initial': {
            'last_name': f'{self.request.user.last_name}',
            'first_name': f'{self.request.user.first_name}',
            'email': f'{self.request.user.email}',
            'patronymic': f'{self.request.user.profile.patronymic}',
            'photo': f'{self.request.user.profile.photo}',
            'phone_number': f'{self.request.user.profile.phone_number}'
        }})

        return form_kwargs