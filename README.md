![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/rauanisanfelice/python-analise-credito.svg)
![GitHub top language](https://img.shields.io/github/languages/top/rauanisanfelice/python-analise-credito.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/rauanisanfelice/python-analise-credito.svg)
![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/rauanisanfelice/python-analise-credito.svg)
![GitHub contributors](https://img.shields.io/github/contributors/rauanisanfelice/python-analise-credito.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/rauanisanfelice/python-analise-credito.svg)

![GitHub stars](https://img.shields.io/github/stars/rauanisanfelice/python-analise-credito.svg?style=social)
![GitHub followers](https://img.shields.io/github/followers/rauanisanfelice.svg?style=social)
![GitHub forks](https://img.shields.io/github/forks/rauanisanfelice/python-analise-credito.svg?style=social)


# Análise de Crédito

Análise de Crédito utilizando a linguagem Python.

## Instruções

1. Criando um Ambiente Virtual e ativando

```
virtualenv env
source ./venv/bin/activate
```

2. Instalando as dependencias

```
pip3 install -r requirements.txt
```

3. Cria todas as tabelas no Banco de Dados:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

4. Subo o site
```
python3 manage.py runserver
```