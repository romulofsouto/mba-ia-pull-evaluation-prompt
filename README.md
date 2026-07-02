# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

**A) Seção "Técnicas Aplicadas (Fase 2)":**

- Quais técnicas avançadas você escolheu para refatorar os prompts?
Foram aplicadas técnicas avançadas para refatorar o prompt, tais como Role Prompting, Few-shot e Chain-of-thought
- Justificativa de por que escolheu cada técnica?
Optei a utilização da técnica de Role Prompting devido uma vez definida a persona "Você é um Product Manager especializado em transformar relatos de bugs em User Stories claras, testáveis e adequadas para times de Produto, QA e Engenharia" a LLM irá conextualizar melhor como deverá se comportar e refinar o que deverá ser feito. 
Além disso, utilizei o Few-shot para que as informações de saída sejam apresentadas de forma padronizada. 

- Exemplos práticos de como aplicou cada técnica
Role prompting: "Você é um Product Manager especializado em transformar relatos de bugs em User Stories claras, testáveis e adequadas para times de Produto, QA e Engenharia".
Few-shot: Apresentei vários exemplos com complexidades Simples, Média e Complexa, segue um dos exemplos que utilizei: 

Exemplo 1 - Simples
    bug_report: "Botão de remover do carrinho não funciona no produto ID 5678."

    resposta: "Como um cliente navegando na loja, eu quero remover produtos do meu carrinho de compras, para que eu possa ajustar os itens antes de finalizar minha compra.\n\nCritérios de Aceitação:\n- Dado que tenho um produto no carrinho\n- Quando clico no botão "Remover do Carrinho"\n- Então o produto deve ser removido do carrinho\n- E devo ver uma confirmação visual\n- E o contador do carrinho deve ser atualizado"


**B) Seção "Resultados Finais":**

- Link público do seu dashboard do LangSmith mostrando as avaliações:    
https://smith.langchain.com/hub/romulofsouto/bug_to_user_story_v2

- Screenshots das avaliações com as notas mínimas de 0.8 atingidas
![alt text](image.png)

- Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)
| Item      | Total | V1 – F1   | V1 – Clareza | V1 – Precisão | V2 – F1   | V2 – Clareza | V2 – Precisão |
|-----------|------:|----------:|-------------:|--------------:|----------:|-------------:|--------------:|
| 1         |    15 |    0,45   |         0,52 |          0,46 |    0,75   |         0,90 |          0,90 |
| 2         |    15 |    0,42   |         0,57 |          0,42 |    0,75   |         0,80 |          0,90 |
| 3         |    15 |    0,43   |         0,49 |          0,43 |    0,87   |         0,90 |          1,00 |
| 4         |    15 |    0,50   |         0,60 |          0,52 |    1,00   |         1,00 |          1,00 |
| 5         |    15 |    0,37   |         0,52 |          0,37 |    0,58   |         0,90 |          0,67 |
| 6         |    15 |    0,39   |         0,69 |          0,43 |    0,85   |         0,90 |          0,90 |
| 7         |    15 |    0,27   |         0,60 |          0,38 |    1,00   |         1,00 |          1,00 |
| 8         |    15 |    0,39   |         0,45 |          0,39 |    0,75   |         0,85 |          0,80 |
| 9         |    15 |    0,78   |         0,50 |          0,62 |    1,00   |         1,00 |          1,00 |
| 10        |    15 |    0,45   |         0,43 |          0,45 |    0,90   |         0,90 |          0,90 |
| 11        |    15 |    0,48   |         0,50 |          0,48 |    0,80   |         0,90 |          0,80 |
| 12        |    15 |    0,49   |         0,70 |          0,49 |    1,00   |         0,95 |          1,00 |
| 13        |    15 |    0,43   |         0,50 |          0,52 |    0,90   |         0,95 |          1,00 |
| 14        |    15 |    0,42   |         0,42 |          0,45 |    0,80   |         0,90 |          1,00 |
| 15        |    15 |    0,40   |         0,39 |          0,52 |    0,90   |         0,75 |          0,67 |
| **Média** |       | **0,445** |    **0,525** |     **0,462** | **0,857** |    **0,907** |     **0,903** |


**C) Seção "Como Executar":**

- Instruções claras e detalhadas de como executar o projeto
1. Clonar o arquivo .env.example alterar o nome para .env
2. Substituir as chaves da OpenIA ou Gemine, e langsmith.
3. python3 -m venv venv
4. source venv/bin/activate 

A partir de agora se projeto deverá funcionar normalmente.


- Pré-requisitos e dependências
Deverá ser instalado o python3. 


- Comandos para cada fase do projeto

1. Executar pull dos prompts ruins
python src/pull_prompts.py


2. Fazer push dos prompts otimizados
python src/push_prompts.py

3. Executar avaliação
python src/evaluate.py

4. Executar testes de validação do prompt otimizado.
pytest tests/test_prompts.py


**3. Evidências no LangSmith:**

- Link público (ou screenshots) do dashboard do LangSmith
- Devem estar visíveis:
  - Dataset de avaliação com 15 exemplos
      ![alt text](image-1.png)
  - Execuções dos prompts v2 (otimizados) com notas ≥ 0.8
      ![alt text](image-2.png)
  - Tracing detalhado de pelo menos 3 exemplos
      Exemplo 1

      ![alt text](image-3.png) - Resposta 1
      ![alt text](image-4.png) - Avaliador F1 - Resposta 1
      ![alt text](image-5.png) - Avaliador Clareza - Resposta 1
      ![alt text](image-6.png) - Avaliador Precisão - Resposta 1

      Exemplo 2

      ![alt text](image-7.png) - Resposta 2
      ![alt text](image-8.png) - Avaliador F1 - Resposta 2
      ![alt text](image-9.png) - Avaliador Clareza - Resposta 2
      ![alt text](image-10.png) - Avaliador Precisão - Resposta 2

      Exemplo 3

      ![alt text](image-11.png) - Resposta 3
      ![alt text](image-12.png) - Avaliador F1 - Resposta 3
      ![alt text](image-13.png) - Avaliador Clareza - Resposta 3
      ![alt text](image-14.png) - Avaliador Precisão - Resposta 3

---
