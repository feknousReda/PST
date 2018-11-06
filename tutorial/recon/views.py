from django.views.generic import TemplateView
from django.shortcuts import render
from recon.forms import HomeForm
from recon.back import backProcess

class HomeView(TemplateView):
    template_name = 'recon/login.html'

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['Domaine']
            backProcess.globalProcess(text)
            form = HomeForm()
        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)
