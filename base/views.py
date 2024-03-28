from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .models import UserPost, UserPostComments, User, LikePost
from .forms import UserPostForm, UserForm, MyUserCreationForm
from django.core.paginator import Paginator

# Create your views here.
def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    userposts = UserPost.objects.all()
    paginator = Paginator(userposts, 2)
    page_number = request.GET.get("page")
    ServicesDataFinal = paginator.get_page(page_number)

    post_comments = UserPostComments.objects.filter(
        Q(userpost__content__icontains=q))[0:3]

    context = {'ServicesDataFinal': ServicesDataFinal, 'post_comments':post_comments}
    return render(request, 'home.html', context)


def userProfile(request, pk):
    author = User.objects.get(id=pk)
    userpost = author.userpost_set.all()
    context = {'author':author, 'userpost':userpost}
    return render(request, 'base/profile.html', context )


def userpost(request, pk):
    userpost = UserPost.objects.get(id=pk)
    room_messages = userpost.userpostcomments_set.all()

    if request.method == 'POST':
        userpostcomments = UserPostComments.objects.create(
            user=request.user,
            userpost=userpost,
            body=request.POST.get('body')
        )
        return redirect('userpost', pk=userpost.id)

    context = {'userpost': userpost, 'room_messages': room_messages}
    return render(request, 'base/single.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login')
def createUserpost(request):
    form = UserPostForm()

    if request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES,)

        UserPost.objects.create(
            author=request.user,
            image=request.FILES.get('image'),
            content=request.POST.get('content'),
        )
        return redirect(request.META.get('HTTP_REFERER'))
        #return redirect('.')

    context = {'form': form}
    return render(request, 'base/post_upload_form.html', context)


@login_required(login_url='login')
def updateUserpost(request, pk):
    userpost = UserPost.objects.get(id=pk)
    form = UserPostForm(instance=userpost)

    if request.user != userpost.author:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES, instance=userpost)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form, 'userpost':userpost,}
    return render(request, 'base/post_upload_form.html', context)


@login_required(login_url='login')
def deleteUserpost(request, pk):
    userpost = UserPost.objects.get(id=pk)

    if request.user != userpost.author:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        userpost.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':userpost})


@login_required(login_url='login')
def deleteComment(request, pk):
    comment = UserPostComments.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        comment.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':comment})


#like post function
@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    userposts = UserPost.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        userposts.no_of_likes = userposts.no_of_likes + 1
        userposts.save()
        return redirect('/')
    else:
        like_filter.delete()
        userposts.no_of_likes = userposts.no_of_likes-1
        userposts.save()
        return redirect('/')


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form':form})


@property
def image_url(self):
    if self.image and hasattr(self.image, 'url'):
        return self.image.url
