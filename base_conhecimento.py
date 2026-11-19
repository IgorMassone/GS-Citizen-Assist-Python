import json
from orientacao import Orientacao


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            arquivo = open(self.caminho, "r", encoding="utf-8")
            dados = json.load(arquivo)
            arquivo.close()

            self.orientacoes = []
            for item in dados:
                orientacao = Orientacao(item)
                self.orientacoes.append(orientacao)

        #keyError: faltou algum campo em um registro
        #typeError: o JSON está num formato inesperado (não é uma lista de dicionários)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            print("Não foi possível carregar a base de conhecimento.")
            self.orientacoes = []

    def categorias(self):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                lista.append(orientacao)
        return lista

    def normalizar(self, texto):
        acentos = {
            "á": "a", "à": "a", "ã": "a", "â": "a",
            "é": "e", "ê": "e", "í": "i", "ó": "o",
            "õ": "o", "ô": "o", "ú": "u", "ç": "c"
        }

        texto = texto.lower().strip()
        for letra, troca in acentos.items():
            texto = texto.replace(letra, troca)

        for sinal in "?!.,;:()":
            texto = texto.replace(sinal, " ")

        return " " + " ".join(texto.split()) + " "

    def pontuar(self, pergunta, orientacao):
        pergunta = self.normalizar(pergunta)
        titulo = self.normalizar(orientacao.titulo)
        pontos = 0

        # +3 para cada palavra-chave que aparece na pergunta
        for palavra_chave in orientacao.palavras_chave:
            chave = self.normalizar(palavra_chave)
            if chave in pergunta:
                pontos = pontos + 3

        # +1 para cada palavra da pergunta (4 letras ou mais) que aparece no título
        palavras = pergunta.split()
        palavras_titulo = titulo.split()

        for palavra in palavras:
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos = pontos + 1

        return pontos

    def buscar(self, pergunta):
        resultados = []

        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            # só guarda quem fez pelo menos 1 ponto
            if pontos > 0:
                resultados.append((pontos, orientacao))

        # ordena da maior para a menor pontuação (item[0] = os pontos da tupla)
        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados
