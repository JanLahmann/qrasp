# Main controller for Qiskit on Raspberry PI SenseHat.

# Start by importing and simplifying required modules. 
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD
#from sense_emu import SenseHat
hat = SenseHat()
from time import sleep


# Understand which direction is down, and rotate the SenseHat display accordingly.
def set_display():
        acceleration = hat.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']
        x=round(x,0)
        y=round(y,0)
        z=round(z,0)
        if x == 1:
            hat.set_rotation(270)
        else:
            if x == -1:
                hat.set_rotation(90)
            else:
                if y == 1:
                    hat.set_rotation(0)
                else:
                    hat.set_rotation(180)

set_display()       

#Check if online
from urllib.request import urlopen

def internet_on():
    try:
        response = urlopen('https://www.google.com', timeout=10)
        return True
    except:
        return False

#Import Qiskit classes
from qiskit import IBMQ, execute
from qiskit import BasicAer as Aer #<-Workaround
from qiskit.providers.ibmq import least_busy
import Qconfig_IBMQ_experience
# from qiskit.tools.monitor import job_monitor

# If online, enable the account based on the stored API key
if internet_on():
    provider = IBMQ.enable_account(Qconfig_IBMQ_experience.APItoken)
else:
    hat.show_message("Offline mode")


# Set default SenseHat configuration.
hat.clear()
hat.low_light = True

def show_pic(name, pic):
    #global hat
    print(name)
    hat.set_pixels(pic)
    sleep(4)

# Background icon
X = [255, 0, 255]  # Magenta
Y = [255,192,203] # Pink
P = [255,255,0] #Yellow
O = [0, 0, 0]  # Black
B = [0,0,255] # Blue
#B = [70,107,176] # IBM Blue
W = [255, 255, 255] #White

super_position = [
O, O, O, Y, X, O, O, O,
O, O, Y, X, X, Y, O, O,
O, Y, O, O, X, O, Y, O,
O, Y, O, O, X, O, Y, O,
O, Y, O, O, X, O, Y, O,
O, Y, O, O, X, O, Y, O,
O, O, Y, O, X, Y, O, O,
O, O, O, X, X, X, O, O
]
show_pic("super_position", super_position)

IBMQ_super_position = [
O, O, O, Y, B, O, O, O,
O, O, Y, B, B, Y, O, O,
O, Y, O, O, B, O, Y, O,
O, Y, O, O, B, O, Y, O,
O, Y, O, O, B, O, Y, O,
O, Y, O, O, B, O, Y, O,
O, O, Y, O, B, Y, O, O,
O, O, O, B, B, B, O, O
]
show_pic("IBMQ_super_position", IBMQ_super_position)

IBM_Q = [
B, B, B, W, W, B, B, B,
B, B, W, B, B, W, B, B,
B, W, B, B, B, B, W, B,
P, P, P, B, B, B, W, B,
B, W, P, B, B, B, W, B,
P, P, P, B, B, W, B, B,
P, B, B, W, W, B, B, B,
P, P, P, W, W, W, B, B
]
show_pic("IBM_Q", IBM_Q)

IBM_Q_4 = [
B, B, B, W, W, B, B, B,
B, B, W, B, B, W, B, B,
B, W, B, B, B, B, W, B,
P, W, P, B, B, B, W, B,
P, W, P, B, B, B, W, B,
P, P, P, B, B, W, B, B,
B, B, P, W, W, B, B, B,
B, B, P, W, W, W, B, B
]
show_pic("IBM_Q_4", IBM_Q_4)

IBM_Q_B = [
B, B, B, W, W, B, B, B,
B, B, W, B, B, W, B, B,
B, W, B, B, B, B, W, B,
B, W, B, B, B, B, W, B,
B, W, B, B, B, B, W, B,
B, P, W, B, B, W, B, B,
P, P, P, W, W, B, B, B,
B, P, B, W, W, W, B, B
]
show_pic("IBM_Q_B", IBM_Q_B)

IBM_AER = [
O, O, W, W, W, W, O, O,
O, W, W, O, O, W, W, O,
W, W, W, O, O, W, W, W,
W, W, O, W, W, O, W, W,
W, W, O, O, O, O, W, W,
W, O, W, W, W, W, O, W,
O, W, O, O, O, O, W, O,
O, O, W, W, W, W, O, O
]
show_pic("IBM_AER", IBM_AER)         

# Function to set the backend
def set_backend(back):
    global backend
    if back == "ibmq_best" and internet_on():
        backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 3 
                                                        and not x.configuration().simulator
                                                        and x.status().operational==True))        
        hat.show_message(backend.name())
        hat.set_pixels(IBM_Q_B)
    else:
        backend = Aer.get_backend('qasm_simulator')
        hat.show_message(backend.name())
        hat.set_pixels(IBM_AER)
                
    
# Load the Qiskit function files. Showing messages when starting and when done.
hat.show_message("Qiskit")

import q2_calling_sense_func
import q3_calling_sense_func
import bell_calling_sense_func
import GHZ_calling_sense_func

# Initialize the backend to AER
back = "aer" 
set_backend(back)


# The main loop.
# Use the joystick to select and execute one of the Qiskit function files.
# see examples in https://pythonhosted.org/sense-hat/api/

def show_super_position(back):
    global hat, super_position, IBMQ_super_position 
    if back != "aer" and internet_on():
        hat.set_pixels(IBMQ_super_position)
    else:
        hat.set_pixels(super_position)

def pushed_up(event):
    global hat, backend, back
    if event.action == ACTION_PRESSED:
        print("Bell on ", back)
        hat.show_message("Bell")
        show_super_position(back)
        bell_calling_sense_func.execute(backend,back)
        hat.stick.get_events() # empty the event buffer

def pushed_down(event):
    global hat, backend, back
    if event.action == ACTION_PRESSED:
        print("GHZ on ", back)
        hat.show_message("GHZ")
        show_super_position(back)
        GHZ_calling_sense_func.execute(backend,back)
        hat.stick.get_events() # empty the event buffer

def pushed_left(event):
    global hat, backend, back
    if event.action == ACTION_PRESSED:
        print("2Q on ", back)
        hat.show_message("2Q")
        show_super_position(back)
        q2_calling_sense_func.execute(backend,back)
        hat.stick.get_events() # empty the event buffer

def pushed_right(event):
    global hat, backend, back
    if event.action == ACTION_PRESSED:
        print("3Q on ", back)
        hat.show_message("3Q")
        show_super_position(back)
        q3_calling_sense_func.execute(backend,back)
        hat.stick.get_events() # empty the event buffer

def pushed_middle(event):
    global hat, backend, back
    if event.action == ACTION_PRESSED:
        print("Middle ACTION_PRESSED")
        if back == "aer" and internet_on():
            print("Backend: Best")
            hat.show_message("Best")
            back = "ibmq_best"
        else:
            print("Backend: aer simulator")
            back = "aer"
        show_super_position(back)
        set_backend(back)
    else:
        if event.action == ACTION_HELD:
            print("Middle ACTION_HELD")
            quit()


hat.stick.get_events() # empty the event buffer
print("starting main loop")
while True:
    hat.stick.direction_up = pushed_up
    hat.stick.direction_down = pushed_down
    hat.stick.direction_left = pushed_left
    hat.stick.direction_right = pushed_right
    hat.stick.direction_middle = pushed_middle
