/* 
 * File:   eCompass.h
 * Author: RODRIGO
 *
 * Created on 27 de Abril de 2021, 11:25
 */

#ifndef ECOMPASS_H
#define	ECOMPASS_H

#include<Arduino.h>

const uint16_t MINDELTATRIG = 1; /* final step size for iTrig */

const uint16_t MINDELTADIV = 1; /* final step size for iDivide */

/* fifth order of polynomial approximation giving 0.05 deg max error */ 
const uint16_t K1 = 5701; 
const uint16_t K2 = -1645; 
const uint16_t K3 = 446;

/* roll pitch and yaw angles computed by iecompass */ 
static int16_t iPhi, iThe, iPsi;
/* magnetic field readings corrected for hard iron effects and PCB orientation */ 
static int16_t iBfx, iBfy, iBfz; /*
/* hard iron estimate */ 
static int16_t iVx, iVy, iVz;

int16_t iecompass(int16_t iBpx, int16_t iBpy, int16_t iBpz, int16_t iGpx, int16_t iGpy, int16_t iGpz);
int16_t iHundredAtan2Deg(int16_t iy, int16_t ix);
int16_t iTrig(int16_t ix, int16_t iy);
int16_t iHundredAtanDeg(int16_t iy, int16_t ix);
int16_t iDivide(int16_t iy, int16_t ix);

#endif	/* ECOMPASS_H */
