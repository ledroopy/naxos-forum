from django.views.generic import CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from django.contrib import messages

from braces.views import LoginRequiredMixin

from .forms import RegisterForm, UpdateUserForm, CrispyPasswordForm
from .models import ForumUser


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('user:login')


class UpdateUser(LoginRequiredMixin, UpdateView):
    form_class = UpdateUserForm
    template_name = 'user/profile.html'

    def get_object(self):
        return ForumUser.objects.get(username=self.request.user)

    def get_form_kwargs(self):
        """Pass user to form."""
        kwargs = super(UpdateUser, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Paramètres sauvegardés.")
        return reverse('user:profile', kwargs=self.kwargs)


@login_required
def UpdatePassword(request):
    form = CrispyPasswordForm(user=request.user)

    if request.method == 'POST':
        form = CrispyPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Mot de passe modifié.")

    return render(request, 'user/password.html', {
        'form': form,
    })


class MemberList(LoginRequiredMixin, ListView):
    template_name = "user/members.html"
    model = ForumUser
