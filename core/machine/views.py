from django.shortcuts import render, redirect
from django.views.generic import View
from machine.forms import *
from machine.models import *

import numpy as np
from django_pandas.io import read_frame

import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
#from sklearn.externals import joblib
from joblib import dump, load

from sklearn.neighbors import KNeighborsClassifier

# Create your views here.
class index(View):
    retorno = 'index.html'
    def get(self, request):
        form = AnaliseForm()
        return render(request, self.retorno, {
            'AnaliseForm' : form
        })

############################################################################
# KNN  #####################################################################
def GeraDump(arquivo, X_train, y_train):
    arquivo = "./DumpPredict.sav"

    # PASSA OS PARAMETROS
    KNN_model = KNeighborsClassifier(n_neighbors=13)
    
    # REALIZA O FIT
    KNN_model.fit(X_train, y_train)
    
    # DUMP NO MODELO
    dump(KNN_model, arquivo)

def MachineLearning():
    analises = ANALISE.objects.all()
    pdAnalise = read_frame(analises)

    # CRIA AS COLUNAS
    pdAnalise["FaixaRenda"] = 0
    pdAnalise["FaixaEtaria"] = 0
    pdAnalise["FaixaEmprestimo"] = 0

    # REMOVE IDADE NEGATIVA
    pdAnalise = pdAnalise[pdAnalise["IDADE"] > 0]

    # CRIA FAIXAS DE RENDA
    pdAnalise.loc[(pdAnalise["RENDA"] < 20000), "FaixaRenda"] = 0
    pdAnalise.loc[(pdAnalise["RENDA"] >= 20000) & (pdAnalise["RENDA"] < 30000), "FaixaRenda"] = 1
    pdAnalise.loc[(pdAnalise["RENDA"] >= 30000) & (pdAnalise["RENDA"] < 40000), "FaixaRenda"] = 2
    pdAnalise.loc[(pdAnalise["RENDA"] >= 40000) & (pdAnalise["RENDA"] < 50000), "FaixaRenda"] = 3
    pdAnalise.loc[(pdAnalise["RENDA"] >= 50000) & (pdAnalise["RENDA"] < 60000), "FaixaRenda"] = 4
    pdAnalise.loc[(pdAnalise["RENDA"] >= 60000) & (pdAnalise["RENDA"] < 70000), "FaixaRenda"] = 5
    pdAnalise.loc[(pdAnalise["RENDA"] >= 70000), "FaixaRenda"] = 6

    # CRIA FAIXAS DE IDADE
    pdAnalise.loc[(pdAnalise["IDADE"]) >= 18 & (pdAnalise["IDADE"] < 25), "FaixaEtaria"] = 0
    pdAnalise.loc[(pdAnalise["IDADE"]) >= 25 & (pdAnalise["IDADE"] < 60), "FaixaEtaria"] = 1
    pdAnalise.loc[(pdAnalise["IDADE"] >= 60), "FaixaEtaria"] = 2

    # CRIA FAIXAS DE EMPRESTIMO
    pdAnalise.loc[(pdAnalise["EMPRESTIMO"] < 2000), "FaixaEmprestimo"] = 0
    pdAnalise.loc[(pdAnalise["EMPRESTIMO"] >= 2000) & (pdAnalise["EMPRESTIMO"] < 4000), "FaixaEmprestimo"] = 1
    pdAnalise.loc[(pdAnalise["EMPRESTIMO"] >= 4000) & (pdAnalise["EMPRESTIMO"] < 6000), "FaixaEmprestimo"] = 2
    pdAnalise.loc[(pdAnalise["EMPRESTIMO"] >= 6000) & (pdAnalise["EMPRESTIMO"] < 8000), "FaixaEmprestimo"] = 3
    pdAnalise.loc[(pdAnalise["EMPRESTIMO"] >= 8000) & (pdAnalise["EMPRESTIMO"] < 10000), "FaixaEmprestimo"] = 4
    pdAnalise.loc[(pdAnalise["EMPRESTIMO"] >= 12000) & (pdAnalise["EMPRESTIMO"] < 14000), "FaixaEmprestimo"] = 5
    pdAnalise.loc[(pdAnalise["EMPRESTIMO"] >= 14000) & (pdAnalise["EMPRESTIMO"] < 16000), "FaixaEmprestimo"] = 6
    pdAnalise.loc[(pdAnalise["EMPRESTIMO"] >= 16000), "FaixaEmprestimo"] = 7

    # AJUSTA PROBLEMA DE BASE DESBALANCEADA

    # SEPARA O REGISTRO NOVO QUE FOI IMPORTADO
    dtNovRegistroAnalise = pdAnalise[pdAnalise["id"] > 2000]
    dtAntigosRegistrosAnalise = pdAnalise[pdAnalise["id"] <= 2000]

    # SEPARA EM DOIS DF UM SOMENTE CLASSIFICADO COM 0 E OUTRO COM 1
    dtAnaliseZero = dtAntigosRegistrosAnalise[dtAntigosRegistrosAnalise["RESULTADO"] == 0]
    dtAnaliseUm = dtAntigosRegistrosAnalise[dtAntigosRegistrosAnalise["RESULTADO"] == 1]

    # SHUFFLE NO DF
    dtAnaliseZero = dtAnaliseZero.sample(frac=1, random_state=905).reset_index(drop=True)

    # DEIXA SOMENTE 1000 REGISTROS COM RESULTADOS IGUAL A 0 PARA NÃO DEIXAR A BASE DESBALANCEADA
    indexZero = dtAnaliseZero[dtAnaliseZero.index > 1000]
    dtAnaliseZero = dtAnaliseZero.drop(indexZero.index, axis=0)

    # UNE OS DF NOVAMENTE
    dtFullTratadaAnalise = pd.concat([dtAnaliseUm, dtAnaliseZero])

    # SHUFFLE NO DF
    dtFullTratadaAnalise = dtFullTratadaAnalise.sample(frac=1, random_state=1).reset_index(drop=True)

    #############################################################################
    # VERIFICAR SE POSSUI JA DUMP SALVO
    arquivo = "./DumpPredict.sav"

    # CRIA BASE TREINO E TESTE
    X_train, X_test, y_train, y_test = train_test_split(dtFullTratadaAnalise.iloc[:,5:8], dtFullTratadaAnalise["RESULTADO"], test_size=0.30, random_state=27)

    if not os.path.exists(arquivo):
        GeraDump(arquivo, X_train, y_train)

    # CLASSIFICA O NOVO REGISTRO
    Loaded_model = load(arquivo)
    KNN_prediction_New = Loaded_model.predict(dtNovRegistroAnalise.iloc[:,5:8])

    # REALIZE A NOVA PREDICT
    KNN_prediction = Loaded_model.predict(X_test)
    acuracia = round(accuracy_score(KNN_prediction, y_test) * 100,2)

    resultado = [[acuracia], [KNN_prediction_New[0]]]
    return resultado

def validacao(request):
    retorno = 'validacao.html'
    if request.method == "POST":
        form = AnaliseForm(request.POST)
        if form.is_valid():
            renda = form.cleaned_data['renda']
            idade = form.cleaned_data['idade']
            emprestimo = form.cleaned_data['emprestimo']
            
            # Salva no banco de dados
            analise = ANALISE(RENDA=renda, IDADE=idade, EMPRESTIMO=emprestimo, RESULTADO=False)
            analise.save()

            # MACHINE LEARNING
            RetornoMachine = MachineLearning()
            #print(RetornoMachine[0])

            # remove o usuario atual
            analise = ANALISE.objects.filter(id__gte=2001)
            analise.delete()

            return render(request, retorno, {
                'acuracia': RetornoMachine[0],
                'retorno': RetornoMachine[1]
            })
        
    return render(request, retorno, {'erro': 'Erro, por gentileza refazer o teste.'})