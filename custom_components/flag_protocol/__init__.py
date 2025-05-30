import importlib
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Flag Protocol from a config entry."""
    country = entry.data.get("country")
    if not country:
        _LOGGER.error("Flag Protocol: no country specified in entry %s", entry.entry_id)
        return False

    # Dynamically load the country-specific rules module
    try:
        module = importlib.import_module(f"{__package__}.flag_rules.{country}")
    except ImportError as err:
        _LOGGER.error("Flag Protocol: could not load flag_rules.%s: %s", country, err)
        return False

    # Extract the two required functions
    get_status = getattr(module, "get_flag_status", None)
    get_next   = getattr(module, "get_next_flag_day", None)
    if not callable(get_status) or not callable(get_next):
        _LOGGER.error("Flag Protocol: missing functions in flag_rules.%s", country)
        return False

    # Store them for the sensor platform
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "get_flag_status": get_status,
        "get_next_flag_day": get_next,
    }

    # Forward setup to the sensor platform
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and its sensor platform."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
