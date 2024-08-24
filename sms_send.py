import requests

def Send_SMS(n1, n2, n3):
    requests.post(f"http://vas.mobilogi.com/api.php?username=ISHAAN&password=pass1234&route=1&sender=STIPLS&mobile[]={n1}&message[]=Please%20check%20routine%20of%20{n2}%20{n3},%20he%20left%20the%20campus%20for%201%20hour.%20Kindly%20do%20needful.%20STIPLS&templateid=1007937732269442138")
    
#Send_SMS("9149868903", "Yasir", "Malla")  

