                                           SOURCE CODE

TEAM ID : PNT2022TMID24018
PROJECT : SIGNS WITH SMART CONNECTIVITY FOR BETTER ROAD SAFETY
DATE : 16/11/2022


#OPENWEATHER MAP(SPRINT 2)-{REQUIREMENT 1 OF THE PROJECT TO GET WEATHER DATA}
#TRAFFIC AND FATAL SITUATION ALERT BY ROADSAFETY CONTROL OFFICE(SPRINT 3) - {REQUIREMENT 2 OF THE PROJECT TO DISPLAY THE ALERT AND DIVERSION MESSAGE THAT WAS FROM ROAD SAFETY OFFICE
#HOSPITAL,SCHOOL AND PEOPLE CROWDED AREA LIKE RESTAURANT SIGNS DISPLAYED SPEED RECOMMENDATION ARE PROVIDED(SPRINT 4) - {REQUIREMENT 3 0F THE PROJECT TO DISPLAY HOSPITAL AND SCHOOL REGION BY THE ROAD SAFETY CONTROL OFFICE}


import wiotp.sdk.device  #importing library files for connecting with CLOUD,sdk=software developement kit
import requests  #for API request
import json  #converting it to json(key:values)
import sys

myConfig = { 
    "identity": {
        "orgId": "7f5hee",
        "typeId": "testdevicetype",     #configuration wit CLOUD,finding identity
        "deviceId":"12345"
    },
    "auth": {
        "token": "AQCLi6rYJrcoiDpW6?"   #authenticating with cloud device
    }
}
#TRAFFIC AND FATAL SITUATION ALERT MESSAGE DISPLAYING IN WEB UI WHWN THE 
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)     #initialising device client with above myconfig detail  
client.connect()

ALERT=""
NOTIFY=""
def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
        #THIS IF COMDITION BLOCK IS FOR TRAFFIC AND FATAL SITUATION ALERT MESSAGE DISPLAYING IN WEB UI WHEN THE MESSAGE WAS RECEIVED FROM THE ROAD SAFETY OFFICE 
    ALERT=""
    NOTIFY=""
    if(m=="TRAFFIC"):
        
        ALERT="TRAFFIC - PLEASE WAIT OR PREFER ANOTHER ROUTE"
        print("*****///PLEASE WAIT OR PREFER ANOTHER ROUTE///*****")
        
    elif(m=="ACCIDENT"):
        ALERT="ACCIDENT - TAKE DIVERSION"
        print("*****///TAKE DIVERSION///*****")
    elif(m=="MESSAGE"):
        ALERT="HAVE A NICE DAY!"
        print("HAVE A NICE DAY!")

        #THE BELOW CONDITION BLOCK IS TO DISPLAY HOSPITAL ,SCHOOL, AND RESTAURANT REGIONED AREA AND SPEED RECOMMENDATION  
    if(m=="SCHOOL"):                                                       
        NOTIFY="SCHOOL REGION MAINTAIN SPEED LIMIT BELOW 40KM/HR"
        print("SCHOOL REGION MAINTAIN SPEED LIMIT BELOW 40KM/HR")    
    elif(m=="HOSPITAL"):
        NOTIFY="HOSPITAL REGION DONT USE HORN"
        print("HOSPITAL REGION DONT USE HORN")
    elif(m=="RESTAURANT"):
        NOTIFY="CROWDED AREA PLEASE MAINTAIN SPEED LIMIT BELOW 40KM/HR"
        print("CROWDED AREA PLEASE MAINTAIN SPEED LIMIT BELOW 40KM/HR")
    mydata1={}   
    if(m=="TRAFFIC" or m=="ACCIDENT" or m=="MESSAGE"):
        mydata1={"SITUATION":ALERT}
    elif(m=="SCHOOL"or m=="HOSPITAL" or m=="RESTAURANT" ):
        mydata1={"CAUTION":NOTIFY}
        
        
    
    client.publishEvent("12345","json",mydata1)
        
     

while True:
    print("======================================")
    AREA = "Chennai,%20IN"
    weatherData = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + AREA + "&appid=b966927276060e981c650a5ca4409f8b&units=metric")
    a=weatherData.text
    b=json.loads(a)
    temp = b["main"]["temp"]
    humi = b["main"]["humidity"]
    main = b["weather"][0]["main"]      #0th index is taken from the object
    description = b["weather"][0]["description"]
    visibility = b["visibility"]
    Windspeed = b["wind"]["speed"]

    
    

    TemperatureRecommendation =""
    SpeedRecommendation = ""
    RecommendationForVisibilty = ""
    
    #print("Temperature(celcius) :",b["main"]["temp"])
    if (temp>33):
        TemperatureRecommendation="Temperature is higher than ideal value"
        #print("Temperature is higher than ideal value")
    elif (temp<19):
        TemperatureRecommendation="Temperature is lower than ideal value"
        #print("Temperature is lower than ideal value")
    else:
        TemperatureRecommendation="Temperature is ideal"
        #print("Temperature is ideal ")
        
    #print("Humidity :",b["main"]["humidity"])
    #print("WeatherCondition",(b["weather"][0]["main"]))
    if (main == "Rain"):
        rain = b["rain"]["1h"]
        SpeedRecommendation = "30KM/HR ,ROAD WILL BE SLIPPERY"
        #print("Rain:",b["rain"]["1h"])
        #print("SPEED RECOMMENDATION : 30KM/HR ,ROAD WILL BE SLIPPERY")
    elif (main == "Drizzle"):
        SpeedRecommendation = "30KM/HR"
        #print("SPEED RECOMMENDATION : 30KM/HR")
    elif (main == "Mist"):
        SpeedRecommendation = "30KM/HR and switch on the headlight"
        #print("SPEED RECOMMENDATION : 30KM/HR and switch on the Headlight")
    elif (main == "Thunderstorm"):
        SpeedRecommendation = "30KM/HR and stay away in the open place"
        #print("SPEED RECOMMENDATION : 30KM/HR and stay away in the open place")
    elif (main == "Clouds"):
        SpeedRecommendation = "MAINTAIN NORMAL SPEED LIMIT UPTO 5O KM/HR"
        #print("SPEED RECOMMENDATION : 30KM/HR and stay away in the open place")
        
        
    
    #print("Description of weather :",(b["weather"][0]["description"]))
    #print("visibility",(b["visibility"]))
    if (visibility<1000):
        RecommendationForVisibilty = "SPEED RECOMMENDATION : 30KM/HR and SWITCH ON THE HEAD LIGHT"
    else:
        RecommendationForVisibilty = "visibility range is ideal for vechicles"
        
        #print("SPEED RECOMMENDATION : 30KM/HR and SWITCH ON THE HEAD LIGHT")
    mydata={"temperature":temp, "TemperatureRecommendation":TemperatureRecommendation,"humidity":humi,"WeatherCondition":main,"SpeedRecommendation":SpeedRecommendation ,"DescriptionOfWeather":description,"visibility":visibility,"RecommendationForVisibilty":RecommendationForVisibilty,"WindSpeed":Windspeed,"LOCATION":AREA}
    print(mydata)
    client.publishEvent("12345","json",mydata)
    client.commandCallback = myCommandCallback
    
