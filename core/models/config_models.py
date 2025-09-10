from django.db import models

class CompanyConfig(models.Model):
    company = models.OneToOneField("Company", on_delete=models.CASCADE, related_name="config")
    # Obligatorios
    name = models.CharField(max_length=255)
    primary_logo_url = models.URLField()
    favicon_url = models.URLField()
    resume_banner_url = models.URLField()
    send_email = models.BooleanField(default=False)
    # Opcionales
    secondary_logo_url = models.URLField(blank=True, null=True)
    mobile_logo_url = models.URLField(blank=True, null=True)
    primary_color = models.CharField(max_length=30, blank=True, null=True)
    secondary_color = models.CharField(max_length=30, blank=True, null=True)
    tertiary_color = models.CharField(max_length=30, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    def __str__(self): return f"Config for {self.company.name}"

class EmailConfig(models.Model):
    company = models.ForeignKey("Company", on_delete=models.CASCADE, related_name="email_configs")
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField(default=587)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    timeout = models.PositiveIntegerField(default=10)
    def __str__(self): return f"SMTP {self.host}:{self.port} ({self.company.name})"
