from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Count
from django.http import JsonResponse


from .forms import ProductForm

def home(request):
    return render(request,'home.html')

def product_create(request):
    if request.method == 'POST':
        Count=Product.objects.filter(author=request.user).values('id')
        form=ProductForm()
        c=0
        for i in Count:
            c=c+1
        if c<5: 
            if request.POST:
                form = ProductForm(request.POST)
                if form.is_valid():
                    forms=form.save(commit=False)
                    forms.author=request.user
                    forms.save()
                    return redirect('page_list')
        else:
            return HttpResponse('Reached the limit')
    else:
        form =ProductForm()
    return render(request, 'create.html', {'form': form})

# def product_read(request):
#     product_list=Product.objects.all()
#     return render(request,'retrieve.html',{'product_list':product_list})

def product_update(request, id):
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('page_list')
    else:
        form =ProductForm(instance=product)           
    return render(request, 'update.html', {'form': form})

def product_delete(request,id):
    product=Product.objects.get(pk=id)  
    if request.method == 'POST':
        product.delete()
        return redirect('page_list')
    
    return render(request,'delete.html',{'product':product})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            # Redirect to login page after successful signup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            # Redirect to home page after successful login
            return redirect('page_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login/')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    context = {
        'user': request.user
    }

    return render(request, 'logout.html', context)

def listing(request):
    product_list = Product.objects.filter(author=request.user)
    paginator = Paginator(product_list, 2)  # Set the number of items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.POST:
        data=request.POST.get('medicine')
        if data:
           
            datas=Product.objects.filter(medicine__istartswith=data).filter(author=request.user)
        else:
            datas=Product.objects.none()    

      
        return render(request, 'list.html', {'page_obj':datas})
    return render(request, 'list.html', {'page_obj': page_obj})

def search(request):
    if 'term' in request.GET:
        jquery=Product.objects.filter(medicine__istartswith=request.GET.get('term')).filter(author=request.user) 
        medicines=list()
        for i in jquery:
            medicines.append(i.medicine)
    return JsonResponse(medicines,safe=False)

