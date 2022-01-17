import PySimpleGUI as sg
from random import randint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import struct as st
import serial
import time

# def get_data(x_ax, y1_ax, i, lines, fig_agg):
#     ser = serial.Serial(port = "COM7", baudrate = 115200)
#     ser.reset_input_buffer()
#     graph_data = ser.read()
#     y=unpack('?',graph_data)
#     print(y)
#     print(y[0])
#     print(y[0] == True)
#     plot_y = y[0]
#     # print ("unpacked " + plot_y)
#     if plot_y == True:
#         plot_y = 1
#         # print('set ' + plot_y)
#     else:
#         plot_y = 0
#         # print('set ' + plot_y)
#     print(plot_y)
#     if len(y1_ax) < 100:
#         x_ax.append(i*0.01)
#         y1_ax.append(plot_y)
#     else:
#         y1_ax[0:99] = y1_ax[1:100]
#         x_ax[0:99] = x_ax[1:100]
    
#     lines.set_xdata(x_ax)
#     lines.set_ydata(y1_ax)
#     fig_agg.draw()


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def create_plot(window):
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.grid()
    fig_agg = draw_figure(canvas, fig)
    return ax, fig_agg

def update(window, values, ax, fig_agg, event, flag, layout):
    x_ax = []
    atr_ax = []
    vent_ax = []
    t = time.time()
    if (flag == 0):
        ax, fig_agg = create_plot(window)
        flag = 1
    i = 0
    # print("test")
    try:
        ser = serial.Serial(port = "COM11", baudrate = 115200, bytesize = 8, parity = serial.PARITY_ODD, stopbits = serial.STOPBITS_ONE)
        # ser.flushInput()
    except (serial.SerialException):
        window[f'-COL{layout}-'].update(visible=False)
        layout = 3
        window[f'-COL{layout}-'].update(visible=True)
        return layout
    while True:
        event, values = window.read(timeout=10)
        # print(values["-atrial-"])
        if event == "Exit Egram":
            ser.close()
            window[f'-COL{layout}-'].update(visible=False)
            layout = 3
            window[f'-COL{layout}-'].update(visible=True)
            return layout
            break
        ax.cla()                    # clear the subplot
        ax.grid()                   # draw the grid
        # while (ser.inWaiting) !=  16:
        #     if ser.inWaiting() == 16:
        #         break
       
        try:
            # ser.flushInput()
            graph_data = ser.read(16)
        except (serial.SerialException):
            ser.close()
            window[f'-COL{layout}-'].update(visible=False)
            layout = 3
            window[f'-COL{layout}-'].update(visible=True)
            return layout
        atr=st.unpack('<d',graph_data[0:8])[0]
        vent=st.unpack('<d',graph_data[8:16])[0]
        print(atr)
        # plot_y = y[0]
        # print ("unpacked " + plot_y)
        # if plot_y == True:
        #     plot_y = 1
        #     # print('set ' + plot_y)
        # else:
        #     plot_y = 0
            # print('set ' + plot_y)
        # print(plot_y)
        
        
        if len(x_ax) < 100:
            x_ax.append((time.time()-t)*1000)
            atr_ax.append(atr*1000)
            vent_ax.append(vent*1000)
        else:
            atr_ax[0:99] = atr_ax[1:100]
            vent_ax[0:99] = vent_ax[1:100]
            x_ax[0:99] = x_ax[1:100]
            atr_ax[99] = atr*1000
            vent_ax[99] = vent*1000
            x_ax[99] = (time.time()-t)*1000
        # print(values["-atrial-"], " ", values["-vent-"])
        if (values["-atrial-"] == True):
            ax.plot(x_ax, atr_ax, label = "Atrium", color = 'red')
        if (values["-vent-"] == True):
           ax.plot(x_ax, vent_ax, label = "Ventricle", color = 'blue')
        ax.legend(loc="upper left")
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Voltage (mV)")
        fig_agg.draw()
        i+= 1
    #unpack("=HH4BH3BHH3BHBB", self._conn.read(24))
