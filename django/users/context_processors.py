from .models import MailBox,Message_Mailbox,User

def NumOfNotification(request):
    user = User.objects.get(username=request.session['member_id'])
    if user is not None:
        mailbox = user.mailbox
        unread_sum = Message_Mailbox.objects.count(mailbox_id=mailbox.id, viewed=False)
        return {'unread': unread_sum}
    return {}


