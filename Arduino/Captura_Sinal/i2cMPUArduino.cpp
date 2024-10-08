/*
TODO:.....
*/
#include"i2cMPUArduino.h"
#include<Arduino.h>
/*return     0 if successful*/
int Sensors_I2C_WriteRegister(unsigned char slave_addr,
                                        unsigned char reg_addr,
                                        unsigned short len, 
                                        const unsigned char *data_ptr)
{
  int ret = 0;
  int i;

  Wire.beginTransmission(slave_addr);//Inicia transmissão com o MPU6050 (slave) : slave_addr = end. do MPU no barramento i2c --> 0x68
  Wire.write(reg_addr);
  Wire.write(data_ptr, len);
  /*
  for(i = 0; i < len; i++)
  {
    Wire.write(data_ptr[i]);
  }
  */
  ret = Wire.endTransmission(true);//envia os dados no buffer de escrita da i2c e encerra "true" enviando um stop msg e libera o barramento
/*
  Serial.print("Sensors_I2C_WriteRegister"); 
  Serial.print("\n");
  Serial.print("ret: "); 
  Serial.print(ret);
  Serial.print("\n");
  Serial.print("\n");
  */
  return ret;  
  /*
  char retries=0;
  int ret = 0;
  unsigned short retry_in_mlsec = Get_I2C_Retry();
                              
tryWriteAgain:  
  ret = 0;
  ret = ST_Sensors_I2C_WriteRegister( slave_addr, reg_addr, len, data_ptr); 

  if(ret && retry_in_mlsec)
  {
    if( retries++ > 4 )
        return ret;
    
    mdelay(retry_in_mlsec);
    goto tryWriteAgain;
  }
  return ret;  
  */
}

int Sensors_I2C_ReadRegister(unsigned char slave_addr, unsigned char reg_addr,/*unsigned short*/int len, unsigned char *data_ptr)
{
  int ret = 0;
  int i;
  
  Wire.beginTransmission(slave_addr);
  Wire.write(reg_addr);
  Wire.endTransmission(false);
  //Solicita os dados do sensor
  if(Wire.requestFrom(slave_addr,len,true))
  {
    ret = 0;
  }
//Wire.requestFrom(0x68,3,true);
  for(i=0; i < len;i++)
  {
    data_ptr[i] = Wire.read();
    //Serial.print("valor");
    //Serial.print(i);
    //Serial.print(": ");
    //Serial.print(data_ptr[i]);
    //Serial.print(reg_addr);
  }
  return ret;
  /*
  char retries=0;
  int ret = 0;
  unsigned short retry_in_mlsec = Get_I2C_Retry();
  
tryReadAgain:  
  ret = 0;
  ret = ST_Sensors_I2C_ReadRegister( slave_addr, reg_addr, len, data_ptr);

  if(ret && retry_in_mlsec)
  {
    if( retries++ > 4 )
        return ret;
    
    mdelay(retry_in_mlsec);
    goto tryReadAgain;
  } 
  return ret;
  */
}
