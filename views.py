
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
import sqlalchemy as sa
# Create your views here.

from sqlalchemy import create_engine
from sqlalchemy import extract
from sqlalchemy import cast
from sqlalchemy import func
from sqlalchemy import Column, ForeignKey, Integer, String,Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

Base = automap_base()
engine = create_engine('postgresql://dbmasteruser:rqM&y9]Hy>3o)eQ~WQA9:0O8vQilj;rO@ls-449373e22b69bfd9f636b38fc3ef306b0da46ee7.cw8iknkapczz.ca-central-1.rds.amazonaws.com:5432/postgres')
Base.prepare(engine, reflect=True)

predictit = Base.classes.predictitDF
DBSession = sessionmaker(bind=engine)
session = DBSession()





def index(request):
	form = UserCreationForm()
	if request.user.is_authenticated:
		return render(request,'dashboard.html')
	else:
		return render(request, 'index.html',context={"form":form})

def dashboard(request):
	tickers = session.query(predictit.index).all()
	return render(request, 'dashboard.html', context={"tickers":tickers})

def logout_request(request):
	logout(request)
	return redirect("altData:index")

def login_request(request):
	username = password = ''
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('altData:dashboard')
		form = AuthenticationForm()
		return render(request = request, template_name= "registration/login.html",
			context={"form":form,"error":"TRUE"})
	form = AuthenticationForm()
	return render(request = request,
                  template_name = "registration/login.html",
                  context={"form":form,"error":"FALSE"})


def register_user(request):
	form = UserCreationForm()
	context = {}
	if request.user.is_authenticated:
		return redirect('altData:dashboard')
	else:
		if request.method == 'POST':
			form = UserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('altData:dashboard')
			else:
				context['error'] = "TRUE"
	context['form'] = form
	return render(request, 'index.html', context)

def ticker_view(request,ticker):
	ticker = ticker.upper()
	predictit_data = session.query(predictit.Biden_General,predictit.Sanders_General,predictit.Trump_General,predictit.Warren_General).filter(predictit.index == ticker).all()
	context = {}
	context['predictit'] = predictit_data
	context['ticker'] = ticker
	return render(request, 'tickerView.html', context)
