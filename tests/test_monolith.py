from pycrate import IPV4Address, Monolith


address = IPV4Address("0.0.0.0", 8080)

endpoint = Monolith(address)

