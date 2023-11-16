#include "ADS1X15.h"
ADS1115 ADS(0x48);

void setup() {
  Serial.begin(9600);
//  Serial.println("SC_volt Divd_volt Divd_ratio Therm_R Ref_Volt");

  ADS.begin();
}

void loop() {
  ADS.setGain(0);

  int val0 = ADS.readADC(0);
  int val1 = ADS.readADC(1);
  int val2 = ADS.readADC(2);
  int val3 = ADS.readADC(3);

  float f = ADS.toVoltage(1);   //voltage factor
  float Divd_ratio = (val2 * f)/(val3 * f);
  float Therm_R = 988.0*(1.0-Divd_ratio)/Divd_ratio;  //988 = Resistor

  Serial.print(val1 * f, 6);  //SC_volt
  Serial.print(' ');
  Serial.print(val2 * f, 6);  //Divd_volt
  Serial.print(' ');
  Serial.print(Divd_ratio, 6);  //Divd_ratio
  Serial.print(' ');
  Serial.print(Therm_R, 6);   //Therm R
  Serial.print(' ');
  Serial.print(val3 * f, 6);  //Ref_volt
  Serial.println();
  
  delay(1000);
}
