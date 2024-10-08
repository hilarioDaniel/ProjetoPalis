/* 
 * File:   i2cMPUArduino.h
 * Author: RODRIGO
 *
 * Created on 29 de Maio de 2020, 14:08
 */

#ifndef I2CMPUARDUINO_H
#define	I2CMPUARDUINO_H

#include <Wire.h>

int Sensors_I2C_ReadRegister(unsigned char Address, unsigned char RegisterAddr, 
                                          /*unsigned short*/int RegisterLen, unsigned char *RegisterValue);
int Sensors_I2C_WriteRegister(unsigned char Address, unsigned char RegisterAddr, 
                                           unsigned short RegisterLen, const unsigned char *RegisterValue);

#endif	/* I2CMPUARDUINO_H */
