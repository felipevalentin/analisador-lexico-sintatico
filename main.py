import syntaxtree
import automata
import regularexpression
import union
import nfa_to_dfa
import sys
from collections import defaultdict

'''Classe para armazenar a tabla léxica e suas informações e metodos pertinentes'''
class Tabela_Lexica():
    def __init__(self, p_r, automatos, automato_geral, regex):
        self.p_r = p_r # Simbolos
        self.automatos = automatos
        self.automato_geral = automato_geral
        self.regex =  regex
        self.texto = '' # texto fonte de entrada
        self.palavras = [] # lista das palavras separadas do texto
        self.tokens = [] # lista dos tokens na forma (lexema, padrão(
        self.estado_tokens = [] # lista dos estados finais do automato final e o padrão que ele gera
    
    ''' Função para mostrar a tabela de Símbolos'''
    
    def listar_Simbolos(self):
        tab = []
        for i in range(0, len(self.p_r)):
            tab.append(self.p_r)
        for i in range(0, len(self.regex)):            
            tab.append([self.regex[i].re, self.regex[i].def_re])
        for i in range(0,len(tab)):
            print(tab[i])
    
    '''Função que lê o texto de entrada e separa em uma lista de palavras''' 
    def ler_texto(self, arq):
        
        with open(arq) as f:
            self.texto = f.read()            
            self.palavras = self.texto.split()
        f.close()
        
    
    ''' Função que lê uma palavra e usando o automato verifica se ela é uma palavra válida'''
    
    def ler_palavra(self, input_):
        state = self.automato_geral.estado_inicial
        
        
        " verifica se palavra vazia faz parte e se for retorna estado inicial "
        if(input_ == ""):
            if(state in self.automato_geral.estados_finais):
                return state          
            else:
                return ("Entrada inválida")
        
        
        
    
        ''' Função que le a palavra letra a letra e a cada letra faz a transição de state(estado atual) para o detino da transição'''
        for p in range(0, len(input_)):
            for i in range(0, len(self.automato_geral.transicoes)):
                
                if(state == self.automato_geral.transicoes[i][0] and input_[p] == self.automato_geral.transicoes[i][1]):
                    state = self.automato_geral.transicoes[i][2]                    
                    break
                '''Se não há transição do estado para outro com aquela letra retorna entrada inválida'''
                if(i == (len(self.automato_geral.transicoes) - 1)):
                    #print("aqui2")
                    return ("Entrada inválida")
        
            ''' Ao chegar no fim da palavra, verifica se o estado atual faz parte do conjunto de estados finais'''
            if(p == len(input_) - 1):
               
                for i in range(0, len(self.automato_geral.estados_finais)):
                    
                    if (state == self.automato_geral.estados_finais[i]):
                        return (state)
                    if (i == len(self.automato_geral.estados_finais) - 1) :
                        return ("Entrada inválida")
                  
    ''' Função para gerar a lista de tokens, verifica primeiro se a palavra é palavra reservada(p_r)'''
    def gera_lista(self):
        #print(self.palavras)
        for p in self.palavras:
            #print(p)
            
            if (p in self.p_r):
                padrao = ("p_r")
                aux = (p + " " + padrao)
                self.tokens.append(aux)
                continue
            
            
            s = self.ler_palavra(p)
            if (s == "Entrada inválida"):
                #print("Palavra " + p + " não reconhecida")
                return(-1)
            
                    
            #Acha o padrão pelo automato
            else:
                padrao = ''
                #print(s)                
                               
                for k in range(0,len(s)):
                    for i in range(0,len(self.automatos)):
                        for j in range (0, len(self.automatos[i].estados_finais)):
                        
                            #print("")
                            #print(s[k])
                            #print(self.automatos[i].estados_finais[j])
                            
                            if (s[k] ==  self.automatos[i].estados_finais[j]):
                                #print("entrou")
                                padrao = self.automatos[i].def_re
                aux = (p + " " + padrao)
                self.tokens.append(aux)
        return(0)
    
    
    '''Escreve os tokens num arquivo de saída'''
    def output_token(self):
        out = open("lista_tokens.txt", "w")
        for i in range(0, len(self.tokens)):
            out.write(self.tokens[i])
            out.write("\n")
            
        out.close()
    
    
    ''' Imprime os uma tabela de transições de estados com os estado finais e seu tokens'''
    def imprimir_tab(self):
        states = []
        for l in range(0, len(self.automato_geral.transicoes)):
            
            if (self.automato_geral.transicoes[l][0] not in states):
                
                states.append(self.automato_geral.transicoes[l][0])
               
            if (self.automato_geral.transicoes[l][2] not in states):
                
                states.append(self.automato_geral.transicoes[l][2])
               
       
        
        
        for i in range(0, len(self.automato_geral.estados_finais)):
            for e in range(0, len(self.automato_geral.estados_finais[i])):
                padrao = ''
                for a in range(0, len(self.automatos)):
                    
                    for f in range(0, len(self.automatos[a].estados_finais)):
                        if (self.automato_geral.estados_finais[i][e] == self.automatos[a].estados_finais[f]):
                            padrao = self.automatos[a].def_re
                            estado_token = (self.automato_geral.estados_finais[i] , padrao)
                if (padrao != ''):
                    self.estado_tokens.append(estado_token)
        
        
        print(self.estado_tokens)
         
        
        
        
        tab = [[]]*(len(states)+1)
        for s in range(0, (len(states) + 1)):

            if(s == 0):
                tab[0] = ['|']
                for a in range(1, (len(self.automato_geral.alfabeto) + 1)):
                    #print(a)
                    tab[0].append(self.automato_geral.alfabeto[a-1])
            if(s > 0):


                tab[s] =  [str(states[s - 1])]

                for a in range(1, (len(self.automato_geral.alfabeto) + 1)):
                    found = 0
                    # print(str(a))

                    for t in range(0, len(self.automato_geral.transicoes)):
                        if(states[s-1] == self.automato_geral.transicoes[t][0]):
                            if(self.automato_geral.transicoes[t][1] == self.automato_geral.alfabeto[a-1]):
                                tab[s].append(str(self.automato_geral.transicoes[t][2]))
                                found = 1
                                break
                    if (found != 1):
                        tab[s].append('|')



        #print(tab)

        d = 25
        tam = 0
        for s in range(0, len(states) + 1):
            tam = max(0 , len("".join(tab[s])))


        for s in range(0, len(states) + 1):
            dif = tam - len("".join(tab[s]))
            print(((d + dif//(len(self.automato_geral.alfabeto)))*" ").join(tab[s]))
            
            
    def salvar_tabela(self):
        states = []
        for l in range(0, len(self.automato_geral.transicoes)):

            if (self.automato_geral.transicoes[l][0] not in states):
                states.append(self.automato_geral.transicoes[l][0])

            if (self.automato_geral.transicoes[l][2] not in states):
                states.append(self.automato_geral.transicoes[l][2])

        for i in range(0, len(self.automato_geral.estados_finais)):
            for e in range(0, len(self.automato_geral.estados_finais[i])):
                padrao = ''
                for a in range(0, len(self.automatos)):

                    for f in range(0, len(self.automatos[a].estados_finais)):
                        if (self.automato_geral.estados_finais[i][e] == self.automatos[a].estados_finais[f]):
                            padrao = self.automatos[a].def_re
                            estado_token = (self.automato_geral.estados_finais[i], padrao)

                if (padrao != ''):
                    self.estado_tokens.append(estado_token)

        with open("tabela_analise.txt", "w") as f:
            largura_maior_estado = max(len(state) for state in states)*4
            f.write(f"{'':<{largura_maior_estado}}")
            for simbolo in self.automato_geral.alfabeto:
                f.write(f"{simbolo:^{largura_maior_estado}}")
            f.write("\n")

            for state in states:
                for estado_token in self.estado_tokens:
                    if state in estado_token:
                        f.write(f"{str(estado_token[1]) + ' ' +  str(state):<{largura_maior_estado}}")
                        break
                else:
                    f.write(f"{str(state):<{largura_maior_estado}}")
                for simbolo in self.automato_geral.alfabeto:
                    for transicao in self.automato_geral.transicoes:
                        estado_atual, simbolo_trans, estado_final = transicao
                        if estado_atual == state:
                            if simbolo_trans == simbolo:
                                f.write(f"{str(estado_final):^{largura_maior_estado}}")
                f.write("\n")
        
            
        

def regex_from_read_file(name):
    res = []
    with open(name) as f:
        for line in f:
            def_re, raw_re = line.split(":")
            res.append(regularexpression.Regex(def_re, raw_re, res))
    return res





def main():
    regexs = regex_from_read_file("input/er6.txt")
    automatos = {}
    ats = []
    for regex in regexs:
        tree = syntaxtree.Tree(regex.add_end_of_regex_symbol(regex.re))
        dfa = automata.Automata(alfabeto=regex.alphabet)
        dfa.re2dfa(tree)
        dfa.def_re = regex.def_re
        automatos[regex.def_re] = dfa
    for k, v in automatos.items():
        v.escrever_arquivo("output/" + str(k) + ".txt")
    
    
    
    for k, v in automatos.items():
        ats.append(v)    
    
    #print(len(ats))
    '''for i in ats:
        i.imprimir_atributos()'''
       
   
    
    automato_unido = union.union(ats)
    
    #ats_teste[0].imprimir_atributos()
    #ats_teste[1].imprimir_atributos()
    
    #automato_unido.imprimir_atributos()
    
    automato_det = nfa_to_dfa.nfa_e_to_dfa(automato_unido)
    
    #automato_det.imprimir_atributos()
    
    
                       
    p_r =  ["begin", "end", ";", "if", "then", "while", "write", "(", ")"] # TABELA DE SIMBOLOS, PALAVRAS RESERVADAS
    arq = 'texto.txt'
    
    tabela = Tabela_Lexica(p_r, ats, automato_det, regexs)
    tabela.ler_texto(arq)
    if (tabela.gera_lista() == -1):
        print("Erro léxico")
        sys.exit(-1)
    print(tabela.tokens)
    tabela.output_token()
    tabela.salvar_tabela()
    #tabela.listar_Simbolos()
    #s = tabela.ler_palavra()
    #print(s)'''
    
    
    
    
    

if __name__ == "__main__":
    main()
