from django.db import models
class Campaign(models.Model):
    STATE_CHOICES = ((1,"DRAFT"),(2,"ACTIVE"),(3,"PAUSED"),(4,"FINISHED"))
    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="campaigns")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, default=1)
    creators = models.ManyToManyField("UserProfile", related_name="campaigns", blank=True)
    categories = models.ManyToManyField("Category", related_name="campaigns", blank=True)
    def __str__(self): return f"{self.name} ({self.get_state_display()})"
