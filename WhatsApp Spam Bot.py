import os
#You will have 10 seconds to open WhatsApp and place cursor to the typing area.
#You can change sleep time in the python program. ( Do at your own risk )


# Check if libraries are installed, and install if necessary.
required_libraries = ['pyautogui', 'time']
for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        print(f'{library} not found, Installing {library}....')
        os.system(f'pip install {library}')
        
        
import pyautogui as pt
import time

print("Proqramın istifadə qaydası:")
print(" \n 1.'Limit' və 'mesaj' -ı daxil etdikdən sonra, WhatsApp -ı açaraq kursoru yazı hissəsinə yerləşdirmək üçün 10 saniyə vaxtınız olacaq. ")
print(" 1. Ilk açılan - 'Limiti daxil edin' bölməsinə, mesajın neçə dəfə göndərilməsini istədiyinizi daxil edib 'Enter' düyməsinə basın" )
print(" 2. Ikinci açılan - 'Mesajı daxil edin' bölməsinə, göndərilməsini istədiyiniz mesajı daxil edib, 'Enter' düyməsinə basın.")
print(" 3. Artıq 10 saniyə ərzində kursoru mesaj bölməsinə yerləşdirə bilərsiniz")
print("_____________________________________________________________________________________________________________________________________")


limit = input ("\nLimiti daxil edin: ")
message = input ("Mesajı daxil edin: ")

i = 0
time.sleep(10)

while i < int(limit):
    pt.typewrite(message)
    pt.press("enter")
    
    i+=1

input("Başqa bir hücum etmək üçün ENTER klikləyin ")