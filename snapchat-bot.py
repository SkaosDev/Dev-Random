import mouse
from time import *

a = int(input('Combien de fois ?'))

sleep(5)

photo_btn = (0,0)
snap_btn = (0,0)
share_btn = (0,0)

print("Photo")
sleep(5)
photo_btn = mouse.get_position()
print(photo_btn)

print("Snap")
sleep(5)
snap_btn = mouse.get_position()
print(snap_btn)

print("Share")
sleep(5)
share_btn = mouse.get_position()
print(share_btn)

sleep(5)
print("Start")
for i in range(a):
    mouse.move(photo_btn[0], photo_btn[1], True)
    mouse.press()
    mouse.release()
    sleep(3)
    mouse.move(snap_btn[0], snap_btn[1], True)
    mouse.press()
    mouse.release()
    sleep(2)
    mouse.move(share_btn[0], share_btn[1], True)
    mouse.press()
    mouse.release()
    sleep(2)
    print(i+1)