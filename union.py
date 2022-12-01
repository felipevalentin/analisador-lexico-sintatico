from automata import Automata
from nfa_to_dfa import *

                
'''Função que recebe uma lista ats de automatos e renomeia os ids dos estados de cada automato em ordem crescente começando de 1'''
def rename_states(ats): 
    
    index = 0
    
    '''Vasculha as transições e coloca os estados id de estado na lista states'''
    for i in range(0, len(ats)):
        states = []
        for l in range(0, len(ats[i].transicoes)):
            if (ats[i].transicoes[l][0] not in states):
                states.append(ats[i].transicoes[l][0])
            if (ats[i].transicoes[l][2] not in states):
                states.append(ats[i].transicoes[l][2])
    
        
        
        ''' A partir de states, procura cada valor dele nos atributos respectivos de id de estado e se achar iguais, substitui por index'''
        for s in range(0, len(states)):
            if (ats[i].estado_inicial == states[s]):
                ats[i].estado_inicial = index
            
            for l in range(0, len(ats[i].estados_finais)):
                if (ats[i].estados_finais[l] == states[s]):
                    ats[i].estados_finais[l] = index
            
            for l in range(0, len(ats[i].transicoes)):                             
                if (ats[i].transicoes[l][0] == states[s]):
                    ats[i].transicoes[l][0] = index
                if (ats[i].transicoes[l][2] == states[s]):
                    ats[i].transicoes[l][2] = index
            index = index + 1
    
               
                
    ''' Soma 1 a cada identificador de estado '''
    for i in range(0, len(ats)):
        ats[i].estado_inicial = ats[i].estado_inicial + 1
        for l in range(0, len(ats[i].estados_finais)):            
            ats[i].estados_finais[l] = ats[i].estados_finais[l] + 1
        for l in range(0, len(ats[i].transicoes)):            
            ats[i].transicoes[l][0] = ats[i].transicoes[l][0] + 1
            ats[i].transicoes[l][2] = ats[i].transicoes[l][2] + 1   
           
        '''print(ats[i].estado_inicial)
        print(ats[i].estados_finais)
        print(ats[i].transicoes)
        print("\n")'''
    print(index)
    return(index)
''' Faz a união por epsilon(&) dos automatos no vetor ats'''
def union(ats):
    
    def_re_= "uniao"
    num_estados_ = 0
    estado_inicial_ = 0
    estados_finais_ = []
    transicoes_ = []
    alfabeto_ = ['&']
    
    num_estados_ = rename_states(ats)
    
    for a in range(0, len(ats)):
        '''Soma os nuemros de estados dos automatos'''
        #num_estados_ = num_estados_ + ats[a].numero_estados
        
        
        '''Coloca todas os simbolos do alfabetos automatos'''
        for s in range(0, len(ats[a].alfabeto)):
            if(ats[a].alfabeto[s] not in alfabeto_):
                alfabeto_.append(ats[a].alfabeto[s])
        
        '''Reune todos os estados finais'''
        for f in range(0, len(ats[a].estados_finais)):
            if(ats[a].estados_finais[f] not in estados_finais_):
                estados_finais_.append(ats[a].estados_finais[f])        
        
        '''Cria a primeira transição do estado zero por epsilon para cada automato a'''
        transicoes_.append([0,'&', ats[a].estado_inicial])
        
        '''Coloca todas as transições dos automatos na mesma lista'''
        for t in range(0, len(ats[a].transicoes)):
            transicoes_.append(ats[a].transicoes[t])
        
    '''    
    print("União")
    print(estados_finais_)        
    print(transicoes_)
    print(alfabeto_)
    print(num_estados_ + 1)'''
    
    '''Cria o automato geral não deterministico'''
    automatos_unidos = Automata(def_re_, num_estados_ + 1, estado_inicial_, estados_finais_, alfabeto_, transicoes_)
    #automatos_unidos.imprimir_atributos()
    
    return automatos_unidos
            
    

'''dfa1 = Automata ("dfa1", 3, 0,[1,2],['a','b'],[[0,'a',1],[0,'b',2]])
dfa2 = Automata ("dfa2", 3, 0,[0,1,2],['a','c'],[[0,'a',1],[0,'c',2],[1,'a',1],[1,'c',2], [2,'c',2]])
dfa3 = Automata ("dfa3", 4, 0,[1,2,3],['0','1','2'],[[0,'1',1],[0,'2',2],[0,'3',3], [1,'1',1],[2,'2',2],[3,'3',3]])
dfa4 = Automata ("dfa4", 4, 'a',['b','c','d'],['0','1','2'],[['a','1','b'],['a','2','c'],['a','3','d'], ['b','1','b'],['c','2','c'],['d','3','d']])
ats_ = []
ats_.append(dfa1)
ats_.append(dfa2)
#ats_.append(dfa3)
#ats_.append(dfa4)
nfa = union(ats_)
nfd = nfa_e_to_dfa(nfa)
nfd.imprimir_atributos()'''
