from django.db import models
class Content(models.Model):
    TYPE_CHOICES = (("video","Video"),("image","Image"),("post","Post"),("other","Other"))
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE, related_name="contents")
    creator = models.ForeignKey("UserProfile", on_delete=models.CASCADE, related_name="contents")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="other")
    is_approved = models.BooleanField(default=False)
    categories = models.ManyToManyField("Category", related_name="contents", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.title
