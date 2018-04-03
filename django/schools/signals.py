from django.db.models.signals import post_save
from django.dispatch import receiver
from schools.models import Kindergarten
from users.models import Message, MailBox, User
from users.views import notifyUser, getschoolfollower


@receiver(post_save, sender=Kindergarten)
def save_callback(sender, **kwargs):
    """
        Django includes a "signal dispatcher" which helps allow decoupled applications get notified when actions occur
        elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some
        action has taken place.

        This is a receiver function as a signal handler for post_save signal. Once triggered, it will notify all users
        if a new kindergarten is in the system, or notify all following users of a kindergarten if it has some updates.

        Decorator @receiver:
                signal: A signal or a list of signals to connect a function to.
                sender: A specific signal sender

                post_save signal get sent many times, but we are only interested in receiving update of
                kindergarten models.
        Args:
            sender: an HttpRequest object.
            kwargs:
                post_save signal will send following keyword arguments:

                instance: The actual instance being saved.
                created: A boolean; True if a new record was created.
                raw: A boolean; True if the model is saved exactly as presented (i.e. when loading a fixture).
                using: The database alias being used.
                update_fields: The set of fields to update as passed to Model.save(),
                                or None if update_fields wasn't passed to save().

        Returns:
            None
    """


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
        notifyUser(User(), userlist, msg)
