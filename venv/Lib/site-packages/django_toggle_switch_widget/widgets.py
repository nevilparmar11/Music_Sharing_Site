from django.forms.widgets import Widget
from django.forms.widgets import CheckboxInput


class DjangoToggleSwitchWidget(CheckboxInput):
    template_name = 'django-toggle-switch-widget/django-toggle-switch-widget.html'

    def __init__(self, attrs=None, check_test=None, round=False, klass=""):
        self.round = round
        self.klass = klass
        super().__init__(attrs, check_test)

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        context.update({
            "round": self.round,
            "klass": self.klass,
        })
        return context

    class Media:
        css = {
            "all": [
                "django-toggle-switch-widget/css/django-toggle-switch-widget.css",
            ]
        }
