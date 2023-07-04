from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Post,Profile
from .forms import PostForm,UserLoginForm,UserRegisterForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import(
    authenticate,
    logout,
    login,
  
)

def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'app/all_posts.html', context)

def login_view(request):
    form=UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user =authenticate(username=username,password=password)
        login(request,user)

        return redirect('home')
    context ={
        'form':form,
    }
    return render(request, "app/login.html", context)

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user, address='', phone_number='')

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('login_view')
    
    context = {'form': form}
    return render(request, 'app/signup.html', context)



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            subject = 'New Post Created'
            message = f'A new post "{post.caption},{post.content}" has been created.'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])

            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'app/create_post.html', {'form': form})

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'app/update_post.html', {'form': form,})
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'app/delete_post.html', {'post': post})

def all_posts(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'app/all_posts.html', context)
@login_required
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'app/post_details.html', {'post': post})

def logout_view(request):
    logout(request)
    return redirect('home')