from zeroconf import Zeroconf, ServiceBrowser


class NetworkScanner:
    def __init__(self):
        self.services = {}

    def add_service(self, zeroconf, type_, name):
        info = zeroconf.get_service_info(type_, name)
        if info:
            self.services[name] = info

    def scan_network(self):
        zeroconf = Zeroconf()

        service_types = [
            "_http._tcp.local.",
            "_printer._tcp.local.",
            "_ros-master._tcp.local.",
            # Add more service types as needed
        ]

        for service_type in service_types:
            browser = ServiceBrowser(zeroconf, service_type, self)

        input("Press enter to stop scanning...\n")
        zeroconf.close()

    def print_services(self):
        for name, info in self.services.items():
            print(f"Service Name: {name}")
            print(f"  Address: {info.server}")
            print(f"  IP: {info.addresses}")
            print(f"  Port: {info.port}")
            print(f"  Properties: {info.properties}")
            print()


# Run the network scanner and print discovered services
scanner = NetworkScanner()
scanner.scan_network()
scanner.print_services()
