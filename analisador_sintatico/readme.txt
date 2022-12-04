# Formato arquivos

Para executar é necessário uma gramática e uma lista de tokens salvos em arquivo no seguinte formato:

Gramática:

S A B
S -> aA | bB
A -> aA | &
B -> bB | b

Lista de tokens:

id
+
id
*
id

Salvar em gramatica1.txt e tokens1.txt
Para rodar um arquivo diferente altere o caminho em parser.py.

# Executar

python3 parser.py

# Testes

Há 3 testes para cada um dos algoritmos: epsilon, fatoração, first_follow e recursao_esquerda.
Para alterar o teste, altere no próprio arquivo .py o caminho da grámatica.

Para rodar basta executar seus .py

python3 epsilon.py


