from sre_constants import SRE_FLAG_ASCII
import unittest

from vialis_models import *
from vialis_server import model_params


class Test_car(unittest.TestCase):
    def setUp(self) -> None:

        self.model = environment(56, 56, 13, 13, 12, 7, 13, 11, 13, 'black', 'black')
        self.spawnpoint = spawnpoint("E5", "black", self.model)
        self.spawnpoint2 = spawnpoint("E10", "black", self.model)
        self.car =  self.spawnpoint.spawn_vehicle()
        self.car2 = self.spawnpoint2.spawn_vehicle()
        self.car3 = self.spawnpoint2.spawn_vehicle()

    def test_angel(self):
        self.car.pos = (2, 2)
        self.assertEqual(self.car.get_angle([1, 1]), -135)
        self.assertEqual(self.car.get_angle([0, 0]), -135)
        self.assertEqual(self.car.get_angle([1, 3]), 135)
        self.assertEqual(self.car.get_angle([3, 1]), -45)
        self.car.pos = (0, 0)
        self.assertEqual(self.car.get_angle([3, 3]), 45)
    
    def test_new_pos(self):
        self.car.pos = (5, 5) 
        self.assertEqual(self.car.new_pos_ang(135), ((4,6),(-1, 1), False))
        self.assertEqual(self.car.new_pos_ang(0), ((6,5),(1, 0), True))
        self.assertEqual(self.car.new_pos_ang(90), ((5,6),(0, 1), True))
        self.assertEqual(self.car.new_pos_ang(180), ((4, 5),(-1, 0), True))
        self.assertEqual(self.car.new_pos_ang(-45), ((6,4),(1, -1), False))
        self.assertEqual(self.car.new_pos_ang(45), ((6, 6),(1, 1), False))
    
    def test_move_stop_at_redlight(self):
        for i in range(20):
            self.car.move()
        self.assertEqual(self.car.pos, (25, 41))
    
    def test_move_go_at_greenlight(self):
        for i in range(14):
            self.car.move()
        self.model.step()
        self.assertEqual(self.car.pos, (25, 40))

    def test_move_prevent_collision(self):
        for i in range(20):
            self.car2.move()
        self.assertEqual(self.car2.pos, (35, 18))

        for i in range(20):
            self.car3.move()
        self.assertEqual(self.car3.pos, (36, 18))
    
    def test_move_change_direction(self):
        for i in range(14):
            self.car.move()
        self.model.step()
        
        for i in range(2):
            self.car.move()
        self.assertEqual(self.car.pos, (24, 39))

    # def test_remove_car_from_simulation(self):
    #     self.model.step()
    #     self.car.remove()
    #     print(self.car.unique_id)
    #     if self.car:
    #         # self.fail("Car not removed")
    #         print("fail")
    #     else:
    #         print("pass")

class test_trafficlight_sensors(unittest.TestCase):
    def setUp(self) -> None:

        self.model = environment(56, 56, 13, 13, 12, 7, 13, 11, 13, 'black', 'black')
        self.spawnpoint = spawnpoint("E5", "black", self.model)
        
        self.sensor = self.model.grid.get_cell_list_contents((25, 54))[0]
        self.car = self.spawnpoint.spawn_vehicle()

    def test_detect_car_and_add_to_queue(self):
        self.model.step()
        self.assertIn(self.car, self.sensor.trafficlight.vehicle_queue)
    
    def test_remove_car_from_queue(self):
        for i in range(14):
            self.model.step
        self.assertNotIn(self.car, self.sensor.trafficlight.vehicle_queue)
    
    def test_start_trafficlight_cycle(self):
        for i in range(15):
            self.model.step()
        self.assertEqual(self.sensor.trafficlight.color, "#33BD00")


if __name__ == "__main__":
    unittest.main()