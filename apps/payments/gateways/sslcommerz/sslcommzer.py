from sslcommerz_lib import SSLCOMMERZ
import uuid
from decouple import config


def SslCommerzPayment(product_name, amount, email, phone=None):
    store = {
     'store_id': config("STOREID"), 
    'store_pass': config("STOREPASS"),  
    'issandbox': config("SANDBOX", default=True, cast=bool) 
}

    sslcommerz = SSLCOMMERZ(store)
    transection_id =  str(uuid.uuid4())
    payment_data = {
        'total_amount': float(amount),  
        'currency': "BDT", 
        'tran_id': transection_id,  
        'success_url': "http://localhost:8000/api/v1/sslcz/payment/success/",  
        'fail_url': "http://localhost:8000/api/v1/sslcz/payment/failed/", 
        'cancel_url': "http://localhost:5173/",  
        'emi_option': 0, 
        'cus_name': email,
        'cus_email': email,  
        'cus_phone': phone or "",
        'cus_add1': "customer address",
        'cus_city': "Dhaka", 
        'cus_country': "Bangladesh", 
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': 1,  
        'product_name':product_name,
        'product_category': "Test Category", 
        'product_profile': "general",
         "value_a": product_name,
         "value_b":email
    }
    
    try:
        response = sslcommerz.createSession(payment_data) 

        return {
            "GatewayPageURL": response.get("GatewayPageURL"),
            "tran_id" : response.get("sessionkey") 
        }
    except Exception as e:
        print("from ssl", str(e))
        return {'error': str(e)}