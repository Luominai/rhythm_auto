import cv2
import numpy
import mss
import time
import keyboard
from event_scheduler import EventScheduler

THRESHOLD = 150
delay = .32
on = False

columns = {
    1 : {
        "color" : 0,
        "active" : False,
        "key" : "a"
    },
    2 : {
        "color" : 0,
        "active" : False,
        "key" : "s"
    },
    3 : {
        "color" : 0,
        "active" : False,
        "key" : "k"
    },
    4 : {
        "color" : 0,
        "active" : False,
        "key" : "l"
    }
}

event_scheduler = EventScheduler()
# Starts the scheduler
event_scheduler.start()

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 600, "left": 720, "width": 480, "height": 100}
    # Image captured
    img = numpy.array(sct.grab(monitor))

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        cv2.imshow('OpenCV/Numpy grayscale', 
                   cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))
        
        # update pixels
        columns[1]["color"] = img[0][60][0]
        columns[2]["color"] = img[0][180][0]
        columns[3]["color"] = img[0][300][0]
        columns[4]["color"] = img[0][420][0]
        
        if(on):
            for colNum, pixel in columns.items():
                # if pixel color is greater than threshold, switch the active value to true if not already
                if pixel["color"] > THRESHOLD and not pixel["active"]:
                    pixel["active"] = True
                    event_scheduler.enter(delay, 1, keyboard.press, pixel['key']) # start a key press at the beginning of the note
                # if pixel color is less than threshold, deactivate
                if pixel["color"] < THRESHOLD and pixel["active"]:
                    pixel["active"] = False
                    event_scheduler.enter(delay, 1, keyboard.release, pixel['key']) # stop the key press at the end of the note

        key = cv2.waitKey(10)
        # Press "q" to quit
        if key == ord("q"):
            cv2.destroyAllWindows()
            event_scheduler.stop()
            break

        # Press "o" to increase delay
        if key == ord("o"):
            delay += .01
            print(delay)

        # Press "i" to decrease delay
        if key == ord("i"):
            delay -= .01
            print(delay)

        # Press "m" to toggle
        if key == ord("m"):
            on = not on
            print(on)