/*
 * Copyright (c) 2024 Telink Semiconductor
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_KEY_MATRIX_H
#define ZEPHYR_KEY_MATRIX_H

#ifdef __cplusplus
extern "C" {
#endif

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>

/* Data types */

typedef void (*key_matrix_on_button_change_t)(size_t button, bool pressed, void *context);

struct key_matrix_data {
	const struct gpio_dt_spec    *col;
	const size_t                  col_len;
	const struct gpio_dt_spec    *row;
	const size_t                  row_len;
	uint8_t                      *buttons;
	key_matrix_on_button_change_t on_button_change;
	void                         *context;
	struct k_work_delayable       work;
};

/*
 * Declare struct key_matrix_data variable base on data from .dts.
 * The name of variable should correspond to .dts node name.
 * .dts fragment example:
 * name {
 *     compatible = "gpio-keys";
 *     col {
 *         gpios = <&gpiod 6 GPIO_ACTIVE_HIGH>, <&gpiof 6 GPIO_ACTIVE_HIGH>;
 *     };
 *     row {
 *         gpios = <&gpiod 2 (GPIO_PULL_DOWN | GPIO_ACTIVE_HIGH)>,
 *                 <&gpiod 7 (GPIO_PULL_DOWN | GPIO_ACTIVE_HIGH)>;
 *     };
 * };
 */
#define KEY_MATRIX_DEFINE(name)                                                  \
	struct key_matrix_data name = {                                              \
		.col = (const struct gpio_dt_spec []) {                                  \
			COND_CODE_1(                                                         \
			 DT_NODE_HAS_PROP(DT_PATH_INTERNAL(DT_CHILD(name, col)), gpios),     \
			(DT_FOREACH_PROP_ELEM_SEP(DT_PATH_INTERNAL(DT_CHILD(name, col)),     \
				gpios, GPIO_DT_SPEC_GET_BY_IDX, (,))),                           \
			())                                                                  \
		},                                                                       \
		.col_len = COND_CODE_1(                                                  \
			 DT_NODE_HAS_PROP(DT_PATH_INTERNAL(DT_CHILD(name, col)), gpios),     \
			(DT_PROP_LEN(DT_PATH_INTERNAL(DT_CHILD(name, col)), gpios)),         \
			(0)),                                                                \
		.row = (const struct gpio_dt_spec []) {                                  \
			COND_CODE_1(                                                         \
			 DT_NODE_HAS_PROP(DT_PATH_INTERNAL(DT_CHILD(name, row)), gpios),     \
			(DT_FOREACH_PROP_ELEM_SEP(DT_PATH_INTERNAL(DT_CHILD(name, row)),     \
				gpios, GPIO_DT_SPEC_GET_BY_IDX, (,))),                           \
			())                                                                  \
		},                                                                       \
		.row_len = COND_CODE_1(                                                  \
			 DT_NODE_HAS_PROP(DT_PATH_INTERNAL(DT_CHILD(name, row)), gpios),     \
			(DT_PROP_LEN(DT_PATH_INTERNAL(DT_CHILD(name, row)), gpios)),         \
			(0)),                                                                \
		.buttons = (uint8_t [COND_CODE_1(UTIL_AND(                               \
			 DT_NODE_HAS_PROP(DT_PATH_INTERNAL(DT_CHILD(name, col)), gpios),     \
			 DT_NODE_HAS_PROP(DT_PATH_INTERNAL(DT_CHILD(name, row)), gpios)),    \
			(DIV_ROUND_UP(                                                       \
				DT_PROP_LEN(DT_PATH_INTERNAL(DT_CHILD(name, col)), gpios) *      \
				DT_PROP_LEN(DT_PATH_INTERNAL(DT_CHILD(name, row)), gpios), 8)),  \
			(0))]) {},                                                           \
	}

/* Public APIs */

bool key_matrix_init(struct key_matrix_data *key_matrix);
void key_matrix_set_callback(struct key_matrix_data *key_matrix,
	key_matrix_on_button_change_t on_button_change, void *context);

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_KEY_MATRIX_H */
