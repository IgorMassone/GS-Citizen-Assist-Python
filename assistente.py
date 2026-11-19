import json
import csv
import time


class Assistente:
    def __init__(self, nome, base, caminho_historico, caminho_csv):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.historico = []  # todos os atendimentos (de todas as vezes que o programa rodou)
        self.sessao = []     # só os atendimentos desta execução (usado na nota de facilidade)
        self.carregar_historico()

    def carregar_historico(self):
        try:
            arquivo = open(self.caminho_historico, "r", encoding="utf-8")
            dados = json.load(arquivo)
            arquivo.close()

            # o histórico precisa ser uma lista. se for outra coisa, começa vazio
            if type(dados) == list:
                self.historico = dados
            else:
                self.historico = []
        except (FileNotFoundError, json.JSONDecodeError):
            self.historico = []

    def salvar_historico(self):
        try:
            arquivo = open(self.caminho_historico, "w", encoding="utf-8")
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)
            arquivo.close()
        except OSError:
            print("Não foi possível salvar o histórico.")

    def tem_dado_pessoal(self, texto):
        quantidade = 0
        for caractere in texto:
            if caractere.isdigit():
                quantidade = quantidade + 1

        if quantidade >= 8 or "@" in texto:
            return True
        return False

    def pedir_sim_nao(self, mensagem):
        # repete até a pessoa digitar s ou n devolve True para "s" e False para "n"
        resposta = input(mensagem).lower().strip()
        while resposta != "s" and resposta != "n":
            resposta = input("Digite s ou n: ").lower().strip()
        return resposta == "s"

    def registrar(self, origem, pergunta, id_orientacao, encontrou,
                  ajudou, tentativas, tempo):
        atendimento = {
            "data": time.strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
            "nota_facilidade": None  # é preenchida quando a pessoa der a nota ao sair
        }

        self.historico.append(atendimento)
        self.sessao.append(atendimento)
        self.salvar_historico()

    def perguntar(self):
        # cada DÚVIDA é um atendimento: pode ter várias tentativas até resolver
        inicio = time.time()
        tentativas = 0
        encontrou = False
        ultima_pergunta = ""
        id_orientacao = None

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                break

            if pergunta == "":
                print("Digite uma pergunta.")
                continue

            # dado pessoal: recusa e não registra (nem conta como tentativa)
            if self.tem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas = tentativas + 1
            ultima_pergunta = pergunta
            resultados = self.base.buscar(pergunta)

            if len(resultados) == 0 or resultados[0][0] < 3:
                print("Não encontrei uma orientação para essa dúvida.")
                print("Tente escrever com outras palavras ou use as categorias:")
                for categoria in self.base.categorias():
                    print("-", categoria)
                continue

            encontrou = True
            pontos = resultados[0][0]
            melhor = resultados[0][1]
            id_orientacao = melhor.id

            if pontos >= 6:
                confianca = "ALTA"
            else:
                confianca = "MÉDIA"

            print("\nConfiança da resposta:", confianca, "(" + str(pontos), "pontos)")
            melhor.exibir()

            print("\nOutras orientações que podem ajudar:")
            quantidade = 0
            for resultado in resultados[1:]:
                if resultado[0] >= 3 and quantidade < 2:
                    print("-", resultado[1].titulo)
                    quantidade = quantidade + 1

            if self.pedir_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): "):
                tempo = round(time.time() - inicio, 1)
                self.registrar("pergunta", ultima_pergunta, id_orientacao,
                               True, True, tentativas, tempo)

                # dúvida resolvida: zera tudo para a próx dúvida começar do zero
                inicio = time.time()
                tentativas = 0
                encontrou = False
                ultima_pergunta = ""
                id_orientacao = None
            # se respondeu n, o loop continua: é outra tentativa da MESMA dúvida

        # saiu com 0: se ficou uma dúvida sem resolver, registra uma vez
        if tentativas > 0:
            tempo = round(time.time() - inicio, 1)
            self.registrar("pergunta", ultima_pergunta, id_orientacao,
                           encontrou, False, tentativas, tempo)

    def navegar(self):
        categorias = self.base.categorias()

        while True:
            print("\n--- CATEGORIAS ---")
            for i in range(len(categorias)):
                print(str(i + 1) + " - " + categorias[i])
            print("0 - Voltar")

            opcao = input("Escolha uma categoria: ").strip()
            if opcao == "0":
                break

            if not opcao.isdigit() or int(opcao) < 1 or int(opcao) > len(categorias):
                print("Opção inválida.")
                continue

            categoria = categorias[int(opcao) - 1]
            orientacoes = self.base.por_categoria(categoria)

            while True:
                print("\n---", categoria, "---")
                for i in range(len(orientacoes)):
                    print(str(i + 1) + " - " + orientacoes[i].titulo)
                print("0 - Voltar")

                escolha = input("Escolha uma orientação: ").strip()
                if escolha == "0":
                    break

                if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(orientacoes):
                    print("Opção inválida.")
                    continue

                inicio = time.time()  # começa a contar quando a orientação aparece
                orientacao = orientacoes[int(escolha) - 1]
                orientacao.exibir()
                ajudou = self.pedir_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
                tempo = round(time.time() - inicio, 1)

                self.registrar("categoria", orientacao.titulo, orientacao.id,
                               True, ajudou, 1, tempo)

    def avaliar_facilidade(self):
        # sem atendimento nesta execução não tem o que avaliar
        if len(self.sessao) == 0:
            return

        nota = input("Dê uma nota de facilidade de 1 a 5: ").strip()
        while not nota.isdigit() or int(nota) < 1 or int(nota) > 5:
            nota = input("Digite uma nota de 1 a 5: ").strip()

        # a nota vale para todos os atendimentos feitos nesta execução
        for atendimento in self.sessao:
            atendimento["nota_facilidade"] = int(nota)
        self.salvar_historico()

    def indicadores(self):
        if len(self.historico) == 0:
            print("Ainda não existem atendimentos registrados.")
            return

        total = len(self.historico)
        encontrados = 0
        ajudaram = 0
        tempo_dos_encontrados = 0
        tentativas_total = 0
        soma_notas = 0
        qtd_notas = 0
        sem_solucao = []

        for atendimento in self.historico:
            if atendimento["encontrou"]:
                encontrados = encontrados + 1
                # o tempo médio é "para encontrar", então só soma quem encontrou
                tempo_dos_encontrados = tempo_dos_encontrados + atendimento["tempo_segundos"]
            if atendimento["ajudou"]:
                ajudaram = ajudaram + 1
            else:
                sem_solucao.append(atendimento["pergunta"])
            tentativas_total = tentativas_total + atendimento["tentativas"]

            # .get() devolve None se a chave não existir (histórico de versões antigas)
            nota = atendimento.get("nota_facilidade")
            if nota != None:
                soma_notas = soma_notas + nota
                qtd_notas = qtd_notas + 1

        print("INDICADORES")
        print("Atendimentos:", total)
        print("Resposta encontrada:", round(encontrados / total * 100, 1), "%")
        print("Taxa de acerto (ajudou):", round(ajudaram / total * 100, 1), "%")

        if encontrados > 0:
            print("Tempo médio para encontrar:",
                  round(tempo_dos_encontrados / encontrados, 1), "segundos")
        else:
            print("Tempo médio para encontrar: sem dados")

        print("Tentativas por atendimento:", round(tentativas_total / total, 1))

        if qtd_notas > 0:
            print("Facilidade de uso:", round(soma_notas / qtd_notas, 1), "/ 5")
        else:
            print("Facilidade de uso: ainda sem notas")

        print("Dúvidas sem solução:")
        if len(sem_solucao) == 0:
            print("- Nenhuma")
        else:
            for duvida in sem_solucao:
                print("-", duvida)

    def exportar_csv(self):
        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                  "ajudou", "tentativas", "tempo_segundos", "nota_facilidade"]
        try:
            arquivo = open(self.caminho_csv, "w", newline="", encoding="utf-8")
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()

            for atendimento in self.historico:
                escritor.writerow(atendimento)

            arquivo.close()
            print("Atendimentos exportados para data/atendimentos.csv")
        except OSError:
            print("Não foi possível exportar o CSV.")
