import random

# Create your views here.
from django.http import HttpResponseRedirect

from feemgmt.models import *
from django.shortcuts import render_to_response


# Create your views here.

def randomword():
    choose = "qwertyuiopasdfghjklzxcvbnm1234567890AQWSEDRFTGYHUJIKOLPZXCVBNM"
    return ''.join(random.choice(choose) for i in range(25))

def print_history(request):
    if request.method == 'POST' and request.user.is_authenticated():
        print("in post")
        stud_id = request.user.user_map.stud_id.stud_id
        print(stud_id)
        trans = Transactions.objects.filter(stud_id=stud_id)  # can be taken from session
        # print trans
		#for t in trans:
        print("in get")
        args = {'trans': trans}
        print(args)
        return render_to_response('print_history.html', args)
    else:
        HttpResponseRedirect('insti/login/')
