/*
 * serial.h
 *
 *  Created on: 17/ago/2015
 *      Author: Paolo Santinelli
 */



#ifndef SERIAL_
#define SERIAL_

void init_serial(void);
int bsend_ch(unsigned char ch);
unsigned char breceive_ch(unsigned char * ch);

#endif
