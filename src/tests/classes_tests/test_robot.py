import unittest
from unittest.mock import patch
from clases.robot import Robot

class TestRobot(unittest.TestCase):
    def setUp(self):
        self.robot = Robot()

    @patch('clases.robot.random.uniform', return_value=0.5)
    @patch('clases.robot.time.sleep', return_value=None)
    def test_realizarTrabajo_all_found(self, mock_sleep, mock_random):
        json_message = {'product_ids': ['product1', 'product2', 'product3']}
        result = self.robot.realizarTrabajo(json_message)
        self.assertEqual(result, (True, ['product1', 'product2', 'product3']))

    @patch('clases.robot.random.uniform', return_value=0.9)
    @patch('clases.robot.time.sleep', return_value=None)
    def test_realizarTrabajo_some_not_found(self, mock_sleep, mock_random):
        json_message = {'product_ids': ['product1', 'product2', 'product3']}
        result = self.robot.realizarTrabajo(json_message)
        self.assertEqual(result, (False, ['product1', 'product2', 'product3']))