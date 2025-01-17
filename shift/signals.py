from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Shift
import schedule
import time
import telepot
import threading
from datetime import datetime
import os
from django.utils import timezone
from skpy import Skype


# Replace with your group chat ID
chat_id = os.environ.get('SKYPE_CHATID') #"19:your_group_id@thread.skype"

using_telegram = os.environ.get('USE_TELEGRAM','false') =='true'
sk = Skype(os.environ.get("SKYPE_USERNAME"), os.environ.get('SKYPE_PASSWORD'))

def send_telegram_message(message):
    if using_telegram:
        bot = telepot.Bot(os.environ.get('TELEGRAM_BOT_API_KEY'))
        bot.sendMessage(os.environ.get('GROUP_CHAT_ID'), message)
    else:
        sk.chats[chat_id].sendMsg(message)
    
def job(shift):
    if shift.date == timezone.localdate():
        message = f"شیف ساعت {shift.start_time} تا {shift.end_time} شیف کاری آقای {shift.name} هست"
        send_telegram_message(message)

def schedule_job(shift):
    start_time = datetime.combine(shift.date, shift.start_time)
    schedule.every().day.at(start_time.strftime('%H:%M')).do(job, shift=shift).tag(shift.pk)
    print(f'shift {shift.pk} scheduled to {start_time.strftime("%H:%M")}')

def remove_jobs(shift_id):
    schedule.clear(shift_id)
    print(f'shift {shift_id} removed')

@receiver(post_save, sender=Shift)
def create_or_update_shift(sender, instance, **kwargs):
    remove_jobs(instance.pk)
    schedule_job(instance)

@receiver(post_delete, sender=Shift)
def delete_shift(sender, instance, **kwargs):
    remove_jobs(instance.pk)
