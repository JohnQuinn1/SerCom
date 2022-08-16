import serial
import typing

class SerCom:
    """Class to send and receive strings over serial connections
    and which handles multiple serial port openings gracefully.
    The class internally takes care of encoding and translating
    line endings.

    The class member "serial" is an instance of serial.Serial 
    and can be used to call additional pyserial functions such
    as flush() etc. 

    Notes: RBD 9103 Picoammater needs baudrate of 57600
           Rapsberry Pi Pico needs baudrate of 9600"""
    
    configured_ports = dict()
    
    def __init__(
        self,
        port: str = "com4",
        baudrate: int = 57600,  
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        xonxoff: bool = False,
        timeout: float = 1.0,
    ):
        """Open a serial connection with given parameters.
        For help on the options see the serial.Serial help."""

        self.port = port

        self.serial = self.__class__.configured_ports.get(port)
        
        if self.serial:
            print(f"Port {self.port} has already been configured - reopening")
            if not self.serial.is_open:
                self.serial.open()
        else:
            self.serial = serial.Serial(
                port = port,
                baudrate = baudrate,
                bytesize = bytesize,
                parity = parity,
                stopbits = stopbits,
                xonxoff = xonxoff,
                timeout = timeout,
            )
        
            self.__class__.configured_ports[self.port] = self.serial

        
    def print_config(self) -> None:
        """Print the port configuration"""
    
        print(self.serial)
    
    
    def send(self, text: str) -> None:
        """send a string to the serial device"""

        self.serial.write(bytes(text + "\n", "utf-8"))


    def readline(self) -> str:
        """read one line (\n terminated) from the serial device"""

        return self.serial.readline().decode("utf-8").rstrip()

    
    def readlines(self) -> typing.List[str]:
        """read multiple lines from the serial device.
        Returns a list of strings with one string for each line read.
        Needs timeout to be set to know when to end."""

        lines = self.serial.readlines()
        return [line.decode("utf-8").rstrip() for line in lines]
        
    
