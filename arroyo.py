from visa import constants

class CurrentSource(object):
    def __init__(self, rm):
        '''Connect to Arroyo 4302 current source on serial port 5'''
        self.arroyo = rm.get_instrument("ASRL5::INSTR")
        
        # Set serial comm parameters
        self.arroyo.baud_rate = 38400
        self.arroyo.timeout   = 500
        self.arroyo.write_termination = '\n'
        self.arroyo.send_end  = True
        self.arroyo.data_bits = 8
        self.arroyo.stop_bits = constants.StopBits['one']
        self.arroyo.parity    = constants.Parity['none']
        response = self.arroyo.ask("*IDN?")
        print("Communications established with " + response)

    def set_output_current(self, I):
        '''Set the output current in mA'''
        self.arroyo.write("LASER:LDI " + str(I))

    def get_voltage(self):
        '''Get the measured voltage in V'''
        return self.arroyo.query_ascii_values("LASER:LDV?")[0]

    def enable_output(self, enable):
        '''Enable or disable output current'''
        if enable:
            self.arroyo.write("LASER:OUTPUT 1")
        else:
            self.arroyo.write("LASER:OUTPUT 0")

    def close(self):
        print("Closing current source")
        self.enable_output(False)
        self.arroyo.close()
  
    def __del__(self):
        self.close()
