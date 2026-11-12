/* main.c - Application main entry point */

/*
 * Copyright (c) 2019 Aaron Tsui <aaron.tsui@outlook.com>
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/types.h>
#include <stddef.h>
#include <string.h>
#include <errno.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/byteorder.h>
#include <zephyr/kernel.h>
#include <zephyr/pm/pm.h>

#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/hci.h>
#include <zephyr/bluetooth/conn.h>
#include <zephyr/bluetooth/uuid.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/bluetooth/services/bas.h>

#include "hts.h"
#include "analog.h"

/* Values recorded around the pull-up configuration in soc.c (retained RAM). */
extern volatile unsigned char ana18_boot_before;
extern volatile unsigned char ana18_boot_after;
extern volatile unsigned char ana18_wake_before;
extern volatile unsigned char ana18_wake_after;
extern volatile unsigned int ana18_wake_count;

/* PM path diagnostic counters (power.c / tl_sleep.c). */
extern volatile unsigned int dbg_pm_state_set_count;
extern volatile unsigned int dbg_pm_state_last;
extern volatile unsigned int dbg_pm_exit_count;
extern volatile unsigned int dbg_tl_deep_sleep_count;
extern volatile unsigned int dbg_tl_suspend_count;
extern volatile unsigned int dbg_skip_sws_restore;
extern bool pm_has_deep_sleep_retention_occurred(void);

static const struct bt_data ad[] = {
	BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
	BT_DATA_BYTES(BT_DATA_UUID16_ALL,
		      BT_UUID_16_ENCODE(BT_UUID_HTS_VAL),
		      BT_UUID_16_ENCODE(BT_UUID_DIS_VAL),
		      BT_UUID_16_ENCODE(BT_UUID_BAS_VAL)),
};

static const struct bt_data sd[] = {
	BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1),
};

static void connected(struct bt_conn *conn, uint8_t err)
{
	if (err) {
		printk("Connection failed, err 0x%02x %s\n", err, bt_hci_err_to_str(err));
	} else {
		printk("Connected\n");
	}
}

static void disconnected(struct bt_conn *conn, uint8_t reason)
{
	printk("Disconnected, reason 0x%02x %s\n", reason, bt_hci_err_to_str(reason));
}

BT_CONN_CB_DEFINE(conn_callbacks) = {
	.connected = connected,
	.disconnected = disconnected,
};

static void bt_ready(void)
{
	int err;

	printk("Bluetooth initialized\n");

	hts_init();

	err = bt_le_adv_start(BT_LE_ADV_CONN_FAST_1, ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));
	if (err) {
		printk("Advertising failed to start (err %d)\n", err);
		return;
	}

	printk("Advertising successfully started\n");
}

static void auth_cancel(struct bt_conn *conn)
{
	char addr[BT_ADDR_LE_STR_LEN];

	bt_addr_le_to_str(bt_conn_get_dst(conn), addr, sizeof(addr));

	printk("Pairing cancelled: %s\n", addr);
}

static struct bt_conn_auth_cb auth_cb_display = {
	.cancel = auth_cancel,
};

static void bas_notify(void)
{
	uint8_t battery_level = bt_bas_get_battery_level();

	battery_level--;

	if (!battery_level) {
		battery_level = 100U;
	}

	bt_bas_set_battery_level(battery_level);
}

/* code: 0=float, 1=1M pull-up, 2=100K pull-down, 3=10K pull-up
 * (only ANA18 bits 7:6, i.e. PA7).
 */
static void set_pa7_pull(unsigned int code)
{
	analog_write_reg8(0x18, (analog_read_reg8(0x18) & 0x3F) | ((code & 0x3) << 6));
}

int main(void)
{
	int err;

	/* Cold boot: ANA18 before/after the PA7 pull-up in soc_early_init_hook(). */
	printk("ANA18 boot: before=%02x after=%02x now=%02x\n",
	       ana18_boot_before, ana18_boot_after, analog_read_reg8(0x18));

	err = bt_enable(NULL);
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
		return 0;
	}

	bt_ready();

	bt_conn_auth_cb_register(&auth_cb_display);

	/* Advertise for a few seconds, then disable the Bluetooth controller:
	 * while the controller is ACTIVE, tl_deep_sleep() uses the BLE PM path
	 * (blc_pm_handler) and never calls soc_tlx_restore(). Disabling it forces
	 * the non-BT path and exercises soc_tlx_restore() on wake.
	 */
	k_sleep(K_SECONDS(3));
	(void)bt_le_adv_stop();
	printk("bt_disable=%d\n", bt_disable());

	/* Implement indicate. At the moment there is no suitable way
	 * of starting delayed work so we do it here
	 */
	while (1) {
		static unsigned int step;
		/* Four modes:
		 * 0: preset 1M (0x40), restore applies  -> baseline
		 * 1: preset 1M (0x40), restore skipped  -> is the restore call redundant?
		 * 2: preset 10K (0xC0), restore skipped -> does the register survive retention?
		 * 3: preset 10K (0xC0), restore applies -> can the restore call change it?
		 */
		static const unsigned char pre_code[4] = {1, 1, 3, 3};
		static const unsigned char skip[4] = {0, 1, 1, 0};
		unsigned int mode = step % 4;
		struct pm_state_info si = { .state = PM_STATE_STANDBY };
		unsigned char pre_now;

		set_pa7_pull(pre_code[mode]);
		dbg_skip_sws_restore = skip[mode];
		pre_now = analog_read_reg8(0x18);

		pm_state_force(0, &si);
		k_sleep(K_SECONDS(1));

		printk("mode=%u pre=%02x skip=%u -> wake before=%02x after=%02x now=%02x "
		       "wakes=%u deep=%d\n",
		       mode, pre_now, skip[mode],
		       ana18_wake_before, ana18_wake_after, analog_read_reg8(0x18),
		       ana18_wake_count, (int)pm_has_deep_sleep_retention_occurred());

		step++;

		/* Temperature measurements simulation */
		hts_indicate();

		/* Battery level simulation */
		bas_notify();
	}
	return 0;
}
