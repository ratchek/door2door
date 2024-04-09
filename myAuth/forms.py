from allauth.account.forms import ChangePasswordForm, SignupForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


# Helper function used to switch the password help texts
# So that it appears under the second password instead of the first
def switchHelpTexts(form):
    help_text = form.fields["password1"].help_text
    form.fields["password1"].help_text = None
    form.fields["password2"].help_text = help_text


# Helper function used to delete the password help texts
# when validation errors are displayed. We don't need the same info twice
def deleteHelpTexts(form):
    form.fields["password1"].help_text = None
    form.fields["password2"].help_text = None


class MyCustomSignupForm(SignupForm):
    captcha = ReCaptchaField(
        label="",
        widget=ReCaptchaV2Checkbox(
            attrs={
                "data-theme": "dark",
            }
        ),
    )
    field_order = ["username", "email", "password1", "password2", "captcha"]

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        switchHelpTexts(self)

        # # Commented out because deleteHelpTexts doesn't work for some reason
        # if self.errors and (self.errors.keys() & {"password1", "password2"}):
        #     deleteHelpTexts(self)


class MyCustomChangePasswordForm(ChangePasswordForm):
    field_order = ["oldpassword", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(MyCustomChangePasswordForm, self).__init__(*args, **kwargs)
        switchHelpTexts(self)
