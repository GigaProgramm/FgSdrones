#ifndef DRONE_COMMAND_H
#define DRONE_COMMAND_H

#include <basicMPU6050.h> 

#define LU_Motor 7
#define RU_Motor 6
#define LD_Motor 5
#define RD_Motor 10 

basicMPU6050<> imu;

float dev_x, dev_y;

class DroneComm{
public:
    void drone_init(){
      imu.setup();
      dev_x = imu.ax() * 9.8;
      dev_y = imu.ay() * 9.8;
      pinMode(LU_Motor, OUTPUT);
      pinMode(RU_Motor, OUTPUT);
      pinMode(LD_Motor, OUTPUT);
      pinMode(RD_Motor, OUTPUT);
      Serial.println(dev_x);
      Serial.println(dev_y);
    }
    void check_accel_x(){
      Serial.println((imu.ax() * 9.8) - dev_x);
    }
    void check_accel_y(){
      Serial.println((imu.ay() * 9.8) - dev_y);
    }
    void check_accel_z(){
      Serial.println(imu.az() * 9.8);
    }
    
};

DroneComm droneComm;


#endif