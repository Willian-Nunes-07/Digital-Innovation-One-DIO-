---
---
# Apresentação do Desafio

Aqui é comentado de forma resumida a proposta do desafio e o cronograma do que será feito nas próximas etapas.

# Criar um Copilot em Branco

Dentro do copilot studio, vá na parte **Agentes** e crie um novo agente.

Aqui a proposta é criar um agente que irá pesquisar conteúdos de Copilot Studio dentro da documentação oficial da Microsoft. Logo, o prompt deve ser criado neste sentido.

```Prompot
Você é o agente chamado "Agente da DIO" e vai agir em tom formal com o idioma português brasileiro, para retornar informações relevantes da documentação oficial da Microsoft, o Microsoft Learn.

Ao retornar uma resposta para a pergunta do usuário,você deve considerar:

- Buscar a melhor resposta na documentação;
- Retornar a resposta apropriada e amigável em tom formal;
- Retornar uma ou mais citações da documentação
```

Após definir as configurações, finalize a criação do agente
# Customizar um Tópico

Vá em tópicos e crie um em branco
 - Determine os gatilhos;
 - Crie uma resposta generativa, como variável, use a variável do sistema "Activity.Text", assim a IA irá utilizar o texto do usuário; 
 - Coloque uma mensagem de encerramento daquele tópico.

Após isto, realize o teste do tópico e verifique se o gatilho é acionado corretamente.

# Personalizar uma mensagem de erro de tópico

Em tópicos, você pode ir em sistema, e escolher tanto o tópico de melhoramento de conversa quanto o fallback, e adicionar uma mensagem customizada de erro no fluxo do tópico.

Através destas ações, você pode criar um fluxo de rastreamento de erros, afim de aprimorar a experiência do usuário final.
# Aumentar e diminuir a qualidade da resposta com GenAI

No tópico do sistema "Melhora da conversa", você pode editar as configurações da resposta generativa, mudando pontos como:

- Moderação: Alto, Média, Baixa;
- Prompt customizável: Ordenar diretrizes da reposta generativa;
- Fontes de conhecimento: Limita ou expande o escopo de pesquisa da IA.

Você pode habilitar nas configurações do agente o modo clássico ou generativo, e moderar para ele ser mais criativo ou mais preciso. 
# Entendendo o Desafio

## O que fazer?

- Explore a demonstração apresentada no conteúdo prático e faça um resumo do que aprendeu neste conteúdo. Em seguida armazene em um repositório no GitHub e compartilhe o link na entrega do desafio.
    

## Orientações para Entrega

- Crie um repositório no GitHub.
- Envie em "Entregar Projeto", o link do seu repositório no GitHub.
# Consideração Final

Todo este documento foi gerado no Obsidian, levando em consideração todos os pontos citados acima para resumir o que foi aprendido com o conteúdo disponibilizado na plataforma da DIO.
