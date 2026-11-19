import os
from base_conhecimento import BaseConhecimento
from assistente import Assistente

#o programa funciona mesmo rodando de outro lugar
pasta = os.path.dirname(os.path.abspath(__file__))
caminho_base = os.path.join(pasta, "data", "base_conhecimento.json")
caminho_historico = os.path.join(pasta, "data", "historico.json")
caminho_csv = os.path.join(pasta, "data", "atendimentos.csv")


print("CITIZEN ASSIST - CONSUMIDOR DIGITAL")
print("Orientações sobre compras e serviços digitais.")
print("Este assistente não é um canal oficial.\n")

base = BaseConhecimento(caminho_base)
base.carregar()

if len(base.orientacoes) == 0:
    print("Não há orientações para mostrar.")
else:
    assistente = Assistente("Citizen Assist", base, caminho_historico, caminho_csv)

    while True:
        print("MENU")
        print("1 - Fazer uma pergunta")
        print("2 - Navegar por categorias")
        print("3 - Ver indicadores")
        print("4 - Exportar CSV")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            assistente.avaliar_facilidade()
            assistente.indicadores()
            assistente.exportar_csv()
            print("Obrigado por utilizar o Citizen Assist!")
            break
        else:
            print("Opção inválida. Tente novamente.")
