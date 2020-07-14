                        #Project: Fever Detection and Alert System
#Import the Required Libraries

from boltiot import Sms,Bolt #Libraries required to connect with Bolt Wifi Module
import requests 
import json
import time

API_KEY = "xxxxxxxxxxxxxxx"   # Bolt API Key
DEVICE_ID = "xxxxxxxxxxxxxxx" # Bolt Device ID
SID = 'xxxxxxxxxxxxxxx' # Twilio Account SID
AUTH_TOKEN = 'xxxxxxxxxxxxxxx' #Twilio Auth Token
FROM_NUMBER = 'xxxxxxxxxxxxxxx' # Twilio Trial Number
TO_NUMBER = 'xxxxxxxxxxxxxxx' #Your own mobile number
threshold = 380                    


mybolt = Bolt(API_KEY,DEVICE_ID)
sms = Sms(SID, AUTH_TOKEN, TO_NUMBER, FROM_NUMBER)

#Function for reading sensor value from Bolt Wifi Module
def get_sensor_value_from_pin(pin): 
    """Returns the sensor value. Returns -999 if request fails"""
    try:
        response = mybolt.analogRead(pin)
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull")
            print("This is the response->", data)
            return -999
        sensor_value = int(data["value"])
        return sensor_value
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999
    

while True:
    print("*******************************")
    print("Loop Starting")
    mybolt.digitalWrite("2","HIGH") # Both buzzer and led will be 'ON' which  
    mybolt.digitalWrite("1","HIGH") # indicate that the loop has started and you
    time.sleep(0.5)                 # need to place the temperature sensor 
    mybolt.digitalWrite("2","LOW")  # between your arms
    mybolt.digitalWrite("1","LOW")
    print("Reading time 15 secs") # Read the temperature of your body for 15 sec
    time.sleep(15)
    sensor_value = get_sensor_value_from_pin("A0")
    print(sensor_value)
    
    if(sensor_value > threshold): # true, means the Person has fever
        print("Making request to Twilio to send a SMS")
        response = sms.send_sms("Alert! The Person has fever. Body temperure is" + "{:.2f}".format(sensor_value*100/1024) + "°C. Don't let him enter the House")#sending message
        print("Response received from Twilio is: " + str(sensor_value))
        mybolt.digitalWrite("2","HIGH") 
        time.sleep(4)                    # Buzzer will be 'ON' for 4 seconds
        mybolt.digitalWrite("2","LOW")
        
    # true, means the person is safe
    else: 
        print("Making request to Twilio to send a SMS")
        response = sms.send_sms("Don't worry, the Person is Safe. Body temperature is "+ "{:.2f}".format(sensor_value*100/1024) + "°C. You may let him enter the House")#sending message
        print("Response received from Twilio is: " + str(sensor_value))
        mybolt.digitalWrite("1","HIGH")
        time.sleep(4)                   # LED will GLOW for 4 seconds
        mybolt.digitalWrite("1","LOW")
        
        for _ in range(5): #buzzer will 'ON' and 'OFF' 5 times which indicate 
            mybolt.digitalWrite("2","HIGH") #that the loop is over
            time.sleep(0.5)
            mybolt.digitalWrite("2","LOW")
    print("next cycle will start in 5 secs") # next cycle to test next person
    print("*******************************")
    time.sleep(5)
