import unittest
from clases.delivery import Delivery

class TestDelivery(unittest.TestCase):
	def test_entregarPedido_success(self):
		delivery = Delivery()
		delivery.p_entrega = 1.0
		
		result = delivery.entregarPedido()
		
		self.assertTrue(result)
	
	def test_entregarPedido_failure(self):
		delivery = Delivery()
		delivery.p_entrega = 0.0
		
		result = delivery.entregarPedido()
		
		self.assertFalse(result)

