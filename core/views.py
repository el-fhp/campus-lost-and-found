from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Item
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


def index(request):
    items = Item.objects.filter(status='Lost')[:6]
    return render(request, 'index.html', {'items': items})


def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'username_error': 'User already exists'
            })

        if password != cpassword:
            return render(request, 'signup.html', {
                'password_error': 'Passwords do not match'
            })

        User.objects.create_user(
            first_name=fname, last_name=lname,
            email=email, username=username, password=password
        )
        messages.success(request, f'Account created successfully. Welcome, {username}!')
        return redirect('sign-in')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('home-page')


@login_required(login_url='sign-in')
def submititems(request):
    if request.method == "POST":
        Item.objects.create(
            user=request.user,
            item=request.POST['item'],
            description=request.POST['description'],
            category=request.POST['category'],
            image=request.FILES.get('image'),
            date_lost=request.POST['date_lost'],
            owner_name=request.POST['owner_name'],
            email=request.POST.get('email', ''),
            phone_number=request.POST.get('phone_number', ''),
            status='Lost',  # always starts as Lost
        )
        messages.success(request, 'Your lost item has been reported.')
        return redirect('home-page')

    return render(request, 'submititem.html')


@login_required(login_url='sign-in')
def mypost(request):
    items = Item.objects.filter(user=request.user)
    return render(request, 'mypost.html', {'items': items})


@login_required(login_url='sign-in')
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Post deleted.')
    return redirect('my-posts')


@login_required(login_url='sign-in')
def mark_found(request, pk):
    """Owner marks their lost item as found."""
    item = get_object_or_404(Item, pk=pk, user=request.user)
    if request.method == 'POST':
        item.status = 'Found'
        item.save()
        messages.success(request, f'"{item.item}" has been marked as Found.')
    return redirect('my-posts')


@login_required(login_url='sign-in')
def allitems(request):
    q = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    lost_qs  = Item.objects.filter(status='Lost')
    found_qs = Item.objects.filter(status='Found')

    # Apply search across both
    if q:
        lost_qs  = lost_qs.filter(item__icontains=q)  | lost_qs.filter(description__icontains=q)
        found_qs = found_qs.filter(item__icontains=q) | found_qs.filter(description__icontains=q)

    if category_filter:
        lost_qs  = lost_qs.filter(category=category_filter)
        found_qs = found_qs.filter(category=category_filter)

    # Paginate-style: show 6 by default, "view more" shows all
    lost_limit  = None if request.GET.get('show_lost')  == 'all' else 6
    found_limit = None if request.GET.get('show_found') == 'all' else 6

    lost_total  = lost_qs.count()
    found_total = found_qs.count()

    lost_items  = lost_qs  if lost_limit  is None else lost_qs[:lost_limit]
    found_items = found_qs if found_limit is None else found_qs[:found_limit]

    context = {
        'lost_items':   lost_items,
        'found_items':  found_items,
        'lost_total':   lost_total,
        'found_total':  found_total,
        'show_lost_all':  lost_limit  is None,
        'show_found_all': found_limit is None,
        'q': q,
        'category_filter': category_filter,
        'CATEGORY_CHOICES': Item.CATEGORY_CHOICES,
    }
    return render(request, 'allitems.html', context)