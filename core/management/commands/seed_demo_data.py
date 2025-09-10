from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from core.models import UserProfile, Company, CompanyConfig, Category, Campaign, Content

class Command(BaseCommand):
    help = "Crea datos de prueba (sitios, usuarios, compañías, campañas, contenido)."

    def handle(self, *args, **options):
        localhost, _ = Site.objects.get_or_create(domain="localhost", defaults={"name": "Localhost"})
        example, _   = Site.objects.get_or_create(domain="example.com", defaults={"name": "Example"})

        admin_user,_ = User.objects.get_or_create(username="admin@test.com", defaults={"email":"admin@test.com"})
        admin_user.set_password("password123"); admin_user.save()
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        brand_user,_ = User.objects.get_or_create(username="brand@test.com", defaults={"email":"brand@test.com"})
        brand_user.set_password("password123"); brand_user.save()
        creator_user,_ = User.objects.get_or_create(username="creator@test.com", defaults={"email":"creator@test.com"})
        creator_user.set_password("password123"); creator_user.save()

        admin_profile,_ = UserProfile.objects.get_or_create(user=admin_user, defaults={"role":"ADMIN"})
        brand_profile,_ = UserProfile.objects.get_or_create(user=brand_user, defaults={"role":"BRAND"})
        creator_profile,_ = UserProfile.objects.get_or_create(user=creator_user, defaults={"role":"CREATOR"})

        techcorp,_ = Company.objects.get_or_create(name="TechCorp", site=localhost, defaults={"email":"info@techcorp.local"})
        fashion,_ = Company.objects.get_or_create(name="FashionBrand", site=localhost, defaults={"email":"hello@fashion.local"})
        food,_ = Company.objects.get_or_create(name="FoodChain", site=localhost, defaults={"email":"contact@food.local"})

        brand_profile.companies.add(techcorp, fashion, food)
        creator_profile.companies.add(techcorp, fashion)
        admin_profile.companies.add(techcorp, fashion, food)

        for c in (techcorp, fashion, food):
            CompanyConfig.objects.get_or_create(company=c, defaults=dict(
                name=f"{c.name} Site",
                primary_logo_url="https://placehold.co/600x200?text=Logo",
                favicon_url="https://placehold.co/32x32",
                resume_banner_url="https://placehold.co/1200x300?text=Banner",
                send_email=False,
            ))

        cat_tech,_ = Category.objects.get_or_create(name="Tecnología")
        cat_fashion,_ = Category.objects.get_or_create(name="Moda")
        cat_food,_ = Category.objects.get_or_create(name="Comida")

        camp_app,_ = Campaign.objects.get_or_create(company=techcorp, name="Lanzamiento App", defaults={"state":1})
        camp_summer,_ = Campaign.objects.get_or_create(company=fashion, name="Colección Verano", defaults={"state":2})
        camp_delivery,_ = Campaign.objects.get_or_create(company=food, name="Delivery", defaults={"state":3})

        camp_summer.creators.add(creator_profile)
        camp_summer.categories.add(cat_fashion)

        Content.objects.get_or_create(
            campaign=camp_summer, creator=creator_profile,
            title="Video campaña verano", url="https://example.com/content/1", type="video", is_approved=True
        )

        self.stdout.write(self.style.SUCCESS("Datos de prueba creados correctamente."))
