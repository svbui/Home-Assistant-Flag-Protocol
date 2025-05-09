from homeassistant.components.sensor import SensorEntity
from homeassistant.util import dt as dt_util
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import logging

from .const import DOMAIN, COUNTRIES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    fns = hass.data[DOMAIN][entry.entry_id]
    country = entry.data.get("country")
    async_add_entities([
        FlagProtocolSensor(hass, fns["get_flag_status"], country, entry.entry_id),
        NextFlagCountdownSensor(hass, fns["get_next_flag_day"], country, entry.entry_id)
    ])

class FlagProtocolSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(self, hass: HomeAssistant, fn_get, country: str, entry_id: str):
        self.hass = hass
        self._fn = fn_get
        self._country = country
        self._entry_id = entry_id
        # Unique per country
        self._attr_unique_id = f"{DOMAIN}_{country}_main"
        # Display name includes country
        display = COUNTRIES.get(country, country)
        self._attr_name = f"Flag Protocol ({display})"
        self._attr_icon = "mdi:flag"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        now = dt_util.now()
        sun = self.hass.states.get("sun.sun")
        elevation = sun.attributes.get("elevation", 0) if sun else 0

        flag_type, reason = self._fn(now)
        if elevation <= 3:
            flag_type, reason = "no_flag", "Flag not lit"

        icon_map = {
            "full_mast": "mdi:flag",
            "half_mast": "mdi:flag-outline",
            "full_mast_with_banner": "mdi:flag-variant",
            "no_flag": "mdi:flag-off"
        }

        self._attr_native_value = flag_type
        self._attr_icon = icon_map.get(flag_type, "mdi:flag")
        self._attr_extra_state_attributes = {"reason": reason}

class NextFlagCountdownSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(self, hass: HomeAssistant, fn_next, country: str, entry_id: str):
        self.hass = hass
        self._fn_next = fn_next
        self._country = country
        self._entry_id = entry_id
        self._attr_unique_id = f"{DOMAIN}_{country}_next_countdown"
        display = COUNTRIES.get(country, country)
        self._attr_name = f"Next Flag Day Countdown ({display})"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        now = dt_util.now()
        days_until, next_reason, next_flag_type = self._fn_next(now)
        self._attr_native_value = days_until
        self._attr_extra_state_attributes = {
            "next_reason": next_reason,
            "next_flag_type": next_flag_type
        }
