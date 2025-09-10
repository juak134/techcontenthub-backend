from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from unittest.mock import patch

from core.models import UserProfile, Company, CompanyConfig, Category, Campaign, Content
from core.tests.utils import auth_client

class BusinessRulesTests(TestCase):
    def setUp(self):
        self.site, _ = Site.objects.get_or_create(id=1, defaults={"domain": "testserver", "name": "Test"})
        # Users
        self.admin_u = User.objects.create_user("admin@test.com", password="pw")
        self.brand_u = User.objects.create_user("brand@test.com", password="pw")
        self.creator_u = User.objects.create_user("creator@test.com", password="pw")
        self.admin_p = UserProfile.objects.create(user=self.admin_u, role="ADMIN")
        self.brand_p = UserProfile.objects.create(user=self.brand_u, role="BRAND")
        self.creator_p = UserProfile.objects.create(user=self.creator_u, role="CREATOR")

        # Company/Config
        self.company = Company.objects.create(name="Acme", site=self.site)
        CompanyConfig.objects.create(
            company=self.company, name="Acme Site",
            primary_logo_url="https://x/logo.png", favicon_url="https://x/fav.png",
            resume_banner_url="https://x/banner.png", send_email=False
        )

        # Category
        self.cat = Category.objects.create(name="Moda")

        # Campaigns
        self.camp_draft = Campaign.objects.create(company=self.company, name="Draft", state=1)
        self.camp_active = Campaign.objects.create(company=self.company, name="Active", state=2)
        self.camp_active.categories.add(self.cat)
        self.camp_active.creators.add(self.creator_p)

    def test_brand_only_creates_draft(self):
        client = auth_client(self.brand_u)
        payload = {
            "company": self.company.id,
            "name": "Brand Campaign",
            "state": 2  # ACTIVE (should be rejected)
        }
        resp = client.post("/api/campaigns/", payload, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("borrador", str(resp.data))

    def test_admin_can_change_state_brand_cannot(self):
        # brand tries to patch -> should fail
        client_brand = auth_client(self.brand_u)
        resp_brand = client_brand.patch(f"/api/campaigns/{self.camp_draft.id}/", {"state": 2}, format="json")
        self.assertEqual(resp_brand.status_code, 400)

        # admin can patch -> ok
        client_admin = auth_client(self.admin_u)
        resp_admin = client_admin.patch(f"/api/campaigns/{self.camp_draft.id}/", {"state": 2}, format="json")
        self.assertIn(resp_admin.status_code, (200, 202))

    def test_creator_uploads_only_own_content_and_active_campaign(self):
        client_creator = auth_client(self.creator_u)

        # Not active campaign -> 400
        resp1 = client_creator.post("/api/content/", {
            "campaign": self.camp_draft.id,
            "creator": self.creator_p.id,
            "title": "X", "url": "https://x", "type": "video"
        }, format="json")
        self.assertEqual(resp1.status_code, 400)

        # Active but wrong creator id (impersonation) -> 400
        other_creator_u = User.objects.create_user("other@test.com", password="pw")
        other_creator_p = UserProfile.objects.create(user=other_creator_u, role="CREATOR")
        resp2 = client_creator.post("/api/content/", {
            "campaign": self.camp_active.id,
            "creator": other_creator_p.id,
            "title": "X", "url": "https://x", "type": "video"
        }, format="json")
        self.assertEqual(resp2.status_code, 400)

        # Active and correct creator who is part of campaign -> 201
        resp3 = client_creator.post("/api/content/", {
            "campaign": self.camp_active.id,
            "creator": self.creator_p.id,
            "title": "OK", "url": "https://ok", "type": "video"
        }, format="json")
        self.assertEqual(resp3.status_code, 201)

    def test_admin_uploads_content_for_added_creator_only(self):
        client_admin = auth_client(self.admin_u)

        # Creator added -> should work
        resp_ok = client_admin.post("/api/content/", {
            "campaign": self.camp_active.id,
            "creator": self.creator_p.id,
            "title": "Admin OK", "url": "https://ok", "type": "video"
        }, format="json")
        self.assertEqual(resp_ok.status_code, 201)

        # Creator not added -> 400
        new_u = User.objects.create_user("newc@test.com", password="pw")
        new_p = UserProfile.objects.create(user=new_u, role="CREATOR")
        resp_bad = client_admin.post("/api/content/", {
            "campaign": self.camp_active.id,
            "creator": new_p.id,
            "title": "Admin BAD", "url": "https://bad", "type": "video"
        }, format="json")
        self.assertEqual(resp_bad.status_code, 400)

    def test_metrics_post_and_put_with_mocked_es(self):
        # Create content first
        from core.models import Content
        content = Content.objects.create(
            campaign=self.camp_active, creator=self.creator_p,
            title="Vid", url="https://v", type="video", is_approved=True
        )
        client_creator = auth_client(self.creator_u)

        class FakeES:
            def __init__(self):
                self.store = {}
            def index(self, index, id, body, refresh=True):
                self.store[id] = body
                return {"result": "created"}
            def get(self, index, id):
                if id not in self.store:
                    raise Exception("not found")
                return {"_source": self.store[id]}
            def search(self, index, body):
                # return the doc if exists
                term = body.get("query", {}).get("term", {}).get("content_id.keyword")
                hits = []
                for k,v in self.store.items():
                    if v.get("content_id") == str(term):
                        hits.append({"_source": v})
                return {"hits": {"hits": hits}}

        with patch("integrations.elasticsearch.client.get_es", return_value=FakeES()):
            # POST metrics
            resp_post = client_creator.post(f"/api/metrics/content/{content.id}/", {
                "metrics": {"views": 10, "likes": 2, "shares": 1, "comments": 0}
            }, format="json")
            self.assertEqual(resp_post.status_code, 201)
            # PUT update metrics
            resp_put = client_creator.put(f"/api/metrics/content/{content.id}/", {
                "metrics": {"views": 20}
            }, format="json")
            self.assertEqual(resp_put.status_code, 200)
