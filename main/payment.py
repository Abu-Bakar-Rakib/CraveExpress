import uuid
from django.conf import settings
from .models import Payment, Order

class PaymentGateway:
    @staticmethod
    def process_payment(order, payment_method, amount):
        # Generate a unique payment ID
        payment_id = str(uuid.uuid4())
        
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            payment_id=payment_id,
            amount=amount,
            payment_method=payment_method,
            status='pending'
        )
        
        if payment_method == 'cod':
            # For cash on delivery, just mark as pending
            return {
                'success': True,
                'payment_id': payment_id,
                'message': 'Cash on delivery selected'
            }
        
        # For online payment (e.g., bKash, Nagad)
        # In a real implementation, you would integrate with the payment gateway's API
        # This is a placeholder for demonstration
        try:
            # Simulate API call to payment gateway
            # In production, replace with actual API call
            response = {
                'success': True,
                'transaction_id': f'TXN-{uuid.uuid4().hex[:10].upper()}',
                'status': 'completed'
            }
            
            # Update payment record
            payment.transaction_id = response['transaction_id']
            payment.status = response['status']
            payment.save()
            
            # Update order payment status if payment is successful
            if response['status'] == 'completed':
                order.payment_status = True
                order.save()
            
            return {
                'success': True,
                'payment_id': payment_id,
                'transaction_id': response['transaction_id'],
                'message': 'Payment processed successfully'
            }
            
        except Exception as e:
            payment.status = 'failed'
            payment.save()
            return {
                'success': False,
                'payment_id': payment_id,
                'message': str(e)
            }
    
    @staticmethod
    def process_refund(payment):
        # In a real implementation, you would integrate with the payment gateway's refund API
        try:
            # Simulate API call to payment gateway for refund
            # In production, replace with actual API call
            response = {
                'success': True,
                'refund_id': f'REF-{uuid.uuid4().hex[:10].upper()}',
                'status': 'refunded'
            }
            
            # Update payment record
            payment.status = 'refunded'
            payment.save()
            
            return {
                'success': True,
                'refund_id': response['refund_id'],
                'message': 'Refund processed successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }