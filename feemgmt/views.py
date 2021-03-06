import hashlib
import random

# Create your views here.
import datetime

from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.context_processors import csrf
from math import ceil

from django.views.decorators.csrf import csrf_exempt

from feemgmt.models import *
from django.shortcuts import render_to_response
from Crypto.Hash import SHA512
from . import bank_public_key,key

# Create your views here.
def clg_key():
    return 'VNIT'

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


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def make_payment(request):
    if request.method == 'POST':
        print("in post")
        if request.user.is_authenticated():
            stud_id = request.user.user_map.stud_id.stud_id
            student = StudentInfo.objects.filter(stud_id=stud_id).first()  # can be taken from session
            if student is not None:
                # save in temp trans
                sem = ceil((diff_month(datetime.datetime.today(), student.date_of_joining) / 6) + 1)
                print("sem:")
                print(sem)
                print("year:")
                print(datetime.datetime.today().year)
                fee_id = FeeStruct.objects.filter(course_type=student.course_type, sem=sem,
                                                  is_handi=student.is_handi,
                                                  year=datetime.datetime.today().year).first()
                pay_time = datetime.datetime.now()
                unique_id = randomword()
                if fee_id is not None:
                    if int(fee_id.fees) != 0:
                        interface_object = TempTrans(stud_id=student, fee_id=fee_id, pay_time=pay_time,
                                                     unique_id=unique_id)
                        interface_object.save()
                        print(unique_id)
                        uuid=bank_public_key.encrypt(str(unique_id),32)
                        fee=bank_public_key.encrypt(str(fee_id.fees),32)
                        c_key=bank_public_key.encrypt(str(clg_key()),32)
                        m = SHA512.new()
                        m.update(uuid.encode('utf-8'))
                        m.update(fee.encode('utf-8'))
                        m.update(c_key.encode('utf-8'))
                        # context = {"uid": unique_id, "fees": fee_id.fees, "college_id": clg_key, }
                        # data = urllib.urlencode({"uid":unique_id,"fees":fee_id.fees,"acct_num":"123456789"})
                        # u = urllib.urlopen("http://google.com/", data)
                        hash=m.hexdigest()
                        signature=key.sign(hash,'')
                        context = {"uid": unique_id, "fees": fee_id.fees, "college_id":clg_key,"hash": signature}
                        print("proceeding for transaction")
                        return render_to_response('redirect.html', context, context_instance=RequestContext(request))
                    else:
                        Transactions(stud_id=student, fee_id=fee_id, pay_time=pay_time,
                                     trans_id='Automatically Paid').save()
                else:
                    print("some problem in transaction")
            else:
                print("error:no such clg id")
        args = {}
        # args.update(csrf(request))
        return render_to_response('login.html', args)
    else:
        print("in get178")
        if request.user.is_authenticated():
            print("in get100")

            # args.update(csrf(request))
            stud_id = request.user.user_map.stud_id.stud_id
            student = StudentInfo.objects.filter(stud_id=stud_id).first()  # can be taken from session
            if student is not None:
                # save in temp trans
                sem = ceil((diff_month(datetime.datetime.today(), student.date_of_joining) / 6) + 1)
                print("sem:")
                print(sem)
                print("year:")
                print(datetime.datetime.today().year)
                fee_id = FeeStruct.objects.filter(course_type=student.course_type, sem=sem,
                                                  is_handi=student.is_handi,
                                                  year=datetime.datetime.today().year).first()
                args = {'student': student, 'fee_id': fee_id, 'sem': sem}
                trans=Transactions.objects.filter(stud_id=student,fee_id=fee_id)
                if trans.exists():
                    args={'trans':trans,'message':'You have already Paid your fees. Here are transaction details'}
                    return render_to_response('print_history.html', args)
                else:
                    args.update(csrf(request))
                    return render_to_response('make_payment.html', args)
            else:
                return render_to_response('error.html', {'reason': 'student does not exist'})
        else:
            print("in get566")
            args = {}
            args.update(csrf(request))
            return render_to_response('login.html', args)


@csrf_exempt
def TransactionComplete(request):
    # if request.user.is_authenticated():
    id = request.POST.get('uid')
    status = request.POST.get('status')
    t_id = request.POST.get('t_id')
    signature = request.POST.get('hash')
    m = SHA512.new()
    m.update(status.encode('utf-8'))
    m.update(id.encode('utf-8'))
    m.update(t_id.encode('utf-8'))
    m.update(clg_key().encode('utf-8'))
    hash=m.hexdigest()
    if bank_public_key.verify(hash,signature):
        id=key.decrypt(id)
        status=key.decrypt(status)
        t_id=key.decrypt(t_id)
        temp_trans_obj = TempTrans.objects.filter(unique_id=id)[0]
        # login(request, temp_trans_obj.stud_id.stud_map.user)
        if int(status) == 2:
            Transactions(stud_id=temp_trans_obj.stud_id,
                         fee_id=temp_trans_obj.fee_id,
                         pay_time=temp_trans_obj.pay_time,
                         trans_id=t_id).save()
        student = temp_trans_obj.stud_id
        sem = ceil((diff_month(datetime.datetime.today(), student.date_of_joining) / 6) + 1)
        print("sem:")
        print(sem)
        print("year:")
        print(datetime.datetime.today().year)
        fee_id = FeeStruct.objects.filter(course_type=student.course_type, sem=sem,
                                          is_handi=student.is_handi,
                                          year=datetime.datetime.today().year)[0]
        args = {"status": int(status), "t_id": t_id, 'student': student, 'fee_id': fee_id, 'sem': sem}
        temp_trans_obj.delete()
        return render_to_response('payment_complete.html', args, context_instance=RequestContext(request))
    else :
        return render_to_response('confirm_payment_with_bank.html')
