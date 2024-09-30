from django.shortcuts import render,redirect,get_object_or_404
from .forms import Task_Form,RegistrationForm,LoginForm
from .models import Task_Model,UserProfile
from django.contrib.auth import login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework import viewsets
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from .encrypting_keys import encrypt_key,decrypt_key
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class TaskList(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey , IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        print("User: ",user)
        return Task_Model.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        # Set the user to the request user before saving
        request.user = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@login_required(login_url='login')
def display_api_key(request):
    refresh = RefreshToken.for_user(request.user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    task,created = UserProfile.objects.get_or_create(user=request.user)
    api_name = APIKey.objects.filter(name=request.user.username)
    if api_name:
        stored_key = task.apikey
        decrypted_key = decrypt_key(stored_key)
        return render(request,'display_api_key.html',{'api_key':decrypted_key,'access':access_token,'refresh':refresh_token})
    else:
        api_key,key = APIKey.objects.create_key(name=request.user.username)
        encrypted_key = encrypt_key(key)
        task.apikey = encrypted_key
        task.save()
        
        return render(request,'display_api_key.html',{'api_key':key})

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        form = Task_Form(request.POST)
        if form.is_valid():
            user_task = form.save(commit=False)
            user_task.user = request.user
            user_task.save()
            return redirect('home')
        task_id = request.POST.get('finished')
        if task_id:
            task = get_object_or_404(Task_Model,id=task_id)
            task.task_status = not task.task_status
            task.save()
            return redirect('home')
        delete_task_id = request.POST.get('delete')
        if delete_task_id:
            Task_Model.objects.filter(id=delete_task_id).delete()
            return redirect('home')
    tasks = Task_Model.objects.filter(user=request.user)
    form = Task_Form()
    return render(request,'home.html',{'form':form,'tasks':tasks})

def delete_all(request):
    if request.method == 'POST':
        Task_Model.objects.all().delete()
        return redirect('home')
    
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request,user)
            return redirect("home")
    form = RegistrationForm()
    return render(request,'register.html',{'form':form})

def get_token(username,password):
    token_url = "http://127.0.0.1:8000/api/token/"
    payload = {
        'username':username,
        'password':password
    }
    try:
        response = requests.post(token_url,json=payload)
        if response.status_code == 200:
            access_token = response.json().get('access')
            refresh_token = response.json().get('refresh')
            return access_token,refresh_token
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            username_give = user.username
            password_give = request.POST['password']
            access_token,refresh_token = get_token(username_give,password_give)
            if access_token:
                auth_login(request,user)
                return redirect('home')
            else:
                form.add_error(None,"Authentication Failed please check credentials again!")
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

def logout(request):
    auth_logout(request)
    return redirect("login")

def edit(request,task_id):
    task = get_object_or_404(Task_Model,pk=task_id)
    if request.method == 'POST':
        form = Task_Form(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = Task_Form(instance=task)
    return render(request,"edit.html",{'form':form})

def api_docs(request):
    return render(request,'api_docs.html')