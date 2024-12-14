#ifndef DRONE_COMMAND_H
#define DRONE_COMMAND_H

#include <basicMPU6050.h>

#define LU_Motor 7
#define RU_Motor 0
#define LD_Motor 5
#define RD_Motor 10
#define cnst 9.8

basicMPU6050<> imu;

float x_cor = -1;
float y_cor = -1;
float dev_x, dev_y;

class DroneComm {
public:
    void drone_init() {
        imu.setup();
        dev_x = imu.ax() * cnst;
        dev_y = imu.ay() * cnst;
        pinMode(LU_Motor, OUTPUT);
        pinMode(RU_Motor, OUTPUT);
        pinMode(LD_Motor, OUTPUT);
        pinMode(RD_Motor, OUTPUT);
        Serial.println(dev_x);
        Serial.println(dev_y);
    }

    void check_accel_x() {
        Serial.println((imu.ax() * cnst) - dev_x);
    }

    void check_accel_y() {
        Serial.println((imu.ay() * cnst) - dev_y);
    }

    void check_accel_z() {
        Serial.println(imu.az() * cnst);
    }

    

    void up(String params) {
        analogWrite(LU_Motor, 64);
        analogWrite(RU_Motor, 64);
        analogWrite(LD_Motor, 64);
        analogWrite(RD_Motor, 64);
        unsigned long duration_ms = params.toInt();
        unsigned long start_time = millis();
        while (millis() - start_time < duration_ms) {
            up_check();
        }
        Serial.println("complete");
    }

private:
    void up_check() {
        int x_otkl, y_otkl;
        x_otkl = abs(128 * imu.ax());
        y_otkl = abs(128 * imu.ay());
        if(x_otkl < 0)x_otkl = 0;
        if(y_otkl < 0)y_otkl = 0;
        if (((abs(imu.ax() * cnst)) - x_cor) >= x_cor) {
            if ((imu.ax() * cnst) < 0) {
                analogWrite(LU_Motor, 64 - x_otkl);
                analogWrite(RU_Motor, 64 - x_otkl);
                analogWrite(LD_Motor, 64 - x_otkl);
                analogWrite(RD_Motor, 64 - x_otkl);
            } else {
                analogWrite(LU_Motor, 64 - x_otkl);
                analogWrite(RU_Motor, 64 - x_otkl);
                analogWrite(LD_Motor, 64 - x_otkl);
                analogWrite(RD_Motor, 64 - x_otkl);
            }
        }

        if (((abs(imu.ay() * cnst)) - y_cor) >= y_cor) {
            if ((imu.ay() * cnst) < 0) {
                analogWrite(RU_Motor, 64 + y_otkl);
                analogWrite(RD_Motor, 64 + y_otkl);
                analogWrite(LU_Motor, 64 - y_otkl);
                analogWrite(LD_Motor, 64 - y_otkl);
            } else {
                analogWrite(RU_Motor, 64 - y_otkl);
                analogWrite(RD_Motor, 64 - y_otkl);
                analogWrite(LU_Motor, 64 + y_otkl);
                analogWrite(LD_Motor, 64 + y_otkl);
            }
        }
    }
};

DroneComm droneComm;

#endif
