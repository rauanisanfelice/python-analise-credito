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

1. Inicialização dos container
```
docker-compose up -d
```

2. Configurando o pgAdmin
Acesse o link:

[pgAdmin](http://localhost:80/)

Realize o login:

>User: admin  
>Pass: admin

Clique em: Create >> Server

Conecte no Banco com os seguintes parametros:

Name: **#nome desejado#**
| Parametros | Configurações |
|:--|:--|
| Host | python-analise-postgre |
| Port | 5432 |
| DB | postgres |
| User | postgres |
| Pass |docker123 |

3. Importando os dados

Execute o arquivo abaixo para importar os dados.
> ./database/insert-table.sql

4. Criando um Ambiente Virtual e ativando

```
virtualenv env
source ./venv/bin/activate
```

5. Instalando as dependencias

```
pip3 install -r requirements.txt
```

6. Cria todas as tabelas no Banco de Dados:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

7. Subo o site
```
python3 manage.py runserver
```


## Tabelas de classificação:

### Renda
| Faixa | Numero |
|:--|:--|
| < 20k | 0 |
| 20k - 30k | 1 |
| 30k - 40k | 2 |
| 40k - 50k | 3 |
| 50k - 60k | 4 |
| 60k - 70k | 5 |
| > 70k | 6 |

### Idade
| Faixa | Numero |

|:--|:--|
| 18 - 25 | 0 |
| 25 - 60 | 1 |
| > 60 | 2 |

### Emprestimo
| Faixa | Numero |
|:--|:--|
| < 20k | 0 |
| 2k - 4k | 1 |
| 4k - 6k | 2 |
| 6k - 8k | 3 |
| 8k - 10k | 4 |
| 10k - 12k | 5 |
| 14k - 16k | 6 |
| > 16k | 7 |
