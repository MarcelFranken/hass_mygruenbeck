"""MyGruenbeck Integration for Home Assistant."""
import logging
import voluptuous as vol
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN
from .mygruenbeck_api import login

_LOGGER = logging.getLogger(__name__)

# Validierungsschema für die Konfiguration
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up the MyGruenbeck integration."""
    conf = config.get(DOMAIN)
    if conf is not None:
        # Hier können Sie auf die Konfigurationsdaten zugreifen
        username = conf[CONF_USERNAME]
        password = conf[CONF_PASSWORD]

        # 1. Login-Funktion aufrufen
        loginProcess = await login(username, password, hass)
        if loginProcess:
            # hass.data[DOMAIN] = {"access_token": access_token}
            _LOGGER.info("MyGruenbeck integration successfully configured")

            # 2. getDevices-Funktion aufrufen
            devices = await getDevices()
            if devices:
                _LOGGER.info(f"Found {len(devices)} devices")

                # 3. parseDeviceInfos-Funktion für jedes Gerät aufrufen
                for device in devices:
                    await parseDeviceInfos(device)
        else:
            _LOGGER.error("Login to MyGruenbeck failed")

    return True