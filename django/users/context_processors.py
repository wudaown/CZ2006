from .models import MailBox,Message_Mailbox,User

def NumOfNotification(request):
    user = None
    if 'member_id' in request.session:
        print(request.session['member_id'])
        user = User.objects.get(username=request.session['member_id'])
    else:
        print("AHAHAHAH!")
    if user is not None:
        print(user)
        mailbox = user.mailbox
        unread_sum = Message_Mailbox.objects.filter(mailbox_id=mailbox.id, viewed=False).count()
        print(unread_sum)
        return {'unread': unread_sum}
    return {}


