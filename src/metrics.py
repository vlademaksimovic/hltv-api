import socket
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.environ['HOSTEDGRAPHITE_APIKEY']
url = 'carbon.hostedgraphite.com'

allowed_units = ['counter', 'milliseconds']


def log(key, unit, value):
    try:
        if unit not in allowed_units:
            logging.error('Unit [%s] is not an allowed unit type')
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = '{}.hltv-api.{}.{} {}\n'.format(api_key, key, unit, value)
        data = data.encode('utf-8')
        sock.sendto(data, (url, 2003))

    except socket.error:
        logger.exception('Unable to log metric')
