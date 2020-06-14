from background_task import background
from django.contrib.auth.models import User


@background(schedule=5)
def notify_user(user_id):
    # lookup user by id and send them a message
    user = User.objects.get(pk=user_id)
    print("AAAAA")
    user.email_user('Here is a notification', 'You have been notified')
#
# @background(schedule=60)
# def start():
#     scheduler = BackgroundScheduler()
#     print("\n\n\nSCHEDULED TRAINING!!!\n\n\n")
#     scheduler.add_job(detection.run(), 'interval', minutes=15)
#     scheduler.shutdown()
#     scheduler.start()
