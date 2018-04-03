from django.db.models.signals import post_save
from django.dispatch import receiver
from schools.models import Kindergarten
from users.models import Message, MailBox, User
from users.views import notifyUser, getschoolfollower


@receiver(post_save, sender=Kindergarten)
def save_callback(sender, **kwargs):
    print(kwargs)
    kindergarten = kwargs['instance']
    if kwargs['created'] == True:
        msg = Message()
        msg.content = "A new kindergarten, " + kindergarten.name + ", is available now!"
        #msg.from_id = 1
        msg.save()
        userlist = User.objects.all()
        print(userlist)
        notifyUser(userlist, msg)
    else:
        msg = Message()
        msg.content = "There is an update in the " + kindergarten.name + "!"
        #msg.from_id= 1
        msg.save()
        userlist = getschoolfollower(kindergarten)
<<<<<<< HEAD
        notifyUser(userlist,msg)




=======
        notifyUser(User(), userlist, msg)
>>>>>>> 317af31165fae2597b1744c6025a3b82a9e89d2d
