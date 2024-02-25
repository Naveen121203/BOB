from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import U_Profile,Post,Likes
from django.contrib.auth.decorators import login_required

def signup(request):
    try:
        if request.method == 'POST':
            nm = request.POST.get('nm')
            email = request.POST.get('email')
            pwd = request.POST.get('pwd')
            my_user =User.objects.create_user(nm,email,pwd)
            my_user.save()
            user_model = User.objects.get(username=nm)
            new_profile= U_Profile.objects.create(user=user_model,id_user=user_model.id)
            new_profile.save()
            if my_user is not None:
                login(request,my_user)
                return redirect('/')
            return redirect('/loginn')
        
    except:
        invalid="User Already Exists"
        return render(request,'signup.html',{'invalid':invalid})

    return render(request,'signup.html')
        

def logiin(request):
    if request.method == 'POST':
        nm=request.POST.get('nm')
        pwd=request.POST.get('pwd')
        print(nm,pwd)
        userr=authenticate(request,username=nm,password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/')
        
 
        invalid="Invalid Credentials"
        return render(request, 'logiin.html',{'invalid':invalid})
               
    return render(request, 'logiin.html')

@login_required(login_url='/logiin')
def likes(request,id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)

        like_filter = Likes.objects.filter(post_id=id, username=username).first()

        if like_filter is None:
            new_like = Likes.objects.create(post_id=id, username=username)
            post.likes_count = post.likes_count + 1
        else:
            like_filter.delete()
            post.likes_count = post.likes_count - 1

        post.save()

        
        print(post.id)

        
        return redirect('/#'+id)


@login_required(login_url='/logiin')
def logouut(request):
    logout(request)
    return redirect('/logiin')

@login_required(login_url='/logiin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/logiin')
def hub_post(request,id):
    post=Post.objects.get(id=id)
    profile = U_Profile.objects.get(user=request.user)
    context={
        'post':post,
        'profile':profile
    }
    return render(request, 'main.html',context)
@login_required(login_url='/logiin')
def hub(request):
    post = Post.objects.all().order_by('-posted_at')
    profile = U_Profile.objects.get(user=request.user)
    context = {
        'post':post,
        'profile':profile
    }
    return render(request,'main.html',context)

@login_required(login_url='/logiin')
def profile(request,id_user):
    user_object = User.objects.get(username=id_user)
    print(user_object)
    profile = U_Profile.objects.get(user=request.user)
    user_profile = U_Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=id_user).order_by('-posted_at')
    user_post_length = len(user_posts)
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': profile,
    }
    
    if request.user.username == id_user:
        if request.method == 'POST':
            if request.FILES.get('image') == None:
             image = user_profile.profilepic
             bio = request.POST['bio']
             

             user_profile.profilepic = image
             user_profile.about = bio
             
             user_profile.save()
            if request.FILES.get('image') != None:
             image = request.FILES.get('image')
             bio = request.POST['bio']
             

             user_profile.profilepic = image
             user_profile.about = bio
             
             user_profile.save()

             return redirect('/profile/'+id_user)
        else:
            return render(request, 'profile.html', context)

    return render(request, 'profile.html',context)
@login_required(login_url='/logiin')
def delete(request,id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('/profile/'+request.user.username)
@login_required(login_url='/logiin')
def search(request):
    query = request.GET.get('q')

    users = U_Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)

    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'search_user.html', context)