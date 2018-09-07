#! python
import appdaemon.appapi as appapi
import telnetlib
import re

#Status (MsgID=0) - Printed as two 8-bit bitfields
#Control setpoint (MsgID=1) - Printed as a floating point value / not used
#Remote parameter flags (MsgID= 6) - Printed as two 8-bit bitfields / not used
#Maximum relative modulation level (MsgID=14) - Printed as a floating point value / not used
#Boiler capacity and modulation limits (MsgID=15) - Printed as two bytes / not used
#Room Setpoint (MsgID=16) - Printed as a floating point value / not used
#Relative modulation level (MsgID=17) - Printed as a floating point value
#CH water pressure (MsgID=18) - Printed as a floating point value / not used
#Room temperature (MsgID=24) - Printed as a floating point value / not used
#Boiler water temperature (MsgID=25) - Printed as a floating point value
#DHW temperature (MsgID=26) - Printed as a floating point value
#Outside temperature (MsgID=27) - Printed as a floating point value / not used
#Return water temperature (MsgID=28) - Printed as a floating point value
#DHW setpoint boundaries (MsgID=48) - Printed as two bytes / not used
#Max CH setpoint boundaries (MsgID=49) - Printed as two bytes / not used
#DHW setpoint (MsgID=56) - Printed as a floating point value
#Max CH water setpoint (MsgID=57) - Printed as a floating point value
#Burner starts (MsgID=116) - Printed as a decimal value
#CH pump starts (MsgID=117) - Printed as a decimal value
#DHW pump/valve starts (MsgID=118) - Printed as a decimal value
#DHW burner starts (MsgID=119) - Printed as a decimal value
#Burner operation hours (MsgID=120) - Printed as a decimal value
#CH pump operation hours (MsgID=121) - Printed as a decimal value
#DHW pump/valve operation hours (MsgID=122) - Printed as a decimal value
#DHW burner operation hours (MsgID=123) - Printed as a decimal value


HOST = "192.168.1.100" #set OTGW ip
PORT = "6638" #set OTGW port
OTGW = telnetlib.Telnet()


class opentherm_OTGW(appapi.AppDaemon):

    def initialize(self):
            
            self.OTGW_variables = ['MsgID=0', 'MsgID=1', 'MsgID=6', 'MsgID=14', 'MsgID=15', 'MsgID=16', 'MsgID=17', 'MsgID=18', 'MsgID=24',
                                  'MsgID=25', 'MsgID=26', 'MsgID=27', 'MsgID=28', 'MsgID=48', 'MsgID=49', 'MsgID=56', 'MsgID=57', 'MsgID=116',
                                  'MsgID=117', 'MsgID=118', 'MsgID=119', 'MsgID=120', 'MsgID=121', 'MsgID=122', 'MsgID=123']
            
            self.OTGW_variables_library = {}
            
            self.log("opentherm_OTGW is ready")
        
            #opentherm_OTGW.OTGW_read(self)
            #opentherm_OTGW.OTGW_write(self)
    
    def OTGW_read(self):
        
        try:
            OTGW.open(HOST,PORT)
            self.log("Port opened")

            OTGW.write(('PS=1' + '\r\n').encode('ascii'))
            self.output=OTGW.read_until(("\n>").encode('ascii'),1)
            OTGW.close()
            self.log("PS=1 sent")

            self.data=str(self.output)

            self.data_1= re.sub("b|P|S|r|n| |:|'|\\\\", "", self.data)

            self.data_2= self.data_1[1:]

            self.data_list = self.data_2.split(',')
            
        except:
            self.log("A problem has arisen")
        

        
    def OTGW_write(self):
    
        try:
            control_setpoint= input("setpoint ?")
            
            
            OTGW.open(HOST,PORT)
            
                
            OTGW.write(('CS=' + control_setpoint + '\r\n').encode('ascii'))
            self.output=OTGW.read_until(("\n>").encode('ascii'),1)
            self.data=str(self.output)
            print(re.sub("b|r|n|'|\\\\", "", self.data))
            OTGW.close()
            
        except:
            self.log("A problem has arisen")
