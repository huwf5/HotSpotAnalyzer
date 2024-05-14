from apps.user.serializer import RoleSerializer
from apps.system.utils.initialize import BaseInitialize


class Initialize(BaseInitialize):
    def run(self):
        self.init_base(RoleSerializer, unique_fields=["id"])
