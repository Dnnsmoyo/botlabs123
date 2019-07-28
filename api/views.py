from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
nltk.download('vader_lexicon')

import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings

from chatterbot.trainers import ChatterBotCorpusTrainer
from .tasks import send_data

from django.core.mail import send_mail
from django.conf import settings

chatbot = ChatBot('Robert')


trainer = ChatterBotCorpusTrainer(chatbot)


chatbot.set_trainer(ChatterBotCorpusTrainer)

chatbot.train("chatterbot.corpus.english")

class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    #chatterbot = ChatBot(**settings.CHATTERBOT)
    

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        #response = self.chatterbot.get_response(input_data)
        response = chatbot.get_response(input_data)
        response_data = response.serialize()
        send_data.delay(response_data)
        if response =='bye':
            return JsonResponse(response_data, status=200)

        return JsonResponse(response_data, status=200)


    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })
        


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request,'signup.html',{'form': form})

def myview(request):
    return render(request,'science_bot.html')

def index(request):
    return render(request,'index.html')

def email(request):    
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['dnnsmoyo@gmail.com',]    
    send_mail( subject, message, email_from, recipient_list )    
    return redirect('/')