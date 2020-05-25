
import pyaudio
import numpy
import math
import matplotlib.pyplot as plt
import matplotlib.animation

RATE = 44100
BUFFER = 882

p = pyaudio.PyAudio()

stream = p.open(
    format = pyaudio.paUInt8,
    channels = 1,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = BUFFER
)


fig = plt.figure()
rascunho = plt.plot([],[])[0]


r = range(0, int(RATE), int(RATE/BUFFER))   #range( [start], stop[, step] )
l = len(r)


# data = numpy.fromstring(stream.read(BUFFER), dtype=numpy.uint8)

# print(len(data))

# print(len(r))

def init_line():
    #Define os eixos X e Y"
        # rascunho.clear()
        rascunho.set_data(r,[-100]*l)
        
        return(rascunho,)

def update_line(i):
    data = numpy.fromstring(stream.read(BUFFER), dtype=numpy.uint8)
    rascunho.set_data(r,data)
    
    return (rascunho,) 

plt.xlim(0, RATE/2+1)
plt.ylim(0, 255)
plt.xlabel('Frequência')
plt.ylabel('Amplitudemo ')
plt.title('Forma de onda')
plt.grid()



line_ani = matplotlib.animation.FuncAnimation(fig, update_line, init_func=init_line, interval=0, blit=True)

plt.show()
