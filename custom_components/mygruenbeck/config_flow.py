"""Config flow for My Gruenbeck."""
from homeassistant import config_entries

class MyGruenbeckConfigFlow(config_entries.ConfigFlow, domain="mygruenbeck"):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Hier können Sie die eingegebenen Informationen überprüfen und speichern
            # Wenn alles in Ordnung ist, können Sie den Konfigurationsfluss abschließen
            return self.async_create_entry(title="MyGruenbeck", data=user_input)

        # Hier definieren Sie die Benutzeroberfläche zum Eingeben der erforderlichen Informationen
        # Zum Beispiel ein Formular für Benutzername und Passwort

        return self.async_show_form(step_id="user", data_schema=vol.Schema({
            vol.Required("username"): str,
            vol.Required("password"): str,
        }))
