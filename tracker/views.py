import random
import functools
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import CustomUser, Order, Restaurant, FoodItem


# ─────────────────────────────────────────────
#  Email helper
# ─────────────────────────────────────────────
def send_order_confirmation_email(order):
    """Send a styled HTML confirmation email to the customer after order creation."""
    customer = order.customer
    to_email = customer.email
    if not to_email:
        return  # No email registered – skip silently

    subject = f"📦 Order Confirmed! Your Order #{order.id} is Being Prepared"

    # ─ Plain-text fallback ─
    text_body = (
        f"Hi {customer.username},\n\n"
        f"Your order has been placed successfully!\n\n"
        f"Order ID    : #{order.id}\n"
        f"Items       : {order.item_details}\n"
        f"Address     : {order.delivery_address}\n"
        f"Total Price : ₨{order.total_price}\n"
        f"Status      : {order.status}\n"
        + (f"Rider       : {order.driver.username}\n" if order.driver else "Rider       : Being assigned\n") +
        f"\nThank you for ordering with us!\n\nFood Delivery Team"
    )

    # ─ HTML email body ─
    driver_row = (
        f"""
        <tr>
          <td style="padding:8px 12px;color:#6b7280;font-weight:600;">Rider</td>
          <td style="padding:8px 12px;color:#111827;">{order.driver.username}</td>
        </tr>"""
        if order.driver else
        """
        <tr>
          <td style="padding:8px 12px;color:#6b7280;font-weight:600;">Rider</td>
          <td style="padding:8px 12px;color:#f59e0b;">Being assigned shortly</td>
        </tr>"""
    )

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="margin:0;padding:0;background:#f3f4f6;font-family:'Segoe UI',Arial,sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f3f4f6;padding:40px 0;">
        <tr><td align="center">
          <table width="580" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

            <!-- Header -->
            <tr>
              <td style="background:linear-gradient(135deg,#f97316,#ef4444);padding:36px 40px;text-align:center;">
                <div style="font-size:40px;margin-bottom:8px;">🛍️</div>
                <h1 style="margin:0;color:#ffffff;font-size:24px;font-weight:700;">
                  Order Confirmed!
                </h1>
                <p style="margin:8px 0 0;color:rgba(255,255,255,0.85);font-size:15px;">
                  Your delicious food is being prepared
                </p>
              </td>
            </tr>

            <!-- Greeting -->
            <tr>
              <td style="padding:32px 40px 16px;">
                <p style="margin:0;font-size:16px;color:#374151;">
                  Hi <strong>{customer.username}</strong>, 👋
                </p>
                <p style="margin:12px 0 0;font-size:15px;color:#6b7280;line-height:1.6;">
                  Great news! Your order has been placed successfully and
                  our kitchen is already working on it.
                </p>
              </td>
            </tr>

            <!-- Order Summary Table -->
            <tr>
              <td style="padding:16px 40px 32px;">
                <table width="100%" cellpadding="0" cellspacing="0"
                       style="background:#f9fafb;border-radius:12px;border:1px solid #e5e7eb;overflow:hidden;">
                  <tr style="background:#f3f4f6;">
                    <td colspan="2" style="padding:12px 16px;font-weight:700;font-size:14px;color:#374151;letter-spacing:.5px;text-transform:uppercase;">Order Details</td>
                  </tr>
                  <tr>
                    <td style="padding:8px 12px;color:#6b7280;font-weight:600;">Order ID</td>
                    <td style="padding:8px 12px;color:#111827;"><strong>#{order.id}</strong></td>
                  </tr>
                  <tr style="background:#fff;">
                    <td style="padding:8px 12px;color:#6b7280;font-weight:600;">Items</td>
                    <td style="padding:8px 12px;color:#111827;">{order.item_details}</td>
                  </tr>
                  <tr>
                    <td style="padding:8px 12px;color:#6b7280;font-weight:600;">Delivery Address</td>
                    <td style="padding:8px 12px;color:#111827;">{order.delivery_address}</td>
                  </tr>
                  <tr style="background:#fff;">
                    <td style="padding:8px 12px;color:#6b7280;font-weight:600;">Total Price</td>
                    <td style="padding:8px 12px;color:#059669;font-weight:700;font-size:16px;">₨{order.total_price}</td>
                  </tr>
                  <tr>
                    <td style="padding:8px 12px;color:#6b7280;font-weight:600;">Status</td>
                    <td style="padding:8px 12px;">
                      <span style="background:#dbeafe;color:#1d4ed8;padding:3px 10px;border-radius:99px;font-size:13px;font-weight:600;">
                        {order.status}
                      </span>
                    </td>
                  </tr>
                  {driver_row}
                </table>
              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td style="background:#f9fafb;border-top:1px solid #e5e7eb;padding:24px 40px;text-align:center;">
                <p style="margin:0;font-size:13px;color:#9ca3af;">This is an automated message from Food Delivery. Please do not reply.</p>
                <p style="margin:8px 0 0;font-size:13px;color:#9ca3af;">&copy; 2026 Food Delivery. All rights reserved.</p>
              </td>
            </tr>

          </table>
        </td></tr>
      </table>
    </body>
    </html>
    """

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
    except Exception as e:
        # Log to server console but never break the order flow
        import traceback
        print(f"[EMAIL ERROR] Failed to send confirmation to {to_email}: {e}")
        traceback.print_exc()



# ─────────────────────────────────────────────
#  Role guard decorator
# ─────────────────────────────────────────────
def role_required(roles):
    def decorator(view_func):
        @functools.wraps(view_func)          # preserves __name__ so login_required works
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in roles:
                return HttpResponseForbidden("You do not have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# ─────────────────────────────────────────────
#  Public views
# ─────────────────────────────────────────────
def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'driver':
            return redirect('driver_dashboard')
        elif request.user.role == 'customer':
            return redirect('customer_dashboard')
    return render(request, 'tracker/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, 'tracker/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'tracker/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email    = request.POST.get('email', '').strip()
        phone    = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '')
        role     = request.POST.get('role', 'customer')

        # Validate required fields
        if not username or not email or not password:
            messages.error(request, "Username, email and password are required.")
            return render(request, 'tracker/register.html')

        # Validate role
        if role not in ('customer', 'driver', 'admin'):
            messages.error(request, "Invalid account role selected.")
            return render(request, 'tracker/register.html')

        # Check duplicate username
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken. Please choose another.")
            return render(request, 'tracker/register.html')

        # Check duplicate email
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "An account with that email already exists.")
            return render(request, 'tracker/register.html')

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone or None,
                role=role
            )
            login(request, user)
            messages.success(request, f"Welcome, {username}! Your account has been created.")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")

    return render(request, 'tracker/register.html')


@require_POST          # logout must be POST only (CSRF protection)
def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────────
#  Customer views
# ─────────────────────────────────────────────
@login_required
@role_required(['customer'])
def customer_dashboard(request):
    all_orders    = Order.objects.filter(customer=request.user).select_related('driver', 'restaurant').order_by('-id')
    active_orders = all_orders.exclude(status__in=['Delivered', 'Cancelled'])
    past_orders   = all_orders.filter(status__in=['Delivered', 'Cancelled'])

    total_spent = (
        all_orders.exclude(status='Cancelled')
        .aggregate(total=Sum('total_price'))['total'] or 0
    )

    latest_order    = all_orders.first()
    latest_order_id = latest_order.id if latest_order else None

    restaurants = Restaurant.objects.prefetch_related('fooditem_set').all()

    context = {
        'active_orders':  active_orders,
        'past_orders':    past_orders,
        'latest_order_id': latest_order_id,
        'total_spent':    total_spent,
        'restaurants':    restaurants,
        # Category counts
        'all_count':      restaurants.count(),
        'burgers_count':  restaurants.filter(cuisine='Burgers & American').count(),
        'pizzas_count':   restaurants.filter(cuisine='Italian & Pizza').count(),
        'asian_count':    restaurants.filter(cuisine='Asian & Noodles').count(),
        'desserts_count': restaurants.filter(cuisine='Desserts & Bakery').count(),
    }
    return render(request, 'tracker/customer_dashboard.html', context)


@login_required
@role_required(['customer'])
@require_POST
def create_order(request):
    item_details     = request.POST.get('item_details', '').strip()
    delivery_address = request.POST.get('delivery_address', '').strip()
    restaurant_id    = request.POST.get('restaurant_id', '').strip()

    # Parse and validate total_price
    try:
        total_price = float(request.POST.get('total_price', 0))
        if total_price < 0:
            total_price = 0
    except (ValueError, TypeError):
        total_price = 0

    if not item_details or not delivery_address:
        messages.error(request, "Item details and delivery address are required.")
        return redirect('customer_dashboard')

    # Resolve restaurant
    restaurant = None
    if restaurant_id:
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            pass  # Order placed without a linked restaurant (edge case)

    # Auto-assign a random available driver
    driver = None
    status = 'Pending'
    available_drivers = list(CustomUser.objects.filter(role='driver'))
    if available_drivers:
        driver = random.choice(available_drivers)
        status = 'Assigned'

    order = Order.objects.create(
        customer         = request.user,
        restaurant       = restaurant,
        item_details     = item_details,
        delivery_address = delivery_address,
        status           = status,
        driver           = driver,
        total_price      = total_price,
    )

    if driver:
        messages.success(request, f"✅ Order placed! Rider {driver.username} is on the way.")
    else:
        messages.success(request, "✅ Order placed! We'll assign a rider shortly.")

    # ─ Send confirmation email to customer ─
    send_order_confirmation_email(order)

    return redirect('customer_dashboard')



# ─────────────────────────────────────────────
#  Driver views
# ─────────────────────────────────────────────
@login_required
@role_required(['driver'])
def driver_dashboard(request):
    orders = Order.objects.filter(driver=request.user).select_related('customer', 'restaurant').order_by('-id')
    return render(request, 'tracker/driver_dashboard.html', {'orders': orders})


@login_required
@role_required(['driver'])
@require_POST
def update_status(request, order_id):
    order      = get_object_or_404(Order, id=order_id, driver=request.user)
    new_status = request.POST.get('status', '').strip()

    allowed = ['Picked Up', 'Delivered']
    if new_status not in allowed:
        messages.error(request, f"Invalid status. Allowed: {', '.join(allowed)}")
        return redirect('driver_dashboard')

    # Prevent going backwards (Delivered → Picked Up)
    status_order = ['Pending', 'Assigned', 'Picked Up', 'Delivered']
    current_idx  = status_order.index(order.status) if order.status in status_order else 0
    new_idx      = status_order.index(new_status)
    if new_idx < current_idx:
        messages.error(request, "Cannot set a previous status.")
        return redirect('driver_dashboard')

    order.status = new_status
    order.save()
    messages.success(request, f"Order #{order.id} updated to '{new_status}'.")
    return redirect('driver_dashboard')


# ─────────────────────────────────────────────
#  Admin views
# ─────────────────────────────────────────────
@login_required
@role_required(['admin'])
def admin_dashboard(request):
    total_orders    = Order.objects.count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    pending_orders  = Order.objects.filter(status='Pending').count()
    assigned_orders = Order.objects.filter(status='Assigned').count()
    picked_up_orders = Order.objects.filter(status='Picked Up').count()
    cancelled_orders = Order.objects.filter(status='Cancelled').count()

    status_filter = request.GET.get('status', '').strip()
    valid_statuses = ['Pending', 'Assigned', 'Picked Up', 'Delivered', 'Cancelled']
    if status_filter in valid_statuses:
        orders = Order.objects.filter(status=status_filter).select_related('customer', 'driver', 'restaurant').order_by('-id')
    else:
        orders = Order.objects.all().select_related('customer', 'driver', 'restaurant').order_by('-id')
        status_filter = ''

    drivers   = CustomUser.objects.filter(role='driver')
    customers = CustomUser.objects.filter(role='customer')
    all_users = CustomUser.objects.all().order_by('role', 'username')

    context = {
        'total_orders':    total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders':  pending_orders,
        'assigned_orders': assigned_orders,
        'picked_up_orders': picked_up_orders,
        'cancelled_orders': cancelled_orders,
        'orders':          orders,
        'drivers':         drivers,
        'customers':       customers,
        'all_users':       all_users,
        'selected_status': status_filter,
        'valid_statuses':  valid_statuses,
    }
    return render(request, 'tracker/admin_dashboard.html', context)


@login_required
@role_required(['admin'])
@require_POST
def assign_driver(request, order_id):
    order     = get_object_or_404(Order, id=order_id)
    driver_id = request.POST.get('driver_id', '').strip()

    if not driver_id:
        messages.error(request, "Please select a driver.")
        return redirect('admin_dashboard')

    driver = get_object_or_404(CustomUser, id=driver_id, role='driver')
    order.driver = driver
    order.status = 'Assigned'
    order.save()
    messages.success(request, f"Driver {driver.username} assigned to Order #{order.id}.")
    return redirect('admin_dashboard')


# ── Admin User CRUD ──────────────────────────
@login_required
@role_required(['admin'])
@require_POST
def admin_create_user(request):
    username = request.POST.get('username', '').strip()
    email    = request.POST.get('email', '').strip()
    phone    = request.POST.get('phone', '').strip()
    password = request.POST.get('password', '')
    role     = request.POST.get('role', 'customer')

    if not username or not email or not password or role not in ('customer', 'driver', 'admin'):
        messages.error(request, "All fields are required and role must be valid.")
        return redirect('admin_dashboard')

    if CustomUser.objects.filter(username=username).exists():
        messages.error(request, f"Username '{username}' already exists.")
        return redirect('admin_dashboard')

    CustomUser.objects.create_user(
        username=username, email=email,
        password=password, phone=phone or None, role=role
    )
    messages.success(request, f"User '{username}' created successfully.")
    return redirect('admin_dashboard')


@login_required
@role_required(['admin'])
@require_POST
def admin_edit_user(request, user_id):
    user     = get_object_or_404(CustomUser, id=user_id)
    username = request.POST.get('username', '').strip()
    email    = request.POST.get('email', '').strip()
    phone    = request.POST.get('phone', '').strip()
    role     = request.POST.get('role', '').strip()
    password = request.POST.get('password', '')

    if not username or not email or role not in ('customer', 'driver', 'admin'):
        messages.error(request, "Username, email and a valid role are required.")
        return redirect('admin_dashboard')

    if CustomUser.objects.filter(username=username).exclude(id=user_id).exists():
        messages.error(request, f"Username '{username}' is already taken.")
        return redirect('admin_dashboard')

    user.username = username
    user.email    = email
    user.phone    = phone or None
    user.role     = role
    if password:
        user.set_password(password)
    user.save()
    messages.success(request, f"User '{username}' updated successfully.")
    return redirect('admin_dashboard')


@login_required
@role_required(['admin'])
@require_POST
def admin_delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('admin_dashboard')
    username = user.username
    user.delete()
    messages.success(request, f"User '{username}' deleted.")
    return redirect('admin_dashboard')


# ── Admin Order CRUD ─────────────────────────
@login_required
@role_required(['admin'])
@require_POST
def admin_create_order(request):
    customer_id      = request.POST.get('customer_id', '').strip()
    item_details     = request.POST.get('item_details', '').strip()
    delivery_address = request.POST.get('delivery_address', '').strip()
    status           = request.POST.get('status', 'Pending').strip()
    driver_id        = request.POST.get('driver_id', '').strip()

    try:
        total_price = float(request.POST.get('total_price', 0))
    except (ValueError, TypeError):
        total_price = 0

    if not item_details or not delivery_address or not customer_id:
        messages.error(request, "Customer, item details and address are required.")
        return redirect('admin_dashboard')

    customer = get_object_or_404(CustomUser, id=customer_id, role='customer')

    driver = None
    if driver_id:
        driver = get_object_or_404(CustomUser, id=driver_id, role='driver')
        if status == 'Pending':
            status = 'Assigned'

    valid_statuses = ['Pending', 'Assigned', 'Picked Up', 'Delivered', 'Cancelled']
    if status not in valid_statuses:
        status = 'Pending'

    Order.objects.create(
        customer=customer, item_details=item_details,
        delivery_address=delivery_address, status=status,
        driver=driver, total_price=total_price
    )
    messages.success(request, "Order created successfully.")
    return redirect('admin_dashboard')


@login_required
@role_required(['admin'])
@require_POST
def admin_edit_order(request, order_id):
    order            = get_object_or_404(Order, id=order_id)
    item_details     = request.POST.get('item_details', '').strip()
    delivery_address = request.POST.get('delivery_address', '').strip()
    status           = request.POST.get('status', order.status).strip()
    driver_id        = request.POST.get('driver_id', '').strip()

    try:
        total_price = float(request.POST.get('total_price', order.total_price))
    except (ValueError, TypeError):
        total_price = float(order.total_price)

    if not item_details or not delivery_address:
        messages.error(request, "Item details and delivery address are required.")
        return redirect('admin_dashboard')

    valid_statuses = ['Pending', 'Assigned', 'Picked Up', 'Delivered', 'Cancelled']
    if status not in valid_statuses:
        status = order.status

    # Only update driver if a driver_id was submitted in the form
    # Empty driver_id means "no change", not "remove driver"
    if driver_id:
        order.driver = get_object_or_404(CustomUser, id=driver_id, role='driver')
    # if driver_id is blank, keep existing driver (don't clear it)

    order.item_details     = item_details
    order.delivery_address = delivery_address
    order.status           = status
    order.total_price      = total_price
    order.save()
    messages.success(request, f"Order #{order.id} updated successfully.")
    return redirect('admin_dashboard')


@login_required
@role_required(['admin'])
@require_POST
def admin_delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    oid   = order.id
    order.delete()
    messages.success(request, f"Order #{oid} deleted.")
    return redirect('admin_dashboard')
