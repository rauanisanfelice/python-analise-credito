from django.shortcuts import render, redirect
from django.views.generic import View
from machine.forms import *
from machine.models import *

import numpy as np
from django_pandas.io import read_frame

# Create your views here.
class index(View):
    retorno = 'index.html'
    def get(self, request):
        form = AnaliseForm()
        return render(request, self.retorno, {
            'AnaliseForm' : form
        })

def validacao(request):
    retorno = 'validacao.html'
    if request.method == "POST":
        form = AnaliseForm(request.POST)
        if form.is_valid():
            renda = form.cleaned_data['renda']
            idade = form.cleaned_data['idade']
            emprestimo = form.cleaned_data['emprestimo']
            
            # Salva no banco de dados
            #analise = ANALISE(RENDA=renda, IDADE=idade, EMPRESTIMO=emprestimo, RESULTADO=False)
            #analise.save()

            # CRIANDO COLUNAS NO DATA FRAME
            analises = ANALISE.objects.all()
            pdAnalise = read_frame(analises)

            pdAnalise["FaixaRenda"] = 0
            pdAnalise["FaixaEtaria"] = 0
            pdAnalise["FaixaEmprestimo"] = 0
            
            # CRIANDO FAIXAS ETÁRIAS
            pdAnalise.loc[(pdAnalise["FaixaRenda"] < 18), 'FaixaEtaria'] = "CRIANCA"
            pdAnalise.loc[(pdAnalise["FaixaRenda"] >= 18) & (pdAnalise["FaixaRenda"] < 25), 'FaixaEtaria'] = "JOVEM"
            pdAnalise.loc[(pdAnalise["FaixaRenda"] >= 25) & (pdAnalise["FaixaRenda"] < 60), 'FaixaEtaria'] = "ADULTO"
            pdAnalise.loc[(pdAnalise["FaixaRenda"] >= 60), 'FaixaEtaria'] = "IDOSO"

            print(pdAnalise)

            # remove o usuario atual
            # analise = ANALISE.objects.filter(id__gte=2001)
            # analise.delete()

            return render(request, retorno, {'sucess': 'sucess'})
        
    return render(request, retorno, {'erro': 'Erro, por gentileza refazer o teste.'})