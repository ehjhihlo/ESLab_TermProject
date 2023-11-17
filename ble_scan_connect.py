from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle

class NewDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, handle, data):
        print(data)
        # data1, data2, data3 = struct.unpack('<3h', data)
        print(f"Notification, handle: {handle}, data:{data}")


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

n=0
addr = []
num = -1
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print (" %s = %s" % (desc, value))
        if (value=='EnJhih' and desc=='Complete Local Name'):
            num = n-1
            break
    if (num != -1):
        break
assert(num!=-1)


# number = input('Enter your device number: ')
# print ('Device', number)
# num = int(number)
# print (addr[num])
#

print ("Connecting...")
dev = Peripheral(addr[num], 'random')
#
print ("Services...")
for svc in dev.services:
    print (str(svc))
#
setup_data = b"\x01\x00"
notify = dev.getCharacteristics(uuid=0x2a37)[0]
notify_handle = notify.getHandle() + 1
dev.writeCharacteristic(notify_handle, setup_data, withResponse=True)


while True:
    #for ch in dev.getCharacteristics(uuid=UUID(0xfff4)):
        # ch.write('52399254'.encode('utf-8'))
    dev.setDelegate(NewDelegate())

    print("writing done")
    if dev.waitForNotifications(1.0):
        #ch.write('44444'.encode('utf-8'))
        # handleNotification() was called
        print("write notify")
        #ch = dev.getCharacteristics(uuid=UUID(0xfff4))[0]
        #if (ch.supportsRead()):
        #print(ch.read())
        print("waiting")

#finally:
    #dev.disconnect() 