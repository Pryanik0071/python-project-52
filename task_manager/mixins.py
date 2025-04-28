from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View


class CustomLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')  # URL перенаправления когда нет auth
    redirect_field_name = ''  # Имя параметра для перенаправления обратно

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                                 _("You are not logged in! Please sign in."))
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class CustomCheckUserMixin(UserPassesTestMixin, View):
    def test_func(self):
        return self.get_user() == self.request.user

    def handle_no_permission(self):
        messages.add_message(self.request,
                             messages.ERROR,
                             _("You do not have permission to modify this user."))
        return redirect('/users/')
