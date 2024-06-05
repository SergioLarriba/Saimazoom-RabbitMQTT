import unittest
from clases.client import Client
import uuid
from clases.pedido import *

class TestClient(unittest.TestCase):
	def setUp(self):
		self.client = Client("username", "password")
	
	def test_registrarCliente(self):
		self.client.registrarCliente()
		self.assertTrue(self.client.isRegistrado())
	
	def test_getRegistrado(self):
		self.assertFalse(self.client.getRegistrado())
		self.client.registrarCliente()
		self.assertTrue(self.client.getRegistrado())
	
	def test_getUser(self):
		self.assertEqual(self.client.getUser(), "username")
	
	def test_getPassword(self):
		self.assertEqual(self.client.getPassword(), "password")
	
	def test_isRegistrado(self):
		self.assertFalse(self.client.isRegistrado())
		self.client.registrarCliente()
		self.assertTrue(self.client.isRegistrado())
	
	
