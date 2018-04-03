# _*_ encoding:utf-8 _*_

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from .models import *
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import make_password
from djangoTut.utils import send_verify_mail
from django.http import HttpResponse, HttpResponseRedirect


class ActiveView(View):
    def get(self, request, active_code):
        record = EmailVerifyRecord.objects.filter(code=active_code)[0]
        user = User.objects.filter(email=record.email)[0]
        user.is_active = True
        user.save()
        # TODO
        # Invalid active code
        record.delete()
        return render(request, 'index.html')

class ResetView(View):
    # TODO
    # some more logic
    # felt something wrong
    # form validation
    def get(self, request, reset_code):
        record = EmailVerifyRecord.objects.filter(code=reset_code)
        if record:
            return render(request, 'reset.html')
        else:
            return HttpResponse('Invalid link')

    def post(self, request, reset_code):
        record = EmailVerifyRecord.objects.filter(code=reset_code)[0]
        user = User.objects.filter(email=record.email)[0]
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            user.password = make_password(password)
            user.save()
            record.delete()
            # return render(request, 'index.html')
            return redirect('/')
        else:
            return render(request, 'reset.html', {'msg': 'Password does not match'})


class LoginView(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['uname']
            passwd = request.POST['passwd']
            # username and password need to be specify
            user = authenticate(username=username, password=passwd)
            if user is not None:
                login(request, user)
                # request.session['member_id'] = username
                # u = request.user.username
                # return HttpResponseRedirect('login.html')
                # return render(request, 'index.html')
                #  a = checkMailbox(user)
                # return render(request, 'user_page.html')
                # a = checkMailbox(user)

                # return redirect('/users/' + username)
                # if not user.is_superuser:
                # 	a = checkMailbox(user, isviewed=False)
                return HttpResponseRedirect(reverse('index'))
            else:
                msg = {'msg': 'Username or Password Wrong'}
                return render(request, 'index.html', msg)
        else:
            error = login_form.errors
            errors = {'name_of_error': error}
            # To pass the parameter into html
            # the key inside the dict is use
            return render(request, 'index.html', errors)


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.data['username']
            password = register_form.data['password']
            email = register_form.data['email']
            if User.objects.filter(username=username):
                return HttpResponseRedirect(reverse('register'))
            # return render(request, 'register.html', {'msg': 'Username already exists'})
            user = User()
            # Only if email activation is needed then set is_active false
            user.is_active = False
            user.username = username
            user.email = email
            user.password = make_password(password)
            mailbox = MailBox()
            mailbox.save()
            user.mailbox = mailbox
            user.save()
            send_verify_mail(email)
            return render(request, 'index.html')
        else:
            # Actual not need
            # by using the django form in html
            # all validation is done hence
            # should not end up here
            error = register_form.errors
            errors = {'name_of_error': error}
            return render(request, 'register.html', errors)


class LogoutView(View):
    def get(self, request):
        logout(request)
        try:
            del request.session['member_id']
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('index'))
        # return render(request, 'index.html')



# class NotificationCenterView(View):
# 	# todo 这个和userpageview重合了
# 	def get(self, request):
# 		user = request.user
# 		output = set()
# 		messages = Message_Mailbox.objects.filter(mailbox_id=user.mailbox_id)
# 		for qs in messages:
# 			output.add(qs.message.content)
# 		return output


class ForgetPasswordView(View):
    # TODO
    # form validation
    def get(self, request):
        return render(request, 'forget.html')

    def post(self, request):
        email = request.POST['email']
        send_verify_mail(email, 1)
        return render(request, 'forget.html', {'msg': 'Submission done. Please your email'})


class UserPageView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        read = checkMailbox(user, isviewed=True)
        unread = checkMailbox(user, isviewed=False)
        flist = user.following.all()
        if user is not None:
            return render(request, 'user_page.html',
                          {'username': username, 'read_message_list': read,
                           'followingList': flist, 'unread_message_list':unread})
        else:
            return HttpResponse("Wrong username")


def checkMailbox(user, isviewed):
    mailbox = user.mailbox
    output = set()
    unread_messages = Message_Mailbox.objects.filter(mailbox_id=mailbox.id, viewed=isviewed)
    for qs in unread_messages:
        output.add(qs.message.content)
        qs.viewed = True
        qs.save()
    return output


def notifyUser(userlist, msg):
    #msg = Message.objects.create(content=message)
    for user in userlist:
        Message_Mailbox.objects.create(mailbox = user.mailbox, message = msg)
    return


def getschoolfollower(school):
    userlist = school.following_kd.all()
    return userlist


'''def user_page(request):
    try:
        user = User.objects.get(username=request.session['member_id'])
    except:
        raise Http404('Requested user not found.')
    bookmarks = user.bookmark_set.all()
    template = get_template('user_page.html')
    variables = Context({
            'username': username,
            'bookmarks': bookmarks
    })
    output = template.render(variables)
    return HttpResponse(output)'''


def saveToList(request, id):
    user = User.objects.get(username=request.session['member_id'])
    if user is not None:
        school = Kindergarten.objects.get(id=id)
        user.following.add(school)
        user.save()
        return HttpResponse("<script>Save.Response_OK();</script>")
    else:
        return render(request, 'login.html')


'''
class WatchListView(ListView):
    model = Kindergarten


    def get_queryset(self):
        return User.following.all()



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
'''
