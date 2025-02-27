# Web Scraper para Web of Science com Playwright

Este script realiza buscas automatizadas na plataforma Web of Science e exporta os resultados para arquivos Excel, segmentados por faixas de registros.

## Funcionalidades

- Realiza login utilizando o acesso remoto via CAFe (opcional).
- Realiza buscas com base em termos de pesquisa configurados.
- Exporta os resultados em lotes (1000 registros por vez).
- Exibe uma barra de progresso com informações sobre o tempo de execução.

---

## Pré-requisitos

1. **Python 3.12**
2. **Instalar as dependências necessárias**:  
   Execute o seguinte comando no terminal:

   ```bash
   pip install playwright==1.49.1 tqdm==4.67.1
   ```

3. **Configuração do Playwright**:  
   Antes de rodar o script, instale os navegadores necessários com o comando:

   ```bash
   playwright install
   ```

---

## Configuração

No arquivo `config.py`, configure as seguintes variáveis:

- **LOGIN**: Seu nome de usuário para login na plataforma CAFe.  
- **SENHA**: Sua senha.  
- **PESQUISA**: Termo de pesquisa que será utilizado na Web of Science.  
- **SIGLA**: Sigla da instituição para o login CAFe.  
- **NOME_UNIVERSIDADE**: Nome da universidade (como aparece no portal CAFe).  
- **NOME_PASTA**: Nome da pasta onde os arquivos exportados serão salvos.  
- **CAFE**: Define se o login via CAFe será necessário (`True` ou `False`).

Exemplo de configuração (`config.py`):

```python
LOGIN = "seu_login"
SENHA = "sua_senha"
PESQUISA = "seu termo de pesquisa"
SIGLA = "sigla_da_instituicao"
NOME_UNIVERSIDADE = "Nome da Universidade"
NOME_PASTA = "resultados"
CAFE = True  # Coloque False se não precisar de login via CAFe
```

---

## Como executar

1. **Configuração**: Certifique-se de que o arquivo `config.py` está devidamente preenchido.  

2. **Rodar o script**: Execute o script no terminal com:

   ```bash
   python nome_do_arquivo.py
   ```

---

## Estrutura do Script

1. **Login no Portal CAFe (opcional)**: Realiza login para acessar a Web of Science via proxy.
2. **Busca e Exportação**: Realiza a busca com os termos fornecidos e exporta os resultados em arquivos Excel.
3. **Progresso e Métricas**: A barra de progresso (`tqdm`) exibe o andamento da exportação e o tempo de execução.
