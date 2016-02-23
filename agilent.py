from numpy import *

class SpectrumAnalyzer(object):
    def __init__(self, rm):
        self.inst = rm.get_instrument("GPIB::3::INSTR")
        print("Communications established with " + self.inst.ask("ID?"))

        # Restore instrument presets and configure single-sweep mode
        self.inst.write("IP;SNGLS;")
        self.inst.write("DATEMODE DMY;") # Set UK date format

        # Number of sample points
        # TODO: Check that this is always true!
        self.nf = 401

    def close(self):
        print("Closing spectrum analyzer")
        self.inst.close()

    def reset(self):
        '''Reset to default state'''
        self.inst.write("IP;SNGLS;")

    def get_id(self):
        '''Return the identity string of this device'''
        return self.inst.ask("ID?;")

    def get_input_impedence(self):
        '''Return the input impedence of the instrument'''
        return self.inst.ask_for_values("INZ?")[0];

    def take_sweep(self):
        '''Take a spectral sweep and return the data values'''
        self.inst.write("TS;")
        return self.inst.ask_for_values("TRA?;")

    def set_start_frequency(self, freq):
        '''Set the start frequency in Hz'''
        self.inst.write("FA " + str(freq))

    def get_start_frequency(self):
        '''Get the start frequency in Hz'''
        return self.inst.ask_for_values("FA?")[0]

    def set_center_frequency(self, freq):
        '''Set the centre frequency in Hz'''
        self.inst.write("CF " + str(freq))

    def get_center_frequency(self):
        '''Returns the centre frequency in Hz'''
        return self.inst.ask_for_values("CF?")[0]

    def set_stop_frequency(self, freq):
        '''Set the stop frequency in Hz'''
        self.inst.write("FB " + str(freq))[0]

    def get_stop_frequency(self):
        '''Get the stop frequency in Hz'''
        return self.inst.ask_for_values("FB?")[0]

    def set_frequency_span(self, span):
        '''Set the frequency span for a sweep in Hz'''
        self.inst.write("SP " + str(span))

    def get_frequency_span(self):
        '''Get the frequency span in Hz'''
        return self.inst.ask_for_values("SP?")[0]

    def set_frequency_range(self, start, stop):
        '''Set the start and end frequencies for a sweep'''
        self.inst.write("FA " + str(start) + ";FB " + str(stop))

    def get_frequency_array(self):
        '''Get the array of all frequencies'''
        fa = self.get_start_frequency()
        fb = self.get_stop_frequency()
        return linspace(fa, fb, num=self.nf)

    def save_trace(self, filename):
        '''Save the trace to file'''
        trace = self.take_sweep()
        f = self.get_frequency_array()
        #output = array(f, trace)
        #print(filename, output)
        savetxt(filename, column_stack((f,trace)))
        
    def set_sweep_time(self, time):
        '''Set the sweep time in s'''
        self.inst.write("ST " + str(time))

    def set_resolution_bandwidth(self, bandwidth):
        '''Set resolution bandwidth in Hz'''
        self.inst.write("RB " + str(bandwidth))

    def get_resolution_bandwidth(self):
        '''Get the resolution bandwidth in Hz'''
        return self.inst.ask_for_values("RB?;")[0]

    def place_marker_at_peak(self):
        '''Places the marker at the highest peak'''
        self.inst.write("MKPK HI;")

    def get_marker_frequency(self):
        '''Read the marker frequency in Hz'''
        return self.inst.ask_for_values("TDF P;MKREAD FRQ;MKF?;")[0]

    def get_marker_amplitude(self):
        '''Read the amplitude of the marker'''
        return self.inst.ask("MKA?")

    def get_marker_3dB_bandwidth(self):
        '''Read the 3dB bandwidth of the peak around the marker'''
        return self.inst.ask("MKBW -3?")
    
    def draw_alex(self):
        '''Draw a little picture of Alex'''
        self.inst.write("CLRDSP")
        self.inst.write("BLANK TRA")
        self.inst.write("ANNOT OFF")
        self.inst.write("GRAT OFF")
        self.inst.write("MENU OFF")
        self.inst.write("DRAWBOX 150,0, 150,50")
        self.inst.write("DRAWBOX 250,0 ,250,50")
        self.inst.write("DRAWBOX 150,50,250,50")
        self.inst.write("DRAWBOX 200,50,200,125")  # torso
        self.inst.write("DRAWBOX 150,125,250,175") # head
        self.inst.write("DRAWBOX 160,160,180,170")
        self.inst.write("DRAWBOX 210,160,230,170")
        self.inst.write("DRAWBOX 160,135,210,140,2,2") # mouth
        self.inst.write("DRAWBOX 150,125,225,147,4,4") # beard
        self.inst.write("DRAWBOX 150,175,250,180,4,4") # hair
        self.inst.write("DRAWBOX 125,100,220,100")
        self.inst.write("DRAWBOX 220,100,220,70")
        self.inst.write("PU;PA10,170;TEXT%\"Paul,\r\nI figured out\r\nthe API for the\r\nold spectrum\r\nanalyzer.\r\n\r\n  Alex xx\"%")
        
    def __del__(self):
        close()
