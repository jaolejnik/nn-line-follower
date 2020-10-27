import Pyro4

remote_robot = Pyro4.Proxy("PYRONAME:test.lf")
remote_robot.run()
