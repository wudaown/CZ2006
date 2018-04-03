from .models import MailBox,Message_Mailbox,User

def NumOfNotification(request):
    user = None
    if 'member_id' in request.session:
        user = User.objects.get(username=request.session['member_id'])
        print(user)
    else:
        for item in request.session:
            print(item)
    user = User.objects.get(username=request.session['member_id'])
    if user is not None:
        print(user)
        mailbox = user.mailbox
        unread_sum = Message_Mailbox.objects.count(mailbox_id=mailbox.id, viewed=False)
        return {'unread': unread_sum}
    return {}


