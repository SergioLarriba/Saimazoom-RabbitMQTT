from tabulate import tabulate

def print_pretty(json_message):
	# Convertir el mensaje de JSON en una tabla 
	table = [[key, value] for key, value in json_message.items()]
	print(tabulate(table, headers=["Key", "Value"], tablefmt="pretty"))