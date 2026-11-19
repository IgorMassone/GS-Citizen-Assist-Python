# Citizen Assist – Consumidor Digital

## Público e problema

O projeto é voltado para pessoas que fazem compras pela internet e utilizam serviços digitais. O assistente reúne orientações simples sobre entrega, defeitos, cancelamento, cobranças indevidas e golpes envolvendo Pix.

Seu objetivo é facilitar o acesso a informações e indicar caminhos para que o consumidor saiba como agir diante de problemas em compras e serviços digitais.

## Integrantes

- Carlos Eduardo Affonso — RM 569676
- Igor Massone Monteiro — RM 573853

## ODS relacionados

- **ODS 12 – Consumo e produção responsáveis:** incentivo ao consumo consciente e ao conhecimento dos direitos do consumidor.
- **ODS 16 – Paz, justiça e instituições eficazes:** divulgação de canais oficiais de reclamação e orientação ao cidadão.

## Como executar

1. Instale o Python 3.
2. Abra a pasta do projeto no terminal.
3. Execute o comando:

   ```bash
   python main.py
   ```

Não é necessário instalar bibliotecas externas.

## Organização dos arquivos

- `main.py`: apresenta o menu e inicia o programa.
- `orientacao.py`: contém a classe `Orientacao`, responsável por armazenar e exibir uma orientação.
- `base_conhecimento.py`: contém a classe `BaseConhecimento`, que carrega o JSON, organiza as categorias e realiza a busca.
- `assistente.py`: contém a classe `Assistente`, responsável pela interação com o usuário, registro dos atendimentos e cálculo dos indicadores.
- `data/base_conhecimento.json`: armazena as orientações disponíveis.
- `data/historico.json`: armazena o histórico dos atendimentos.
- `data/atendimentos.csv`: arquivo CSV exportado pelo programa.

## Orientação a objetos

A composição segue a ideia trabalhada na Aula 10, utilizando como referência o exemplo de `Aluno` e `Disciplina`.

- `Assistente` possui um objeto `BaseConhecimento`.
- `BaseConhecimento` possui uma lista de objetos `Orientacao`.
- Cada objeto `Orientacao` guarda os dados de um registro carregado do JSON.

As classes utilizam construtores `__init__`, atributos com `self` e métodos para organizar as responsabilidades do programa.

## Regra de pontuação

A busca utiliza um sistema de pontuação para identificar as orientações mais relacionadas à pergunta do usuário:

- Cada palavra-chave encontrada na pergunta soma 3 pontos.
- Cada palavra da pergunta com 4 letras ou mais que aparece no título soma 1 ponto.
- **6 pontos ou mais:** confiança alta.
- **De 3 a 5 pontos:** confiança média.
- **Menos de 3 pontos:** o sistema informa que não encontrou uma orientação.

A busca devolve uma lista de tuplas `(pontos, orientacao)`, ordenada da maior para a menor pontuação.

## Fontes consultadas

As fontes oficiais e as respectivas datas de conferência estão registradas nas orientações do arquivo `data/base_conhecimento.json`.

Entre as instituições consultadas estão:

- PROCON-SP.
- Banco Central do Brasil.
- Ministério da Justiça.

## Testes com usuários

Foram analisados **11 registros de atendimento** realizados durante os testes do projeto.

### Indicadores obtidos

| Indicador | Resultado |
|---|---:|
| Total de atendimentos registrados | 11 |
| Respostas encontradas | 3 (27,3%) |
| Respostas avaliadas como úteis | 3 (27,3%) |
| Tempo médio por atendimento | 13,3 segundos |
| Média de tentativas por atendimento | 1 |
| Facilidade de uso | 3,3 de 5 |

A nota de facilidade considera as três avaliações registradas no histórico.

### Perguntas sem orientação encontrada

Durante os testes, 8 das 11 perguntas não encontraram uma orientação correspondente. Entre elas estavam:

- Meu produto não foi entregue.
- Não sei como localizar a minha compra.
- Quero cancelar uma compra pela internet.
- Comprei um produto e ele veio com defeito.
- Fiz um Pix para um golpista.
- Minha encomenda não chegou.
- Estão cobrando algo que não comprei.
- Como posso me proteger de fraudes digitais.

### Melhoria realizada

A partir dos testes, foi identificada a dificuldade do sistema em reconhecer perguntas escritas de maneira diferente das palavras-chave cadastradas.

Como melhoria, foi adicionada a expressão `"onde minha compra"` às palavras-chave da orientação sobre produtos não entregues. Assim, uma pergunta como "Não sei onde minha compra tá" passou a ter maior possibilidade de encontrar a orientação correspondente.

**Participantes dos testes:** Os atendimentos foram feitos por 3 pessoas de fora da equipe. Os 11 registros representam atendimentos, não necessariamente 11 pessoas diferentes.

## Limitações

- O programa não consulta a internet durante o atendimento.
- A busca compara palavras-chave e palavras dos títulos; por isso, pode não reconhecer perguntas escritas de maneiras muito diferentes.
- As orientações não substituem atendimento jurídico, bancário ou dos órgãos oficiais.
- O programa recusa perguntas que contenham e-mail ou 8 ou mais dígitos, como medida para evitar o registro de dados pessoais.
- A qualidade das respostas depende da quantidade e da atualização das informações cadastradas na base de conhecimento.

## Vídeo técnico

**Link do vídeo:** https://youtu.be/Y0MfIGNWk9k

O vídeo apresenta o funcionamento do Citizen Assist, explica a estrutura do código e demonstra as principais funcionalidades, incluindo a busca por pontuação, a navegação por categorias, o registro de atendimentos, os indicadores e a alteração da base de conhecimento.