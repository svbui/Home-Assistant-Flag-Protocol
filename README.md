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
2. Ensure folder structure is correct.
4. Restart Home Assistant.  
5. Add the integration via **Settings → Devices & Services → Add Integration**.

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

### 🧠 Entities Created

The **Flag Protocol** integration provides the following entities per configured country:

#### `sensor.flag_today_<country>`
- **Description**: Text sensor indicating the current flag status (`full_mast`, `half_mast`, or `no_flag`)
- **State**: `"full_mast"`, `"half_mast"`, or `"no_flag"`
- **Attributes**:
  - `reason`: Description of today's flag status
  - `icon`: Automatically selected based on status

#### `sensor.next_flag_day_countdown_<country>`
- **Description**: Sensor showing the number of days until the next official flag day.
- **State**: Integer number of days
- **Attributes**:
  - `next_reason`: Description of the next flag day
  - `next_flag_type`: `"full_mast"` or `"half_mast"`
  - `next_date_time`: ISO 8601 timestamp of the next flag day

#### `binary_sensor.flag_today_<country>`
- **Description**: Binary sensor that is `on` when a flag should be flown today, and `off` otherwise.
- **State**: `on` or `off`
- **Attributes**:
  - `flag_type`: `"full_mast"` or `"half_mast"` (if active)
  - `reason`: Description of the flag day (if active)

> ⚠️ Note: `<country>` corresponds to the configured country code (e.g., `nl`, `se`, `no`, etc.).
