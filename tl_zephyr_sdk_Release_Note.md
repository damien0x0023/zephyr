# Telink Zephyr Release Notes

## Introduction

This release is based on the latest `tl_develop_v4.1.0` branch (commit: `e08fc42546e58d808bfd39f35c8df296f5617a44`), incorporating multiple bug fixes, driver updates, and BLE SDK improvements for Telink TL323x series chips and other platforms.

### ✨ New Features
- Added full support for tl323x series chips
- New CI build pipelines specifically for the tl323x platform
- Added device tree and pin configuration support for the tl3238x development board
- Added PLIC interrupt controller support for TL3238X
- Added LZMA module support for Telink SoCs
- Added tl523x skeleton board support

### 🐛 Bug Fixes
- **TL323x RF TX Performance Fix**: Resolves 1M PHY DEVM transmission performance issue on TL323x series
- **WFI Function Fix**: Adjusted macro definitions and removed `ARCH_HAS_CUSTOM_CPU_IDLE` for tlx platform to fix wfi functionality
- **Amazon Bug Fix - Jump Fail & Reconnect Fail**: Reset RF related registers in `soc_early_init_hook` to fix jump and reconnect failures on Amazon devices
- **PM/Clock Fix**: Updated reset and clock clear on TL323x PM, adjusted include and code format
- **AES Reentrancy Fix**: Resolved AES reentrancy issue
- **Pinctrl Fix**: Fixed peripherals input pins in pinctrl driver; fixed pinctrl Kconfig to always disable GPIOs
- **PWM Revert**: Reverted incorrect PWM driver changes for Telink platform (including `pwm_b9x` and `pwm_tlx`)
- **SHA HW Cryptography Fix**: Reworked Telink SHA calculation using HW unit on TLX platforms, supporting MbedTLS & Tinycrypt, fixed multithread & power management issues
- **Kconfig Fix**: Fixed dependency for bootloader HW cryptography on Telink B9X & TLX platforms
- **32K Watchdog Fix**: Changed the logic of 32k wd - open 32k wd in idle and standby mode, disable wd stop to fix wd stop code
- **Tercel V2 Fix**: Updated hal_v1 to hal_v2, optimized power consumption, fixed 802154 rx setting, optimized idle task ramcode

### 📦 Updates
- Updated MCUBoot (https://github.com/telink-semi/mcuboot/commit/ce0da85c39c749df49b0ec62b33d2ecdea24c927) to Telink submanifest (zephyr/submanifests/telink.yaml)
- Update OpneThread source code (https://github.com/telink-semi/openthread/commit/542aaab44e1308e1a8a24573dfbd413fade342ee)
- Updated OpenThread Telink Library (default source set to https://github.com/telink-semi/openthread, tags/v4.1.2)
- Updated hal_telink (https://github.com/telink-semi/hal_telink/commit/14c6149f6cc466c49d81e3b2f7f1e4d8ff6fbbb5)
- Updated Telink BLE SDK (https://github.com/telink-semi/tl_ble_sdk_zephyr/commit/46322e5b570e2a68373b18d4f08811acadd1266c)

### ⚠️ Important Notes
This is an ALPHA pre-release version for demonstration and testing purposes.
Not recommended for production use.
- WEST tool will not update `tl_ble_sdk` automatically because Zephyr CI does NOT allow modules with binary files.
- Please go to `modules/hal/telink` and manually perform `./hal_v2/fetch_sdk.sh` to pull or update `tl_ble_sdk` to the specific version.
- You can check Section `Install Zephyr Project Environment` (in our user guide https://doc.telink-semi.cn/doc/en/software/res/sdk/matter/telink_matter_developer_guide_en/) to understand the manual steps to set up the Telink Zephyr developing environment.

---

## Version Information

### Zephyr SDK & Toolchain
- **Zephyr SDK Version:** Telink Zephyr v4.1.0
- **Zephyr SDK:** 0.17.0
- **Toolchain:** riscv64-zephyr-elf

This is code base of the Telink SDK from Zephyr RTOS community.

### Telink SDK
**Branch:** tl_develop_v4.1.0
**Target Commit:** e08fc42546e58d808bfd39f35c8df296f5617a44
**Tag Name:** tl_v4.1.0.2-alpha
**Release Type:** Pre-Release (Alpha)

### Chip & Hardware Versions
- **Chip Versions:**
  - TLSR921X/TLSR951X(B91):  A2
  - TLSR922X/TLSR952X(B92):  A3/A4
  - TL721X:                  A2/A3
  - TL321X:                  A1/A2/A3
  - TL322X:                  A1
  - TL323X:                  A0

- **Hardware EVK Versions:**
  - TLSR921X:                C1T213A20_V1.3
  - TLSR952X:                C1T266A20_V1.3
  - TL721X:                  C1T315A20_V1.2/AIOT_DK1:ML7218D1/ML7218A
  - TL321X:                  C1T331A20_V1.0/C1T335A20_V1.3
  - TL322X:                  C1T382A20_V1.2
  - TL323X:                  C1T388A20_V1.1

---

## Resource Usage (Code Size)

This section shows the RAM and ROM usage for various Zephyr samples on Telink platforms, based on Zephyr SDK 0.17.0 with riscv64-zephyr-elf toolchain and PR #774 CI workflows.

### Supported Boards
- tlsr9518adk80d (TLSR951X/B91)
- tlsr9528a (TLSR952X/B92)
- tl3218x (TL321X)
- tl3228x (TL322X)
- tl3238x (TL323X)
- tl7218x (TL721X)
- tlsr9118bdk40d (TLSR9118BDK40D)

---

### TLSR951X

#### tlsr9518adk80d

* **samples/basic/blinky**
     - RAMILM: 21248 B (16.21% of 128 KB)
     - ROM: 23848 B (2.27% of 1 MB)
     - RAM: 868 B (0.66% of 128 KB)

* **samples/bluetooth/peripheral_ht**
     - RAMILM: 65856 B (50.24% of 128 KB)
     - ROM: 210412 B (20.07% of 1 MB)
     - RAM: 12556 B (9.58% of 128 KB)

* **samples/boards/tlsr9x/gpio-kbd-matrix**
     - RAMILM: 24512 B (18.70% of 128 KB)
     - ROM: 32388 B (3.09% of 1 MB)
     - RAM: 2736 B (2.09% of 128 KB)

* **samples/net/openthread/cli**
     - RAMILM: 53472 B (40.80% of 128 KB)
     - ROM: 552436 B (52.68% of 1 MB)
     - RAM: 88912 B (67.83% of 128 KB)

---

### TLSR952X

#### tlsr9528a

* **samples/basic/blinky**
     - RAMILM: 24016 B (9.16% of 256 KB)
     - ROM: 29626 B (2.83% of 1 MB)
     - RAM: 972 B (0.37% of 256 KB)

* **samples/bluetooth/peripheral_ht**
     - RAMILM: 76720 B (29.27% of 256 KB)
     - ROM: 231488 B (22.08% of 1 MB)
     - RAM: 25592 B (9.76% of 256 KB)

* **samples/boards/tlsr9x/gpio-kbd-matrix**
     - RAMILM: 27280 B (10.41% of 256 KB)
     - ROM: 38166 B (3.64% of 1 MB)
     - RAM: 2840 B (1.08% of 256 KB)

* **samples/net/openthread/cli**
     - RAMILM: 57712 B (22.02% of 256 KB)
     - ROM: 561762 B (53.57% of 1 MB)
     - RAM: 89048 B (33.97% of 256 KB)

---

### TL321X

#### tl3218x

* **samples/basic/blinky**
     - RAM_ILM_N: 5144 B (15.70% of 32 KB)
     - ROM: 27820 B (2.65% of 1 MB)
     - RAM: 18960 B (19.29% of 96 KB)

* **samples/basic/button**
     - RAM_ILM_N: 5144 B (15.70% of 32 KB)
     - ROM: 28456 B (2.71% of 1 MB)
     - RAM: 18984 B (19.31% of 96 KB)

* **samples/basic/fade_led**
     - RAM_ILM_N: 5144 B (15.70% of 32 KB)
     - ROM: 41676 B (3.97% of 1 MB)
     - RAM: 22432 B (22.82% of 96 KB)

* **samples/bluetooth/peripheral_ht**
     - RAM_ILM_N: 14676 B (44.79% of 32 KB)
     - ROM: 191862 B (18.30% of 1 MB)
     - RAM: 42024 B (42.75% of 96 KB)

* **samples/boards/tlsr9x/gpio-kbd-matrix**
     - RAM_ILM_N: 5144 B (15.70% of 32 KB)
     - ROM: 36352 B (3.47% of 1 MB)
     - RAM: 24084 B (24.50% of 96 KB)

* **samples/drivers/adc/adc_dt**
     - RAM_ILM_N: 5592 B (17.07% of 32 KB)
     - ROM: 36756 B (3.51% of 1 MB)
     - RAM: 20168 B (20.52% of 96 KB)

* **samples/drivers/spi_flash**
     - RAM_ILM_N: 5442 B (16.61% of 32 KB)
     - ROM: 35050 B (3.34% of 1 MB)
     - RAM: 19116 B (19.45% of 96 KB)

* **samples/drivers/watchdog**
     - RAM_ILM_N: 5144 B (15.70% of 32 KB)
     - ROM: 35696 B (3.40% of 1 MB)
     - RAM: 19040 B (19.37% of 96 KB)

* **samples/hello_world**
     - RAM_ILM_N: 5144 B (15.70% of 32 KB)
     - ROM: 27288 B (2.60% of 1 MB)
     - RAM: 18960 B (19.29% of 96 KB)

* **samples/net/openthread/cli**
     - RAM_ILM_N: 9812 B (29.94% of 32 KB)
     - ROM: 439018 B (41.87% of 1 MB)
     - RAM: 85108 B (86.58% of 96 KB)

* **samples/sensor/sht3xd**
     - RAM_ILM_N: 5144 B (15.70% of 32 KB)
     - ROM: 40996 B (3.91% of 1 MB)
     - RAM: 18996 B (19.32% of 96 KB)

---

### TL322X

#### tl3228x

* **samples/basic/blinky**
     - RAMILM: 26512 B (5.06% of 512 KB)
     - ROM: 34778 B (3.32% of 1 MB)
     - RAM: 1160 B (0.89% of 128 KB)

* **samples/basic/button**
     - RAMILM: 26512 B (5.06% of 512 KB)
     - ROM: 35406 B (3.38% of 1 MB)
     - RAM: 1176 B (0.90% of 128 KB)

* **samples/drivers/adc/adc_dt**
     - RAMILM: 26528 B (5.06% of 512 KB)
     - ROM: 40838 B (3.89% of 1 MB)
     - RAM: 2044 B (1.56% of 128 KB)

* **samples/drivers/watchdog**
     - RAMILM: 26512 B (5.06% of 512 KB)
     - ROM: 42650 B (4.07% of 1 MB)
     - RAM: 1236 B (0.94% of 128 KB)

* **samples/hello_world**
     - RAMILM: 26512 B (5.06% of 512 KB)
     - ROM: 34246 B (3.27% of 1 MB)
     - RAM: 1160 B (0.89% of 128 KB)

* **samples/sensor/sht3xd**
     - RAMILM: 26512 B (5.06% of 512 KB)
     - ROM: 48322 B (4.61% of 1 MB)
     - RAM: 1224 B (0.93% of 128 KB)

---

### TL323X

#### tl3238x

* **samples/basic/blinky**
     - RAM_ILM_N: 11346 B (17.31% of 64 KB)
     - ROM: 37790 B (3.60% of 1 MB)
     - RAM: 19528 B (19.86% of 96 KB)

* **samples/basic/button**
     - RAM_ILM_N: 11346 B (17.31% of 64 KB)
     - ROM: 38426 B (3.66% of 1 MB)
     - RAM: 19544 B (19.88% of 96 KB)

* **samples/basic/fade_led**
     - RAM_ILM_N: 11346 B (17.31% of 64 KB)
     - ROM: 51254 B (4.89% of 1 MB)
     - RAM: 23004 B (23.40% of 96 KB)

* **samples/bluetooth/peripheral_ht**
     - RAM_ILM_N: 22034 B (33.62% of 64 KB)
     - ROM: 211242 B (20.15% of 1 MB)
     - RAM: 42464 B (43.20% of 96 KB)

* **samples/crypto/mbedtls**
     - RAM_ILM_N: 11346 B (17.31% of 64 KB)
     - ROM: 137558 B (13.12% of 1 MB)
     - RAM: 26244 B (26.70% of 96 KB)

* **samples/drivers/adc/adc_dt**
     - RAM_ILM_N: 11346 B (17.31% of 64 KB)
     - ROM: 52126 B (4.97% of 1 MB)
     - RAM: 20520 B (20.87% of 96 KB)

* **samples/drivers/spi_flash**
     - RAM_ILM_N: 11514 B (17.57% of 64 KB)
     - ROM: 45002 B (4.29% of 1 MB)
     - RAM: 19676 B (20.02% of 96 KB)

* **samples/drivers/watchdog**
     - RAM_ILM_N: 11346 B (17.31% of 64 KB)
     - ROM: 45666 B (4.36% of 1 MB)
     - RAM: 19604 B (19.94% of 96 KB)

* **samples/hello_world**
     - RAM_ILM_N: 11346 B (17.31% of 64 KB)
     - ROM: 37314 B (3.56% of 1 MB)
     - RAM: 19528 B (19.86% of 96 KB)

* **samples/net/openthread/cli**
     - RAM_ILM_N: 16014 B (24.44% of 64 KB)
     - ROM: 436138 B (41.59% of 1 MB)
     - RAM: 80752 B (82.15% of 96 KB)

* **samples/net/sockets/echo_client**
     - RAM_ILM_N: 23562 B (35.95% of 64 KB)
     - ROM: 268760 B (25.63% of 1 MB)
     - RAM: 59352 B (60.38% of 96 KB)

* **samples/sensor/sht3xd**
     - RAM_ILM_N: 11346 B (17.31% of 64 KB)
     - ROM: 51202 B (4.88% of 1 MB)
     - RAM: 19592 B (19.93% of 96 KB)

---

### TL721X

#### tl7218x

* **samples/basic/blinky**
     - RAMILM: 26608 B (10.15% of 256 KB)
     - ROM: 33626 B (3.21% of 1 MB)
     - RAM: 1012 B (0.39% of 256 KB)

* **samples/basic/button**
     - RAMILM: 26608 B (10.15% of 256 KB)
     - ROM: 34254 B (3.27% of 1 MB)
     - RAM: 1028 B (0.39% of 256 KB)

* **samples/basic/fade_led**
     - RAMILM: 28656 B (10.93% of 256 KB)
     - ROM: 47554 B (4.54% of 1 MB)
     - RAM: 2440 B (0.93% of 256 KB)

* **samples/bluetooth/peripheral_ht**
     - RAMILM: 57232 B (21.83% of 256 KB)
     - ROM: 211324 B (20.15% of 1 MB)
     - RAM: 8548 B (3.26% of 256 KB)

* **samples/crypto/mbedtls**
     - RAMILM: 31728 B (12.10% of 256 KB)
     - ROM: 133070 B (12.69% of 1 MB)
     - RAM: 2608 B (0.99% of 256 KB)

* **samples/drivers/adc/adc_dt**
     - RAMILM: 28384 B (10.83% of 256 KB)
     - ROM: 43928 B (4.19% of 1 MB)
     - RAM: 1648 B (0.63% of 256 KB)

* **samples/drivers/spi_flash**
     - RAMILM: 26784 B (10.22% of 256 KB)
     - ROM: 41754 B (3.98% of 1 MB)
     - RAM: 1284 B (0.49% of 256 KB)

* **samples/drivers/watchdog**
     - RAMILM: 26608 B (10.15% of 256 KB)
     - ROM: 41498 B (3.96% of 1 MB)
     - RAM: 1088 B (0.42% of 256 KB)

* **samples/hello_world**
     - RAMILM: 26608 B (10.15% of 256 KB)
     - ROM: 33094 B (3.16% of 1 MB)
     - RAM: 1012 B (0.39% of 256 KB)

* **samples/net/openthread/cli**
     - RAMILM: 60768 B (23.18% of 256 KB)
     - ROM: 570260 B (54.38% of 1 MB)
     - RAM: 89184 B (34.02% of 256 KB)

* **samples/net/sockets/echo_client**
     - RAMILM: 38828 B (14.81% of 256 KB)
     - ROM: 259978 B (24.79% of 1 MB)
     - RAM: 34640 B (13.21% of 256 KB)

* **samples/net/sockets/echo_client**
     - RAM_ILM_N: 25890 B (19.75% of 128 KB)
     - RAM_DLM: 0 GB (0.00% of 256 KB)
     - ROM: 268840 B (25.64% of 1 MB)
     - RAM: 59200 B (45.17% of 128 KB)

* **samples/net/sockets/echo_server**
     - RAMILM: 77564 B (29.59% of 256 KB)
     - ROM: 416206 B (39.69% of 1 MB)
     - RAM: 50940 B (19.43% of 256 KB)

* **samples/sensor/sht3xd**
     - RAMILM: 26608 B (10.15% of 256 KB)
     - ROM: 46754 B (4.46% of 1 MB)
     - RAM: 1056 B (0.40% of 256 KB)

* **samples/usb/console**
     - RAMILM: 33520 B (12.79% of 256 KB)
     - ROM: 49424 B (4.71% of 1 MB)
     - RAM: 4688 B (1.79% of 256 KB)

---

### TLSR9118BDK40D

#### tlsr9118bdk40d

* **samples/basic/blinky**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 23728 B (0.57% of 4 MB)
     - RAM: 24776 B (12.60% of 192 KB)

* **samples/basic/button**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 24332 B (0.58% of 4 MB)
     - RAM: 24784 B (12.61% of 192 KB)

* **samples/bluetooth/peripheral_ht**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 137380 B (3.28% of 4 MB)
     - RAM: 39572 B (20.13% of 192 KB)

* **samples/boards/tlsr9x/gpio-kbd-matrix**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 30956 B (0.74% of 4 MB)
     - RAM: 27620 B (14.05% of 192 KB)

* **samples/boards/tlsr9x/key_matrix**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 24468 B (0.58% of 4 MB)
     - RAM: 24856 B (12.64% of 192 KB)

* **samples/boards/tlsr9x/key_pool**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 24416 B (0.58% of 4 MB)
     - RAM: 24848 B (12.64% of 192 KB)

* **samples/boards/tlsr9x/led_pool**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 25016 B (0.60% of 4 MB)
     - RAM: 24840 B (12.63% of 192 KB)

* **samples/boards/tlsr9x/pwm_pool**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 25384 B (0.61% of 4 MB)
     - RAM: 24840 B (12.63% of 192 KB)

* **samples/boards/tlsr9x/sock_simple**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 154140 B (3.67% of 4 MB)
     - RAM: 73096 B (37.18% of 192 KB)

* **samples/boards/tlsr9x/sock_simple**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 154276 B (3.68% of 4 MB)
     - RAM: 73064 B (37.16% of 192 KB)

* **samples/crypto/mbedtls**
     - RAM_ILM: 108 B (0.33% of 32 KB)
     - ROM: 125924 B (3.00% of 4 MB)
     - RAM: 30188 B (15.35% of 192 KB)

* **samples/drivers/spi_flash_at45**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 38520 B (0.92% of 4 MB)
     - RAM: 27064 B (13.77% of 192 KB)

* **samples/drivers/uart/echo_bot**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 26084 B (0.62% of 4 MB)
     - RAM: 26520 B (13.49% of 192 KB)

* **samples/net/openthread/cli**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 549632 B (13.10% of 4 MB)
     - RAM: 143248 B (72.86% of 192 KB)

* **samples/sensor/mpu6050**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 38048 B (0.91% of 4 MB)
     - RAM: 24876 B (12.65% of 192 KB)

* **samples/subsys/nvs**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 38108 B (0.91% of 4 MB)
     - RAM: 24860 B (12.64% of 192 KB)

* **samples/subsys/shell/devmem_load/**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 52400 B (1.25% of 4 MB)
     - RAM: 28888 B (14.69% of 192 KB)

* **tests/drivers/adc/adc_api**
     - RAM_ILM: 60 B (0.18% of 32 KB)
     - ROM: 55972 B (1.33% of 4 MB)
     - RAM: 24548 B (12.49% of 192 KB)

---

---

## Additional Notes
- **Memory Regions:** May vary between chip variants; check individual board configurations
- **Full CI Data:** For complete resource usage information across all samples (including Bluetooth, OpenThread, and MCUBoot), refer to CI build artifacts from PR #774
- **Production Optimizations:** For production builds, disable debug logging and enable appropriate optimizations to reduce RAM/ROM usage
- **Bluetooth & OpenThread:** For Bluetooth LE and OpenThread-specific resource usage, see the respective CI workflow files in `.github/workflows/`
- **Build Config:** All builds use `-DCONFIG_COMPILER_WARNINGS_AS_ERRORS=y` as in the CI pipelines
