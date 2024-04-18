import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST


def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response


@require_POST
def login_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'detail': "You are already logged in."}, status=400)

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'detail': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'detail': 'Invalid credentials.'}, status=400)

    login(request, user)
    return JsonResponse({'detail': 'Successfully logged in.'})


def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'detail': 'Successfully logged out.'})

from django.contrib.auth.forms import UserCreationForm     
class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', "email", "password1", "password2"]

def register_view(request):
    data = json.loads(request.body)
    username = data.get('username').lower()
    password1 = data.get('password1')
    password2 = data.get('password2')
    form = RegForm(data)
    if form.is_valid():

        if username is None:
            form.add_error(None,"Поле пользователя пустое")
        elif password1 != password2:
            form.add_error(None,"Пароли не совпадают")
        elif User.objects.filter(username=username).exists():
            print(User.objects.filter(username=username).exists())
            form.add_error(None,"Пользователь с таким логином уже зарегистрирован")
        else:
            user = User.objects.create(username=username, password=password1)
            login(request, user)
            return JsonResponse({'detail': f'Created user {user.username}', 'errors' : ""})
    return JsonResponse({'detail': 'Form is NOT valid', 'errors': [value for value in form.errors.values()][0]},status=400)


@ensure_csrf_cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'isAuthenticated': True, 'username': request.user.username, 'id': request.user.id})