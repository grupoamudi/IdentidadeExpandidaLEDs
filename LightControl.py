import time
import serial
import numpy as np
import threading


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

porta = serial.Serial('COM3', 9600)    # abre a porta. Atencao c o caminho!
t_inicial = time.time()                        # salva o tempo inicial pra contagem do tempo
f_lento   = 0.3 * 2 * np.pi                    # Frequencia da oscilacao lenta (estado "stand-by")
f_rapido  = 3 * 2 * np.pi                      # frequencia da oscilacao rapida (estado "leitura")
f_medio =  2 * np.pi
i_projecao = 50                                # intensidade luminosa durante a projeçao (estado "projeçao")
estado_anterior = 1                                     # estado inicial = 1 (standby), outros estados sao 2 (leitura) e 3 (projecao)

goToTransition = False

actual_value = 0
change_state = False
actual_thread = None


class Animation(threading.Thread):
        """Thread class with a stop() method. The thread itself has to check
        regularly for the stopped() condition."""

        actual_value = 0

        def __init__(self, porta):
            super(Animation, self).__init__()
            self._stop_event = threading.Event()
            self.porta = porta
            self.allow_continuation = False

        def stop(self):
            self._stop_event.set()

        def stopped(self):
            return self._stop_event.is_set()

        def sendValue(self,int_value):
            self.porta.write((str(int_value)+ '\n').encode('utf-8'))

        def easeInOutCubic(self,time, start_value, change_in_value, duration):
        	time = time/(duration/2)
        	if (time < 1):
                 return change_in_value/2*time*time*time + start_value
        	time -= 2
        	return change_in_value/2*(time*time*time + 2) + start_value

        def transition(self,from_value, to_value, steps = 10):
            for i in range(steps):
                self.sendValue(int(self.easeInOutCubic(i,from_value,from_value-to_value, steps)))







class AnimationReading(Animation):
    def __init__(self, porta):
        super().__init__(porta)

    def run(self):
        t_inicial = time.time()
        t = 0
        while True:
            valor = int((np.sin(f_medio*t- np.pi/2))*125+125)
            actual_value = valor
            super().sendValue(valor)
            t = time.time() - t_inicial
            if(t > 2):
                self.stop()
                break

class AnimationStandby(Animation):
    def __init__(self, porta):
        super().__init__(porta)

    def run(self):
        t_inicial = time.time()
        t = 0
        while not self.stopped():
            valor = int((np.sin(f_lento*t- np.pi/2))*25+50)
            super().sendValue(valor)
            t = time.time() - t_inicial


from socketIO_client import SocketIO
import subprocess

def on_state_change(newState):
    global actual_value, change_state, actual_thread
    print("Called on state change")
    if newState == 'startingDetection':
        change_state = True
        if actual_thread:
            actual_thread.stop()
            actual_thread.join()
        actual_thread = AnimationReading(porta)
        actual_thread.start()
    if newState == 'fingerDetected':
        #actual_thread.transition( 50, 200)
        if actual_thread:
            actual_thread.stop()
            actual_thread.join()

        actual_thread = AnimationStandby(porta)
        actual_thread.start()

socketIO = SocketIO('127.0.0.1',8000)
socketIO.on('stateChanged', on_state_change)
print("Light Control Started")
socketIO.wait()



#
# while True:      #laço que roda constantemente
#
#     #t = time.time() - t_inicial   #t e variavel de tempo
#
#     estado = verifica_estado(estado_anterior)
#
#     if(estado == 1):                       #Loop do estado 'stand-by'
#         valor = int((np.sin(f_lento*t) + 1 )*125)
#         porta.write(str(valor)+ '\n')
#         print valor
#         t = time.time() - t_inicial
#
#
#     if (estado == 2):                       # Loop do estado 'leitura'
#         animation_reading()
#
#
#     if (estado == 3):                     # Loop do estado 'projeçao'
#
#
#
#     #t_inicial = time.time()   # linha apenas para manter o teste em loop.
#     estado_anterior = estado
