import working_on_foxy as wf
import rclpy

def main() :
    rclpy.init()

    navigator = wf.BasicNavigatorFoxy()
    security_route = [
            [-0.138, 0.462],
            [3.08, 2.6],
            [2.46, -0.564],
            [1.96, 0.591]]
    navigator.patrol_demo(security_route)

    exit(0)

if __name__ == '__main__':
    main()