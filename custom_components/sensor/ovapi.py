"""
Support for real-time departure information for public transport in the Netherlands.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.ovapi/
"""
import logging
from datetime import timedelta

from copy import deepcopy
import voluptuous as vol
import requests

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.util import Throttle
from homeassistant.const import (
    CONF_NAME, ATTR_ATTRIBUTION, STATE_UNKNOWN
)

REQUIREMENTS = ['requests==1.1.4']

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=1)

CONF_LOCATIONS = 'locations'
CONF_STOPAREA = 'stoparea'
CONF_TIMINGPOINT = 'timingpoint'
CONF_DESTINATIONS = 'destinations'
# CONF_DIRECTIONS = 'directions'
# CONF_LINES = 'lines'
# CONF_PRODUCTS = 'products'
# CONF_TIMEOFFSET = 'timeoffset'
# CONF_NUMBER = 'number'

DEFAULT_PRODUCT = ['metro', 'bus', 'train', 'tram', 'boat']

ICONS = {
    'METRO': 'mdi:subway',
    'TRAM': 'mdi:tram',
    'BUS': 'mdi:bus',
    'TRAIN': 'mdi:train',
    'BOAT': 'mdi:boat',
    'UNKNOWN': 'mdi:clock'
}
ATTRIBUTION = "Data provided by ovapi.nl"

SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_LOCATIONS): [{
        vol.Optional(CONF_STOPAREA): cv.string,
        # vol.Optional(CONF_TIMINGPOINT): cv.string,
        # vol.Optional(CONF_DESTINATIONS, default=['']): cv.ensure_list_csv,
        # vol.Optional(CONF_DIRECTIONS, default=['']): cv.ensure_list_csv,
        # vol.Optional(CONF_LINES, default=['']): cv.ensure_list_csv,
        # vol.Optional(CONF_PRODUCTS, default=DEFAULT_PRODUCT):
        #     cv.ensure_list_csv,
        # vol.Optional(CONF_TIMEOFFSET, default=0): cv.positive_int,
        # vol.Optional(CONF_NUMBER, default=1): cv.positive_int,
        vol.Optional(CONF_NAME): cv.string}]
})

DEFAULT_HEADER = {
    'user-agent': 'Home Assistant',
}


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the OVAPI sensor."""
    sensors = []

    for station in config.get(CONF_LOCATIONS):
        sensors.append(
            OVApiSensor(
                station.get(CONF_STOPAREA),
                station.get(CONF_NAME)))

    add_entities(sensors, True)


class OVApiSensor(Entity):
    """Implementation of an OVAPI sensor."""

    def __init__(self, stoparea, name):
        """Initialize the sensor."""
        self._stoparea = stoparea
        self._name = name
        self._icon = ICONS['UNKNOWN']

        self.api = OV_API(stoparea)

        self._attributes = None
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        if self._name:
            return self._name
        return self._stoparea

    @property
    def state(self):
        """Return the next departure time."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return "min"

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data and update the state."""
        departures = self.api.get_departures()

        if not departures:
            self._state = '-'
            self._icon = ICONS['unknown']
        else:
            self._state = departures[0].get('ExpectedArrivalTime', '-').lower()
            self._icon = ICONS[departures[0].get(
                'TransportType', 'UNKNOWN')]

            self._attributes = {
                ATTR_ATTRIBUTION: ATTRIBUTION,
                **departures[0]
            }

            self._attributes['departures'] = deepcopy(departures[:10])


class OV_API(object):
    """ Interface class for the OV API """

    def __init__(self, stopAreaCode):
        """ Constructor """
        self.stopAreaCode = stopAreaCode
        # TODO check if StopAreaCode exists

    def get_departures(self):
        departures = []

        try:
            response = requests.request(
                'GET', 'https://v0.ovapi.nl/stopareacode/' + self.stopAreaCode + '/departures', headers={})
            data = response.json()
        except Exception:
            raise(Exception())

        for key, stoparea in data.items():
            for timingpoint in stoparea:
                for lines in stoparea[timingpoint]['Passes']:
                    line = stoparea[timingpoint]['Passes'][lines]
                    line['TransportTypeIcon'] = ICONS[line['TransportType']]
                    departures.append(line)

            departures.sort(key=lambda x: x["ExpectedArrivalTime"])

        return departures
