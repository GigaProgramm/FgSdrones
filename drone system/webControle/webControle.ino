#include "GyverPortal.h"
GuverPortal ui;

void build(){
  GP.BUILD_BEGIN(GP_DARK);
  GP.TITLE("FGSDrones", "t1");
  GP.HR();
  GP.BUTTON("up", "Start");
  GP.BUTTON("frw", "Forward");
  GP.BUTTON("rgh", "Right");
  GP.BUTTON("lft", "Left");
  GP.BUTTON("bck", "Back");
  GP.BUTTON("lnd", "Landing");
}

void action(){
  if (ui.click()){
        if (ui.click("up")) Serial.println("up");
        if (ui.click("frw")) Serial.println("frw");
        if (ui.click("rgh")) Serial.println("rgh");
        if (ui.click("lft")) Serial.println("lft");
        if (ui.click("bck")) Serial.println("bck");
        if (ui.click("lnd")) Serial.println("lnd");

  }
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFi.mode(WIFI_AP);
  WiFi.softAP("Drone");
    ui.attachBuild(build);
  ui.attach(action);
  ui.start();

}

void loop() {
  // put your main code here, to run repeatedly:
ui.tick();
}
