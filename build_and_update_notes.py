#!/usr/bin/env python3
import os
import re
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class TelinkBuildManager:
    def __init__(self, zephyr_root: Optional[Path] = None):
        self.zephyr_root = zephyr_root or Path(__file__).parent
        
        # 发布构建输出主目录
        self.release_dir = self.zephyr_root / "build_for_release"
        self.release_dir.mkdir(exist_ok=True)
        
        # 构建日志目录
        self.build_logs_dir = self.release_dir / "build_logs"
        self.build_logs_dir.mkdir(exist_ok=True)
        
        # 固件输出目录
        self.firmware_output_dir = self.release_dir / "firmware"
        self.firmware_output_dir.mkdir(exist_ok=True)
        
        # 模板文件和输出文件
        self.template_path = self.zephyr_root / "tl_zephyr_sdk_Release_Note_template.md"
        self.output_path = self.release_dir / "tl_zephyr_sdk_Release_Note.md"
        
        # 定义所有板卡和 samples
        self.board_builds = self._get_board_builds()
        
        # sample 名称映射
        self.sample_map = {
            "blinky": "samples/basic/blinky",
            "hello_world": "samples/hello_world",
            "button": "samples/basic/button",
            "fade_led": "samples/basic/fade_led",
            "blinky_pwm": "samples/basic/blinky_pwm",
            "adc_dt": "samples/drivers/adc/adc_dt",
            "sht3xd": "samples/sensor/sht3xd",
            "mpu6050": "samples/sensor/mpu6050",
            "spi_flash": "samples/drivers/spi_flash",
            "spi_flash_at45": "samples/drivers/spi_flash_at45",
            "watchdog": "samples/drivers/watchdog",
            "uart_echo_bot": "samples/drivers/uart/echo_bot",
            "peripheral_ht": "samples/bluetooth/peripheral_ht",
            "cli": "samples/net/openthread/cli",
            "coprocessor": "samples/net/openthread/coprocessor",
            "echo_client": "samples/net/sockets/echo_client",
            "echo_server": "samples/net/sockets/echo_server",
            "retention_echo_client": "samples/net/sockets/echo_client",
            "retention_basic": "samples/retention/basic",
            "mbedtls": "samples/crypto/mbedtls",
            "console": "samples/usb/console",
            "cdc_acm": "samples/usb/cdc_acm",
            "common": "samples/common",
            "factorydata": "samples/factorydata",
            "smp_svr": "samples/smp_svr",
            "ml3m_button": "samples/ml3m_button",
            "gpio-kbd-matrix": "samples/boards/tlsr9x/gpio-kbd-matrix",
            "sock_simple_ipv4": "samples/boards/tlsr9x/sock_simple",
            "sock_simple_ipv6": "samples/boards/tlsr9x/sock_simple",
            "key_matrix": "samples/boards/tlsr9x/key_matrix",
            "key_pool": "samples/boards/tlsr9x/key_pool",
            "led_pool": "samples/boards/tlsr9x/led_pool",
            "pwm_pool": "samples/boards/tlsr9x/pwm_pool",
            "shell": "samples/subsys/shell/devmem_load/",
            "nvs": "samples/subsys/nvs",
            "adc_api": "tests/drivers/adc/adc_api",
        }
        
        # 板卡家族映射
        self.board_family = {
            "tl3238x": "TL323X",
            "tl3238x_retention": "TL323X",
            "tl7218x": "TL721X",
            "tl7218x_retention": "TL721X",
            "tlsr9118bdk40d": "TLSR9118BDK40D",
            "tlsr9118bdk40d_v1": "TLSR9118BDK40D",
            "tlsr9518adk80d": "TLSR951X",
            "tlsr9528a": "TLSR952X",
            "tl3218x": "TL321X",
            "tl3228x": "TL322X",
        }
        
        # 用户要求的板卡顺序
        self.board_order = [
            ("tlsr9518adk80d", "TLSR951X"),
            ("tlsr9528a", "TLSR952X"),
            ("tl3218x", "TL321X"),
            ("tl3228x", "TL322X"),
            ("tl3238x", "TL323X"),
            ("tl7218x", "TL721X"),
            ("tlsr9118bdk40d", "TLSR9118BDK40D"),
        ]
    
    def _get_board_builds(self) -> List[Tuple[str, str, str, List[str]]]:
        """定义所有板卡和 samples 的构建配置"""
        builds = []
        
        # -------------------------- TL323X --------------------------
        builds.extend([
            ("tl3238x", "blinky", "samples/basic/blinky", []),
            ("tl3238x", "hello_world", "samples/hello_world", []),
            ("tl3238x", "button", "samples/basic/button", []),
            ("tl3238x", "fade_led", "samples/basic/fade_led", []),
            ("tl3238x", "console", "samples/subsys/usb/console", []),
            ("tl3238x", "peripheral_ht", "samples/bluetooth/peripheral_ht", []),
            ("tl3238x", "cli", "samples/net/openthread/cli", []),
            ("tl3238x", "mbedtls", "tests/crypto/mbedtls", ["-DCONFIG_MBEDTLS_ECP_C=y", "-DCONFIG_MBEDTLS_ECP_ALL_ENABLED=y"]),
            ("tl3238x", "spi_flash", "samples/drivers/spi_flash", []),
            ("tl3238x", "watchdog", "samples/drivers/watchdog", []),
            ("tl3238x", "sht3xd", "samples/sensor/sht3xd", []),
            ("tl3238x", "adc_dt", "samples/drivers/adc/adc_dt", []),
            ("tl3238x", "retention_basic", "samples/retention/basic", []),
            ("tl3238x_retention", "retention_echo_client", "samples/net/sockets/echo_client", ["-DOVERLAY_CONFIG=overlay-ot-sed.conf", "-DCONFIG_OPENTHREAD_NETWORKKEY=\"09:24:01:56:04:4a:45:0b:23:22:1e:0e:3b:0d:0e:61:2f:1b:2c:24\"", "-DCONFIG_PM=y", "-DCONFIG_SOC_SERIES_RISCV_TELINK_TLX_NON_RETENTION_RAM_CODE=y"]),
        ])
        
        # -------------------------- TL721X --------------------------
        builds.extend([
            ("tl7218x", "blinky", "samples/basic/blinky", []),
            ("tl7218x", "hello_world", "samples/hello_world", []),
            ("tl7218x", "button", "samples/basic/button", []),
            ("tl7218x", "fade_led", "samples/basic/fade_led", []),
            ("tl7218x", "console", "samples/subsys/usb/console", []),
            ("tl7218x", "peripheral_ht", "samples/bluetooth/peripheral_ht", []),
            ("tl7218x", "cli", "samples/net/openthread/cli", []),
            ("tl7218x", "echo_server", "samples/net/sockets/echo_server", ["-DOVERLAY_CONFIG=overlay-ot.conf", "-DCONFIG_OPENTHREAD_NETWORKKEY=\"09:24:01:56:04:4a:45:0b:23:22:1e:0e:3b:0d:0e:61:2f:1b:2c:24\""]),
            ("tl7218x", "echo_client", "samples/net/sockets/echo_client", ["-DOVERLAY_CONFIG=overlay-ot-sed.conf", "-DCONFIG_OPENTHREAD_NETWORKKEY=\"09:24:01:56:04:4a:45:0b:23:22:1e:0e:3b:0d:0e:61:2f:1b:2c:24\""]),
            ("tl7218x", "mbedtls", "tests/crypto/mbedtls", ["-DCONFIG_MBEDTLS_ECP_C=y", "-DCONFIG_MBEDTLS_ECP_ALL_ENABLED=y"]),
            ("tl7218x", "spi_flash", "samples/drivers/spi_flash", []),
            ("tl7218x", "watchdog", "samples/drivers/watchdog", []),
            ("tl7218x", "sht3xd", "samples/sensor/sht3xd", []),
            ("tl7218x", "adc_dt", "samples/drivers/adc/adc_dt", []),
            ("tl7218x_retention", "retention_echo_client", "samples/net/sockets/echo_client", ["-DOVERLAY_CONFIG=overlay-ot-sed.conf", "-DCONFIG_OPENTHREAD_NETWORKKEY=\"09:24:01:56:04:4a:45:0b:23:22:1e:0e:3b:0d:0e:61:2f:1b:2c:24\"", "-DCONFIG_PM=y", "-DCONFIG_SOC_SERIES_RISCV_TELINK_TLX_NON_RETENTION_RAM_CODE=y"]),
        ])
        
        # -------------------------- TLSR9118BDK40D --------------------------
        builds.extend([
            ("tlsr9118bdk40d", "blinky", "samples/basic/blinky", []),
            ("tlsr9118bdk40d", "button", "samples/basic/button", []),
            ("tlsr9118bdk40d", "uart_echo_bot", "samples/drivers/uart/echo_bot", []),
            ("tlsr9118bdk40d", "mpu6050", "samples/sensor/mpu6050", []),
            ("tlsr9118bdk40d", "spi_flash_at45", "samples/drivers/spi_flash_at45", []),
            ("tlsr9118bdk40d", "nvs", "samples/subsys/nvs", []),
            ("tlsr9118bdk40d", "peripheral_ht", "samples/bluetooth/peripheral_ht", []),
            ("tlsr9118bdk40d", "sock_simple_ipv4", "samples/boards/tlsr9x/sock_simple", []),
            ("tlsr9118bdk40d", "sock_simple_ipv6", "samples/boards/tlsr9x/sock_simple", ["-DCONFIG_APP_SOCKET_UDP_IPV6=y"]),
            ("tlsr9118bdk40d", "key_matrix", "samples/boards/tlsr9x/key_matrix", []),
            ("tlsr9118bdk40d", "key_pool", "samples/boards/tlsr9x/key_pool", []),
            ("tlsr9118bdk40d", "led_pool", "samples/boards/tlsr9x/led_pool/", []),
            ("tlsr9118bdk40d", "pwm_pool", "samples/boards/tlsr9x/pwm_pool/", []),
            ("tlsr9118bdk40d", "shell", "samples/subsys/shell/devmem_load/", []),
            ("tlsr9118bdk40d", "mbedtls", "tests/crypto/mbedtls", ["-DCONFIG_MBEDTLS_ECP_C=y", "-DCONFIG_MBEDTLS_ECP_ALL_ENABLED=y"]),
            ("tlsr9118bdk40d", "adc_api", "tests/drivers/adc/adc_api", []),
            ("tlsr9118bdk40d", "cli", "samples/net/openthread/cli", []),
            ("tlsr9118bdk40d_v1", "gpio-kbd-matrix", "samples/boards/tlsr9x/gpio-kbd-matrix", []),
        ])
        
        # -------------------------- TLSR951X/B91 --------------------------
        builds.extend([
            ("tlsr9518adk80d", "blinky", "samples/basic/blinky", []),
            ("tlsr9518adk80d", "peripheral_ht", "samples/bluetooth/peripheral_ht", []),
            ("tlsr9518adk80d", "gpio-kbd-matrix", "samples/boards/tlsr9x/gpio-kbd-matrix", []),
            ("tlsr9518adk80d", "mbedtls", "samples/crypto/mbedtls", []),
            ("tlsr9518adk80d", "cli", "samples/net/openthread/cli", []),
            ("tlsr9518adk80d", "retention_basic", "samples/retention/basic", []),
            ("tlsr9518adk80d", "smp_svr", "samples/smp_svr", []),
            ("tlsr9518adk80d", "console", "samples/usb/console", []),
        ])
        
        # -------------------------- TLSR952X/B92 --------------------------
        builds.extend([
            ("tlsr9528a", "blinky", "samples/basic/blinky", []),
            ("tlsr9528a", "peripheral_ht", "samples/bluetooth/peripheral_ht", []),
            ("tlsr9528a", "gpio-kbd-matrix", "samples/boards/tlsr9x/gpio-kbd-matrix", []),
            ("tlsr9528a", "mbedtls", "samples/crypto/mbedtls", []),
            ("tlsr9528a", "factorydata", "samples/factorydata", []),
            ("tlsr9528a", "cli", "samples/net/openthread/cli", []),
            ("tlsr9528a", "retention_basic", "samples/retention/basic", []),
            ("tlsr9528a", "smp_svr", "samples/smp_svr", []),
            ("tlsr9528a", "console", "samples/usb/console", []),
        ])
        
        # -------------------------- TL321X --------------------------
        builds.extend([
            ("tl3218x", "blinky", "samples/basic/blinky", []),
            ("tl3218x", "button", "samples/basic/button", []),
            ("tl3218x", "fade_led", "samples/basic/fade_led", []),
            ("tl3218x", "peripheral_ht", "samples/bluetooth/peripheral_ht", []),
            ("tl3218x", "gpio-kbd-matrix", "samples/boards/tlsr9x/gpio-kbd-matrix", []),
            ("tl3218x", "common", "samples/common", []),
            ("tl3218x", "mbedtls", "samples/crypto/mbedtls", []),
            ("tl3218x", "adc_dt", "samples/drivers/adc/adc_dt", []),
            ("tl3218x", "spi_flash", "samples/drivers/spi_flash", []),
            ("tl3218x", "watchdog", "samples/drivers/watchdog", []),
            ("tl3218x", "hello_world", "samples/hello_world", []),
            ("tl3218x", "ml3m_button", "samples/ml3m_button", []),
            ("tl3218x", "cli", "samples/net/openthread/cli", []),
            ("tl3218x", "coprocessor", "samples/net/openthread/coprocessor", []),
            ("tl3218x", "retention_basic", "samples/retention/basic", []),
            ("tl3218x", "sht3xd", "samples/sensor/sht3xd", []),
            ("tl3218x", "cdc_acm", "samples/usb/cdc_acm", []),
            ("tl3218x", "console", "samples/usb/console", []),
        ])
        
        # -------------------------- TL322X --------------------------
        builds.extend([
            ("tl3228x", "blinky", "samples/basic/blinky", []),
            ("tl3228x", "button", "samples/basic/button", []),
            ("tl3228x", "common", "samples/common", []),
            ("tl3228x", "adc_dt", "samples/drivers/adc/adc_dt", []),
            ("tl3228x", "watchdog", "samples/drivers/watchdog", []),
            ("tl3228x", "hello_world", "samples/hello_world", []),
            ("tl3228x", "sht3xd", "samples/sensor/sht3xd", []),
        ])
        
        return builds
    
    def build_all(self):
        """构建所有板卡的所有 samples"""
        print("=" * 80)
        print("Building all Telink samples...")
        print("=" * 80)
        print()
        
        success_count = 0
        fail_count = 0
        
        for board, sample_name, source, extra_args in self.board_builds:
            build_dir_name = f"build_{board}_{sample_name}"
            build_dir = self.release_dir / build_dir_name
            
            # 移除 _retention 后缀用于 log 文件名
            base_board_name = board.replace("_retention", "").replace("_v1", "")
            log_filename = f"build_{base_board_name}_{sample_name}.log"
            log_file = self.build_logs_dir / log_filename
            
            print(f"  Building {board} {sample_name}...")
            print(f"  Source: {source}")
            
            cmd = [
                "west", "build",
                "-b", board,
                "-d", str(build_dir),
                source,
                "--",
                "-DCONFIG_COMPILER_WARNINGS_AS_ERRORS=y"
            ] + extra_args
            
            print(f"  Command: {' '.join(cmd)}")
            
            # 执行构建
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.zephyr_root),
                check=False
            )
            
            # 写入日志
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"Command: {' '.join(cmd)}\n\n")
                f.write(f"STDOUT:\n{result.stdout}\n\n")
                f.write(f"STDERR:\n{result.stderr}\n\n")
                f.write(f"Return code: {result.returncode}\n")
            
            # 复制 build.log
            build_log = build_dir / "build.log"
            if build_log.exists():
                with open(log_file, "ab") as f:
                    f.write(b"\n\n" + b"=" * 80 + b"\n")
                    f.write(b"build.log:\n\n")
                    with open(build_log, "rb") as src:
                        shutil.copyfileobj(src, f)
            
            if result.returncode == 0:
                print(f"  Success! Log written to {log_file}")
                success_count += 1
            else:
                print(f"  Failed! Log written to {log_file}")
                fail_count += 1
            
            print()
        
        print("=" * 80)
        print(f"Build complete! {success_count} succeeded, {fail_count} failed.")
        print("=" * 80)
    
    def extract_memory_info(self) -> Dict[str, Dict[str, List[Dict]]]:
        """从 log 文件中提取内存信息"""
        data = {}
        
        print()
        print("=" * 80)
        print("Extracting memory usage information from logs...")
        print("=" * 80)
        print()
        
        for log_file in self.build_logs_dir.glob("build_*.log"):
            filename = log_file.name
            base = filename.replace("build_", "").replace(".log", "")
            
            # 查找板卡
            board = None
            sample_part = None
            for b in sorted(self.board_family.keys(), key=lambda x: -len(x)):
                if base.startswith(b):
                    board = b
                    sample_part = base[len(b):]
                    if sample_part.startswith("_"):
                        sample_part = sample_part[1:]
                    break
            
            if not board:
                # 尝试不带 _retention/_v1 后缀查找
                for b in sorted(self.board_family.keys(), key=lambda x: -len(x)):
                    base_b = b.replace("_retention", "").replace("_v1", "")
                    if base.startswith(base_b):
                        board = base_b
                        sample_part = base[len(base_b):]
                        if sample_part.startswith("_"):
                            sample_part = sample_part[1:]
                        break
            
            if not board:
                continue
            
            sample_name = self.sample_map.get(sample_part, f"samples/{sample_part}")
            
            # 读取文件
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # 查找内存信息
            idx = content.find("Memory region")
            if idx == -1:
                continue
            
            # 提取内存区域
            memory_end = content.find("Generating files from", idx)
            if memory_end == -1:
                memory_end = idx + 600
            
            memory_text = content[idx:memory_end]
            
            # 解析
            memory_regions = []
            lines = memory_text.split("\n")
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                if "IDT_LIST" in line:
                    break
                
                # 使用正则解析
                match = re.match(r"(\S+):\s*(\d+)\s*(\S+)\s*(\d+)\s*(\S+)\s*([\d.]+)%", line)
                if match:
                    name = match.group(1).rstrip(":")
                    used = f"{match.group(2)} {match.group(3)}"
                    size = f"{match.group(4)} {match.group(5)}"
                    percent = f"{match.group(6)}%"
                    memory_regions.append({
                        "name": name,
                        "used": used,
                        "size": size,
                        "percent": percent
                    })
                else:
                    # 另一种格式如 RAM_ILM_N:         27 KB       128 KB     21.09%
                    match2 = re.match(r"(\S+):\s*([\d.]+)\s*(\S+)\s*([\d.]+)\s*(\S+)\s*([\d.]+)%", line)
                    if match2:
                        name = match2.group(1).rstrip(":")
                        used = f"{match2.group(2)} {match2.group(3)}"
                        size = f"{match2.group(4)} {match2.group(5)}"
                        percent = f"{match2.group(6)}%"
                        memory_regions.append({
                            "name": name,
                            "used": used,
                            "size": size,
                            "percent": percent
                        })
            
            if memory_regions:
                # 查找基础板卡名（不带 _retention/_v1）
                base_board = board.replace("_retention", "").replace("_v1", "")
                family = None
                for b, f in self.board_family.items():
                    if b.startswith(base_board):
                        family = f
                        break
                
                if not family:
                    family = self.board_family.get(base_board, base_board.upper())
                
                if family not in data:
                    data[family] = {}
                if base_board not in data[family]:
                    data[family][base_board] = []
                data[family][base_board].append({
                    "name": sample_name,
                    "memory": memory_regions
                })
        
        total_samples = sum(len(b) for f in data.values() for b in f.values())
        print(f"Processed {total_samples} samples successfully!")
        
        return data
    
    def update_release_notes(self, data: Dict[str, Dict[str, List[Dict]]]):
        """更新 tl_zephyr_sdk_Release_Note.md 文件"""
        print()
        print("=" * 80)
        print("Updating tl_zephyr_sdk_Release_Note.md...")
        print("=" * 80)
        print()
        
        # 检查模板文件是否存在
        if not self.template_path.exists():
            print(f"Warning: Template file {self.template_path} does not exist! Creating from current release note.")
            if self.output_path.exists():
                shutil.copy(self.output_path, self.template_path)
            else:
                print("Error: Neither template nor current release note exists!")
                return
        
        # 构建新的 Resource Usage 部分（表格格式）
        resource_usage_lines = []
        resource_usage_lines.append("## 📊 Resource Usage (Code Size)")
        resource_usage_lines.append("")
        resource_usage_lines.append("This section shows the RAM and ROM usage for various Zephyr samples on Telink platforms, based on Zephyr SDK 0.17.0 with riscv64-zephyr-elf toolchain.")
        resource_usage_lines.append("")
        resource_usage_lines.append("### Supported Boards")
        resource_usage_lines.append("")
        resource_usage_lines.append("| Board | Chip Family |")
        resource_usage_lines.append("|-------|-------------|")
        resource_usage_lines.append("| tlsr9518adk80d | TLSR951X/B91 |")
        resource_usage_lines.append("| tlsr9528a | TLSR952X/B92 |")
        resource_usage_lines.append("| tl3218x | TL321X |")
        resource_usage_lines.append("| tl3228x | TL322X |")
        resource_usage_lines.append("| tl3238x | TL323X |")
        resource_usage_lines.append("| tl7218x | TL721X |")
        resource_usage_lines.append("| tlsr9118bdk40d | TLSR9118BDK40D |")
        resource_usage_lines.append("")
        resource_usage_lines.append("---")
        resource_usage_lines.append("")
        
        for board_name, family_name in self.board_order:
            if family_name not in data or board_name not in data[family_name]:
                print(f"Warning: No data for {board_name} ({family_name})")
                continue
            
            resource_usage_lines.append(f"### {family_name} ({board_name})")
            resource_usage_lines.append("")
            resource_usage_lines.append("📈 **Resource Usage Details**")
            resource_usage_lines.append("")
            
            samples = sorted(data[family_name][board_name], key=lambda x: x["name"])
            
            if not samples:
                continue
            
            # 获取内存区域名称（使用第一个 sample 的区域名作为表头）
            region_names = [r["name"] for r in samples[0]["memory"]]
            
            # 表头
            headers = ["Sample"] + region_names
            resource_usage_lines.append("| " + " | ".join(headers) + " |")
            resource_usage_lines.append("|" + "|".join(["---" for _ in headers]) + "|")
            
            # 数据行
            for sample in samples:
                row = [f"**{sample['name']}**"]
                region_map = {r["name"]: r for r in sample["memory"]}
                for region_name in region_names:
                    if region_name in region_map:
                        r = region_map[region_name]
                        row.append(f"{r['used']} ({r['percent']} of {r['size']})")
                    else:
                        row.append("N/A")
                resource_usage_lines.append("| " + " | ".join(row) + " |")
            
            resource_usage_lines.append("")
            resource_usage_lines.append("---")
            resource_usage_lines.append("")
        
        # 读取模板文件
        with open(self.template_path, "r", encoding="utf-8") as f:
            template_lines = f.read().split("\n")
        
        new_lines = []
        i = 0
        
        while i < len(template_lines):
            line = template_lines[i]
            
            # 匹配 Resource Usage 部分开始（支持带 emoji 的标题）
            if "Resource Usage" in line and line.startswith("#"):
                # 添加生成的 Resource Usage 内容
                new_lines.extend(resource_usage_lines)
                
                # 跳过原 Resource Usage 部分，直到找到 Additional Notes
                i += 1
                while i < len(template_lines):
                    if "Additional Notes" in template_lines[i] and template_lines[i].startswith("#"):
                        break
                    i += 1
                continue
            
            new_lines.append(line)
            i += 1
        
        # 写回
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        
        print(f"Updated tl_zephyr_sdk_Release_Note.md successfully from {self.template_path}!")
    
    def collect_firmware(self):
        """收集所有板卡的所有 samples 固件"""
        print()
        print("=" * 80)
        print("Collecting firmware files...")
        print("=" * 80)
        print()
        
        # 需要收集的固件文件类型
        firmware_files = [
            "zephyr.bin",
            "zephyr.elf",
            "zephyr.hex",
            "zephyr.dts",
            ".config"
        ]
        
        # 按板卡组织固件
        board_firmware = {}
        
        for board, sample_name, source, extra_args in self.board_builds:
            build_dir_name = f"build_{board}_{sample_name}"
            build_dir = self.release_dir / build_dir_name
            zephyr_dir = build_dir / "zephyr"
            
            if not zephyr_dir.exists():
                continue
            
            # 获取基础板卡名
            base_board_name = board.replace("_retention", "").replace("_v1", "")
            
            if base_board_name not in board_firmware:
                board_firmware[base_board_name] = []
            
            # 创建板卡 sample 目录
            sample_firmware_dir = self.firmware_output_dir / base_board_name / sample_name
            sample_firmware_dir.mkdir(parents=True, exist_ok=True)
            
            # 复制固件文件
            copied_files = []
            for fw_file in firmware_files:
                src_file = zephyr_dir / fw_file
                if src_file.exists():
                    dst_file = sample_firmware_dir / fw_file
                    shutil.copy2(src_file, dst_file)
                    copied_files.append(fw_file)
            
            # 记录成功的固件
            if copied_files:
                board_firmware[base_board_name].append({
                    "sample_name": sample_name,
                    "source": source,
                    "directory": sample_firmware_dir,
                    "files": copied_files
                })
                print(f"  Collected: {base_board_name}/{sample_name} - {len(copied_files)} files")
        
        return board_firmware
    
    def create_firmware_archives(self, board_firmware: Dict[str, List[Dict]]):
        """为每个板卡创建独立的压缩包"""
        print()
        print("=" * 80)
        print("Creating firmware archives...")
        print("=" * 80)
        print()
        
        archives_created = []
        
        for board_name, samples in board_firmware.items():
            if not samples:
                continue
            
            # 创建压缩包文件名
            archive_path = self.firmware_output_dir / f"{board_name}_firmware.zip"
            
            # 删除已存在的压缩包
            if archive_path.exists():
                archive_path.unlink()
            
            # 创建压缩包
            print(f"  Creating archive for {board_name}...")
            
            import zipfile
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for sample in samples:
                    sample_dir = sample["directory"]
                    for file_name in sample["files"]:
                        file_path = sample_dir / file_name
                        arcname = f"{board_name}/{sample['sample_name']}/{file_name}"
                        zipf.write(file_path, arcname)
            
            archives_created.append(archive_path)
            print(f"  Created: {archive_path}")
        
        return archives_created
    
    def run(self, build: bool = True, collect_firmware: bool = True):
        """运行完整流程"""
        if build:
            self.build_all()
        
        data = self.extract_memory_info()
        self.update_release_notes(data)
        
        # 收集并打包固件
        if collect_firmware:
            board_firmware = self.collect_firmware()
            self.create_firmware_archives(board_firmware)
        
        print()
        print("=" * 80)
        print("All tasks complete!")
        print("=" * 80)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Telink samples and update release notes.")
    parser.add_argument("--skip-build", action="store_true", help="Skip building samples, just update release notes from existing logs")
    parser.add_argument("--skip-firmware", action="store_true", help="Skip collecting and archiving firmware")
    args = parser.parse_args()
    
    manager = TelinkBuildManager()
    
    # 修改 run 方法来支持跳过固件收集
    manager.run(build=not args.skip_build, collect_firmware=not args.skip_firmware)


if __name__ == "__main__":
    main()
