from homeassistant.components.sensor import SensorEntity
from homeassistant.util import dt as dt_util
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    fns = hass.data["flag_protocol"][entry.entry_id]
    async_add_entities([
        FlagProtocolSensor(hass, fns["get_flag_status"]),
        NextFlagCountdownSensor(hass, fns["get_next_flag_day"])
    ])

class FlagProtocolSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(self, hass: HomeAssistant, get_flag_status):
        self.hass = hass
        self._get_flag_status = get_flag_status
        self._attr_name = "Flag Protocol"
        self._attr_unique_id = "flag_protocol_main"
        self._attr_icon = "mdi:flag"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        now = dt_util.now()
        sun = self.hass.states.get("sun.sun")
        elevation = sun.attributes.get("elevation", 0) if sun else 0

        flag_type, reason = self._get_flag_status(now)
        if elevation <= 3:
            flag_type = "no_flag"
            reason = "Flag not allowed - sun too low"

        # dynamic icon
        icon_map = {
            "full_mast": "mdi:flag",
            "half_mast": "mdi:flag-outline",
            "full_mast_with_banner": "mdi:flag-variant",
            "no_flag": "mdi:flag-off"
        }

        self._attr_native_value = flag_type
        self._attr_icon = icon_map.get(flag_type, "mdi:flag")
        self._attr_extra_state_attributes = {
            "reason": reason
        }

class NextFlagCountdownSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(self, hass: HomeAssistant, get_next_flag_day):
        self.hass = hass
        self._get_next_flag_day = get_next_flag_day
        self._attr_name = "Next Flag Day Countdown"
        self._attr_unique_id = "flag_protocol_next_countdown"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        now = dt_util.now()
        days_until, next_reason, next_flag_type = self._get_next_flag_day(now)

        self._attr_native_value = days_until
        self._attr_extra_state_attributes = {
            "next_reason": next_reason,
            "next_flag_type": next_flag_type
