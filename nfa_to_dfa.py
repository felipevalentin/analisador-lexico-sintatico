from automata import Automata
#from union import rename_states

'''Função que recebe um estado, calcula seu fecho a partir das transições e coloca na lista de fecho'''
def calc_fecho(estado , transicoes, fecho):
    
    '''Coloca o própio estado no fecho se ele ainda não estiver'''
    if(estado not in fecho):
        fecho.append(estado)
    
    '''Para cada trasição verifia se é uma transição por &. Se for verifica se o estado de destino já está no fecho e se não tiver
    coloca no fecho o estado'''
    
    for i in range(0, len(transicoes)):
        if(transicoes[i][0] == estado and transicoes[i][1] == '&'):
            if(transicoes[i][2] not in fecho):
                fecho.append(transicoes[i][2])
                '''Calcula o fecho do novo estado achado'''
                calc_fecho(transicoes[i][2], transicoes, fecho)
                
                '''Para evitar fechos com mesmo estados mas com estados em posições diferente na lista colocamos eles sempre em ordem crescente'''
                fecho.sort() 
    

'''Função que calcula os novos estados'''
def calc_estado(estado, estados, e_fechos, transicoes_nfa, transicoes_dfa, alfabeto):
    
    '''print("")
    print("init")
    print(estado)
    print(estados)
    print(e_fechos)
    print(transicoes_nfa)
    print(transicoes_dfa)
    print(alfabeto)
    print("init")
    print("")'''
    
    ''' Para cada estado a e letra b, calcula a transição e o novo estado'''
    for b in range(0, len(alfabeto)):
        
        '''lista temporaria para guardar os estados que compõem o novo estado'''
        estado_temp = []
        
        if (alfabeto[b] == '&'):
            continue
        
        
        for a in range(0, len(estado)):           
            
            ''' Para cada transição c do estado a por b, verifica se o destino já esta em estado_temp. Se não estiver, coloca.'''
            for c in range(0, len(transicoes_nfa)):
                
                if(estado[a] == transicoes_nfa[c][0] and alfabeto[b] == transicoes_nfa[c][1]):
                    if(transicoes_nfa[c][2] not in estado_temp):
                        estado_temp.append(transicoes_nfa[c][2])
        ''' A partir de estado_temp, olha cada um dos fechos dos elementos de estado_temp. Se o elemento não estiver lá, ele é colocado.'''    
        for d in range(0, len(estado_temp)):            
            
            
            for e in range(0, len(e_fechos[estado_temp[d]][1])):               
                if(e_fechos[estado_temp[d]][1][e] not in estado_temp):
                    estado_temp.append(e_fechos[estado_temp[d]][1][e])
            
        '''Organiza temp para evitar redundancia'''   
        estado_temp.sort()
        
        
        '''print("")
        print("aqui")
        print(b)
        print(estado_temp)
        print("aqui")
        print("")'''
        
        '''Cria a transição do estado atual para o novo estado criado'''
        transicoes_dfa.append([estado, alfabeto[b] , estado_temp])
        
        '''Verifica se o novo estado já existe. Se não calcula os novos estados a partir dele'''
        if(estado_temp not in estados):
            estados.append(estado_temp)            
            calc_estado(estado_temp, estados, e_fechos, transicoes_nfa, transicoes_dfa, alfabeto)
            
            
        
    '''print("")    
    print("estados")
    print(estados)
    print("")'''
            
            
    
        
                        
                    
                   
                 

'''Função que converte um automato finito não deterministico nfa para um deterministuco dfa'''
def nfa_e_to_dfa(nfa):
    def_re = nfa.def_re
    alfabeto = nfa.alfabeto
    estado_inicial = []
    estados_finais = []
    transicoes = []
    estados = []
    e_fechos = []
    
    
    
    '''Calcula o e-fecho para cada um dos estados'''
    for i in range(0, nfa.numero_estados):
        fecho =  []
        calc_fecho(i, nfa.transicoes, fecho)        
        e_fechos.append([i, fecho])
        #print(e_fechos)
    
    estado_inicial = e_fechos[0][1]
    estados.append(e_fechos[0][1])
    
    
    
    calc_estado(estado_inicial , estados, e_fechos, nfa.transicoes, transicoes, alfabeto)
    
    
    '''Função para eliminar transições que são inuteis'''
    remove = []
    for k in range(0, len(transicoes)):
        if(transicoes[k][0] == [] or transicoes[k][1] == [] or transicoes[k][2] == []):
            remove.append(transicoes[k])
    for k in range(0, len(remove)):
        transicoes.remove(remove[k])
    
    remove = []
    for k in range(0, len(estados)):
        if(estados[k] == []):
            remove.append(estados[k])    
    for k in range(0, len(remove)):
        estados.remove(remove[k])
        
    '''for k in range(0, len(estados)):
        print(estados[k])'''
    
    
    '''Analisa os items que compões cada estado novo e verifica se algum dele era esado final. Depois coloca ess estado novo como final'''
    for k in range(0, len(nfa.estados_finais)):
        for j in range(0, len(estados)):
            if (nfa.estados_finais[k] in estados[j]):
                if (estados[j] not in estados_finais):
                    estados_finais.append(estados[j])
    #print(estados_finais)
    
    
        
    automato = Automata(def_re, len(estados), estado_inicial, estados_finais, alfabeto, transicoes)
    return automato
         
    
            
    
    
    
    

    
            
'''nfa1 =  Automata("nfa1", 3, 0, [2], ['a', 'b', 'c', '&'], [[0,'&',0], [0,'&',1], [0,'b',1], [0,'c', 2], [1,'a',0], [1,'b',2], [1,'c',0], [1,'c',1]])    
nfa2 =  Automata("nfa2", 5, 0, [1,2], ['a','b', '&'], [[0,'a',0],[0,'a',1],[0,'b',2],[0,'&',3],[1,'a',1],[1,'b',3],[1,'&',3],[2,'b',2],[2,'a',4],[3,'a',1],[3,'a',3],[3,'b',2],[3,'b',3],[3,'&',4],[4,'a',4],[4,'b',2],[4,'&',3]])
nfa3 =  Automata("nfa3", 3, 0, [0,1,2], ['0', '1', '2', '&'], [[0,'&',1], [0,'0',0], [1,'1',1], [1,'&',2],[2,'2',2]])
nfa4 =  Automata("nfa4", 4, 0, [3], ['a', 'b', 'c', 'd'], [[0,'a',0], [0,'&', 1], [0,'&',2],[1,'b', 1],[1,'b',3],[2,'c',2],[2,'c',3]])
dfa = nfa_e_to_dfa(nfa1)
#dfa = nfa_e_to_dfa(nfa2)
#dfa = nfa_e_to_dfa(nfa3)
#dfa = nfa_e_to_dfa(nfa4)
dfa.imprimir_atributos()'''


    
    