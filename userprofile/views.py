from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import UserProfile


# Create your views here.

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            if 'firstname' in request.POST:
                user.first_name = request.POST.get('firstname')
            if 'lastname' in request.POST:
                user.last_name = request.POST.get('lastname')
            user.save()

            if 'profile_picture' in request.FILES:
                user_profile.profile_picture = request.FILES['profile_picture']
            
            if 'address' in request.POST:
                user_profile.address = request.POST.get('address')
            if 'contact_number' in request.POST:
                user_profile.contact_number = request.POST.get('contact_number')

            user_profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile', username=username)

        elif 'change_password' in request.POST:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('new_password2')
            
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match")
            elif new_password:
                user.set_password(new_password)
                user.save()
                logout(request)
                messages.success(request, "Password changed successfully. Please log in again.")
                return redirect('login')

    return render(request, 'userprofile/profile.html', {'user': user, 'user_profile': user_profile})
