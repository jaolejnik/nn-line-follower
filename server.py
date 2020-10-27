import Pyro4

from robot.linefollower import LineFollower

robot = LineFollower(50, 0.1)

daemon = Pyro4.Daemon(host="192.168.1.106")
name_server = Pyro4.locateNS()
uri = daemon.register(robot)
name_server.register("test.lf", uri)

print("READY")
daemon.requestLoop()
