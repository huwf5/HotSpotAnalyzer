from apps.user.serializers.user import RoleSerializer
from apps.user.serializers.email import EmailSuffixFormatSerializer
from apps.system.utils.initialize import BaseInitialize

from config.conf import EMAIL_WHITELIST


class Initialize(BaseInitialize):
    def init_email_suffix_format(self):
        if len(EMAIL_WHITELIST) == 0:
            # if not specified, all emails are allowed
            EMAIL_WHITELIST.append("@*")
        self.init_from_list(
            EmailSuffixFormatSerializer,
            [{"format": email_suffix} for email_suffix in EMAIL_WHITELIST],
        )

    def init_super_admin(self):
        pass

    def run(self):
        self.init_from_json(RoleSerializer, unique_fields=["id"])
        self.init_email_suffix_format()
        self.init_super_admin()
