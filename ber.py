import serial
import sys
import traceback

PORT = 'COM6'
BAUDRATE = 2000000
TIMEOUT = 0.1
TRIALS = 10
N = 512
A = 'ABCDEFGHIJKLMNOP'*N

total_errors = 0
total_sent = 0

def send_and_receive():
    global total_sent
    global total_errors
    N0 = len(A)
    N1 = s.write(A)
    if N0 != N1: raise Exception('sent %d of %d octets' % (N1, N0))
    B = s.read(N1)
    N2 = len(B)
    if N1 != N2: raise Exception('received %d of %d octets' % (N2, N1))
    for a, b in zip(A, B):
        if a != b: total_errors += 1
    total_sent += N1
# Run the experiment.
try:
    s = serial.Serial(port=PORT,baudrate=BAUDRATE,timeout=TIMEOUT)
    s.flushInput()
    s.flushOutput()
    for i in xrange(TRIALS):
        send_and_receive()
except:
    traceback.print_exc(file=sys.stdout)
    print('failed on test %d of %d with N=%d' % (i+1, TRIALS, N))
finally:
    s.close()
# Compute BER.
ber = float(total_errors)/float(total_sent)
print('%d/%d = %f BER' % (total_errors,total_sent,ber))