from django.db import models
from django.contrib.auth.models import User, Group
from leaves_types.models import LeavesTypes


class Leaves(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    leave_type = models.ForeignKey(LeavesTypes,on_delete=models.DO_NOTHING)
    from_date = models.DateField()
    to_date = models.DateField()
    leave_days = models.IntegerField(default=0, editable=False)
    reason = models.TextField()
    LEAVES_STATUS = [
        ("PENDING_SUPERVISOR","pending_supervisor"),
        ("APPROVED_BY_SUPERVISOR","approved_by_supervisor"),
        ("REJECTED_BY_SUPERVISOR","rejected_by_supervisor"),
        ("PENDING_ADMIN","pending_admin"),
        ("APPROVED","approved"),
        ("REJECTED","rejected"),
        ("CANCELLED","cancelled"),
    ]
    status = models.CharField(choices=LEAVES_STATUS, default="PENDING_SUPERVISOR", max_length=50)
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_leaves')
    supervisor_comment = models.TextField(blank=True, null=True)
    admin_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_user_supervisor(self):
        """Get the supervisor for this user"""
        try:
            supervisor_group = Group.objects.get(name='supervisor')
            # You might want to implement a more sophisticated way to assign supervisors
            # For now, this returns the first supervisor found
            return User.objects.filter(groups=supervisor_group).first()
        except Group.DoesNotExist:
            return None
    
    def can_be_approved_by_supervisor(self):
        return self.status == "PENDING_SUPERVISOR"
    
    def can_be_handled_by_admin(self):
        return self.status in ["REJECTED_BY_SUPERVISOR", "PENDING_ADMIN"]
    
    def save(self, *args, **kwargs):
        print(f"DEBUG: Saving leave - pk={self.pk}")
        print(f"DEBUG: from_date={self.from_date}, to_date={self.to_date}")
        
        if self.from_date and self.to_date:
            self.leave_days = (self.to_date - self.from_date).days + 1
            print(f"DEBUG: Calculated leave_days={self.leave_days}")

            if not self.pk:  # pk is None if object is not saved yet
                if self.leave_days > 2:
                    self.status = "PENDING_ADMIN"
                    print(f"DEBUG: Status set to PENDING_ADMIN (days > 2)")
                else:
                    self.status = "PENDING_SUPERVISOR"
                    print(f"DEBUG: Status set to PENDING_SUPERVISOR (days <= 2)")
            else:
                print(f"DEBUG: Not setting status - object already exists (pk={self.pk})")
        else:
            print(f"DEBUG: Missing dates - from_date={self.from_date}, to_date={self.to_date}")
            
        super().save(*args, **kwargs)