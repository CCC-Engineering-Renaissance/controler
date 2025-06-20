import socket
import os

from inputs import get_gamepad, devices
import math
import threading

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self, gamepad):
        self.gamepad = gamepad
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this methode
        x = self.LeftJoystickX
        y = self.LeftJoystickY
        a = self.A
        b = self.X # b=1, x=2
        rb = self.RightBumper
        return [x, y, a, b, rb]


    def _monitor_controller(self):
        while True:
            events = self.gamepad.read()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

SERVER_IP = '192.168.8.117'  # or your server's IP
SERVER_PORT = 12345

joyROV = XboxController(devices.gamepads[0])
joyClaw = XboxController(devices.gamepads[1])

pushed = False

# Create a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(2.0)  # Optional: timeout in seconds
    pitchAngle = 0;
    yawAngle = 0;
    als = False
    test = 0

    # Send message to serve
    while True:
        if als:
            pitchAngle += pow(joyROV.RightJoystickY, 3) * .001 ;
            yawAngle += pow(joyROV.RightJoystickX, 3) * .001 ;

        if (pushed == True and joyROV.Y == 0):
            als = not als

        if (joyROV.Y == 1):
            pushed = True
        else:
            pushed = False

        out = 0
        if als:
            out = 1



        if pitchAngle < -180:
            pichAngle = 180
        elif pitchAngle > 180:
            pitchAngle = -180

        scale =0.5 
        if (joyROV.A == 1):
            scale = 1.0
        if (joyROV.B == 1):
            scale = 0.25
        if (joyROV.X == 1):
            scale = 1.5
        MESSAGE = (
            str(joyROV.LeftJoystickY * scale * 1.5) + " " +
            str(joyROV.LeftJoystickX * scale * -1) + " " +
            str((joyROV.RightTrigger - joyROV.LeftTrigger) / -3.0 * scale) + " " +
            str(joyROV.RightJoystickX * 0.66 * scale * -2) + " " +
            str(joyROV.RightJoystickY * 0.66 *scale * 2) + " " +
            str((joyROV.RightBumper - joyROV.LeftBumper) * 1 * scale) + " " +
           # str(round(pow(joyClaw.RightJoystickY, 3), 1) * .3) + " " +
           # str(round(pow(joyClaw.LeftJoystickY, 3), 1) * 0.8) + " " +
           # str(round(pow(joyClaw.RightJoystickX, 3), 1) * 0.2) + " " +
           # str(round(pow(joyClaw.LeftJoystickX, 3), 1) * 0.5)   

            str(round(joyClaw.RightJoystickY, 1) * .4) + " " +
            str(int(joyClaw.B) - int(joyClaw.A) * 1.4 ) + " " +
           # str(round(pow(joyClaw.RightJoystickX, 3), 1) * 0.15) + " " +
            str(round(pow(0, 3), 1) * 0.15) + " " +
            str((pow(joyClaw.LeftJoystickY, 3)) * -0.25) + " " +
            str(pitchAngle) + " " + 
            str(yawAngle) + " " + 
            str(out)
        )
        #os.system("clear")
        print(
            "X: {:.2f}".format(joyROV.LeftJoystickY),
            "Y: {:.2f}".format(joyROV.LeftJoystickX),
            "Z: {:.2f}".format((joyROV.RightTrigger - joyROV.LeftTrigger) / 4.0),
            "Roll: {}".format(joyROV.RightBumper - joyROV.LeftBumper),
            "Pitch: {:.2f}".format(joyROV.RightJoystickY),
            "Yaw: {:.2f}".format(joyROV.RightJoystickX),
            "Claw Pitch: {:.1f}".format(pow(joyClaw.RightJoystickY * -1, 3)),
            "Claw Yaw: {:.1f}".format(joyClaw.RightTrigger - joyClaw.LeftTrigger),
            "Claw2 Open: {:.1f}".format(joyClaw.RightJoystickX),
            "Claw Yaw: {:.1f}".format(joyClaw.LeftJoystickX),
            "Angle: {:.1f}".format(pitchAngle),
            "Angle: {:.1f}".format(yawAngle),
            als
        )
        sock.sendto(MESSAGE.encode(), (SERVER_IP, SERVER_PORT))
        #print(f"Sent: {MESSAGE}")

