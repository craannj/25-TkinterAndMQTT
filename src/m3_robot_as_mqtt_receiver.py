"""
Using a Brickman (robot) as the receiver of messages.
"""

# Same as m2_fake_robot_as_mqtt_sender,
# but have the robot really do the action.
# Implement just FORWARD at speeds X and Y is enough.
import mqtt_remote_method_calls as com
import time
import ev3dev.ev3 as ev3
import math

class DelegateThatReceives(object):

    def forward(self, x, y):
        robot = SimpleRoseBot()
        robot.go(x, y)
        print("forward", x, y)

    def stop(self):
        robot = SimpleRoseBot()
        robot.stop()
        print('stop')


def main():
    name1 = input("Enter one name (subscriber): ")
    name2 = input("Enter another name (publisher): ")

    my_delegate = DelegateThatReceives()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect(name1, name2)
    time.sleep(1)  # Time to allow the MQTT setup.
    print()

    while True:
        time.sleep(0.01)  # Time to allow message processing


class SimpleRoseBot(object):

    def __init__(self):
        self.left_motor = Motor('B')
        self.right_motor = Motor('C')

    def go(self, left_wheel_speed, right_wheel_speed):
        self.left_motor.turn_on(left_wheel_speed)
        self.right_motor.turn_on(right_wheel_speed)

    def stop(self):
        self.left_motor.turn_off()
        self.right_motor.turn_off()

    def go_straight_for_seconds(self, seconds, speed):
        self.left_motor.turn_on(speed)
        self.right_motor.turn_on(speed)
        start = time.time()
        while True:
            current = time.time()
            if current - start >= seconds:
                break
        self.left_motor.turn_off()
        self.right_motor.turn_off()


class Motor(object):
    WheelCircumference = 1.3 * math.pi

    def __init__(self, port):  # port must be 'B' or 'C' for left/right wheels
        self._motor = ev3.LargeMotor('out' + port)

    def turn_on(self, speed):  # speed must be -100 to 100
        self._motor.run_direct(duty_cycle_sp=speed)

    def turn_off(self):
        self._motor.stop(stop_action="brake")

    def get_position(self):  # Units are degrees (that the motor has rotated).
        return self._motor.position

    def reset_position(self):
        self._motor.position = 0


main()
