from registration.forms import RegistrationForm
from registration.users import UsernameField
from registration.users import UserModel

USER = UserModel()


def first_name_field():
    return getattr(USER, 'FIRST_NAME_FIELD', 'first_name')
def last_name_field():
    return getattr(USER, 'LAST_NAME_FIELD', 'last_name')
class PVRegistrationForm(RegistrationForm):
    class Meta:
        model = USER
        fields = (UsernameField(), "email", first_name_field(), last_name_field())
