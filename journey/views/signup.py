from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from journey.forms import CreateUserAccountForm

'''
Handle the signup process.  Displays the signup form, and,when submitted and validated, creates the user and
logs them in.
'''
def signup(request):
    if request.method == 'POST':
        user_form = CreateUserAccountForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("journey:post_list")
    else:
        user_form = CreateUserAccountForm()
    return render(request, 'journey/signup.html', {'user_form': user_form})
