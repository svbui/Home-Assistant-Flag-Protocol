import importlib
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    country = entry.data["country"]  # "nl", "be", or "se"
    module = importlib.import_module(f".flag_rules.{country}", package=__name__)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "get_flag_status": module.get_flag_status,
        "get_next_flag_day": module.get_next_flag_day,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
