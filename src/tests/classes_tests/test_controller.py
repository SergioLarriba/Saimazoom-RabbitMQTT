import unittest
from unittest.mock import patch, MagicMock
from clases.controller import Controller
from clases.client import Client
from clases.pedido import Pedido

class TestController(unittest.TestCase):
	def setUp(self):
		self.controller = Controller()
  
	def test_loginCliente(self):
			user = "user"
			password = "password"
			cliente = Client(user=user, password=password)
			self.controller.clientes_registrados.append(cliente)
			
			result = self.controller.loginCliente(user, password)
			
			self.assertTrue(result)
  
	@patch('uuid.uuid4', return_value='1234')
	def test_realizarPedido(self, mock_uuid):
			user = "user"
			password = "password"
			cliente = Client(user=user, password=password)
			self.controller.clientes_registrados.append(cliente)
			client_id = cliente.getClientId()
			message = {"client_id": client_id, "product_ids": ["product1", "product2"]}
			
			result = self.controller.realizarPedido(message)
			
			self.assertIsInstance(result, Pedido)
			self.assertEqual(result.getIdPedido(), '1234')		
  
	def test_setEstadoPedido(self):
			user = "user"
			password = "password"
			cliente = Client(user=user, password=password)
			self.controller.clientes_registrados.append(cliente)
			client_id = cliente.getClientId()
			message = {"client_id": client_id, "product_ids": ["product1", "product2"]}
			pedido = self.controller.realizarPedido(message)
			
			result = self.controller.setEstadoPedido(pedido.getIdPedido(), "processed")
			
			self.assertTrue(result)
			self.assertEqual(pedido.getEstadoPedido(), "EN_ALMACEN")

	def test_cancelarPedido(self):
			user = "user"
			password = "password"
			cliente = Client(user=user, password=password)
			self.controller.clientes_registrados.append(cliente)
			client_id = cliente.getClientId()
			message = {"client_id": client_id, "product_ids": ["product1", "product2"]}
			pedido = self.controller.realizarPedido(message)
			
			result = self.controller.cancelarPedido(pedido.getIdPedido())
			
			self.assertTrue(result)
			self.assertEqual(pedido.getEstadoPedido(), "CANCELADO")

	def test_verPedidos(self):
			user = "user"
			password = "password"
			cliente = Client(user=user, password=password)
			self.controller.clientes_registrados.append(cliente)
			client_id = cliente.getClientId()
			message = {"client_id": client_id, "product_ids": ["product1", "product2"]}
			pedido = self.controller.realizarPedido(message)
			
			result = self.controller.verPedidos(client_id)
			
			self.assertEqual(len(result), 1)
			self.assertEqual(result[0], pedido)
  
	def test_getClientFromClientId(self):
			user = "user"
			password = "password"
			cliente = Client(user=user, password=password)
			self.controller.clientes_registrados.append(cliente)
			client_id = cliente.getClientId()
			
			result = self.controller.getClientFromClientId(client_id)
			
			self.assertEqual(result, cliente)

	def test_isClienteRegistrado(self):
			user = "user"
			password = "password"
			cliente = Client(user=user, password=password)
			self.controller.clientes_registrados.append(cliente)
			
			result = self.controller.isClienteRegistrado(user)
			
			self.assertTrue(result)

	def test_getPedidoFromId(self):
			user = "user"
			password = "password"
			cliente = Client(user=user, password=password)
			self.controller.clientes_registrados.append(cliente)
			client_id = cliente.getClientId()
			message = {"client_id": client_id, "product_ids": ["product1", "product2"]}
			pedido = self.controller.realizarPedido(message)
			
			result = self.controller.getPedidoFromId(pedido.getIdPedido())
			
			self.assertEqual(result, pedido)

	def test_containsPedido(self):
			user = "user"
			password = "password"
			cliente = Client(user=user, password=password)
			self.controller.clientes_registrados.append(cliente)
			client_id = cliente.getClientId()
			message = {"client_id": client_id, "product_ids": ["product1", "product2"]}
			pedido = self.controller.realizarPedido(message)
			
			result = self.controller.containsPedido(pedido.getIdPedido())
			
			self.assertTrue(result)
  
  