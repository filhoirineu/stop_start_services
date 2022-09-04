class ServiceInfo():
    def __init__(self, id, section, display_name, service_name, process_name):
        self.id = id.upper()
        self.section = section.upper()
        self.display_name = display_name.upper()
        self.service_name = service_name.upper()
        self.process_name = process_name.upper()