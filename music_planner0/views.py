from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from music_planner0.forms import UserCreationForm2
from django.shortcuts import render, redirect
#from django.views.generic import RedirectView
from django.utils.http import urlencode
class UserCreateView(CreateView):
    form_class = UserCreationForm2
    template_name = "registration/generic_form.html"
    
    def get_success_url(self):
        return reverse('login')

class AdminUserUpdateView(UpdateView):
    model = User
    slug_field = 'username'
    form_class=UserChangeForm
    template_name = "registration/generic_form.html"

    @method_decorator(permission_required('auth.change_user'))
    def dispatch(self, *args, **kwargs):
        return super(AdminUserUpdateView, self).dispatch(*args, **kwargs)
    
class UserDetailView(DetailView):
    model = User
    tempate_name = "registration/user.html"
    slug_field = 'username'

def index(request):
    return render(request, 'dist/index.html')

def redirect_to_vite(request):
    #d = {'next': vite_url}
    #print(request.path, request.content_params, request.get_full_path())
    url=("/?"+urlencode({'next':request.get_full_path()}))
    print("url = ", url)
    return redirect(url)
