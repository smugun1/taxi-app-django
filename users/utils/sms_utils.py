# # utils/sms_utils.py

# import requests
# import plivo # type: ignore
# from . import send_sms_nexmo, send_sms_plivo


# # Nexmo SMS sending function
# def send_sms_nexmo(phone_number, message):
#     url = 'https://rest.nexmo.com/sms/json'
#     params = {
#         'api_key': 'your_api_key',
#         'api_secret': 'your_api_secret',
#         'from': 'your_sender_number',
#         'to': phone_number,
#         'text': message,
#     }
#     response = requests.post(url, data=params)
#     return response.json()

# # Plivo SMS sending function
# def send_sms_plivo(phone_number, message):
#     client = plivo.RestClient(auth_id='your_auth_id', auth_token='your_auth_token')
#     response = client.messages.create(
#         src='your_sender_number',
#         dst=phone_number,
#         text=message,
#     )
#     return response
