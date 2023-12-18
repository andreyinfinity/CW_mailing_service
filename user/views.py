from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from user.forms import UserLoginForm, UserRegistrationForm


def login(request):
    form = UserLoginForm()
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home:index'))
            else:
                messages.error(request, 'Проверьте имя, пароль и попробуйте снова',
                               extra_tags='alert alert-danger alert-dismissible fade show'
                              )
    context = {'form': form}
    return render(request, 'user/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home:index'))


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message='Вы успешно зарегистрированы',
                             extra_tags='alert alert-success alert-dismissible fade show')
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'user/registration.html', context)


class UserRegistration(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('user:login')