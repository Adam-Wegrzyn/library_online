from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('import_book'))
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'register/register.html', context)
