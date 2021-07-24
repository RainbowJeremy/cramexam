"""from django.db.models.signals import post_save, pre_save
from django.core.signals import request_finished
from django.dispatch import receiver
from .models import Lecture
from amplitude import Amplitude



def lecture_saved_event(sender, instance, **kwargs):
    #### signal when saved, not necessarily when a new one is uploaded
    amplitude = Amplitude()
    event_data = amplitude.build_event_data(
        event_type='Signal Please',
        request=request,
        app_version='1.0.0',
    )
    amplitude.send_events([event_data])
request_finished.connect(lecture_saved_event, sender=Lecture)"""


#Estimate.objects.filter(author=predictor)