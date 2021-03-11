import socket
# -*- coding: utf-8 -*-

import serial
import time
import urx

#import scipy.signal as signal

#import numpy as np

#import pylab as pl

#import matplotlib.pyplot as plt

#import matplotlib




#16位取高12位
def f2s_h(h_byte,l_byte ):
   data =  ((h_byte<<8)|l_byte)>>4
   if((data&0x0800)):
       return -((~((data)-1))&0x0fff)
   else:
       return (data&0x7ff)

#16位取低12位
def f2s_l(h_byte,l_byte ):
   data =  ((h_byte<<8)|l_byte)&0x0fff
   if((data&0x0800)):
       return -((~((data)-1))&0x0fff)
       #return (~((data&0x7ff)-1))
       #return ((~data)+1)|0x800
   else:
       return (data&0x7ff)

#
#

value=0
value1=0
value2=0
value3=0
value4=0
value5=0

def filter(new_value):
   #上次滤波值
   global value
   a=22
   value = (256-a)*value/256+a*new_value/256
   return value

def filter1(new_value1):
   #上次滤波值
   global value1
   a=22
   value1 = (256-a)*value1/256+a*new_value1/256
   return value1

def filter2(new_value2):
   #上次滤波值
   global value2
   a=22
   value2 = (256-a)*value2/256+a*new_value2/256
   return value2

def filter3(new_value3):
   #上次滤波值
   global value3
   a=22
   value3 = (256-a)*value3/256+a*new_value3/256
   return value3

def filter4(new_value4):
   #上次滤波值
   global value4
   a=22
   value4 = (256-a)*value4/256+a*new_value4/256
   return value4

def filter5(new_value5):
   #上次滤波值
   global value5
   a=22
   value5 = (256-a)*value5/256+a*new_value5/256
   return value5
    
if __name__ == "__main__":
    try:
        portx="COM9"
        bps=230400
        #         bps=115200
        timex=0.2
        ser=serial.Serial(portx,bps,timeout=timex)
        #清空
        send_data=b'\x47\xAA\x0D\x0A'
        result=ser.write(send_data)
        time.sleep(1)
        #连续读取
        send_data=b'\x48\xAA\x0D\x0A'
        send_data=b'\x49\xAA\x0D\x0A'
        result=ser.write(send_data)
#        print("写字节数:",result)
#        data = ser.readline() 
#        print("读内容:",data)
#        print("process started.")
        
        
        HOST = "192.168.1.100"
        PORT = 30003
        
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))

        while True:
             
            send_data=b'\x49\xAA\x0D\x0A'
            result=ser.write(send_data)
            data = ser.read(12)
#            print(data)
#            print(len(data))
            if(len(data)!=12):
                continue
            q1=f2s_h(data[1],data[2])*0.009765625
            q2=-f2s_l(data[2],data[3])*0.009765625
            q3=-f2s_h(data[4],data[5])*0.009765625
            q4=f2s_l(data[5],data[6])*0.000390625/10
            q5=-f2s_h(data[7],data[8])*0.000390625/10
            q6=-f2s_l(data[8],data[9])*0.000390625/10
            
            
            
            q1=filter(q1)
            q2=filter1(q2)
            q3=filter2(q3)
            # q4=filter3(q4)
            # q5=filter4(q5)
            # q6=filter5(q6)
#           q7=1;\
#           q8=0.01;
#           q1=0
#           q2=0
#           q3=0
#             q4=0.05
#             q5=0.05
#             q6=0.05

            
            q1=round(q1,3)
            q2=round(q2,3)
            q3=round(q3,3)
            q4=round(q4,3)
            q5=round(q5,3)
            q6=round(q6,3)
            
            
            if (abs(q1)<0.2)and(abs(q2)<0.2)and(abs(q3)<0.2):
                #and(abs(q4)<0.01)and(abs(q5)<0.01)and(abs(q6)<0.01):
                continue
            if (abs(q1)>3)or(abs(q2)>3)or(abs(q3)>3):
                continue
              
           # print(cmd,"speedl([""%if,%if,%if,%if,%if,%if""],%if,%if,)\n",q1,q2,q3,q4,q5,q6,q7,q8);
            #repr(q1)
            q1=-q1/10
            q2=q2/10
            q3=q3/10
            q1=round(q1,3)
            q2=round(q2,3)
            q3=round(q3,3)
            q4=round(q4,3)
            q5=round(q5,3)
            q6=round(q6,3)
          
            d=[str(q2),str(q1),str(q3),str(q4),str(q5),str(q6)]
#            print(d)
#             e=["movel(pose_trans(actual_tcp_pos,[",",".join(d),"])0.5,0.1,0,0)\n"]#加速度 持续时间
            # 加速度 持续时间;\n的功能应该是作为消息结束符
            e=["speedl([",",".join(d),"],1,0.1)\n"]
#            get_joint_temp(4)
#            print(e)
            
            f=bytes("".join(e),encoding='utf-8')
#            g=b"speedl(pose_trans(get_forward_kin(),var_1),1,1)\n"
#            s.send(g)

            
            s.send(f)
            print(f)
            #time.sleep(0.03)
        s.close()
        ser.close()
        
            
            
    except Exception as e: 
        print("err:",e)
#        s.close()
#        ser.close()
