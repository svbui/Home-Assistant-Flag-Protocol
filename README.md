# Flag Protocol integration for Home-Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
![License](https://img.shields.io/github/license/svbui/Home-Assistant-Flag-Protocol)
![Version](https://img.shields.io/github/v/release/svbui/Home-Assistant-Flag-Protocol?include_prereleases&sort=semver)

**Flag Protocol** is a custom integration for [Home Assistant](https://www.home-assistant.io/) that provides national flag day information for supported countries. The integration dynamically shows when flags should be flown at full mast, half mast, or with a pennant—based on official protocols—and also counts down to the next official flag day.

The background of this integration is that I found I was not the only one looking sensors to tell me when to flag. Hence I decided to create a Dutch Flag Protocol integration. After short deliberation with a co-worker we came to the conclusion it made sense to create a more generic Flag Protocol integration with multi country support. 

## Assumptions and choices
Due to almost no countries having a public API for the flag protocol, the dates are hardcoded. Yet due to the setup with a separate file for each country it is still easy to maintain. 

In general I have kept in mind that the flag should only be flown during daylight (expect for when well litt on both sides), as this is the case for most countries. There is however some flexibility to it with a set time instead of relying on `sun.sun` elevation. 

Election days are excluded, some countries will allow you to flag during election days (Belgium, Sweden), some don't (The Netherlands). However there is in general no logic to when it is election day.

Dates and flag position should be confirmed by official government websites.

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
## Installation

### HACS (recommended)

1. In Home Assistant, go to **Settings → Add-ons & Backups → Add-on Store → Integrations**.  
2. Search for **Flag Protocol**, click **Install**.  
3. Restart Home Assistant.  
4. Go to **Settings → Devices & Services → Add Integration**, search for **Flag Protocol**, and follow the UI flow to pick one or more countries.

### Manual

1. Copy the `custom_components/flag_protocol` folder into your Home Assistant `config/custom_components/` directory.  
2. Ensure folder structure is:
config/
└── custom_components/
└── flag_protocol/
├── init.py
├── manifest.json
├── config_flow.py
├── const.py
├── sensor.py
└── translations/
├── en.json
└── nl.json
3. Restart Home Assistant.  
4. Add the integration via **Settings → Devices & Services → Add Integration**.

---

## Configuration

No YAML configuration is needed. Once installed, use the UI to add one or more countries. Supported country codes:

| Code | Country     |
| ---- | ----------- |
| `be` | Belgium     |
| `dk` | Denmark     |
| `fi` | Finland     |
| `is` | Iceland     |
| `nl` | Netherlands |
| `no` | Norway      |
| `se` | Sweden      |

The integration will prevent you from adding the same country twice.

---

## Entities & Attributes

### Flag Status Sensor  
**Entity:** `sensor.flag_protocol_<country>_main`  
**State values:**  
- `full_mast`
- `full_mast_with_banner` 
- `half_mast`  
- `no_flag`  

**Attributes:**  
- `reason` — Why the flag is at that position (e.g. holiday name, “Flag not lit” when the sun is down).

---

### Next Flag Countdown Sensor  
**Entity:** `sensor.flag_protocol_<country>_next_countdown`  
**State:** Number of days until the next flag day.  

**Attributes:**  
- `next_reason` — Name of the upcoming flag day.  
- `next_flag_type` — Flag position on that day (`full_mast`, `half_mast`, etc.).
```
