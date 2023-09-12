"""My Gruenbeck Integration."""

DOMAIN = "mygruenbeck"
DEFAULT_USERNAME = ""
DEFAULT_PASSWORD = ""

async def async_setup(hass, config):
    """Set up the My Gruenbeck integration."""
    return True

async def async_setup_entry(hass, entry):
    """Set up My Gruenbeck from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True

# Verweisen Sie auf den Konfigurationsfluss
async def async_set_config_flow(hass, config_entry):
    """Set up the config flow for My Gruenbeck."""
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data=config_entry.data
        )
    )
