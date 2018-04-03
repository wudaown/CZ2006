from .models import Message_Mailbox,User

def NumOfNotification(request):
    """
        A context processor --
        take a request object as their argument and return a dictionary
        of items to be merged into the context.

        Context processors are applied on top of context data.

        Args:
            request: an HttpRequest object.

        Returns:
            A dictionary that gets added to the template context,
            namely add the number of unread message, if the user is login.

            If the user is not login, an empty dictionary is returned.
    """
    user = None
    if 'member_id' in request.session:
    #   print(request.session['member_id'])
        user = User.objects.get(username=request.session['member_id'])
    if user is not None:
        mailbox = user.mailbox
        unread_sum = Message_Mailbox.objects.filter(mailbox_id=mailbox.id, viewed=False).count()
        #print(mailbox.id, unread_sum)
        return {'unread': unread_sum}
    return {}


