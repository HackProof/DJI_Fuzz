# DJI Drone Firmware Analysis & Emulation Environment

This experiment was conducted using firmware decryption scripts provided by the drone hacking team **"o-gs"**, followed by emulating a DJI drone environment using a **Raspberry Pi**.

---

## 🔍 Experiment Steps

### 1. ADB Dump from DJI Drone

- Performed ADB dump on the DJI drone to extract required internal libraries and components.
- **Note:** All libraries and their invocation paths must be properly set for the binaries to run.

📥 [DJI_ADB_Dump Download](https://1drv.ms/u/c/d30bd892bdb83557/ETBCEmegY6JHrFZ1Vt7__4EBrrzX6jhAKGmLsy7Nz2gVoQ?e=gEcCSJ)

---

### 2. Emulating DJI Drone Environment on Raspberry Pi

- Used a **Raspberry Pi** to replicate a DJI-like environment running **Android 4.0**.
- ✅ **Note:** DJI binaries require Android versions **below 5.0** to execute properly.

📥 [Android 4.0.3 ROM Download](https://forum.xda-developers.com/t/rom-dev-v5-android-4-0-3-ice-cream-sandwich-12-31.1368952/)

---

### 3. Cross-Compiling Android-AFL for Fuzzing

Used the following command to cross-compile [**android-afl**](https://github.com/ele7enxxh/android-afl):

```bash
arm-linux-gnueabi-gcc -march=armv5te -mfloat-abi=soft \
  -I/usr/arm-linux-gnueabi/include afl-fuzz.c -o afl-fuzz
