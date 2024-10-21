from sslcommerz_lib import SSLCOMMERZ
import uuid



def SslCommerzPayment(product_name, amount, email, phone=None):
    store = {
    'store_id': 'codec63b8d5fd1c1bf', 
    'store_pass': 'codec63b8d5fd1c1bf@ssl',
    'issandbox': True
}
    sslcommerz = SSLCOMMERZ(store)
    transection_id =  str(uuid.uuid4())
    payment_data = {
        'total_amount': float(amount),  
        'currency': "BDT", 
        'tran_id': transection_id,  
        'success_url': "http://localhost:5173/payment/success",  
        'fail_url': "http://localhost:5173/payment/fail", 
        'cancel_url': "http://localhost:5173/payment/cancel",  
        'emi_option': 0, 
        'cus_name': email,  # Customer name
        'cus_email': email,  # Customer email
        'cus_phone': phone or "",  # Customer phone number
        'cus_add1': "customer address",  # Customer address
        'cus_city': "Dhaka",  # Customer city
        'cus_country': "Bangladesh",  # Customer country
        'shipping_method': "NO",  # Shipping method
        'multi_card_name': "",  # Multi card option (if applicable)
        'num_of_item': 1,  # Number of items
        'product_name': "Test",  # Product name
        'product_category': "Test Category",  # Product category
        'product_profile': "general",  # Product profile
    }
    
    try:
        response = sslcommerz.createSession(payment_data) # API response
        return {
            "GatewayPageURL": response.get("GatewayPageURL"),
            "tran_id" : transection_id 
        }
    except Exception as e:
        print("from ssl", str(e))
        return {'error': str(e)}