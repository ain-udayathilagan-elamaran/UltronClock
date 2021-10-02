import paho.mqtt.client as mqtt






class mqtt_mod :
    
    def __init__(self,username_mqtt,password_mqtt,mqtt_broker,mqtt_port,Publish_Topic):
        self.username_mqtt =username_mqtt
        self.password_mqtt =password_mqtt
        self.Publish_Topic=Publish_Topic
        self.mqtt_port=mqtt_port
        self.mqtt_broker=mqtt_broker
        
    def MQTT_Connect(self):
        try :    
            client = mqtt.Client()
            client.username_pw_set(self.username_mqtt,password=self.password_mqtt)
            client.connect(host=self.mqtt_broker, port=self.mqtt_port)
            return True,client
        except Exception as e:
            return False,e
        
    def Publish_Data(self,client,Message):
        try: 
            client.publish(self.Publish_Topic,Message)
            return True,None
        except Exception as sd:
            return False,sd            