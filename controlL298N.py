# Libreria controlL298N.py

from machine import Pin, PWM

class DCmotores:
    def __init__(self, motorRRP, motorRRN, motorRLP, motorRLN, motorFRP, motorFRN, motorFLP, motorFLN, enableRR, enableRL, enableFR, enableFL, minDuty = 0, maxDuty = 65535):
        self.mRRP = motorRRP
        self.mRRN = motorRRN
        self.mRLP = motorRLP
        self.mRLN = motorRLN
        self.mFRP = motorFRP
        self.mFRN = motorFRN
        self.mFLP = motorFLP
        self.mFLN = motorFLN
        self.enRR = enableRR
        self.enRL = enableRL
        self.enFR = enableFR
        self.enFL = enableFL
        self.min = minDuty
        self.max = maxDuty # duty -> 1023; duty_u16 -> 65535
        return
    
    def forward(self, speed):
        self.spd = speed
        self.enRR.duty_u16(self.duty_cycle(self.spd))
        self.enRL.duty_u16(self.duty_cycle(self.spd))
        self.enFR.duty_u16(self.duty_cycle(self.spd))
        self.enFL.duty_u16(self.duty_cycle(self.spd))
        self.mRRP.on()
        self.mRRN.off()
        self.mRLP.on()
        self.mRLN.off()
        self.mFRP.on()
        self.mFRN.off()
        self.mFLP.on()
        self.mFLN.off()
        return
    
    def turnClockwise(self, speed):
        self.spd = speed
        self.enRR.duty_u16(self.duty_cycle(self.spd))
        self.enRL.duty_u16(self.duty_cycle(self.spd))
        self.enFR.duty_u16(self.duty_cycle(self.spd))
        self.enFL.duty_u16(self.duty_cycle(self.spd))
        self.mRRP.off()
        self.mRRN.on()
        self.mRLP.on()
        self.mRLN.off()
        self.mFRP.off()
        self.mFRN.on()
        self.mFLP.on()
        self.mFLN.off()
        return
    
    def turnCounterClockwise(self, speed):
        self.spd = speed
        self.enRR.duty_u16(self.duty_cycle(self.spd))
        self.enRL.duty_u16(self.duty_cycle(self.spd))
        self.enFR.duty_u16(self.duty_cycle(self.spd))
        self.enFL.duty_u16(self.duty_cycle(self.spd))
        self.mRRP.on()
        self.mRRN.off()
        self.mRLP.off()
        self.mRLN.on()
        self.mFRP.on()
        self.mFRN.off()
        self.mFLP.off()
        self.mFLN.on()
        return
    
    def stop(self):
        self.mRRP.off()
        self.mRRN.off()
        self.mRLP.off()
        self.mRLN.off()
        self.mFRP.off()
        self.mFRN.off()
        self.mFLP.off()
        self.mFLN.off()
        return
    
    def duty_cycle(self, speed): # def duty_cycle(self, speed):
        self.spd = speed
        if self.spd <= 0 or self.spd > 100: # Porcentaje de velocidad entre la duty cycle minima y maxima
            duty_cycle = 0
        else:
            duty_cycle = int(self.min + (self.max - self.min)*(self.spd/100))
        return duty_cycle



