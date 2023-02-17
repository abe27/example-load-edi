from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

def main():
    try:
        remote_factory = PiGPIOFactory(host='192.168.101.189')
        led_1 = LED(17)  # local pin
        led_2 = LED(17, pin_factory=remote_factory)  # remote pin

        while True:
            led_1.on()
            led_2.off()
            sleep(1)
            led_1.off()
            led_2.on()
            sleep(1)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()