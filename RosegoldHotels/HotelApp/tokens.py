from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        last_login = ""
        if user.last_login:
            last_login = user.last_login.replace(microsecond=0, tzinfo=None)
        return f"{user.pk}{user.password}{last_login}{timestamp}{user.email}{user.is_active}"


account_activation_token = AccountActivationTokenGenerator()
