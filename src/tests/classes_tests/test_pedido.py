import unittest
from clases.pedido import *
import uuid

class TestPedido(unittest.TestCase):
	def setUp(self):
		self.client_id = "12345"
		self.product_ids = ["P1", "P2", "P3"]
		self.id_pedido = str(uuid.uuid4())
		self.pedido = Pedido(self.client_id, self.product_ids, self.id_pedido)

	def test_getClientId(self):
		self.assertEqual(self.pedido.getClientId(), self.client_id)

	def test_getProductIds(self):
		self.assertEqual(self.pedido.getProductIds(), self.product_ids)

	def test_getIdPedido(self):
		self.assertEqual(self.pedido.getIdPedido(), self.id_pedido)

	def test_getEstadoPedido(self):
		self.assertEqual(self.pedido.getEstadoPedido(), EnumEstadosPedido.EN_ALMACEN)

	def test_setEstadoPedido(self):
		self.pedido.setEstadoPedido(EnumEstadosPedido.EN_PREPARACION)
		self.assertEqual(self.pedido.getEstadoPedido(), EnumEstadosPedido.EN_PREPARACION)

	def test_cancelarPedido(self):
		self.pedido.cancelarPedido()
		self.assertEqual(self.pedido.getEstadoPedido(), EnumEstadosPedido.CANCELADO)

	def test_sePuedeCancelarPedido(self):
		self.assertTrue(self.pedido.sePuedeCancelarPedido(EnumEstadosPedido.EN_ALMACEN))
		self.assertFalse(self.pedido.sePuedeCancelarPedido(EnumEstadosPedido.ENTREGADO))

	def test_sePuedeProcesarElPedido(self):
		self.assertTrue(self.pedido.sePuedeProcesarElPedido())


