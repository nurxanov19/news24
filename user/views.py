

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ProfileForm
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Profile
from django.contrib.auth.views import LoginView, LogoutView


def signup_view(request):

    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        print('post kelyapti')
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            print('user qismi ishlayapti')

            profile_form = ProfileForm(request.POST, files=request.FILES)
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                print(profile.profile_picture)
                print('Profil qismi ishlayapti')

            login(request, user)
            return redirect('profile')

    else:
        print('Balo ham ishlamayapti')
        user_form = SignUpForm()
        profile_form = ProfileForm()

    return render(request, 'registration/signup.html', {'user_form': user_form,
                                                        'profile_form': profile_form})



class UserLogin(LoginView):
    redirect_authenticated_user = True      # login qilgan userni qaytib login page ga yubormayd

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('index')

    def form_valid(self, form):
        responses = super().form_valid(form)
        if self.request.user.is_authenticated:
            Profile.objects.get_or_create(user=self.request.user)
        return responses

    def form_invalid(self, form):
        messages.error(self.request, 'Username or Password incorrect')
        return self.render_to_response(self.get_context_data(form=form))


def logout_view(request):
    logout(request)  # Logs out the user (clears session)
    return redirect('index')


def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'registration/profile.html', {'form': form, 'profile': profile, 'user': request.user})






