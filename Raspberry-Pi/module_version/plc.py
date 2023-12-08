import automationhat

class PLC:
    
    """
    INPUT BIT LABELS:
        [Test?, Is Shaking?, Result Received?]
        
    OUTPUT BIT LABELS:
        [Temp Failed?, Pressure Failed?, Gyro Failed?, Result Ready?, Busy?, Gyro Ready for Shaking?]
    """
    input_codes = {
        "test" : [1, 0, 0],
        "shaking": [0, 1, 0],
        "resultReceived": [0, 0, 1]
    }
    
    output_codes = {
        "result": [0, 0, 0, 1, 1, 0],
        "ready": [0, 0, 0, 0, 0, 0],
        "busy": [0, 0, 0, 0, 1, 0],
        "shakeRequest": [0, 0, 0, 0, 1, 1]
    }
    
    nBitsToPLC = 6
    nBitsFromPLC = 3
    
    def __init__(self):
        self.inputs = [0, 0, 0]
        
        if automationhat.is_automation_hat():
            automationhat.light.power.write(1)

    def get_signal(self):
        # INPUTS: digital signals from the PLC
        # METHOD: cross ref these signals with our code assignments
        # OUTPUT: a sensor ("temperature", "pressure" or "acceleration") or None (TO CHANGE)
        
        self.inputs = [automationhat.input[i].read() for i in range(self.nBitsFromPLC)]
        
        try:
            matching_input = list(self.input_codes.keys())[list(self.input_codes.values()).index(self.inputs)]
            return matching_input
        except ValueError:
            return None

    def set_signal(self, signal, testResults=None):
        # print(f"Sending PLC signal {signal} with test results {testResults}")
        
        matching_output = self.output_codes[signal]
        
        # add test results to output
        # note that failed tests give output of 1
        if testResults != None:
            for index in range(len(testResults)):
                matching_output[index] = not testResults[index]
                
        matching_output = [1 - x for x in matching_output] # flip each bit
                
        # display output (first half are output pins, second are relay pins, but functionally the same) 
        for i in range(self.nBitsToPLC):
            if i < 3:
                automationhat.output[i].write(matching_output[i])
            else:
                automationhat.relay[i % 3].write(matching_output[i])
    
    def get_raw(self):
        return [automationhat.input[i].read() for i in range(self.nBitsFromPLC)]
    
    def set_raw(self, signal):
         for i in range(self.nBitsToPLC):
            if i < 3:
                automationhat.output[i].write(signal[i])
            else:
                automationhat.relay[i % 3].write(signal[i])       