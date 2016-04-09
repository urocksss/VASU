from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse



#from tnp.forms import RegistrationForm
from feemgmt.models import *
#from django.contrib.auth.decorators import login_require
#from django.contrib.auth import login,logout 
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.context_processors import csrf 

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def randomword():
	choose="qwertyuiopasdfghjklzxcvbnm1234567890AQWSEDRFTGYHUJIKOLPZXCVBNM"
   	return ''.join(random.choice(choose) for i in range(25))

def print_history(request):
	#if request.method == 'POST':
		print "in post"
		stud_id=1001
		print stud_id
		trans = Transactions.objects.filter(stud_id=stud_id) #can be taken from session
	        #print trans
		#for t in trans:
		print "in get"
		args = {'trans':trans}

		print args
		return render_to_response(
			'/home/vrushali/Desktop/bis/INSTI/feemgmt/templates/print_history.html',args
			)
			 
		
	

