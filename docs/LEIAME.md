# Modelo Base

Utilize a estrutura e os códigos presentes na pasta `src/evento` como base (template) para desenvolver os novos módulos do sistema. Esse módulo serve para ilustrar o fluxo correto da nossa arquitetura de camadas.

Fique totalmente à vontade para modificar, expandir e adaptar as regras de acordo com as necessidades específicas do escopo que você estiver desenvolvendo.

# Regras do Pylint

O **Pylint** está configurado e ativo. 

Todo código desenvolvido no projeto deve seguir estritamente as regras deste guia para obter **nota 10/10**.

---

## 1. Como rodar o Linter antes de commitar?

Antes de dar `git add` ou `git push`, ative a sua `venv` e execute o comando exatamente assim na raiz do projeto:

```bash
PYTHONPATH=. pylint src
```

## 2. Regras de Formatação (Erros de Linha e Espaço)
O Pylint pune pequenos descuidos visuais. Fique atento a estes três alertas:

- Linha em Branco no Final do Arquivo (missing-final-newline)
O Python exige que todo arquivo .py termine com uma linha completamente vazia.

Errado: Terminar o arquivo direto na última linha de código escrita.

Certo: Vá até o final do arquivo, aperte Enter para criar uma linha em branco (uma linha sem nenhum caractere ou espaço) e salve.

- Espaços Invisíveis de Fim de Linha (trailing-whitespace)
Não deixe espaços em branco sobrando depois que o seu código termina ou em linhas que deveriam estar vazias.

Errado: return novo_evento_model    (com espaços invisíveis após o código).

Certo: Posicione o cursor no final da linha e use o Backspace para apagar qualquer espaço solto.

- Limite de Linhas Longas (line-too-long)
O limite do projeto está travado em 100 caracteres por linha.

Se um comentário ou uma linha de código passar desse limite, quebre-a em duas ou mais linhas.

Exceção: Links de URLs longas dentro de comentários são ignorados automaticamente pelo linter.

## 3. Padrão de Nomenclatura (Tudo em Português)
Nossa arquitetura exige código escrito em português. O Pylint vai validar o formato dos nomes usando as seguintes regras:

Funções, Métodos e Variáveis (snake_case): Sempre letras minúsculas separadas por underline.

Exemplo:

```python

id_usuario = "123"
def cadastrar_novo_evento():
    
```

*   **Classes (`PascalCase`):** Iniciais maiúsculas e sem underline.

```python

class ServicoEvento:
class ModeloProduto:

```
    
Constantes Globais (SNAKE_CASE_MAIUSCULO): Todas as letras maiúsculas separadas por underline.

Exemplo:

```python
URL_BANCO_DADOS = "postgresql://..."
```


> **Exceções Liberadas:** Para não quebrar o padrão dos frameworks (FastAPI e SQLAlchemy), os seguintes termos técnicos curtos foram liberados globalmente no `.pylintrc` e **não** vão gerar erro: `db`, `id`, `app`, `router`, `payload`, `Base` e `SessionLocal`.

Se for necessário utilizar outros termos é só adicionar no `.pylintrc`

---

## 4. Regras de Clean Code (Bloqueios de Arquitetura)

### Imports Inúteis (`unused-import`)
Trazer um módulo para o arquivo e não utilizá-lo no código gera erro `W0611`.
*    **Certo:** Se você apagou uma função e o import dela ficou sobrando no topo do arquivo, remova a linha do `import`.

### Funções Gigantescas (`max-statements`)
Nenhuma função ou rota pode passar de **40 linhas de código**.
*    **Certo:** Se a sua lógica ficou muito grande, quebre-a criando funções menores e específicas para apoiar o fluxo.

### Código Duplicado (`duplicate-code`)
Copiar e colar blocos de código idênticos entre módulos diferentes vai travar o pipeline de CI/CD.
*    **Errado:** Copiar uma função de formatação de data de `evento/` para usar em `produtos/`.
*    **Certo:** Mova a lógica repetida para o arquivo utilitário central `src/shared/utils.py` e apenas importe onde precisar.

---

## 5. Como Silenciar um Alerta Justificado?

Se o Pylint apontar um erro em uma linha onde o uso é estritamente obrigatório por causa de alguma ferramenta externa, você pode desativar o alerta **apenas para aquela linha** usando o comentário `# pylint: disable=nome-do-erro`:

```python
# Exemplo de uso aceito para injetar dependências externas do FastAPI:
objeto_externo = DependenciaDoFramework()  # pylint: disable=invalid-name
```
