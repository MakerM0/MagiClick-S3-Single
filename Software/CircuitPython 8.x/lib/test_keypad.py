import board
import keypad


km = keypad.KeyMatrix(
    row_pins=(board.GP22,board.GP23,board.GP24,board.GP25),
    column_pins = (board.GP10,board.GP11,board.GP12,board.GP13,board.GP14,board.GP15,board.GP16,board.GP28,board.GP27,board.GP26)
    )


# 按键map的序号，从左到右，从上到下

PPC_KEYMAP=(30,31,32,33,34,35,36,37,38,39,
            20,21,22,23,24,25,26,27,28,29,
            10,11,12,13,14,15,16,17,18,19,
            0,1,2,3,4,5,6,7,8,9 )


PPC_KEY_NAMES=(
               "q","w","e","r","t","y","u","i","o","p",
               "a","s","d","f","g","h","j","k","l","DEL",
               "ALT","z","x","c","v","b","n","m","UP","ENTER",
               "SHIFT","_","=","("," ",".",")","LEFT","DOWN","RIGHT"
    
    )

PPC_KEY_NAMES_CAPS=(
               "Q","W","E","R","T","Y","U","I","O","P",
               "A","S","D","F","G","H","J","K","L","DEL",
               "ALT","Z","X","C","V","B","N","M","UP","ENTER",
               "SHIFT","_","=","("," ",".",")","LEFT","DOWN","RIGHT"
    
    )

PPC_KEY_NAMES_ALT=(
               "#","1","2","3","+","-","/","\\",":",";",
               "*","4","5","6","%","@","`","'",'"',"DEL",
               "ALT","7","8","9","~","!","&","?","^","ENTER",
               "SHIFT","|","0","["," ",",","]","<","$",">"
    
    )



# Create an event we will reuse over and over.
event = keypad.Event()
 
while True:
    if km.events.get_into(event):
#         print(event)
        if event.pressed :
            print(event.key_number)
            if event.key_number in PPC_KEYMAP:
                index = PPC_KEYMAP.index(event.key_number)
                print(PPC_KEY_NAMES[index])     

        
         
 
                 
                 
                 
                 
                 
                 
                 