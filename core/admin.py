from django.contrib import admin
from .models import (
    UserProfile, Company, CompanyConfig, EmailConfig, Category,
    Campaign, Content, Currency, Language, Country
)
for m in (UserProfile, Company, CompanyConfig, EmailConfig, Category, Campaign, Content, Currency, Language, Country):
    admin.site.register(m)
