# from pypylon import pylon

# camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
# camera.Open()
# camera.TriggerMode.SetValue('On')
# camera.TriggerSource.SetValue('Software')


# numberOfImagesToGrab = 100
# camera.StartGrabbingMax(numberOfImagesToGrab)



# while camera.IsGrabbing():
#     camera.TriggerSoftware()
#     grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    
#     if grabResult.GrabSucceeded():
#         # Access the image data.
#         print("SizeX: ", grabResult.Width)
#         print("SizeY: ", grabResult.Height)
#         img = grabResult.Array
#         print("Gray value of first pixel: ", img[0, 0])

#     grabResult.Release()

#     import cv2
#     cv2.imshow('img', cv2.resize(img, None, fx=0.5, fy=0.5))
#     cv2.waitKey(0)




from pypylon import pylon
import cv2
import time
import numpy as np

class Collector():

    def __init__(self, gain = 0 , exposure = 3000, max_buffer = 20 ):
        """Initializes the Collector

        Args:
            gain (int, optional): The gain of images. Defaults to 0.
            exposure (float, optional): The exposure of the images. Defaults to 3000.
            max_buffer (int, optional): Image buffer for cameras. Defaults to 5.
        """
        self.gain = gain
        self.exposure = exposure
        self.max_buffer = max_buffer

        self.__tl_factory = pylon.TlFactory.GetInstance()
        devices = list()

        for device in self.__tl_factory.EnumerateDevices():
            if (device.GetDeviceClass() == 'BaslerGigE'):                
                devices.append(device)

        assert len(devices) > 0 , 'No Camera is Connected!'

        self.cameras = list()

        for device in devices:
            camera = pylon.InstantCamera(self.__tl_factory.CreateDevice(device))
            self.cameras.append(camera)


    def start_grabbing(self):

        for i in range( len( self.cameras)):
            self.cameras[i].Open()
            self.cameras[i].TriggerMode.SetValue('On')
            self.cameras[i].TriggerSource.SetValue('Software')

            self.cameras[i].ExposureTimeAbs.SetValue(self.exposure)

            self.cameras[i].GainRaw.SetValue(self.gain)

            #camera.MaxNumBuffer = self.max_buffer
            
            #self.setExposure(exposure)
            #self.setGain(gain)

            self.cameras[i].StartGrabbing()


    def stop_grabbing(self):
        for i in range( len( self.cameras)):
            #grabResult.Release()

            self.cameras[i].Close()

            
        
    def listDevices(self):
        """Lists the available devices
        """
        for i ,  camera in enumerate(self.cameras):
            device_info = camera.GetDeviceInfo()
            print(
                "Camera #%d %s @ %s (%s) @ %s" % (
                i,
                device_info.GetModelName(),
                device_info.GetIpAddress(),
                device_info.GetMacAddress(),
                device_info.GetSerialNumber(),
                )
            
            )
            print(device_info)
    def serialnumber(self):
        serial_list=[]
        for i ,  camera in enumerate(self.cameras):
            device_info = camera.GetDeviceInfo()
            serial_list.append(device_info.GetSerialNumber())
        return serial_list         


    def setExposure(self , exposure):
        """Sets exposure of the images

        Args:
            exposure (float, optional)
        """
        self.exposure = exposure

    def setGain(self, gain):
        """Sets gain of the images

        Args:
            gain (int, optional)
        """
        self.gain = gain

    def setBufferNumber(self, max_buffer):
        """Set Maximum buffer number for the cameras.

        Args:
            max_buffer (int, optional): Maximum buffer number.
        """
        self.max_buffer = max_buffer
    def cameras2(self):
        print(self.cameras)


    def getPictures(self, time_out = 5000):
        x=time.time()
        # print(x)
        """Retrives pictures from cameras.

        Args:
            camera_number (int): Camera Number.
            num_grab_images (int, optional): How many images should be retrived from the camera. Defaults to 1.
            time_out (int, optional): Time-out of the grabber. Defaults to 5000.

        Returns:
           list: A list of np.arrays for each retrived image.
        """


 

        #print(f'Using camera #{camera_number + 1}, {camera.GetDeviceInfo().GetModelName()} , on {camera.GetDeviceInfo().GetIpAddress()}')
        
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        imgs = {}
        for camera in self.cameras:
            camera.TriggerSoftware()
        for camera in self.cameras:
            # print('****')
            if camera.IsGrabbing():
                # camera.Width = 800
                # camera.Height = 600
                grabResult = camera.RetrieveResult(time_out, pylon.TimeoutHandling_ThrowException)

                if grabResult.GrabSucceeded():
                    #print(f'camera #{camera_number + 1} grabbed image')
                    # imgs.append( grabResult.Array )
                    image = converter.Convert(grabResult)
                    imgs[camera.GetDeviceInfo().GetSerialNumber()]=image.Array

                    

                else:
                    imgs[camera.GetDeviceInfo().GetSerialNumber()]=np.zeros([1200,1920],dtype=np.unit8)

                    print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
            else:
                    print('erpr')
                    imgs[camera.GetDeviceInfo().GetSerialNumber()]=np.zeros([1200,1920],dtype=np.unit8)

            grabResult.Release()

            #camera.Close()

        z=0   
        return imgs

    def get_names(self):
        mylist=[]
        try:

            # Get the transport layer factory.
            tlFactory = pylon.TlFactory.GetInstance()

            # Get all attached devices and exit application if no device is found.
            devices = tlFactory.EnumerateDevices()
            
            tl_factory = pylon.TlFactory.GetInstance()
            devices = tl_factory.EnumerateDevices()
            for device in devices:
            #  print(device.GetFriendlyName())
                mylist.append(device.GetFriendlyName())
        #  print(mylist)
            mylist=[x for x in mylist if "Emulation" not in x]
            # print(len(mylist))
        # my_finallist = [i for j, i in enumerate(mylist) if i not in mylist[:j]] 
        #  print(mylist)
            
            if len(mylist) == 0:
                mylist.append('No camera present.')
                raise pylon.RuntimeException("No camera present.")
            return mylist   
        except:
        # print('problem')
            mylist.append('prblem')
            return mylist  



if __name__ == '__main__':
    collector = Collector(exposure=10000 , gain=130)
    collector.start_grabbing()
    print(collector.get_names())

    # collector.cameras()
    collector.listDevices()
    # print(collector.cameras[0].GetDeviceInfo().GetIpAddress())
    # while True:
    #     imgs = collector.getPictures()
    #     # if len(imgs)<=1:
    #     #     continue
    #     #imgs = next(camera_grabber)
    #     cv2.imshow('window', imgs['40150886'])
    #   # cv2.imshow('asd',imgs[1])
    #     cv2.waitKey(10)
