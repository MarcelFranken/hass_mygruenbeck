"""Config flow for My Gruenbeck."""
import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, DEFAULT_USERNAME, DEFAULT_PASSWORD

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("username", default=DEFAULT_USERNAME): str,
        vol.Required("password", default=DEFAULT_PASSWORD): str,
    }
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Gruenbeck."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # You can perform validation here, e.g., check if the credentials are valid
            # If there are errors, set them in the `errors` dictionary
            # If everything is fine, return `self.async_create_entry` with the user input
            # as the data dictionary
            # Example:
            # if not await validate_credentials(user_input["username"], user_input["password"]):
            #     errors["base"] = "invalid_credentials"
            # else:
            #     return self.async_create_entry(title="My Gruenbeck", data=user_input)

            # For simplicity, we'll assume no validation for now
            return self.async_create_entry(title="My Gruenbeck", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
