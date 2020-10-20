from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm
    error = ''
    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        else:
            error='Username/password or password confirmation is incorrect!'
            form = UserCreationForm()
            print(form.errors)
            print(error)
    print(form.errors)
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'register/register.html', context)
