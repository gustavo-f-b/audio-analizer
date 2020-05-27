import pyaudio
import numpy
import math
import matplotlib.pyplot as plt
import matplotlib.animation

RATE = 44100
BUFFER = 882

p = pyaudio.PyAudio()

stream = p.open(
    format = pyaudio.paFloat32,
    channels = 1,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = BUFFER
)

fig = plt.figure()
rascunho = plt.plot([],[])[0]
line2 = plt.plot([],[])[0]

#range( [start], stop[, step] )
"""
        start - início da sequência
        stop - último elemento da sequência
        step - intervalo entre os elementos
"""

r = range(0, int(RATE/2+1), int(RATE/BUFFER))   #range( [start], stop[, step] )
"""
        start - início da sequência
        stop - último elemento da sequência
        step - intervalo entre os elementos
"""
l = len(r)

# for n in r:
#   print(n)

def init_line():
    #Define os eixos X e Y
        """
            [-1000]*l multiplica o -1000 l vezes, exemplo:
            
                    [-1000]*3 = [-1000, -1000, -1000]
        """

        """Linha azul"""
        rascunho.set_data(r, [-1000]*l) 
        
        """Linha laranja"""
        line2.set_data(r, [-1000]*l)

        return(rascunho,line2,)

def update_line(i):
    try:
        data = numpy.fft.rfft(numpy.fromstring(stream.read(BUFFER), dtype=numpy.float32))
    except IOError:
        pass
    
    data = numpy.log10(numpy.sqrt(numpy.real(data)**2+numpy.imag(data)**2) / BUFFER) * 10 
    
    rascunho.set_data(r, data)
    

    """
        Define X e Y da linha laranja como o X e Y máximo da última atualização do gráfico rascunho
    """
    line2.set_data(numpy.maximum(rascunho.get_data(), line2.get_data()))
    
    return (rascunho, line2,) 
    # return (lin,)e2

# print(data)
plt.xlim(0, RATE/2+1)
plt.ylim(-60, 0)
plt.xlabel('Frequência')
plt.ylabel('dB')
plt.title('Espectro')
plt.grid()


"""
    animation.FuncAnimation(fig, func, frames=None, init_func=None, fargs=None, save_count=None, *, cache_frame_data=True, **kwargs)]
    fig: a figura que é usada para desenhar 
    init_func: uma função usada para desenhar um frame(quadro) limpo
    inteval: intervalo entre os frames em milissegundos, por padrão interval = 200
"""
line_ani = matplotlib.animation.FuncAnimation(fig, update_line, init_func=init_line, interval=0, blit=True)

plt.show()
