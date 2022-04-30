#include <msp430.h>
#include "timer.h"
#include <stdio.h>
#include "serial.h"

#define CALADC12_15V_30C  *((unsigned int *)0x1A1A)
#define CALADC12_15V_85C  *((unsigned int *)0x1A1C)

void setup(void);
void sendString(const char * toSend);
const char * getTemperature(void);

int main(void) {
    WDTCTL = WDTPW | WDTHOLD;   // stop watchdog timer
    setup();
    unsigned long time=0;
    while (1) {
        if (millis()-time > 1000) {
            time=millis();
            unsigned char read;
            breceive_ch(&read);
            if (read == 'S') {
                const char * temp = getTemperature();
                sendString(temp);
            }
        }
    }
    return 0;
}

void setup(void) {
    REFCTL0 &= ~REFMSTR;
    ADC12CTL0 |= ADC12SHT0_8 + ADC12ON;
    ADC12CTL1 = ADC12SHP + ADC12CONSEQ_0;
    ADC12MCTL0 |= ADC12INCH_10;
    ADC12CTL0 |= ADC12REFON;
    ADC12CTL0 &= ~ADC12REF2_5V;
    ADC12MCTL0 |= ADC12SREF_1;
    ADC12CTL0 |= ADC12ENC + ADC12SC;

    init_timer();
    init_serial();
}

const char * getTemperature(void) {
    char* tempString;
    float temperatureDegC;

    ADC12CTL0 |= ADC12ENC + ADC12SC;
    temperatureDegC = (float)(((long)ADC12MEM0 - CALADC12_15V_30C) * (85 - 30));
    temperatureDegC /= (CALADC12_15V_85C - CALADC12_15V_30C);
    temperatureDegC += 30.0f;

    int intpart = (int)temperatureDegC;
    if (intpart >= 25) {
        P1OUT |= BIT0;
        P4OUT &= ~BIT7;
    }
    else {
        P1OUT &= ~BIT0;
        P4OUT |= BIT7;
    }

    int decpart = (int)((temperatureDegC-intpart)*10);
    sprintf(tempString, "%d.%d,\0", intpart, decpart);

    while (ADC12CTL1 & ADC12BUSY);

    return tempString;
}

void sendString(const char * toSend) {
    size_t i;
    for (i=0; toSend[i] != '\0'; i++) {
        bsend_ch(toSend[i]);
    }
    return;
}
