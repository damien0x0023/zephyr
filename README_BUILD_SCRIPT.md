# Telink Build and Release Notes Update Script

## 脚本说明

这个完整的脚本 `build_and_update_notes.py` 可以：
1. 编译所有 Telink 板卡的所有 samples
2. 从构建日志中提取内存使用信息
3. 从模板文件 `tl_zephyr_sdk_Release_Note_template.md` 生成最终的发布说明文件（Resource Usage 部分使用表格格式）
4. 收集所有板卡的所有 samples 固件文件并为每个板卡创建独立的压缩包
5. 所有输出都组织在 `build_for_release/` 目录下

## 文件说明

- `build_and_update_notes.py` - 主要的构建和更新脚本
- `tl_zephyr_sdk_Release_Note_template.md` - 发布说明模板文件（包含所有静态内容）
- `build_for_release/` - 所有输出的根目录
  - `build_logs/` - 包含所有构建日志的目录
  - `firmware/` - 包含所有板卡固件文件和压缩包的目录
  - `tl_zephyr_sdk_Release_Note.md` - 最终的发布说明文件（由脚本从模板生成）
- `README_BUILD_SCRIPT.md` - 本文件

## 使用方法

### 1. 完整运行（构建 + 更新 + 固件打包）

```bash
cd /home/ubuntu/zephyrproject/zephyr
python3 build_and_update_notes.py
```

这将：
- 构建所有板卡的所有 samples
- 保存日志到 build_logs 目录
- 从日志中提取内存使用信息
- 从模板文件 `tl_zephyr_sdk_Release_Note_template.md` 生成最终的 `tl_zephyr_sdk_Release_Note.md` 文件
- 收集所有固件文件到 firmware/ 目录
- 为每个板卡创建独立的固件压缩包

### 2. 只更新发布说明（跳过构建）

```bash
python3 build_and_update_notes.py --skip-build
```

如果已经有构建日志，只需更新发布说明和收集固件时使用此命令。

### 3. 跳过固件收集和打包

```bash
python3 build_and_update_notes.py --skip-firmware
```

如果不需要收集和打包固件，使用此选项。

## 固件压缩包内容

每个板卡的压缩包包含：
- `board_name/sample_name/zephyr.bin` - 二进制固件文件
- `board_name/sample_name/zephyr.elf` - ELF 格式固件文件
- `board_name/sample_name/zephyr.hex` - Intel HEX 格式固件文件（如果有）
- `board_name/sample_name/zephyr.dts` - 设备树文件
- `board_name/sample_name/.config` - 配置文件

## 支持的板卡

1. tlsr9518adk80d (TLSR951X/B91)
2. tlsr9528a (TLSR952X/B92)
3. tl3218x (TL321X)
4. tl3228x (TL322X)
5. tl3238x (TL323X)
6. tl7218x (TL721X)
7. tlsr9118bdk40d (TLSR9118BDK40D)

## 脚本特点

- 结构化的类设计，易于维护和扩展
- 基于模板生成发布说明，保持所有静态内容的一致性
- Resource Usage 部分使用表格格式，清晰展示各板卡各 sample 的内存使用情况
- 仅更新 Resource Usage 部分，保留其他部分的内容不变
- 支持添加新的板卡和 samples
- 详细的日志输出
- 可跳过构建步骤，直接从现有日志更新
- 如果模板文件不存在，会自动从当前的发布说明文件创建模板
- 自动收集固件文件并为每个板卡创建独立的压缩包
- 支持跳过固件收集和打包的选项

## 添加新的板卡或 samples

在 `TelinkBuildManager` 类中：

1. 在 `_get_board_builds()` 方法中添加新的构建配置
2. 在 `sample_map` 中添加新的 sample 名称映射（如果需要）
3. 在 `board_family` 中添加新的板卡家族映射
4. 在 `board_order` 中添加新的板卡顺序

## 更新模板文件

如果您需要更新模板文件中的静态内容（如 Introduction、Version Information、Additional Notes 等），只需直接编辑 `tl_zephyr_sdk_Release_Note_template.md` 文件即可。下次运行脚本时，这些更改会自动反映在最终的发布说明文件中。
