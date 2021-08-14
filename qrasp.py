# Main controller for Qiskit on Raspberry PI SenseHat.

# Import required modules.
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD
hat = SenseHat()
# Set default SenseHat configuration.
hat.clear()
hat.low_light = True

from time import sleep
import os
# Import the Raspberry PI SenseHat display function.
from qc_sensehat_func import SenseDisplay

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

# Check if online
from urllib.request import urlopen

def internet_on():
    try:
        response = urlopen('https://www.google.com', timeout=10)
        return True
    except:
        return False

# Import Qiskit classes
from qiskit import IBMQ, execute, QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import BasicAer
from qiskit.providers.ibmq import least_busy
import Qconfig_IBMQ_experience
# from qiskit.tools.monitor import job_monitor

# If online, enable the account based on the stored API key
if internet_on():
    # provider = IBMQ.enable_account(Qconfig_IBMQ_experience.APItoken)
    provider=IBMQ.load_account()
else:
    hat.show_message("Offline mode")

# display pics/logos on the SenseHAT
def show_pic(name, pic):
    print(name)
    hat.set_pixels(pic)
    sleep(1)

# Background icons
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
        print("Backend:", backend.name())
        hat.show_message(backend.name())
        hat.set_pixels(IBM_Q_B)
    else:
        backend = BasicAer.get_backend('qasm_simulator')
        print("Backend:", backend.name())
        hat.show_message(backend.name())
        hat.set_pixels(IBM_AER)
    hat.stick.get_events() # empty the event buffer

# Initialize the backend to AER
hat.show_message("Qiskit")
back = "aer" 
set_backend(back)

# Display logo for simulator or IBMQ 
def show_super_position(back):
    global hat, super_position, IBMQ_super_position 
    if back != "aer" and internet_on():
        hat.set_pixels(IBMQ_super_position)
    else:
        hat.set_pixels(super_position)
    sleep(1)

# Define the circuits
def bell_circuit(circuit, qr, cr):
    circuit.h(qr[0])
    circuit.cx(qr[0], qr[1])
    circuit.measure(qr[0], cr[0])
    circuit.measure(qr[1], cr[1])

def q2_circuit(circuit, qr, cr):
    circuit.h(qr[0])
    circuit.h(qr[1])
    circuit.measure(qr[0], cr[0])
    circuit.measure(qr[1], cr[1])    

def q3_circuit(circuit, qr, cr):
    circuit.h(qr[0])
    circuit.h(qr[1])
    circuit.h(qr[2])
    circuit.measure(qr[0], cr[0])
    circuit.measure(qr[1], cr[1])
    circuit.measure(qr[2], cr[2]) 

def GHZ_circuit(circuit, qr, cr):
    circuit.h(qr[0])
    circuit.cx(qr[0], qr[1])
    circuit.cx(qr[0], qr[2])
    circuit.measure(qr[0], cr[0])
    circuit.measure(qr[1], cr[1])
    circuit.measure(qr[2], cr[2])
    

# Build and execute the circuits, and display the results
def do_circuit(circuit_name, backend, back, hat):
    print(circuit_name, "on", back)
    hat.show_message(circuit_name)
    show_super_position(back)
    n = 2 # Set number of bits and number of shots
    if circuit_name == "3Q" or circuit_name == "GHZ":
        n=3
    sh = 1024 # Set number of number of shots
    qr = QuantumRegister(n) # Create a Quantum Register with n qubits
    cr = ClassicalRegister(n) # Create a Classical Register with n bits
    circuit = QuantumCircuit(qr, cr) # Create a Quantum Circuit acting on the qr and cr register
    
    # build the circuit
    if circuit_name == "Bell":
        bell_circuit(circuit, qr, cr)
    elif circuit_name == "2Q":
        q2_circuit(circuit, qr, cr)
    elif circuit_name == "3Q":
        q3_circuit(circuit, qr, cr)
    else:
        GHZ_circuit(circuit, qr, cr)

    # Create a Quantum Program for execution of the circuit on the selected backend
    job = execute(circuit, backend, shots=sh)
    result = job.result() # Get the result of the execution
    Qdictres = result.get_counts(circuit)
    
    print ("Results:", Qdictres) # Print the results
    # Display the quantum dictionary as a bar graph on the SenseHat 8x8 pixel display by calling the SenseDisplay function.
    SenseDisplay(Qdictres,n,back)

    hat.stick.get_events() # empty the event buffer


# The main loop.
# Use the joystick to select and execute one of the Qiskit function files.
# see examples in https://pythonhosted.org/sense-hat/api/

def pushed_up(event):
    global hat, backend, back
    if event.action == ACTION_PRESSED:
        circuit_name = "Bell"
        do_circuit(circuit_name, backend, back, hat)

def pushed_left(event):
    global hat, backend, back
    if event.action == ACTION_PRESSED:
        circuit_name = "2Q"
        do_circuit(circuit_name, backend, back, hat)
      
def pushed_right(event):
    global hat, backend, back
    if event.action == ACTION_PRESSED:
        circuit_name = "3Q"
        do_circuit(circuit_name, backend, back, hat)

def pushed_down(event):
    global hat, backend, back
    if event.action == ACTION_PRESSED:
        circuit_name = "GHZ"
        do_circuit(circuit_name, backend, back, hat)

import atexit, signal
def call_sense_menu():
    os.system("nohup /home/pi/.local/bin/rq_sense_menu_run.sh &")

def pushed_middle(event):
    global hat, backend, back
    event2 = hat.stick.wait_for_event()
    print("The joystick was {} {}".format(event2.action, event2.direction))
    if event2.action == ACTION_HELD:
        print("Middle ACTION_HELD")
        print("Exiting...")
        # option 1: exit the script
#        hat.show_message("Exiting...")
#        hat.clear()
#        os._exit(0)
        # option 2: shutdown raspberry
        hat.show_message("Shutdown...")
        hat.clear()
        os.system('sudo halt')
        # option 3: exit and start menu (DOES NOT WORK)
#        hat.show_message("Menu...")
#        hat.clear()
#        atexit.register(call_sense_menu)
#        os.kill(os.getpid(), signal.SIGINT)
#        cmd="sleep 2 && kill -INT " + str(os.getpid()) + "\n sleep 2 && kill -TERM " + str(os.getpid())
#        with open('cmd.sh', 'w') as f:
#            print(cmd, file=f)  
#        os.system("nohup sh cmd.sh &")
#        exit()
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

from signal import pause
hat.stick.get_events() # empty the event buffer
print("starting main loop")
hat.stick.direction_up = pushed_up
hat.stick.direction_down = pushed_down
hat.stick.direction_left = pushed_left
hat.stick.direction_right = pushed_right
hat.stick.direction_middle = pushed_middle
pause()
sleep(2)
os._exit(0)