# Flag Protocol integration for Home-Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
![License](https://img.shields.io/github/license/YOUR_GITHUB_USERNAME/flag_protocol)
![Version](https://img.shields.io/github/v/release/YOUR_GITHUB_USERNAME/flag_protocol?include_prereleases&sort=semver)

**Flag Protocol** is a custom integration for [Home Assistant](https://www.home-assistant.io/) that provides national flag day information for supported countries. The integration dynamically shows when flags should be flown at full mast, half mast, or with a banner—based on official protocols—and also counts down to the next official flag day.

---

## ✨ Features

- 🔄 Country selection during setup (currently Netherlands 🇳🇱 and Belgium 🇧🇪)
- 📅 Sensor showing today's flag instruction (reason + type)
- ⏳ Sensor counting down days to next flag day
- 🌅 Check if sun is above the horizon as most countries require this (based on Home Assistant's `sun.sun`)
- 🧠 Smart sensor states:
  - `full_mast`
  - `half_mast`
  - `full_mast_with_banner`
  - `no_flag`
- 🌍 Multi-language UI support (🇬🇧 English, 🇳🇱 Dutch)
- 🖼 Dynamic Material Design Icons

---

## 📦 Installation (via HACS)

1. Go to **HACS → Integrations**
2. Click **⋮ → Custom repositories**
3. Add this repo:  
   `https://github.com/YOUR_GITHUB_USERNAME/flag_protocol`  
   Type: `Integration`
4. Install **Flag Protocol** from the list
5. Restart Home Assistant
6. Go to **Settings → Devices & Services → Add Integration**
7. Search for **Flag Protocol** and choose your country
8. Done ✅

---

## 🧱 Entities Created

| Entity                                 | Description                                    |
|----------------------------------------|------------------------------------------------|
| `sensor.flag_protocol`                | Shows today's flag type and reason             |
| `sensor.flag_protocol_next_countdown` | Days remaining until the next flag day         |

---

## 🖼 Example

```yaml
type: entities
entities:
  - entity: sensor.flag_protocol
    name: 🇧🇪 Today's Flag Status
  - entity: sensor.flag_protocol_next_countdown
    name: ⏳ Days Until Next Flag Day
