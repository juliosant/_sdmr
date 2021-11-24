
from django.shortcuts import render, redirect

# Create your views here.

# index
def index_page(request):
    print(request.POST)
    if request.POST:
        print(request.POST['receiverTags'])
        tags = request.POST['receiverTags'].split(',')
        print(tags)
    return render(request, 'index.html')


'''
def userpage(request):
    #search = Q()

    if request.user.profile_type == 'D':
        calls = CustomerService.objects.filter(requester=request.user.id).order_by("-id")
        return render(request, 'authenticated_user/donor/userpage.html', {'calls': calls})
    elif request.user.profile_type == 'R':
        calls = CustomerService.objects.filter(recipient=request.user.id).order_by("-id")
        return render(request, 'authenticated_user/recyclingcenter/userpage.html', {'calls': calls})


def login_profile(request):
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['user'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('users_auth:userpage')
            else:
                return HttpResponse("<h1>Não foi feito login</h1>")
    login_form = LoginForm()
    content = {
        'login_form': login_form
    }
    return render(request, 'management_user/login/login.html', content)


def logout_profile(request):
    logout(request)
    return redirect("users_auth:login")


def register_profile(request):
    if request.POST:
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('users_auth:login')
                
    profile_form = ProfileForm()
    content = {
        'profile_form': profile_form
    }
    return render(request, 'management_user/register/register.html', content)
'''