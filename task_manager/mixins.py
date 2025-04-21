from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View


class CustomLoginRequiredMixin(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')  # URL перенаправления когда нет auth
    redirect_field_name = ''  # Имя параметра для перенаправления обратно

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Вы должны быть авторизованы для просмотра этой страницы.')
            return self.handle_no_permission()  # метод LoginRequiredMixin
        return super().dispatch(request, *args, **kwargs)
