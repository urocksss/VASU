from django.shortcuts import render
import datetime
import random
#from tnp.forms import RegistrationForm
from bis_project_app.models import *
from django.contrib.auth.decorators import login_required
#from django.contrib.auth import login,logout 
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.context_processors import csrf 
import urllib
import urllib2

# Create your views here.
def randomword():
	choose="qwertyuiopasdfghjklzxcvbnm1234567890AQWSEDRFTGYHUJIKOLPZXCVBNM"
   	return ''.join(random.choice(choose) for i in range(25))

def diff_month(d1, d2):
    return (d1.year - d2.year)*12 + d1.month - d2.month


def make_payment(request):
	if request.method == 'POST':
		print "in post"
		stud_id=request.POST.get('id' ,'')
		student = StudentInfo.objects.filter(stud_id=stud_id).first() #can be taken from session
		if student is not None:
			#save in temp trans
			sem=(diff_month(datetime.datetime.today(),student.date_of_joining)/6)+1;
			print "sem:"
                        print sem
			print "year:"
			print datetime.datetime.today().year
			fee_id=FeeStruct.objects.filter(course_type=student.course_type,branch=student.branch,sem=sem,
				is_handi=student.is_handi,category=student.category,year=datetime.datetime.today().year).first()
			pay_time=datetime.datetime.now();
			unique_id=randomword();
			if fee_id is not None:
				interface_object=TempTrans(stud_id=student,fee_id=fee_id,pay_time=pay_time,unique_id=unique_id);
				interface_object.save();
				#data = urllib.urlencode({"uid":unique_id,"fees":fee_id.fees,"acct_num":"123456789"})
                                #u = urllib.urlopen("http://google.com/", data)
				context={"uid":unique_id,"fees":fee_id.fees,"acct_num":"123456789"}
                                return render_to_response('redirect.html',context,context_instance=RequestContext(request))
				print "proceeding for transaction"
			else:
				print "some problem in transaction"
		else:
			print "error:no such clg id";		
	
        print "in get"
	args = {}
        args.update(csrf(request))
        return render_to_response(
        'make_payment.html',args
        )
