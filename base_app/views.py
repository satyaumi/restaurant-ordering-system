from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from base_app.models import  BookTable, AboutUs, Feedback, Category, Item, Cart,Order
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .forms import CustomLoginForm, CustomSignupForm
from django.contrib import auth
from django.contrib.auth import views as auth_views
from .forms import UsernameEmailPasswordResetForm
import json
from django.http import JsonResponse

def cart_page(request):

    cart_items =Cart.objects.filter(user=request.user).select_related('item')
    total_price =sum(cart.total_price() for cart in cart_items)

    
    
    context ={
        'cart_items':cart_items,
        'total_price':total_price
    }
    return render(request,'cart.html',context)


def add_to_cart(request):
    if request.method != "POST":
        return JsonResponse({'error': "Invalid request method"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    item_id = data.get('item_id')
    discount = int(data.get('discount', 0))

    if not item_id:
        return JsonResponse({'error': 'Item ID required'}, status=400)

    item = get_object_or_404(Item, id=item_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        item=item,
        defaults={'discount_percent': discount}
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return JsonResponse({'success': True})

def get_cart_items(request):
  if not request.user.is_authenticated:
      return JsonResponse({'error':'Login required'},status=401)
  
  cart_items =Cart.objects.filter(user=request.user).select_related('item')

  items = []
  for cart in cart_items:
        items.append({
            'id':cart.item.id,
            'name': cart.item.item_name,
            'price': cart.discounted_price(),
            'quantity': cart.quantity,
            'total': cart.total_price(),
            'image': cart.item.image.url if cart.item.image else ''
        })

  return JsonResponse({'items': items})


def remove_from_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login required'}, status=401)

    item_id = None

    # ✅ CASE 1: AJAX JSON request
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body)
            item_id = data.get("item_id")
        except json.JSONDecodeError:
            return JsonResponse({'error': 'invalid JSON'}, status=400)

    # ✅ CASE 2: Normal form POST
    else:
        item_id = request.POST.get("item_id")

    if not item_id:
        return JsonResponse({'error': 'Item ID required'}, status=400)

    cart_item = Cart.objects.filter(
        user=request.user,
        item_id=item_id
    ).first()

    if not cart_item:
        return JsonResponse({'error': 'Item not found in cart'}, status=404)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    # ✅ Return JSON for AJAX, redirect for form
    if request.content_type == "application/json":
        return JsonResponse({'success': True})

    return redirect("cart-page")

def checkout(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login required'}, status=401)
    
    cart_items =Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        return redirect("cart-page")
    total =sum(item.total_price() for item in cart_items)
    
    context ={
        'cart_items':cart_items,
        'total':total
    }
    return render(request,'checkout.html',context)


def place_order(request):
     if not request.user.is_authenticated:
        return JsonResponse({'error': 'login required'}, status=401)
     if request.method !="POST":
         return redirect('cart-page')
     
     cart_items =Cart.objects.filter(user=request.user)
     if not cart_items.exists():
         return redirect('cart-page')
     
     total =sum(item.total_price() for item in cart_items)
    # create order
     order =Order.objects.create(
         user =request.user,
         total_amount=total
     )

    #  create Order Items
     for cart in cart_items:
         OrderItem.objects.create(
             order =order,
             item =cart.item,
             quantity =cart.quantity,
             price =cart.discounted_price()
         )

          #clear cart
         cart_items.delete()

         send_mail(
        subject="Your Order is Confirmed 🎉",
        message=f"""
Hi {request.user.username},

Your order #{order.id} has been placed successfully.

Total Amount: ₹{total}

Thank you for ordering with us!
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
        fail_silently=True
    )

    # 5️⃣ Success Page
     return render(request, "order_success.html", {"order": order})


def login_view(request):
    if request.method=="POST":
        form =CustomLoginForm(request,data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            return redirect('home')
    else:
        form =CustomLoginForm()
    context ={
            'form':form,
        }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomSignupForm()
    context ={
            'form':form,
        }

    return render(request, 'signup.html',context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return render(request, 'logout.html')
         
class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = UsernameEmailPasswordResetForm
    template_name = 'auth/password_reset.html'


def Homeview(request):
    items =Item.objects.all()
    offer_item = Item.objects.first()
    list =Category.objects.all()
    review =Feedback.objects.all()
    return render(request, 'home.html',{'items':items,'list':list,'review':review,'offer_item':offer_item})


def Aboutview(request):
   data =AboutUs.objects.all()
   return render(request, 'about.html',{'data':data})

def Menuview(request):
    items =Item.objects.all()
    list =Category.objects.all()
    return render(request, 'menu.html',{'items':items,'list':list})
   
def BookTableview(request):
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        total_person = request.POST.get('total_person', '0')
        booking_date = request.POST.get('booking_date', '').strip()

        # ✅ Validation
        if (
            name
            and phone_number.isdigit()
            and len(phone_number) == 10
            and email
            and int(total_person) > 0
            and booking_date
        ):
            # ✅ Save booking
            BookTable.objects.create(
                name=name,
                phone_number=phone_number,
                email=email,
                total_person=total_person,
                booking_date=booking_date
            )

            # ✅ Email
            subject = 'Booking Confirmation'
            message = (
                f"Hello {name},\n\n"
                f"Your booking has been successfully received.\n\n"
                f"Booking details:\n"
                f"Total persons: {total_person}\n"
                f"Booking date: {booking_date}\n\n"
                f"Thank you for choosing us!"
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(
                request,
                'Booking request submitted successfully! Please check your confirmation email.'
            )

            return redirect('book-table')  # ✅ URL name

        else:
            messages.error(request, 'Please enter valid booking details.')

    return render(
        request,
        'book_table.html',
        {'google_maps_api_key': google_maps_api_key}
    )


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback, OrderItem

def feedbackview(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name', '').strip()
        description = request.POST.get('description', '').strip()
        rating = request.POST.get('rating')
        selfie = request.FILES.get('selfie')   # ✅ FIXED

        if user_name and description and rating:
            Feedback.objects.create(
                user_name=user_name,
                description=description,
                rating=rating,
                selfie=selfie
            )

            messages.success(request, 'Feedback submitted successfully!')
            return redirect('home')   # ✅ FIXED (URL name)

        else:
            messages.error(request, 'Please fill all required fields.')

    return render(request, 'feedback.html')

