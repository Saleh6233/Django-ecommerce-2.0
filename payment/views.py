import logging
import threading

from django.conf import settings
from django.core.mail import send_mail
from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import render

from cart.cart import Cart
from .models import ShippingAddress, Order, OrderItem

logger = logging.getLogger('__name__')


# Create your views here.


def checkout(request):
    if request.user.is_authenticated:

        try:

            shipping_address = ShippingAddress.objects.get(
                user=request.user.id)

            context = {'shipping': shipping_address}

            return render(request, 'payment/checkout.html', context)

        except:

            return render(request, 'payment/checkout.html')

    else:

        return render(request, 'payment/checkout.html')


def payment_success(request):
    for key in list(request.session.keys()):

        if key == 'session_key':
            del request.session[key]

    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    return render(request, 'payment/payment-failed.html')


def send_email_async(order_id, email_subject, email_message, recipient_email):
    """
    Handle email sending with connection cleanup and error logging
    This function runs in a separate thread
    """
    try:
        # Close any existing database connections
        connection.close()

        # Actual email sending
        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        logger.info(f"Successfully sent email for order #{order_id}")
    except Exception as e:
        logger.error(f"Failed to send email for order #{order_id}: {str(e)}")


logger = logging.getLogger('__name__')


# Other views remain unchanged...

def complete_order(request):
    if request.POST.get('action') == 'post':
        try:
            # Extract form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
            shipping_address = f"{address1}\n{address2}\n{city}\n{state}\n{zipcode}"

            # Initialize cart and calculate total
            cart = Cart(request)
            total_cost = cart.get_total()

            # Determine user (authenticated or None)
            user = request.user if request.user.is_authenticated else None

            # Use atomic transaction to ensure all database operations succeed or fail together
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    full_name=name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=total_cost,
                    user=user
                )
                order_id = order.pk

                # Create order items, update product quantities, and prepare invoice
                invoice_items = []
                for item in cart:
                    product = item['product']
                    quantity = item['qty']

                    # Create order item
                    OrderItem.objects.create(
                        order_id=order_id,
                        product=product,
                        quantity=quantity,
                        price=item['price'],
                        user=user
                    )

                    # Update product quantity in database
                    product.quantity -= quantity
                    product.save()

                    # Add to invoice
                    invoice_items.append(
                        f"{product} - {quantity} x ${item['price']:.2f}"
                    )

            # Prepare and send invoice email (outside transaction block to avoid holding DB connection)
            items_str = "\n".join(invoice_items)
            email_subject = f"Your Order Invoice #{order_id}"
            email_message = (
                f"Hello {name},\n\n"
                f"Thank you for your order! Below is your invoice:\n\n"
                f"Order ID: {order_id}\n"
                f"Date: {order.date_ordered}\n\n"
                f"Items:\n{items_str}\n\n"
                f"Shipping Address:\n{shipping_address}\n\n"
                f"Total Amount: ${total_cost:.2f}\n\n"
                f"If you have any questions, please contact our customer support.\n\n"
                f"Thank you for shopping with us!"
            )

            # Start email thread with daemon flag
            email_thread = threading.Thread(
                target=send_email_async,
                args=(order_id, email_subject, email_message, email),
                daemon=True
            )
            email_thread.start()

            # Return success response
            order_success = True
            response = JsonResponse({'order_success': order_success})
            return response

        except KeyError as ke:
            logger.error(f"Missing form field: {str(ke)}")
            return JsonResponse({'order_success': False, 'error': 'Invalid form data'}, status=400)

        except Exception as e:
            logger.error(f"Order processing failed: {str(e)}")
            return JsonResponse({'order_success': False, 'error': 'Server error'}, status=500)
