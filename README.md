# analisador-lexico-sintatico
O automato é representado da seguinte forma:
	numero_estados: diz quantos estados ele tem
	estado_inicial: qual estado inicial dele
	estados_finais: lista do estados finais
	alfabeto: lista dos simbolos do alfabeto
	def_re: a definição regular que gerou ele
	transicoes: as transicoes na forma [estado de origem, simbolo, estado de destino]. Caso haja n transições de mesma origem e mesmo simbolo, serão criadas n transicoes.

Para ler o regex, é necessário colocar ponto a cada concatenação.
Para executar analisador léxico precisamos executar em ordem as seguintes funções:
	
	regex_from_read_file que abre o arquivo com as definições regulares e as salva numa lista;
	
	Para cada regex na lista:
		syntaxtree.Tree(regex.add_end_of_regex_symbol()) que transforma o regex em uma arvore;
		Criar um automato(classe Automata) com o alfabeto do regex como parametro, automata.Automata(alfabeto=regex.alphabet)
		Usar a função re2dfa(tree) da classe automato para gerar um automato a partir da arvore e salva-lo em alguma lista.
	
	Depois passar a lista para a função union.union(ats) da biblioteca Union que faz a união dos automatos da lista por '&' e renomeia os estados de 0 a o total de estados para identifica-los
	unicamente.
	
	nfa_to_dfa.nfa_e_to_dfa(automato_unido) para determizar o automato gerado no passo anterior.
	
	Com o automato podemos gerar a tabela léxica criando um obejto da classe Tabela_Lexica, passando como parametros a lista de palavras reservadas pré-carregadas, automatos originais, 
	automato determinizado e a lista de regexs.
	
	Com a criação da tabela podemos usar as funções dela ler_texto para ler um texto fonte(padrão de nome "texto.txt"), gera_lista que analisa as palavras do texto para achar seu padrões
	de tokens e salva-los numa lista de tokens, output_token para gerar um arquivo que serve de entrada para o analisador sintático. Podemos opcionalmente usar salvar_tabela para gerar a tabela de
	transições do automato determinizado.
		
Para gerar um automato a partir de um arquivo usa a função da classe Automata ler_arquivo para cria-lo. Com isso ele pode ser passado para as outras as funlçoes de union.union() caso se deseje uni-lo
	com outros automatos ou para nfa_to_defa.nfa_e_to_dfa para determiniza-lo.

Caso se deseje ver os atributos de qualquer automato(numero de estados, transições, estados finais) bastar usar a função imprimir_atributos da classe Automata para imprimir na tela.
A função da tabela léxica imprimir_simbolos, imprimi na tela as palavras reservadas e os padrões de tokens.

Em caso de erro léxico na leitura de uma palavra e verificação se ele é um token, caso ela não pertença a linguagem, um erro léxico é apontado e o programa é abortado.

Os arquivos de teste para as ers estão na pasta input e os automatos gerados na pasta output.

Há também no código automatos colocados manualmente que estão em comentários para testar as funções de união e determinização.
