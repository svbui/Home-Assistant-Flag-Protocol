"""Binary sensor indicating whether today is an official flag day."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import COUNTRY_MODULES, COUNTRIES


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    country = entry.data["country"]
    async_add_entities([FlagTodayBinarySensor(entry.entry_id, country)], True)


class FlagTodayBinarySensor(BinarySensorEntity):
    """Report whether the country's flag rules specify a flag day today.

    Unlike the main flag sensor, this intentionally ignores sun elevation:
    an official flag day remains a flag day after sunset.
    """

    _attr_should_poll = True

    def __init__(self, entry_id: str, country: str) -> None:
        self._attr_unique_id = f"{entry_id}_flag_today"
        self._attr_name = f"Flag Today ({COUNTRIES.get(country, country)})"
        self._module = COUNTRY_MODULES[country]
        self._attr_is_on = False

    async def async_update(self) -> None:
        flag_type, _ = self._module.get_flag_status(dt_util.now())
        self._attr_is_on = flag_type != "no_flag"
