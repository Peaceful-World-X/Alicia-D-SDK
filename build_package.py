#!/usr/bin/env python3
"""
Alicia-D-SDK 打包脚本
用于将项目打包为可分发的 Python 安装包 (wheel 和 tar.gz)
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def print_step(message):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")


def run_command(cmd, cwd=None):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        print(f"输出: {e.stdout}")
        print(f"错误: {e.stderr}")
        return False


def clean_build_artifacts():
    """清理之前的构建产物"""
    print_step("清理旧的构建产物")

    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for pattern in dirs_to_clean:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                print(f"删除目录: {path}")
                shutil.rmtree(path)
            elif path.is_file():
                print(f"删除文件: {path}")
                path.unlink()

    print("清理完成!")


def check_dependencies():
    """检查必要的打包工具"""
    print_step("检查打包工具")

    required_packages = ['setuptools', 'wheel', 'build']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} 已安装")
        except ImportError:
            print(f"✗ {package} 未安装")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n需要安装缺失的包: {', '.join(missing_packages)}")
        print("正在安装...")
        if not run_command(f"pip install {' '.join(missing_packages)}"):
            print("安装失败,请手动安装这些包")
            return False

    return True


def build_source_distribution():
    """构建源代码分发包 (.tar.gz)"""
    print_step("构建源代码分发包 (sdist)")

    if run_command("python setup.py sdist"):
        print("✓ 源代码分发包构建成功!")
        return True
    else:
        print("✗ 源代码分发包构建失败!")
        return False


def build_wheel_distribution():
    """构建 wheel 分发包 (.whl)"""
    print_step("构建 wheel 分发包 (bdist_wheel)")

    if run_command("python setup.py bdist_wheel"):
        print("✓ Wheel 分发包构建成功!")
        return True
    else:
        print("✗ Wheel 分发包构建失败!")
        return False


def build_with_build_module():
    """使用 build 模块构建 (推荐方式)"""
    print_step("使用 build 模块构建所有分发包")

    if run_command("python -m build"):
        print("✓ 所有分发包构建成功!")
        return True
    else:
        print("✗ 分发包构建失败!")
        return False


def list_distributions():
    """列出构建的分发包"""
    print_step("构建的分发包")

    dist_path = Path('dist')
    if not dist_path.exists():
        print("dist 目录不存在!")
        return

    files = list(dist_path.glob('*'))
    if not files:
        print("没有找到分发包!")
        return

    print("已生成以下分发包:\n")
    for file in sorted(files):
        size = file.stat().st_size / (1024 * 1024)  # MB
        print(f"  - {file.name} ({size:.2f} MB)")

    print(f"\n总共 {len(files)} 个文件")


def show_installation_instructions():
    """显示安装说明"""
    print_step("安装说明")

    print("本地安装:")
    print("  pip install dist/alicia_d_sdk-*.whl")
    print("\n或:")
    print("  pip install dist/alicia_d_sdk-*.tar.gz")

    print("\n分享给他人:")
    print("  1. 将 dist/ 目录下的 .whl 或 .tar.gz 文件发送给他人")
    print("  2. 收到文件后使用以下命令安装:")
    print("     pip install alicia_d_sdk-<version>-py3-none-any.whl")

    print("\n上传到 PyPI (需要账号):")
    print("  pip install twine")
    print("  twine upload dist/*")

    print("\n创建离线安装包:")
    print("  pip download -r requirements.txt -d offline_packages/")
    print("  # 然后将 offline_packages/ 和 dist/ 一起分发")


def create_offline_package():
    """创建离线安装包"""
    print_step("创建离线安装包 (可选)")

    response = input("是否创建包含所有依赖的离线安装包? (y/N): ").strip().lower()
    if response != 'y':
        print("跳过离线安装包创建")
        return

    offline_dir = Path('offline_packages')
    if offline_dir.exists():
        shutil.rmtree(offline_dir)
    offline_dir.mkdir()

    print("正在下载所有依赖...")
    if run_command(f"pip download -r requirements.txt -d {offline_dir}"):
        print(f"✓ 依赖已下载到 {offline_dir}/")
        print(f"\n离线安装方法:")
        print(f"  pip install --no-index --find-links={offline_dir} dist/alicia_d_sdk-*.whl")
    else:
        print("✗ 下载依赖失败!")


def main():
    """主函数"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║          Alicia-D-SDK 打包工具                            ║
    ║          将项目打包为 Python 安装包                        ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    # 检查是否在正确的目录
    if not Path('setup.py').exists():
        print("错误: 未找到 setup.py 文件!")
        print("请在项目根目录运行此脚本")
        sys.exit(1)

    # 步骤 1: 清理旧文件
    clean_build_artifacts()

    # 步骤 2: 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 步骤 3: 构建分发包
    print("\n选择构建方式:")
    print("  1. 使用 build 模块 (推荐, 同时构建 wheel 和 sdist)")
    print("  2. 仅构建 wheel")
    print("  3. 仅构建源代码包 (sdist)")
    print("  4. 构建全部 (使用 setuptools)")

    choice = input("\n请选择 (1-4, 默认为 1): ").strip() or "1"

    success = False
    if choice == "1":
        success = build_with_build_module()
    elif choice == "2":
        success = build_wheel_distribution()
    elif choice == "3":
        success = build_source_distribution()
    elif choice == "4":
        success = build_source_distribution() and build_wheel_distribution()
    else:
        print("无效的选择!")
        sys.exit(1)

    if not success:
        print("\n打包失败!")
        sys.exit(1)

    # 步骤 4: 列出生成的文件
    list_distributions()

    # 步骤 5: 创建离线包 (可选)
    create_offline_package()

    # 步骤 6: 显示安装说明
    show_installation_instructions()

    print_step("打包完成!")
    print("✓ 所有分发包已生成在 dist/ 目录中")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
