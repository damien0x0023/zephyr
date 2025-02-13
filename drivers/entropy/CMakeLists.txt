# SPDX-License-Identifier: Apache-2.0

zephyr_library()

zephyr_library_sources_ifdef(CONFIG_ENTROPY_TELINK_B9X_TRNG    entropy_b9x_trng.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_TELINK_TLX_TRNG    entropy_tlx_trng.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_TELINK_W91_TRNG    entropy_w91_trng.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_CC13XX_CC26XX_RNG  entropy_cc13xx_cc26xx.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_ESP32_RNG          entropy_esp32.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_MCUX_RNG           entropy_mcux_rng.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_MCUX_RNGA          entropy_mcux_rnga.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_MCUX_TRNG          entropy_mcux_trng.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_MCUX_CAAM          entropy_mcux_caam.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_MCUX_CSS           entropy_mcux_css.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_NRF5_RNG           entropy_nrf5.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_SAM_RNG            entropy_sam.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_SMARTBOND_TRNG     entropy_smartbond.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_STM32_RNG          entropy_stm32.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_LITEX_RNG          entropy_litex.c)
zephyr_library_sources_ifdef(CONFIG_FAKE_ENTROPY_NATIVE_POSIX  fake_entropy_native_posix.c)
zephyr_library_sources_ifdef(CONFIG_USERSPACE                  entropy_handlers.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_RV32M1_TRNG        entropy_rv32m1_trng.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_GECKO_TRNG         entropy_gecko_trng.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_NEORV32_TRNG       entropy_neorv32_trng.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_BT_HCI             entropy_bt_hci.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_GECKO_SE           entropy_gecko_se.c)
zephyr_library_sources_ifdef(CONFIG_ENTROPY_PSA_CRYPTO_RNG     entropy_psa_crypto.c)

if (CONFIG_BUILD_WITH_TFM)
  target_include_directories(${ZEPHYR_CURRENT_LIBRARY} PRIVATE
    $<TARGET_PROPERTY:tfm,TFM_BINARY_DIR>/install/interface/include
  )
endif()
