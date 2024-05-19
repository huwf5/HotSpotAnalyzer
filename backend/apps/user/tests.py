from django.test import TestCase
from .fixtures.initialize import Initialize
from .serializers.user import RoleSerializer

# Create your tests here.

# Test if roles are initialized
class InitializeTestCase(TestCase):
    def test_init_role(self):
        print("Testing init_role")
        Initialize(app='apps.user').run()
        # test if roles are initialized
        roles = RoleSerializer.Meta.model.objects.all()
        self.assertTrue(roles.exists(), "Roles should be initialized")