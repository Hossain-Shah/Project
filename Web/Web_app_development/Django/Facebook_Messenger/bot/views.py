import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
import requests


def post_facebook_message(fbid, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' %(EAAMtcUCLo5IBACUIZCTEOVdEonSRDZBfx5PZAttZCEQjSwJggn9IZBQ8iYdzzpZBzT6lSYZAnU5yYJchTTf53A5wGYT9970Wi81cRIfKQEbQZAwKRgMHqeEZAAzZClmxoCCoJl2jTEdix8AeAIZBELPMln1CKc1OfGBNNk0peORBHLQ3n72Dd4AHWZAE
)
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)


def process_message(fb_id, msg):
 # You can manipulate and analyze the contents of the user's message in msg
 # For now we will just leave it and always send a static greeting for every message
 greeting = "Hi John! I'm alive!"
 post_facebook_message(fb_id, greeting)


class BotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == 'SECRET85':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    # Post function to handle Facebook messages

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    print(message['message']['text'])
        return HttpResponse()