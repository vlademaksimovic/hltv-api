import logging
import os
import keen

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_production = bool(os.environ.get('IS_PRODUCTION', default=False))

allowed_units = ['counter', 'milliseconds', 'code']


def log(key, unit, value):
    if unit not in allowed_units:
        logging.error('Unit [%s] is not an allowed unit type' % unit)
        return

    if is_production:
        keen.add_event(key, {
            unit: value
        })

    logger.info(
        'Emitted metric with key [%s] and value [%s]' % (key, value))
