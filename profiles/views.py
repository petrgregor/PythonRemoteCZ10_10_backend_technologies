from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage


from profiles.models import *

# Create your views here.
@login_required
def profile(request, pk):
    my_profile = Profile.objects.get(id=pk)

    context = {"profile": my_profile}
    return render(request, 'profiles/profile.html', context)


@login_required
def create_profile(request):
    if request.method == 'POST':
        user = request.user
        file_url = None
        if request.FILES.get('avatar'):
            avatar = request.FILES['avatar']
            file_storage = FileSystemStorage()
            file = file_storage.save(avatar.name, avatar)
            file_url = file_storage.url(file)
        profile = Profile.objects.create(
            user=user,
            avatar=file_url,
            about_me=request.POST.get('about_me'),
            birth_date=request.POST.get('birth_date')
        )
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        return redirect('profile', profile.id)

    return render(request, 'profiles/create_profile.html')

# TODO edit_profile
# TODO možnost definovat jednotlivé položky z profilu jako private

