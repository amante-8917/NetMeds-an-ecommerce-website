import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from store.models import Seller, Product, Query


def home(request):
    all_products = Product.objects.all()
    categories = Product.objects.values_list('product_category').distinct();
    for category in categories:
        print(category[0])
    return render(request, 'store/home.html', {'all_products': all_products, 'categories': categories})


def about(request):
    context = {}
    return render(request, 'store/about.html', context)


def contact(request):
    context = {}
    return render(request, 'store/contact.html', context)


def admin(request):
    context = {}
    return render(request, 'store/siteadmin.html', context)


def forgot_password(request):
    context = {}
    return render(request, 'store/forgotpassword.html', context)


@login_required
def update_profile(request):
    context = {}
    return render(request, 'store/updateprofile.html', context)


@login_required
def change_password(request):
    context = {}
    return render(request, 'store/changepassword.html', context)


def login_page(request):
    context = {}
    return render(request, 'store/login.html', context)


def signup_page(request):
    context = {}
    return render(request, 'store/signup.html', context)


def create_seller(request):
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    email = request.POST['email']
    phone = request.POST['phone']
    username = request.POST['username']
    password1 = request.POST['password']
    password2 = request.POST['confirmpassword']
    if len(username) > 10:
        messages.error(request, " Your user name must be under 10 characters")
        return redirect('signup_page')
    if not username.isalnum():
        messages.error(request, " User name should only contain letters and numbers")
        return redirect('signup_page')
    if password1 != password2:
        messages.error(request, " Passwords do not match")
        return redirect('signup_page')
    seller = Seller()
    seller.first_name = first_name
    seller.last_name = last_name
    seller.email = email
    seller.phone = phone
    seller.username = username
    seller.set_password(password2)
    seller.save()
    login(request, seller)
    return redirect('home')


def seller_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        username = form.data.get('loginusername')
        password = form.data.get('loginpassword')
        seller = authenticate(username=username, password=password)
        print(seller is not None)
        if seller is not None:
            login(request, seller)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login_page")
    form = AuthenticationForm()
    print(messages)
    return render(request=request, template_name="store/home.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


@login_required
def update_seller_profile(request, user_id):
    print(user_id)
    seller = Seller.objects.get(pk=user_id)
    print(request.POST['firstname'] == "")
    if request.method == "POST":

        if request.POST['firstname'] == "":
            seller.first_name = request.user.first_name
        else:
            seller.first_name = request.POST['firstname']
        if request.POST['lastname'] == "":
            seller.last_name = request.user.last_name
        else:
            seller.last_name = request.POST['lastname']
        if request.POST['email'] == "":
            seller.email = request.user.email
        else:
            seller.email = request.POST['email']
        if request.POST['phone'] == "":
            seller.phone = request.user.phone
        else:
            seller.phone = request.POST['phone']
        seller.save()
        return redirect('home')


@login_required
def change_password_page(request):
    return render(request, 'store/changepassword.html')


@login_required
def update_password(request):
    print('in update_password')
    print(request)
    if request.method == "POST":
        oldpassword = request.POST['oldpassword']
        password1 = request.POST['newpassword']
        password2 = request.POST['confirmnewpassword']

        if password1 != password2:
            messages.error(request, "Both entered password's didn't match")
            return redirect('change_password')

        seller = authenticate(username=request.user.username, password=oldpassword)
        if seller is not None:

            seller.set_password(password2)
            seller.save()
            login(request, seller)
            messages.info(request, "Your password has been updated successfully!")
            return redirect('home')
        else:
            messages.error(request, "Old password is incorrect!")
            return redirect('change_password')


def new_product_page(request):
    context = {}
    return render(request, 'store/newproduct.html', context)


def new_product(request):
    seller = Seller.objects.get(username__exact=request.user.username)
    name = request.POST['productname']
    description = request.POST['description']
    category = request.POST['category']
    price = request.POST['price']
    publishing_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = request.POST['status']
    year = request.POST['years']
    image = request.FILES['image']
    listed_by = seller
    Product.objects.create(product_name=name, product_description=description, product_category=category,
                           product_price=price, product_publishing_date=publishing_date, product_status=status,
                           product_year=year, product_image=image, product_listed_by=listed_by)
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/home.html', context)



def product(request, product_id):
    product = Product.objects.get(product_id=product_id)
    context = {'product': product}
    return render(request, 'store/product.html', context)


@login_required
def product_list(request):
    seller = Seller.objects.get(username__exact=request.user.username)
    products = Product.objects.filter(product_listed_by=seller)
    return render(request, 'store/productlist.html', {'products': products})


@login_required(login_url='login_page')
def delete_product(request, product_id):
    seller = Seller.objects.get(username__exact=request.user.username)
    Product.objects.get(product_id=product_id).delete()
    products = Product.objects.filter(product_listed_by=seller)
    context = {'products': products}
    return render(request, 'store/productlist.html', context)


def update_product_page(request, product_id):
    product = Product.objects.get(product_id=product_id)
    context = {'product': product}
    return render(request, 'store/updateproduct.html', context)


@login_required
def update_product(request, product_id):
    print('in update product')
    print(request)
    if request.method == "POST":
        global context
        seller = Seller.objects.get(username__exact=request.user.username)
        product = Product.objects.get(product_id=product_id)

        if request.POST['productname'] != "":
            product.product_name = request.POST['productname']
        else:
            product.product_name = product.product_name

        if request.POST['description'] != "":
            product.product_description = request.POST['description']
        else:
            product.product_description = product.product_description

        if request.POST['category'] != "":
            product.product_category = request.POST['category']
        else:
            product.product_category = product.product_category

        if request.POST['price'] != "":
            product.product_price = request.POST['price']
        else:
            product.product_price = product.product_price

        product.product_publishing_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if request.POST['status'] != "":
            product.product_status = request.POST['status']
        else:
            product.product_status = product.product_status

        if request.POST['years'] != "":
            product.product_year = request.POST['years']
        else:
            product.product_year = product.product_year

        product.product_image = request.FILES['image']
        product.product_listed_by = seller
        product.save()
        products = Product.objects.filter(product_listed_by=seller)
        context = {'products': products}
    return render(request, 'store/productlist.html', context)


def ask_query_page(request, product_id):
    context = {'product_id': product_id}
    return render(request, 'store/query.html', context)


def ask_query(request, product_id):
    # seller = Seller.objects.get(username__exact=request.user.username)
    product = Product.objects.get(product_id=product_id)
    seller = Seller.objects.get(username__exact=product.product_listed_by.username)
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    description = request.POST['description']
    Query.objects.create(query_owner_name=name, query_owner_email=email, query_owner_phone=phone,
                         query_description=description, product_id=product, product_owner_id=seller)
    messages.info(request, "Your query has been sent to product owner successfully!")
    return redirect('home')


@login_required
def notifications(request):
    notifications = Query.objects.filter(product_owner_id_id=request.user.id)
    # notifications = Query.objects.all()
    context = {'notifications': notifications}
    return render(request, 'store/messages.html', context)


def filter(request, category):
    products = Product.objects.filter(product_category=category)
    context = {'products': products}
    return render(request, 'store/home.html', context)


def search(request):
    searchfield = request.POST['search']
    products = Product.objects.all()
    searchresults = []
    for product in products:
        print(product.product_category.lower())
        if (searchfield in product.product_name.lower()) or (searchfield in product.product_category.lower()):
            searchresults.append(product)

        if searchfield in product.product_category.lower():
            searchresults.append(product)
    return render(request, "store/home.html", {'searchresults': searchresults})
