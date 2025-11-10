from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView , DetailView , CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Submission
# Create your views here.


def list_conferences(request):
    conferences_list=Conference.objects.all()
    """retour : liste + page """
    return render(request,"conferences/liste.html", {"liste":conferences_list})

class ConferenceList(ListView):
    model=Conference
    context_object_name="liste"
    template_name="conferences/liste.html"

class ConferenceDetails(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="conferences/details.html"

class ConferenceCreate(LoginRequiredMixin,CreateView):
    model= Conference
    template_name ="conferences/form.html"
    #fields = "__all__"
    form_class =ConferenceForm
    success_url = reverse_lazy("liste_conferences")

class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model =Conference
    template_name="conferences/form.html"
    #fields="__all__"
    form_class =ConferenceForm
    success_url=reverse_lazy("liste_conferences")

class ConferenceDelete(LoginRequiredMixin,DeleteView):
    model=Conference
    template_name ="conferences/conference_confirm_delete.html"
    success_url =reverse_lazy("liste_conferences")


class SubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = 'conferences/submissions/list.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).select_related('conference')

class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = 'conferences/submissions/detail.html'
    context_object_name = 'submission'
    pk_url_kwarg = 'submission_id'

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)
    


class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    template_name = 'conferences/submissions/form.html'
    fields = ['title', 'abstract', 'keywords', 'paper', 'conference']
    success_url = reverse_lazy('submission_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class SubmissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Submission
    template_name = 'conferences/submissions/form.html'
    fields = ['title', 'abstract', 'keywords', 'paper']
    success_url = reverse_lazy('submission_list')
    pk_url_kwarg = 'submission_id'

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.status not in ['Submitted']:
            messages.error(request, "Cette soumission ne peut plus être modifiée.")
            return redirect('submission_list')
        return super().dispatch(request, *args, **kwargs)    