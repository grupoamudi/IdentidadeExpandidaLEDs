import time
import serial
import numpy as np

'''
Esse codigo serve para enviar valores de 0 a 255 pela por serial. 

O arduino nela conectada tem um código apenas para ler o valor da 
porta e escreve-lo na saida PWM com a função analogWrite(valor).

E importante enviar o \n pra rapida leitura do arduino e tb manter 
o fluxo constante de envios de valores pela porta serial mesmo quando 
o valor e constante. 
A variavel 'valor' deve ser sempre int, qdo float 
a comunicacao se atrapalha e interpreta a aprte fracionaria como um 
segundo numero.
'''

# FALTA FAZER A LEITURA DE ESTADOS ! 
# (Atualemnte ele roda os tres estados sequencialmente)
# Nesse caso, e so substituir os laços 'while' pela verificaçao do 
# estado e escolher qual 'valor' deve ser enviado. 

# FALTA CALIBRAR VALORES DE FREQUENCIA DE OSCILAÇAO E INTENSIDADE 
# LUMINOSA (apesar de gostar dos valores que estao aqui).


porta = serial.Serial('/dev/ttyUSB1', 9600)    # abre a porta. Atencao c o caminho!
t_inicial = time.time()                        # salva o tempo inicial pra contagem do tempo
f_lento   = 0.3 * 2 * np.pi                    # Frequencia da oscilacao lenta (estado "stand-by")
f_rapido  = 3 * 2 * np.pi                      # frequencia da oscilacao rapida (estado "leitura")
i_projecao = 50                                # intensidade luminosa durante a projeçao (estado "projeçao")
estado_anterior = 1                                     # estado inicial = 1 (standby), outros estados s�o 2 (leitura) e 3 (projecao) 

def verifica_estado():

    #Checa se imagem mudou, se nao mudou esta em standby
    #

    return 1



while True:      #laço que roda constantemente 

    #t = time.time() - t_inicial   #t e variavel de tempo

    estado = verifica_estado(estado_anterior)
    
    if(estado == 1):                       #Loop do estado 'stand-by'   
        valor = int((np.sin(f_lento*t) + 1 )*125)
        porta.write(str(valor)+ '\n') 
        print valor
        t = time.time() - t_inicial


    if (estado == 2):                       # Loop do estado 'leitura'
        valor = int((np.sin(f_rapido*t) + 1 )*125)
        porta.write(str(valor)+ '\n') 
        print valor
        t = time.time() - t_inicial


    if (estado == 3):                     # Loop do estado 'projeçao'
        valor = int(i_projecao)
        porta.write(str(valor) + '\n')
        print valor
        print t
        t = time.time() - t_inicial


    #t_inicial = time.time()   # linha apenas para manter o teste em loop. 
    estado_anterior = estado
