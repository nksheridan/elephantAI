import time
import picamera
import datetime
import RPi.GPIO as GPIO

def CheckPIR():
    # dependencies are RPi.GPIO and time
    # returns PIR_IS with either 0 or 1 depending if high or low
    time.sleep(1)
    #don't rush the PIR!
    GPIO.setmode(GPIO.BOARD)
    # set numbering system for GPIO PINs are BOARD
    GPIO.setup(7, GPIO.IN)
    # set up number 7 PIN for input from the PIR
    # need to adjust if you connected PIR to another GPIO PIN
    try:
        val = GPIO.input(7)
        if (val == True):
            PIR_IS = 1
            #PIR returned HIGH to GPIO PIN, so something here!
        if (val == False):
            PIR_IS = 0
            #PIR returned LOW to GPIO PIN, so something here!
            GPIO.cleanup()

    except:
        GPIO.cleanup()

    return PIR_IS
   


PIR = 1
count = 0


while True:
    PIR = 0
    #Now to check the PIR and send what it returns to PIR
    PIR = CheckPIR()
    if PIR == 0:
        print("Nothing has been detected by PIR")
    elif PIR == 1:
        print("Something has been seen! Time to photograph it!")
        i = 0
        with picamera.PiCamera() as camera:
            while i < 5:
                i = i+1
                print(i)
                camera.start_preview()
                time.sleep(1)
                utc_datetime = datetime.datetime.utcnow()
                utc_datetime.strftime("%Y-%m-%d-%H%MZ")
                #get date and time so we can append it to the image filename
                camera.capture('image_'+str(utc_datetime)+'.jpg')
                camera.stop_preview()
                time.sleep(1)
                if i == 5:
                    break
            

        
