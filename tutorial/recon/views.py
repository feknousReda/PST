from django.views.generic import TemplateView
from django.shortcuts import render
from recon.forms import HomeForm,SimpleForm
from recon.back import backProcess

class HomeView(TemplateView):
    template_name = 'recon/login.html'

    def get(self, request):
        form = HomeForm()
        sform = SimpleForm()
        done = False
        args = args = {'form': form, 'done': done, 'sform': sform}
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)
        sform = SimpleForm(request.POST)
        selected_modules = request.POST.getlist('favorite_modules')

        if form.is_valid():
            url = form.cleaned_data['Domaine']
            raws = backProcess.globalProcess(url, selected_modules)
            form = HomeForm()
            done = True
        args = {'form': form, 'text': url,'raws': raws, 'done': done}
        return render(request, self.template_name, args)
