import yaml
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)


class Configuration(object):
    def __init__(self):
        self.configuration_file = "application.yml" # Euuuuuurk !
        self.configuration_data = None

        f = open(self.configuration_file, 'r')
        self.configuration_data = yaml.load(f.read())
        f.close()

    def get_rabbitmq_host(self):
        return self.configuration_data['rabbitmq-server']['server']

    def get_rabbitmq_port(self):
        return self.configuration_data['rabbitmq-server']['port']

    def get_rabbitmq_vhost(self):
        return self.configuration_data['rabbitmq-server']['credentials']['vhost']

    def get_rabbitmq_password(self):
        return self.configuration_data['rabbitmq-server']['credentials']['password']

    def get_rabbitmq_username(self):
        return self.configuration_data['rabbitmq-server']['credentials']['username']

    def get_messaging_conversion_exchange(self):
        return self.configuration_data['conversion']['messaging']['rabbitmq']['conversion-exchange']

    def get_messaging_conversion_queue(self):
        return self.configuration_data['conversion']['messaging']['rabbitmq']['conversion-queue']

    def get_video_status_callback_url(self):
        return self.configuration_data['conversion']['messaging']['video-status']['url']
