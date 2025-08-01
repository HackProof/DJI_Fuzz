# DJI Drone Firmware Analysis & Emulation Experiment

This experiment was conducted using firmware decryption scripts from the drone hacking team **"o-gs"**, followed by emulating a DJI drone-like environment using a **Raspberry Pi**.

---

## 1. ADB Dump from DJI Drone

- Performed ADB dump on the DJI drone to extract necessary internal libraries and components.  
- **Note:** All libraries and invocation paths must be properly set for the binaries to function.

📥 **DJI_ADB_Dump Download**  
[https://1drv.ms/u/c/d30bd892bdb83557/ETBCEmegY6JHrFZ1Vt7__4EBrrzX6jhAKGmLsy7Nz2gVoQ?e=gEcCSJ](https://1drv.ms/u/c/d30bd892bdb83557/ETBCEmegY6JHrFZ1Vt7__4EBrrzX6jhAKGmLsy7Nz2gVoQ?e=gEcCSJ)

---

## 2. Emulating DJI Drone Environment on Raspberry Pi

- Configured a **Raspberry Pi** to replicate the DJI environment running **Android 4.0**.  
- **Note:** DJI binaries require Android versions **below 5.0** to operate.

📥 **Android 4.0.3 ROM Download**  
[https://forum.xda-developers.com/t/rom-dev-v5-android-4-0-3-ice-cream-sandwich-12-31.1368952/](https://forum.xda-developers.com/t/rom-dev-v5-android-4-0-3-ice-cream-sandwich-12-31.1368952/)

---

## 3. Cross-Compiling Android-AFL for Fuzzing

- Used the following command to cross-compile [**android-afl**](https://github.com/ele7enxxh/android-afl):

```bash
arm-linux-gnueabi-gcc -march=armv5te -mfloat-abi=soft \
  -I/usr/arm-linux-gnueabi/include afl-fuzz.c -o afl-fuzz
```
---

## 4. Short Demo
**DEMO**  
[https://www.youtube.com/watch?v=80AcX8BpU4Q]
(https://www.youtube.com/watch?v=80AcX8BpU4Q)

