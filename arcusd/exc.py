class UnknownServiceProvider(Exception):
    def __init__(self, service_provider: str):
        self.message = f'Unknown service provider: {service_provider}'
