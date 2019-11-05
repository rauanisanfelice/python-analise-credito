from django.shortcuts import render

# Create your views here.
class index(View):
    retorno = 'index.html'
    def get(self, request):
        return render(request, self.retorno)