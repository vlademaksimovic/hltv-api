import socket
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))

api_key = os.environ['HOSTEDGRAPHITE_APIKEY']
graphite_connection = ('carbon.hostedgraphite.com', 2003)

allowed_units = ['counter', 'milliseconds', 'code']


def log(key, unit, value):
    if unit not in allowed_units:
        logging.error('Unit [%s] is not an allowed unit type' % unit)
        return

    try:
        data = '{}.hltv-api.{}.{} {}\n'.format(api_key, key, unit, value)
        data = data.encode('utf-8')
        if is_production:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data, graphite_connection)

        logger.info(
            'Emitted metric with key [%s] and value [%s]' % (key, value))

    except socket.error:
        logger.exception('Could not emit metric due to socket problems')

    except UnicodeEncodeError:
        logger.exception(
            'Unable to encode the following string to UTF-8 [%s]' % data)
