import serial
import time



class COMMUNICATION:

    def __init__(self, port):
        self.serialcom = serial.Serial(port, 9600)
        self.serialcom.timeout = 1
        self.max_errors=5
        self.payload = None
        self.error_count = 0


        time.sleep(2)  # wait for the serial connection to initialize
        print(f"please wait for connection to be made on port: {port}")

        #payload structure is defined as in idea.txt

        self.payload = None
        self.error_count = 0
    def send(self):
        self.serialcom.write(f"{self.payload} \n".encode())
        print("message sent!")
        start_time = time.time()

        while True:
            if self.serialcom.in_waiting > 0:
                response = self.serialcom.readline().decode('ascii').strip()
                if response == "OK":
                    return response
                elif response.startswith("ERR"):
                    return -1

            elif time.time() - start_time > self.serialcom.timeout:
                return -1
            else:
                time.sleep(0.01)  # Small delay to avoid busy waiting

    def handle_response(self, response):
        #process response here
        pass


#always expects id to be first
    def load_payload(self, id, value):
        self.payload=f"{id},{value}"


    def handle_transmission(self, id, value):
        self.load_payload(id, value)
        response=self.send()
        while True:
            if response == -1:
                self.send()
                self.error_count+=1
                if self.error_count==self.max_errors:
                    print("max errors reached, aborting transmission check connection/current payload")
                    self.serialcom.close()
                    break
    def setup(self):
