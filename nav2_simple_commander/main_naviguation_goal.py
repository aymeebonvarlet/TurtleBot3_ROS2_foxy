import working_on_foxy as wf
import rclpy

def main() :
    rclpy.init()

    navigator = wf.BasicNavigatorFoxy()

    navigator.patrol_demo()

    exit(0)

if __name__ == '__main__':
    main()