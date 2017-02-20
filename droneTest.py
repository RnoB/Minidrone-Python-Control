
import pygatt
import binascii
import bitstring
import time
# The BGAPI backend will attemt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.

#MAMBO  'E0:14:24:XX:XX:XX'
droneIP = 'E0:14:24:XX:XX:XX'

adapter = pygatt.BGAPIBackend()


#Different Comand Buffer used
TakeOffBuffer=bitstring.BitArray('0x02,0x00,0x00,0x01').bytes;
LandingBuffer=bitstring.BitArray('0x02,0x00,0x03,0x00').bytes;
NotifyBuffer =bitstring.BitArray('0x00,0x01').bytes;
# The BGAPI backend will attemt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.


#Communication Channel
Channel0 = '9a66' 
Channel1 = '-0800-9191-11e4-012d1540cb8e'
NoAckChannel = 'fa0a' 
AckChannel = 'fa0b'
NameChannel = '00002a00-0000-1000-8000-00805f9b34fb'

#Notification Channel
notifyChannels =['fa00','fb00','fe01','fe02','fb0e','fb0f','fb1b', 'fb1c', 'fd22', 'fd23', 'fd24', 'fd52', 'fd53', 'fd54']



#Channel uuid creation
def ChannelCombi(channel):
    return Channel0+channel+Channel1

def main():
    connected=False

    #Attempt to connect to the drone
    while not connected:
        try:
            print('Connection to %s'%droneIP)


            adapter = pygatt.BGAPIBackend()
            adapter.start()
            device = adapter.connect(droneIP,address_type=pygatt.BLEAddressType.random)
            print('Connected to %s'%device.char_read(NameChannel).decode("utf-8") )
            connected=True
        except:
            print('Connection Time Out')

    #Set the notification buffer to the channel that should be notifoed
    print('Notification')
    for channel in notifyChannels:
        notifyChannel=ChannelCombi(channel)
        try:
            print("Read UUID %s (handle %d): %s" %
                      (notifyChannel, device.get_handle(notifyChannel), device.char_read(notifyChannel)))
        except:
            pass
        
        
        device.char_write(notifyChannel,NotifyBuffer)
        try:
            print("Read UUID %s (handle %d): %s" %
                      (notifyChannel, device.get_handle(notifyChannel), device.char_read(notifyChannel)))
        except:
            pass
    time.sleep(5)

    #Send take Off Buffer
    print('Taking Off')
    CommandChannel = ChannelCombi(AckChannel)
    print(CommandChannel)
    
    device.char_write(CommandChannel,TakeOffBuffer)
    time.sleep(5)


    device.disconnect()
    adapter.stop()



if __name__ == "__main__":
    main()





