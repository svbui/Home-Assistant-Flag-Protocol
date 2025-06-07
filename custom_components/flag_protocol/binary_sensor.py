from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import COUNTRY_MODULES, COUNTRIES, DOMAIN



async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    country = entry.data["country"]
    name = COUNTRY_MODULES[country].__name__.split(".")[-1].upper()
    async_add_entities([FlagTodayBinarySensor(entry.entry_id, name, country)], True)


class FlagTodayBinarySensor(BinarySensorEntity):
    def __init__(self, entry_id: str, name: str, country: str) -> None:
        self._country = country
        self._attr_unique_id = f"{entry_id}_flag_today"
        display = COUNTRIES.get(country, country)
        self._attr_name = f"Flag Today ({display})"
        self._attr_device_class = "running"
        self._attr_should_poll = False
        self._country = country
        self._module = COUNTRY_MODULES[country]
        self._attr_is_on = False

    async def async_update(self) -> None:
        from datetime import datetime
        now = datetime.now()
        flag_type, _ = self._module.get_flag_status(now)
        self._attr_is_on = flag_type != "no_flag"
