# 📄 Page Source Capture Tool for OTT Devices

This Python script connects to a **debuggable OTT device** (e.g., **Tizen TV**, **webOS**, **Vizio**, **Roku**) using Appium via HeadSpin, and retrieves the XML page source of the current screen. It allows interactive capture during manual navigation to aid debugging, UI inspection, or automation development.

---

## 🎯 Supported Platforms

* Samsung Tizen TV
* LG webOS TV
* Vizio SmartCast
* Roku

> ⚠️ **Note**: Desired capabilities **must be adjusted** depending on the platform. See [Platform Configuration](#-platform-configuration) below.

---

## 📆 Requirements

* Python 3.8+
* `appium-python-client`
* `python-dotenv`
* `rich`

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
appium-python-client
python-dotenv
rich
```

---

## 🔐 Environment Setup

Create a `.env` file in the root directory with the following variables:

```env
HEADSPIN_API_TOKEN=your_headspin_api_key
APP_ID=your_app_id
UDID=your_device_udid
```

---

## ⚙️ Platform Configuration

Modify the `capabilities` dictionary in `get_page_source.py` to match the device you're testing:

### 🔹 Tizen Example

```python
capabilities = {
    'platformName': 'tizentv',
    'appium:automationName': 'tizentv',
    'appium:deviceName': 'SamsungTV',
    'appium:udid': udid,
    'headspin:app.id': app_id,
    'headspin:retryNewSessionFailure': False
}
```

### 🔹 webOS Example

```python
capabilities = {
    'platformName': 'webos',
    'appium:automationName': 'webos',
    'appium:deviceName': 'LGTV',
    'appium:udid': udid,
    'appium:appId': 'com.your.app.id',
    'headspin:app.id': app_id
}
```

### 🔹 Vizio Example

```python
capabilities = {
    'platformName': 'vizio',
    'appium:automationName': 'vizio',
    'appium:deviceName': 'VizioTV',
    'appium:app': 'https://your_app_url'
    'appium:udid': udid,
}
```

### 🔹 Roku Example

```python
capabilities = {
    'platformName': 'roku',
    'appium:automationName': 'roku',
    'appium:deviceName': 'roku',
    'headspin:app.id': app_id,
    'appium:udid': udid,
}
```

---

## 🚀 Usage

Run the script:

```bash
python get_page_source.py
```

You’ll be prompted to interactively capture screen states:

```text
Do you want to get page source? Press any key to continue or q to quit:
```

Captured files will be saved as:

```
get_page_source_YYYY-MM-DD_HH-MM-SS.xml
```

---

## 🫼 Output Management

To remove previously saved XML outputs:

```bash
rm get_page_source_*.xml
```

---

## 🙋‍♂️ Notes

* The script uses [HeadSpin’s Appium Load Balancer](https://ui.headspin.io) via the `HEADSPIN_API_TOKEN`.
* Device-specific behavior may affect how page source is rendered or retrieved.
* Useful for both test development and live debugging on OTT platforms.

---

## 🛠 Support

For help with device access or Appium configuration on HeadSpin, contact your HeadSpin support team.
