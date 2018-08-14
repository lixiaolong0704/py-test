import requests
import threading
import time
# r = requests.get('https://api.github.com/events')
# print(r.text)

def test():
    print('Before: %s' % time.ctime())
    num = input('How long to wait: ')
    print 'start shit'
    # time.sleep(1000)
    print('After: %s\n' % time.ctime())
    print 'shit'


def sleeper():
    while True:
        # Get user input
        num = raw_input('How long to wait: ')

        # Try to convert it to a float
        try:
            num = float(num)
        except ValueError:
            print('Please enter in a number.\n')
            continue

        # Run our time.sleep() command,
        # and show the before and after time
        print('Before: %s' % time.ctime())
        time.sleep(num)
        print('After: %s\n' % time.ctime())
try:
    sleeper()
except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Exiting.')
    exit()
