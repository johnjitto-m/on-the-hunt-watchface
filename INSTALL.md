# Installing On the Hunt

Watch faces from outside the Play Store are installed with **adb** (Android Debug Bridge) over Wi-Fi. You need a computer (Windows, macOS or Linux) on the **same Wi-Fi** as your watch.

## 1. Install adb on your computer

| System | How |
|---|---|
| **Windows** | Download [Platform Tools](https://developer.android.com/tools/releases/platform-tools), unzip, open a terminal in that folder (use `.\adb` instead of `adb`) |
| **macOS** | `brew install android-platform-tools` (or download Platform Tools) |
| **Linux – Fedora** | `sudo dnf install android-tools` |
| **Linux – Ubuntu/Debian** | `sudo apt install adb` |

Check it works: `adb version`

## 2. Prepare the watch (one time)

1. Connect the watch to **Wi-Fi** (Settings › Connections › Wi-Fi). Set Wi-Fi to **On**, not Auto.
2. **Unlock Developer options:** Settings › About watch › Software information → tap **Software version** about 5 times.
3. Settings › **Developer options** → turn on **ADB debugging** and **Wireless debugging**.

## 3. Pair and connect

1. On the watch: **Wireless debugging › Pair new device**. Note the **6-digit code** and **IP:port**.
2. On the computer:
   ```bash
   adb pair 192.168.1.42:41235 123456     # your pairing IP:port and code
   ```
3. Back out one screen on the watch. The main Wireless debugging screen shows **another IP:port**:
   ```bash
   adb connect 192.168.1.42:37011          # your connect IP:port
   adb devices                              # watch should show as "device"
   ```

## 4. Install

```bash
adb install -r OnTheHunt-watchface-v2.6.apk
```
Wait for **Success**. If you see *"more than one device"*, add `-s <IP:port>` after `adb`.

## 5. Use it

Touch and hold your watch face → swipe left → **+ Add watch face** → **On the Hunt**.
Give it a few seconds after the first install while it loads the artwork.

**Turn Wireless debugging off** when you're done: it uses battery.

## Troubleshooting

- **`adb pair` fails:** codes expire fast. Tap *Pair new device* again and retry immediately.
- **Device not found / offline:** the port changes every time Wireless debugging is toggled. Re-check it and `adb connect` again.
- **Step goal shows 0:** set a daily step target in Samsung Health / your fitness app.
- **No weather effects:** make sure location and the weather app are set up on your phone/watch.
- **Uninstall:** `adb uninstall com.assassin.onthehunt`
