from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

def home(request):
    name = "Name Here"
    numbers = {1, 2, 3, 4, 5}
    context = {'name': name, 'numbers': numbers}

    return render(request, 'events/home.html', context)


# def login(request):
#     return render(request, 'events/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()

        args = {'form': form}
        return render(request, 'events/reg_form.html')

