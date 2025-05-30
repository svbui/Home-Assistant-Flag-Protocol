import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, COUNTRIES

class FlagProtocolFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Flag Protocol."""
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def _is_already_configured(self, country: str) -> bool:
        """Check if the given country is already configured."""
        return any(
            entry.data.get("country") == country
            for entry in self._async_current_entries()
        )

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input:
            # Prevent adding the same country twice
            if self._is_already_configured(user_input["country"]):
                return self.async_abort(reason="already_configured")

            return self.async_create_entry(
                title=COUNTRIES[user_input["country"]],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("country"): vol.In(COUNTRIES)
            }),
            errors=errors
        )
