from django.db   import models

from core.models import TimeStampModel


class RaidHistory(TimeStampModel):
    
    STATUS_TYPES = [
        ('in_progress', 'raid in progress'),
        ('success', 'raid success'),
        ('fail', 'raid fail'),
    ]
    
    users      = models.ForeignKey('users.User', related_name='raid_histories', on_delete=models.CASCADE)
    score      = models.PositiveIntegerField(default=0)
    level      = models.PositiveIntegerField()
    status     = models.CharField(max_length=200, choices=STATUS_TYPES, default='in_progress')
    enter_time = models.DateTimeField(auto_now_add=True)
    end_time   = models.DateTimeField(null=True)
    time_limit = models.PositiveIntegerField(default=180)
    
    def __str__(self):
        return self.users.nickname
    
    class Meta:
        db_table = 'raid_histories'