from django.apps import AppConfig
import threading
import schedule
import time
class ShiftConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shift'
    def ready(self):
        import shift.signals
        scheduler_thread = threading.Thread(target=self.run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()

    def run_scheduler(self):
        from .signals import schedule_job
        from .models import Shift
        schedule.clear()
        for shift in Shift.objects.all():
            schedule_job(shift)
        
        while True:
            schedule.run_pending()
            time.sleep(1)



