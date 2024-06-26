import evdev
from evdev import ecodes, categorize
import requests

previous_text = ''
current_text = ''
entryDoorId = '117'
placeName = 'Concasa - Monte Alto'

def read_events(device_path):
    dev = evdev.InputDevice(device_path)
    dev.grab()

    scancodes = { 
        # Scancode: ASCIICode 
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8', 
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r', 
        20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL', 
        30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';', 
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n', 
        50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT', 
        79: u'1', 80: u'2', 81: u'3', 75: u'4', 76: u'5', 
        77: u'6', 71: u'7', 72: u'8', 73: u'9', 82: u'0',
    } 

    caps_codes = { 
        0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*', 
        10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R', 
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL', 
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':', 
        40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N', 
        50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT' 
    } 

    caps = False
    global previous_text 
    current_text = ''

    for event in dev.read_loop(): 
        if event.type == ecodes.EV_KEY: 
            data = categorize(event)
            if data.scancode == 42: 
                if data.keystate == 1: 
                    caps = True 
                if data.keystate == 0: 
                    caps = False 
            if data.keystate == 1: # Down events only 
                if caps: 
                    key_lookup = u'{}'.format(caps_codes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) 
                else: 
                    key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) 
                if (data.scancode != 42) and (data.scancode != 28) and (key_lookup != 'None') and (data.scancode != 15): 
                    current_text += key_lookup 
                if(data.scancode == 15): 
                    if current_text != previous_text:
                        previous_text = current_text
                        return current_text
                    return 'SAME CODE'

def keylogger(device_path='/dev/input/event0'):
    return read_events(device_path)

# Para usar la función:
while True:
    result = keylogger()
    if result and result != 'SAME CODE':
        fullQrTextArray = result.split("=")
        if len(fullQrTextArray)==2:
            aditumData = fullQrTextArray[1]
            aditumQrVerifying = fullQrTextArray[0]
            if(aditumQrVerifying=="ADITUMGATE"):
                if "EXIT" in result:
                    print("es de salida")
                else:
                    print(aditumData)
                    r = requests.get('https://app.aditumcr.com/api/aditum-gate-verifier-entry/'+aditumData+'/'+entryDoorId) 
                    print("encontrado")
        print(result)  # Esto imprimirá solo si hay un cambio en el texto capturado
