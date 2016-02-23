from enum import Enum

class Imodes(Enum):
    '''The set of possible current input modes'''
    off            = 0 # i.e., use voltage mode instead
    high_bandwidth = 1
    low_noise      = 2

class Vmodes(Enum):
    '''The set of possible voltage input modes'''
    grounded  = 0
    A         = 1
    minus_B   = 2
    A_minus_B = 3

class InputDevices(Enum):
    '''The set of possible input devices'''
    bipolar = 0 # 10 kohm, 2 nV/root(Hz) voltage noise @ 1 kHz
    FET     = 0 # 10 Mohm, 5 nV/root(Hz) voltage noise @ 1 kHz

class InputShieldSettings(Enum):
    '''The set of possible settings for the input connector shield'''
    ground   = 0
    floating = 1 # Connected to ground via a 1 kohm resistor

class CouplingModes(Enum):
    '''The set of possible input coupling modes'''
    AC = 0
    DC = 1

class SensitivityModes(Enum):
    '''The set of possible input sensitivity modes'''
    mode_1  = (1,    2e-9,   2e-15,     0)
    mode_2  = (2,    5e-9,   5e-15,     0)
    mode_3  = (3,   10e-9,  10e-15,     0)
    mode_4  = (4,   20e-9,  20e-15,     0)
    mode_5  = (5,   50e-9,  50e-15,     0)
    mode_6  = (6,  100e-9, 100e-15,     0)
    mode_7  = (7,  200e-9, 200e-15,   2e-15)
    mode_8  = (8,  500e-9, 500e-15,   5e-15)
    mode_9  = (9,    1e-6,   1e-12,  10e-15)
    mode_10 = (10,   2e-6,   2e-12,  20e-15)
    mode_11 = (11,   5e-6,   5e-12,  50e-15)
    mode_12 = (12,  10e-6,  10e-12, 100e-15)
    mode_13 = (13,  20e-6,  20e-12, 200e-15)
    mode_14 = (14,  50e-6,  50e-12, 500e-15)
    mode_15 = (15, 100e-6, 100e-12,   1e-12)
    mode_16 = (16, 200e-6, 200e-12,   2e-12)
    mode_17 = (17, 500e-6, 500e-12,   5e-12)
    mode_18 = (18,   1e-3,   1e-9,   10e-12)
    mode_19 = (19,   2e-3,   2e-9,   20e-12)
    mode_20 = (20,   5e-3,   5e-9,   50e-12)
    mode_21 = (21,  10e-3,  10e-9,  100e-12)
    mode_22 = (22,  20e-3,  20e-9,  200e-12)
    mode_23 = (23,  50e-3,  50e-9,  500e-12)
    mode_24 = (24, 100e-3, 100e-9,    1e-9)
    mode_25 = (25, 200e-3, 200e-9,    2e-9)
    mode_26 = (26, 500e-3, 500e-9,    5e-9)
    mode_27 = (27,      1,   1e-6,   10e-9)

class ACGainModes(Enum):
    '''The set of possible gain modes'''
    mode_0 = (0, 0)
    mode_1 = (1, 10)
    mode_2 = (2, 20)
    mode_3 = (3, 30)
    mode_4 = (4, 40)
    mode_5 = (5, 50)
    mode_6 = (6, 60)
    mode_7 = (7, 70)
    mode_8 = (8, 80)
    mode_9 = (9, 90)

# Driver for a Signal Recovery 7265 Lock-in amplifier
class LockIn7265(object):
    def __init__(self, rm):
        self.inst = rm.get_instrument("GPIB0::10::INSTR")
        print("Communications established with " + self.inst.ask("ID?"))

    #### SETTINGS FOR SIGNAL CHANNEL ####
    def set_imode(self, Imode):
        '''Set the current input mode'''
        self.inst.write("IMODE " + str(Imode.value))

    def get_imode(self):
        '''Read the current input mode'''
        return self.inst.query_ascii_values("IMODE")[0]
    
    def set_vmode(self, Vmode):
        '''Set the voltage input mode. Note that Imode takes priority'''
        self.inst.write("VMODE " + str(Vmode.value))

    def get_vmode(self):
        '''Read the voltage input mode'''
        return self.inst.query_ascii_values("VMODE")[0]
    
    def set_input_device(self, InputDevice):
        '''Set the input device for voltage mode'''
        self.inst.write("FET " + str(InputDevice.value))

    def set_input_shield(self, InputShieldSettings):
        '''Set the input connector shield mode'''
        self.inst.write("FLOAT " + str(InputShieldSetting.value))

    def set_coupling_mode(self, CouplingMode):
        '''Set the input coupling mode'''
        self.inst.write("CP " + str(CouplingMode.value))

    def get_magnitude(self):
        '''Get the magnitude of the signal in V'''
        return self.inst.query_ascii_values("MAG.")[0]

    def set_sensitivity(self, SensitivityMode):
        '''Set the sensitivity mode'''
        imode = int(self.get_imode())
        requested_sensitivity = SensitivityMode.value[imode + 1]

        if (requested_sensitivity == 0.0):
            raise ValueError("Cannot use this sensitivity with the current mode") 
        else:
            self.inst.write("SEN " + str(SensitivityMode.value[0]))

    def set_sensitivity_auto(self):
        '''Automatically set sensitivity such that magnitude is 30-90% full-scale'''
        self.inst.write("AS")
    
    def get_sensitivity(self):
        '''Get the sensitivity in V or A, depending on mode'''
        return self.inst.query_ascii_values("SEN.")[0]

    def set_auto_measure(self):
        '''Automatically adjust sensitivity so that magnitude is 30-90% full-scale and then auto-phase to maximise X and minimise Y'''
        self.inst.write("ASM")

    def set_ac_gain(self, ACGainMode):
        '''Set the AC gain on the input channel'''
        self.inst.write("ACGAIN " + str(ACGainMode.value[0]))

    def get_ac_gain(self):
        '''Get the AC gain in dB'''
        mode_index = self.inst.query_ascii_values("ACGAIN")[0]

        # Search for mode in the list of acceptable values and return the gain
        for mode in ACGainModes:
            if mode_index == mode.value[0]:
                return mode.value[1]

    def enable_auto_gain(self, enable = True):
        '''Enable automated setting of the AC Gain'''
        self.inst.write("AUTOMATIC " + str(int(enable)))

    def get_time_constant(self):
        '''Get the integration time-constant in s'''
        return self.inst.query_ascii_values("TC.")[0]

    def close(self):
        print("Closing Lock-in amplifier")
        self.inst.close()

    def reset(self):
        '''Reset to default state'''
        #self.inst.write("IP;SNGLS;")

    def get_id(self):
        '''Return the identity string of this device'''
        return self.inst.ask("ID?;")

    def __del__(self):
        self.close()
