from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Sum
from .models import *
from .payment import PaymentGateway
from .forms import RegistrationForm, UserProfileForm
from .location import LocationService
from django.contrib.admin.views.decorators import staff_member_required
from .delivery import DeliveryManager
from .pricing import compute_delivery_fee
from django.utils import timezone
import random

def home(request):
    q = request.GET.get('q')
    restaurants = Restaurant.objects.all()
    menu_items = MenuItem.objects.filter(is_available=True)
    if q:
        restaurants = restaurants.filter(name__icontains=q)
        menu_items = menu_items.filter(name__icontains=q)
    return render(request, 'home.html', {
        'restaurants': restaurants[:10],
        'menu_items': menu_items[:10],
        'q': q or ''
    })


def search(request):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    restaurants = Restaurant.objects.none()
    menu_items = MenuItem.objects.none()
    if q:
        restaurants = Restaurant.objects.filter(name__icontains=q)
        menu_items = MenuItem.objects.filter(is_available=True, name__icontains=q)
        if category:
            menu_items = menu_items.filter(category=category)
        if min_price:
            try:
                menu_items = menu_items.filter(price__gte=float(min_price))
            except Exception:
                pass
        if max_price:
            try:
                menu_items = menu_items.filter(price__lte=float(max_price))
            except Exception:
                pass
    return render(request, 'search/results.html', {
        'q': q,
        'restaurants': restaurants,
        'menu_items': menu_items,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
    })

# Customer views
@login_required
@user_passes_test(lambda u: u.user_type == 'customer')
def customer_dashboard(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'customer/dashboard.html', {'orders': orders})

# Custom admin views have been removed

# Delivery personnel views
@login_required
@user_passes_test(lambda u: u.user_type == 'delivery')
def delivery_dashboard(request):
    try:
        delivery_person = DeliveryPersonnel.objects.get(user=request.user)
        assigned_orders = Order.objects.filter(
            delivery_person=delivery_person,
            status__in=['confirmed', 'preparing', 'out_for_delivery']
        ).order_by('estimated_delivery_time')
        
        context = {
            'delivery_person': delivery_person,
            'assigned_orders': assigned_orders,
        }
        return render(request, 'delivery/dashboard.html', context)
    except DeliveryPersonnel.DoesNotExist:
        return redirect('home')


@login_required
@user_passes_test(lambda u: u.user_type == 'delivery')
def delivery_update_status(request, order_id, action):
    order = get_object_or_404(Order, order_id=order_id)
    try:
        delivery_person = DeliveryPersonnel.objects.get(user=request.user)
    except DeliveryPersonnel.DoesNotExist:
        return redirect('home')
    if order.delivery_person_id != delivery_person.id:
        messages.error(request, 'This order is not assigned to you.')
        return redirect('delivery_dashboard')
    if action == 'picked' and order.status in ['preparing', 'confirmed']:
        order.status = 'out_for_delivery'
        order.save()
        messages.success(request, 'Order picked up.')
    elif action == 'delivered' and order.status == 'out_for_delivery':
        order.status = 'delivered'
        order.save()
        messages.success(request, 'Order delivered.')
    else:
        messages.error(request, 'Invalid action.')
    return redirect('delivery_dashboard')


@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:5]
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'addresses': addresses,
        'recent_orders': orders
    }
    return render(request, 'profile.html', context)


@login_required
def request_phone_otp(request):
    if not request.user.phone_number:
        messages.error(request, 'Add a phone number to your profile first.')
        return redirect('profile')
    code = f"{random.randint(100000, 999999)}"
    request.user.otp_code = code
    request.user.otp_expires_at = timezone.now() + timezone.timedelta(minutes=10)
    request.user.save(update_fields=['otp_code', 'otp_expires_at'])
    # In production, send via SMS provider. For now, show in message/console.
    messages.info(request, f'OTP sent to {request.user.phone_number}: {code}')
    return redirect('verify_phone_otp')


@login_required
def verify_phone_otp(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        if (
            request.user.otp_code
            and code == request.user.otp_code
            and request.user.otp_expires_at
            and timezone.now() <= request.user.otp_expires_at
        ):
            request.user.phone_verified = True
            request.user.otp_code = ''
            request.user.save(update_fields=['phone_verified', 'otp_code'])
            messages.success(request, 'Phone number verified.')
            return redirect('profile')
        messages.error(request, 'Invalid or expired code.')
    return render(request, 'auth/verify_phone.html')


@login_required
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id, customer=request.user)
        
        # Check if the order can be cancelled
        if order.can_cancel():
            # Update order status
            order.status = 'cancelled'
            order.save()
            
            # Process refund if payment was made online
            if order.payment_method == 'online' and order.payment_status:
                try:
                    payment = Payment.objects.get(order=order)
                    refund_result = PaymentGateway.process_refund(payment)
                    
                    if refund_result['success']:
                        messages.success(request, 'Order cancelled successfully and refund initiated.')
                    else:
                        messages.warning(request, f'Order cancelled but there was an issue with the refund: {refund_result["message"]}')
                except Payment.DoesNotExist:
                    messages.warning(request, 'Order cancelled but payment record not found for refund.')
            else:
                messages.success(request, 'Order cancelled successfully.')
            
            return redirect('order_details', order_id=order_id)
        else:
            messages.error(request, 'This order cannot be cancelled. It may be too late or the order is already being processed.')
            return redirect('order_details', order_id=order_id)
            
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('customer_dashboard')


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant/list.html', {'restaurants': restaurants})

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    q = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    menu_qs = MenuItem.objects.filter(restaurant=restaurant, is_available=True)
    if q:
        menu_qs = menu_qs.filter(name__icontains=q)
    if category:
        menu_qs = menu_qs.filter(category=category)
    if min_price:
        try:
            menu_qs = menu_qs.filter(price__gte=float(min_price))
        except Exception:
            pass
    if max_price:
        try:
            menu_qs = menu_qs.filter(price__lte=float(max_price))
        except Exception:
            pass
    return render(request, 'restaurant/detail.html', {'restaurant': restaurant, 'menu_items': menu_qs, 'category': category, 'min_price': min_price, 'max_price': max_price})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, customer=request.user)
    return render(request, 'order/details.html', {'order': order})


@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, customer=request.user)
    if order.payment_status or order.payment_method != 'online':
        return redirect('order_details', order_id=order.order_id)
    if request.method == 'POST':
        result = PaymentGateway.process_payment(order, 'online', float(order.total_amount))
        if result.get('success'):
            messages.success(request, 'Payment successful.')
            return redirect('order_details', order_id=order.order_id)
        messages.error(request, f"Payment failed: {result.get('message')}")
    return render(request, 'payment/pay.html', {'order': order})


# --------- Cart and Checkout ---------

def _get_cart(session):
    cart = session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    return cart


def _save_cart(session, cart):
    session['cart'] = cart
    session.modified = True


def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id, is_available=True)
    cart = _get_cart(request.session)

    # Enforce single-restaurant cart
    cart_restaurant_id = cart.get('restaurant_id')
    if cart_restaurant_id and cart_restaurant_id != item.restaurant_id:
        messages.error(request, 'You already have items from another restaurant in your cart. Please clear the cart first.')
        return redirect('view_cart')

    cart.setdefault('restaurant_id', item.restaurant_id)
    cart.setdefault('items', {})
    qty = 1
    if request.method == 'POST':
        try:
            qty = max(1, int(request.POST.get('qty', '1')))
        except Exception:
            qty = 1
    item_key = str(item.id)
    line = cart['items'].get(item_key, {'name': item.name, 'price': float(item.price), 'qty': 0})
    line['qty'] += qty
    cart['items'][item_key] = line
    _save_cart(request.session, cart)
    messages.success(request, 'Item added to cart.')
    return redirect('restaurant_detail', pk=item.restaurant_id)


def update_cart_item(request, item_id):
    if request.method != 'POST':
        return redirect('view_cart')
    qty = int(request.POST.get('qty', '1'))
    cart = _get_cart(request.session)
    if 'items' not in cart:
        return redirect('view_cart')
    key = str(item_id)
    if key in cart['items']:
        if qty <= 0:
            del cart['items'][key]
        else:
            cart['items'][key]['qty'] = qty
        if not cart['items']:
            cart.clear()
    _save_cart(request.session, cart)
    return redirect('view_cart')


def clear_cart(request):
    request.session.pop('cart', None)
    messages.info(request, 'Cart cleared.')
    return redirect('restaurant_list')


def view_cart(request):
    cart = _get_cart(request.session)
    items = []
    subtotal = 0.0
    restaurant = None
    if cart and cart.get('items'):
        ids = [int(k) for k in cart['items'].keys()]
        menu_map = {m.id: m for m in MenuItem.objects.filter(id__in=ids)}
        for k, line in cart['items'].items():
            mid = int(k)
            menu = menu_map.get(mid)
            if not menu:
                continue
            qty = line['qty']
            price = float(menu.price)
            total = qty * price
            subtotal += total
            items.append({'id': mid, 'name': menu.name, 'qty': qty, 'price': price, 'total': total})
        if cart.get('restaurant_id'):
            restaurant = Restaurant.objects.filter(id=cart['restaurant_id']).first()
    return render(request, 'cart/view.html', {'items': items, 'subtotal': subtotal, 'restaurant': restaurant})


@login_required
def checkout(request):
    cart = _get_cart(request.session)
    if not cart or not cart.get('items'):
        messages.error(request, 'Your cart is empty.')
        return redirect('restaurant_list')

    addresses = Address.objects.filter(user=request.user, is_serviceable=True)
    # Build summary
    items = []
    subtotal = 0.0
    ids = [int(k) for k in cart['items'].keys()]
    menu_map = {m.id: m for m in MenuItem.objects.filter(id__in=ids)}
    for k, line in cart['items'].items():
        menu = menu_map.get(int(k))
        if not menu:
            continue
        qty = int(line['qty'])
        price = float(menu.price)
        total = qty * price
        subtotal += total
        items.append({'id': menu.id, 'name': menu.name, 'qty': qty, 'price': price, 'total': total})

    # Compute delivery fee using coordinates if available
    restaurant = Restaurant.objects.filter(id=cart.get('restaurant_id')).first()
    sample_address = None
    if addresses:
        sample_address = addresses.first()
    delivery_fee = compute_delivery_fee(restaurant.address if restaurant else None, sample_address, subtotal) if (restaurant and sample_address) else (0.0 if subtotal >= 50 else 2.50)

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        payment_method = request.POST.get('payment_method', 'cod')
        address = get_object_or_404(Address, id=address_id, user=request.user)

        # Build totals
        total_amount = subtotal + delivery_fee

        restaurant = get_object_or_404(Restaurant, id=cart['restaurant_id'])
        order = Order.objects.create(
            customer=request.user,
            restaurant=restaurant,
            delivery_address=address,
            status='pending',
            payment_method=payment_method,
            total_amount=total_amount,
            delivery_fee=delivery_fee,
        )
        # Items
        for k, line in cart['items'].items():
            menu = menu_map.get(int(k))
            if not menu:
                continue
            OrderItem.objects.create(
                order=order,
                menu_item=menu,
                quantity=int(line['qty']),
                price=menu.price,
            )

        if payment_method == 'online':
            request.session.pop('cart', None)
            messages.info(request, 'Order created. Please complete payment.')
            return redirect('pay_order', order_id=order.order_id)
        else:
            payment_result = PaymentGateway.process_payment(order, payment_method, total_amount)
            if not payment_result.get('success'):
                messages.error(request, f"Payment failed: {payment_result.get('message')}")
                order.status = 'cancelled'
                order.save()
                return redirect('view_cart')
            request.session.pop('cart', None)
            messages.success(request, 'Order placed successfully.')
            return redirect('order_details', order_id=order.order_id)

    return render(request, 'checkout/checkout.html', {'addresses': addresses, 'items': items, 'subtotal': subtotal, 'delivery_fee': delivery_fee, 'grand_total': subtotal + delivery_fee})


@login_required
def add_address(request):
    if request.method == 'POST':
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        latitude = request.POST.get('latitude') or None
        longitude = request.POST.get('longitude') or None
        try:
            addr = Address.objects.create(
                user=request.user,
                address_line=address_line,
                city=city,
                state=state,
                postal_code=postal_code,
                latitude=latitude if latitude else None,
                longitude=longitude if longitude else None,
            )
            LocationService.check_and_update_address_serviceability(addr)
            messages.success(request, 'Address added.')
        except Exception as e:
            messages.error(request, f'Failed to add address: {e}')
        return redirect('profile')
    return render(request, 'address/add.html')


@login_required
def delete_address(request, address_id):
    addr = get_object_or_404(Address, id=address_id, user=request.user)
    addr.delete()
    messages.info(request, 'Address deleted.')
    return redirect('profile')


@staff_member_required
def upload_restaurant_image(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST' and request.FILES.get('image'):
        restaurant.image = request.FILES['image']
        restaurant.save()
        messages.success(request, 'Restaurant image updated.')
        return redirect('restaurant_detail', pk=restaurant.id)
    return render(request, 'restaurant/upload_image.html', {'restaurant': restaurant})
