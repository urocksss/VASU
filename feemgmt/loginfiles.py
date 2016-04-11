from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


class LoginForm(forms.Form):
    username = forms.CharField(label=(u'Axis Id'))
    password = forms.CharField(label=(u'password'), widget=forms.PasswordInput(render_value=False))


def LoginRequest(request):
    if request.user.is_authenticated():
        return render_to_response('welcomPage.html', {'stud_name': request.user.user_map.stud_id.name},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render_to_response('welcomPage.html', {'stud_name': user.user_map.stud_id.name}, context_instance=RequestContext(request))
                # return HttpResponse(
                #     '<script type="text/javascript">window.close();window.opener.location.reload(false);</script>')
            else:
                errors = form._errors.setdefault("no_field", form.error_class())
                errors.append("validation Error")
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
    else:
        '''user is not submitting the form, show the login form'''
        form = LoginForm()
        context = {'form': form}
        return render_to_response('login.html', context, context_instance=RequestContext(request))


def LogoutRequest(request):
    if request.user.is_authenticated():
        logout(request)
        # return HttpResponseRedirect('/registration/eventreg/')
        return HttpResponse(
            '<script type="text/javascript">window.close();window.opener.location.reload(false);</script>')
    else:
        return HttpResponse(
            '<script type="text/javascript">window.close();window.opener.location.reload(false);</script>')
