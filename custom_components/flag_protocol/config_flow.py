from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, COUNTRIES

class FlagProtocolConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input:
            return self.async_create_entry(
                title=COUNTRIES[user_input["country"]],
                data=user_input
            )

        schema = vol.Schema({
            vol.Required("country", default="nl"): vol.In(COUNTRIES)
        })
        return self.async_show_form(step_id="user", data_schema=schema)
