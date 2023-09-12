# MyGruenbeck Home Assistant Integration

![GitHub](https://img.shields.io/github/license/MarcelFranken/hass_mygruenbeck)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/MarcelFranken/hass_mygruenbeck)

**Note: This component is only compatible with Grünbeck water softeners of the SD series that communicate through the MyGrünbeck Cloud.**

This is a Home Assistant integration for MyGruenbeck that allows you to monitor and control your MyGruenbeck devices through Home Assistant.

## Installation

This integration can be installed using the Home Assistant Community Store (HACS). Follow these steps:

1. Open the Home Assistant Configuration.
2. Go to "HACS" from the sidebar.
3. Click "Integrations" under "Frontend."
4. In the top right corner, click the three dots (ellipsis) and select "Custom repositories."
5. Paste the URL of this GitHub repository (https://github.com/MarcelFranken/hass_mygruenbeck) into the "Add custom repository" field.
6. Set the Category to "Integration."
7. Click the "Add" button.
8. Now you should see the "MyGruenbeck" integration listed in HACS.
9. Click "Install" next to "MyGruenbeck" and follow the setup instructions.

Once the integration is installed, add the following to your `configuration.yaml` to activate it:

## Configuration

To configure the MyGruenbeck integration, you'll need your MyGruenbeck Cloud username and password. Add the following to your `configuration.yaml`:

```yaml
mygruenbeck:
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
```
Replace YOUR_USERNAME and YOUR_PASSWORD with your MyGruenbeck credentials.

## License

This project is licensed under the GNU General Public License (GPL) - see the [LICENSE](LICENSE) file for details.
