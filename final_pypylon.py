
"""
########################################
---------------------------------------

Made with Malek & Milad

Features:

    ● Create Unlimite Object of Cameras and Live Preview By serial number
    ● Set Bandwitdh Of each Cameras
    ● Set gain,exposure,width,height,offet_x,offset_y
    ● Get tempreture of Cmeras
    ● Set Trigger Mode on
    ● There are Some diffrents between ace2(pro) and ace

---------------------------------------
########################################
"""

from pickle import FALSE
from pypylon import pylon
import cv2
import time
import numpy as np
import sqlite3
import threading

from pypylon import genicam

DEBUG = False

show_eror=False

if show_eror: 

    from eror_window import UI_eror_window

class Collector():

    def __init__(self,serial_number, gain = 0 , exposure = 70000, max_buffer = 20, trigger=True, delay_packet=100, packet_size=1500 , frame_transmission_delay=0 ,width=1000,height=1000,offet_x=0,offset_y=0,manual=False):
        """Initializes the Collector

        Args:
            gain (int, optional): The gain of images. Defaults to 0.
            exposure (float, optional): The exposure of the images. Defaults to 3000.
            max_buffer (int, optional): Image buffer for cameras. Defaults to 5.
        """
        self.gain = gain
        self.exposure = exposure
        self.max_buffer = max_buffer
        self.cont_eror=0
        self.serial_number = serial_number
        self.trigger = trigger
        self.dp = delay_packet
        self.ps=packet_size
        self.ftd=frame_transmission_delay
        self.width=width
        self.height=height
        self.offset_x=offet_x
        self.offset_y=offset_y
        self.manual=manual
        self.exitCode=0

        if show_eror:
            self.window_eror = UI_eror_window()

        self.__tl_factory = pylon.TlFactory.GetInstance()
        devices = []


        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


        for device in self.__tl_factory.EnumerateDevices():
            if (device.GetDeviceClass() == 'BaslerGigE'):                
                devices.append(device)

        # assert len(devices) > 0 , 'No Camera is Connected!'


        for device in devices:
            camera = pylon.InstantCamera(self.__tl_factory.CreateDevice(device))
            print(camera.GetDeviceInfo().GetSerialNumber())
            if camera.GetDeviceInfo().GetSerialNumber() == self.serial_number:
                self.camera = camera
                
                break
        assert len(devices) > 0 , 'No Camera is Connected!'


    def eror_window(self,msg,level):
        self.window_eror = UI_eror_window()
       # self.ui2= UI_eror_window()
        self.window_eror.show()
        self.window_eror.set_text(msg,level)


    def tempreture(self):
        device_info = self.camera.GetDeviceInfo()
        model=str(device_info.GetModelName())
        model=model[-3:]
        if model=='PRO':
            # print(self.camera.DeviceTemperature.GetValue())
            return self.camera.DeviceTemperature.GetValue()
        else :
            # print('temp',self.camera.TemperatureAbs.GetValue())
            return self.camera.TemperatureAbs.GetValue()


    def start_grabbing(self):

        device_info = self.camera.GetDeviceInfo()
        model=str(device_info.GetModelName())
        model=model[-3:]
        # print(model[-3:])


        try:
            print(self.camera.IsOpen())
            print(device_info.GetSerialNumber())

            self.camera.Open()
            if self.manual:

                
                if model=='PRO':
                    print('yes pro')
                    # print(self.camera.DeviceTemperature.GetValue())
                    self.camera.ExposureTime.SetValue(self.exposure)

                    self.camera.Gain.SetValue(self.gain)
                    
                    # self.camera.GevSCPSPacketSize.SetValue(int(self.ps)+1000)
                    # self.camera.Close()
                    # self.camera.Open()
                    self.camera.GevSCPSPacketSize.SetValue(int(self.ps))
                    self.camera.Close()
                    self.camera.Open()
                                                  
                    self.camera.GevSCPD.SetValue(self.dp)
                    self.camera.Close()
                    self.camera.Open()                   
                    self.camera.GevSCFTD.SetValue(self.ftd)
                    self.camera.Close()
                    self.camera.Open()




                    self.camera.Width.SetValue(self.width)
                    self.camera.Height.SetValue(self.height)

                    self.camera.OffsetX.SetValue(self.offset_x)
                    self.camera.OffsetY.SetValue(self.offset_y)
                    



                

                else:
                    


                    self.camera.ExposureTimeAbs.SetValue(self.exposure)
                    self.camera.GainRaw.SetValue(self.gain)

                    self.camera.GevSCPSPacketSize.SetValue(int(self.ps)+1000)
                    self.camera.Close()
                    self.camera.Open()
                                
                    self.camera.GevSCPD.SetValue(self.dp)
                    self.camera.Close()
                    self.camera.Open()                   
                    self.camera.GevSCFTD.SetValue(self.ftd)
                    self.camera.Close()
                    self.camera.Open()

                    self.camera.GevSCPSPacketSize.SetValue(int(self.ps))
                    self.camera.Close()
                    self.camera.Open()
                    self.camera.Width.SetValue(self.width)
                    self.camera.Height.SetValue(self.height)

                    self.camera.OffsetX.SetValue(self.offset_x)
                    self.camera.OffsetY.SetValue(self.offset_y)
                    


            self.camera.Close()

            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 

            self.camera.Open()

            if self.trigger:
                self.camera.TriggerSelector.SetValue('FrameStart')
                self.camera.TriggerMode.SetValue('On')
                self.camera.TriggerSource.SetValue('Software')
            else:
                # self.camera.TriggerMode.SetValue('Off')
                print('triggeroff')

            # if self.manual:
            #     self.camera.ExposureTimeAbs.SetValue(20000)


            #     # self.camera.Width.SetValue(600)
            #     print(self.camera.Width.GetValue())
            #     self.camera.Width.SetValue(600)
            #     # int64_t = self.camera.PayloadSize.GetValue()
            #     # self.camera.GevStreamChannelSelectorCamera.GevStreamChannelSelector.SetValue( 'GevStreamChannelSelector_StreamChannel0 ')
            #     # self.camera.GevSCPSPacketSize.SetValue(1500)
                             
            #     self.camera.GevSCPD.SetValue(self.dp)
                
            #     self.camera.GevSCFTD.SetValue(self.ftd)
            self.exitCode=0
            
        except genicam.GenericException as e:
            # Error handling
            print("An exception occurred.", e.GetDescription())
            self.exitCode = 1
            # self.eror_window('Check The Number of cameras',3)

            
            # return self.exitCode



    def stop_grabbing(self):
        self.camera.Close()

            
        
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




    def trigg_exec(self,):
        
        if self.trigger:
            self.camera.TriggerSoftware()
            print(self.camera.GetQueuedBufferCount(), 'T'*100)
            while self.camera.GetQueuedBufferCount() >=10:
                pass
            print(self.camera.GetQueuedBufferCount(), 'T'*100)


    def getPictures(self, time_out = 5000):
        try:
            
            if DEBUG:
                print('TRIGE Done')
            if self.camera.IsGrabbing():
                if DEBUG:
                    print('Is grabbing')
                    
                    if self.camera.GetQueuedBufferCount() == 10:
                        print('ERRRRRRRRRRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRR')
                grabResult = self.camera.RetrieveResult(time_out, pylon.TimeoutHandling_ThrowException)
                

                # print(self.camera.GetQueuedBufferCount(), 'f'*100)
                if DEBUG:
                    print('RetrieveResult')

                    if self.camera.GetQueuedBufferCount() == 10:
                        print('ERRRRRRRRRRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRR')
                if grabResult.GrabSucceeded():
                    
                    if DEBUG:
                        print('Grab Succed')

                    image = self.converter.Convert(grabResult)
                    img=image.Array

                else:
                    img=np.zeros([1200,1920,3],dtype=np.uint8)
                    self.cont_eror+=1
                    print('eror',self.cont_eror)
                    print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
            else:
                    print('erpr')
                    img=np.zeros([1200,1920,3],dtype=np.uint8)
        except:
            print('eror')
        
        # print(self.camera.GetQueuedBufferCount(), 'f'*100)
        # time.sleep(0.1)
        # print(self.camera.GetQueuedBufferCount(), 'f'*100)
        # self.img = img
        
        return img


    def get_cam(self,i):
        return self.camera
    



def get_threading(cameras):
    def thread_func():
        for cam in cameras:
            cam.trigg_exec()
        for cam in cameras:
            img = cam.getPictures()
            cv2.imshow('img', cv2.resize( img, None, fx=0.5, fy=0.5 ))
            cv2.waitKey(10)

        t = threading.Timer(0.330, thread_func )
        t.start()
    
    return thread_func




if __name__ == '__main__':
    
    cameras = {}
    # for sn in ['40150887']:
        # collector = Collector( sn,exposure=3000 , gain=30, trigger=False, delay_packet=170000)
    collector = Collector('23961515',exposure=3000, gain=10, trigger=False, delay_packet=81062,\
        packet_size=9000,frame_transmission_delay=18036,height=1000,width=1000,offet_x=16,offset_y=4,manual=True)
    collector.start_grabbing()
    cameras=collector

    # cameras.start_grabbing()
    cameras.getPictures()



    while True:
        
    #     # for cam in cameras:
    #     #         cam.trigg_exec()
                
    #     # for cam in cameras:
    #     #print(cam.camera.GetQueuedBufferCount())
        img = cameras.getPictures()
        #print(cam.camera.GetQueuedBufferCount())
        cv2.imshow('img1', cv2.resize( img, None, fx=0.5, fy=0.5 ))
        cv2.waitKey(50)
    #     # img = cameras[1].getPictures()
    #     # #print(cam.camera.GetQueuedBufferCount())
    #     # cv2.imshow('img2', cv2.resize( img, None, fx=0.5, fy=0.5 ))
    #     # cv2.waitKey(50)
    #     # img = cameras[2].getPictures()
    #     # #print(cam.camera.GetQueuedBufferCount())
    #     # cv2.imshow('img3', cv2.resize( img, None, fx=0.5, fy=0.5 ))
    #     # cv2.waitKey(50)
    #     # img = cameras[3].getPictures()
    #     # #print(cam.camera.GetQueuedBufferCount())
    #     # cv2.imshow('img4', cv2.resize( img, None, fx=0.5, fy=0.5 ))
    #     # cv2.waitKey(50)


        #time.sleep(0.330)
        # while cam.camera.GetQueuedBufferCount()!=10:
        #     pass
        # print(cam.camera.GetQueuedBufferCount(), 'f'*100)
        # print('-'*100)
    # func = get_threading(cameras)
    # func()
        
