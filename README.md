<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=00494c&height=120&section=header"/>

# Previsão e Análise de Variações no Mercado Financeiro

Projeto acadêmico desenvolvido para o Curso de Graduação em Ciência da Computação do Centro Universitário Espírito-santense, apresentado como parte das exigências da disciplina Projeto Integrador III.

## Autores

- André Luiz Quintela Santos  
- Bernardo Antônio Merlo Soares  
- Entony Jovino dos Santos  
- Guilherme Ambrozio Bicaris  
- Kaio Barbosa Linhares  
- Raphael Simões Gomes  

Orientação: Prof. Howard Cruz Roatti

---

## Descrição do Projeto

Este projeto tem como objetivo aplicar técnicas de ciência de dados para a **previsão e análise de variações no mercado financeiro brasileiro**, desenvolvendo ferramentas que auxiliem investidores e empresas na tomada de decisões informadas. A solução busca democratizar o acesso a análises preditivas, tradicionalmente restritas a grandes instituições financeiras.

O sistema realiza a consulta de informações de ações brasileiras utilizando a API pública [brapi.dev](https://brapi.dev), exibindo de forma simples os principais dados de uma ação selecionada.


VIDEO DO PROJETO

[Assista o vídeo no YouTube](https://youtu.be/RvmOVJgXrm4)

[Assista o vídeo no drive](https://drive.google.com/file/d/1ch2KitS4MJHGnaMEDn5gOV4eqIH7BqnO/view?usp=sharing)

---

## Estrutura do Projeto

```bash
├── data/
│ └── index.json
├── scripts/
│ ├── api_client.py
│ ├── data_cleaner.py
│ └── get_signal.py
├── .env.example
├── main.py
└── README.md
```

- **data/index.json**: Arquivo JSON que mapeia IDs para códigos de ações da B3.
- **scripts/api_client.py**: Função para buscar dados de ações na API.
- **scripts/data_cleaner.py**: Função para tratar os dados de ações da API.
- **scripts/get_signal.py**: Função para a condição da ação (comprar, vender ou manter).
- **.env**: Os dados confidenciais para a aplicação, como o token da api utilizada.
- **main.py**: Script principal para executar a consulta e exibir o result.

<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=00494c&height=120&section=footer"/>
