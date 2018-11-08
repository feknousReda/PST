from django.views.generic import TemplateView
from django.shortcuts import render
from recon.forms import HomeForm,SimpleForm
from recon.back import backProcess
import string

class HomeView(TemplateView):
    template_name = 'recon/login.html'

    def get(self, request):
        form = HomeForm()
        sform = SimpleForm()
        done = False
        args  = {'form': form, 'done': done, 'sform': sform}
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)
        sform = SimpleForm(request.POST)
        selected_modules = request.POST.getlist('favorite_modules')

        if form.is_valid():
            if len(selected_modules) != 0:
                url = form.cleaned_data['Domaine']
                listurl = url.split()
                length = len(listurl)  == 1
                print(length)
                if " " in url:
                    #print(type(url))

                    lbdd = []
                    for x in listurl:
                        #print(type(lbdd))
                        bdd = backProcess.globalProcess(x, selected_modules)
                        print("global process")
                        lbdd.append(bdd)
                        form = HomeForm()
                        sform = SimpleForm()
                        print(lbdd)
                    done = True
                    length = len(listurl)  == 1
                    print(length)
                    args = {'form': form,'length': length, 'url': listurl,'raws': lbdd,'sform':sform,'done': done}

                else:
                    raws = backProcess.globalProcess(url, selected_modules)
                    form = HomeForm()
                    sform = SimpleForm()
                    done = True
                    args = {'form': form, 'length': length,'url': url,'raws': raws,'sform':sform,'done': done}
            else:
                form = HomeForm()
                sform = SimpleForm()
                msg = 'Please choose at least one module !'
                args = {'form': form, 'msg': msg, 'sform': sform}

        return render(request, self.template_name, args)
