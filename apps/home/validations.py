# All System Validations is Here
from django.db import models
import datetime 
from django.utils import timezone 

# now = datetime.timezone.now()
class SubscriptionManager(models.Manager):
    def Subscription_validator(self, postData):
        errors = {}
        # Check if start_date is empty
        if not postData.get('start_date'):
            errors["start_date"] = "Start date is required."
        else:
            # Convert start_date to a date object
            try:
                start_date = datetime.datetime.strptime(postData['start_date'], '%Y-%m-%d').date()
                ## Ensure start_date is at least today
                ## تم الغائه لوضع تاريخ قديم 
                # if start_date < timezone.localdate():
                #     errors["start_date"] = "Start date should be at least today."
            except ValueError:
                errors["start_date"] = "Invalid start date format."

        # Check if end_date is empty
        if not postData.get('end_date'):
            errors["end_date"] = "End date is required."
        else:
            # Convert end_date to a date object
            try:
                end_date = datetime.datetime.strptime(postData['end_date'], '%Y-%m-%d').date()
                if 'start_date' in postData and postData['start_date']:
                    start_date = datetime.datetime.strptime(postData['start_date'], '%Y-%m-%d').date()
                    # Ensure end_date is after start_date
                    if end_date <= start_date:
                        errors["end_date"] = "End date should be after start date."
                    # Ensure end_date is within one month of start_date
                    if end_date < start_date + datetime.timedelta(days=30):
                        errors["end_date"] = "End date must be within one month after the start date."
            except ValueError:
                errors["end_date"] = "Invalid end date format."

        # Ensure the user selects a valid offer
        if not postData.get('offerID') or postData['offerID'] == "Choose an Offer":
            errors["offerID"] = "Choose an Offer Please."
        
        return errors
#  Dont foget to not add an old Subscription 