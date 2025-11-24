# Alicia-D-SDK 打包使用指南

本指南说明如何将 Alicia-D-SDK 打包为 Python 安装包并分发。

## 快速开始

### 1. 运行打包脚本

在项目根目录下执行:

```bash
cd /path/to/Alicia-D-SDK
python build_package.py
```

### 2. 选择构建方式

脚本会提示您选择:
- **选项 1** (推荐): 使用 build 模块,同时构建 wheel 和源码包
- **选项 2**: 仅构建 wheel 包
- **选项 3**: 仅构建源码包
- **选项 4**: 使用 setuptools 构建全部

### 3. 查看生成的包

打包完成后,在 `dist/` 目录下会生成:
```
dist/
├── alicia_d_sdk-6.0.0-py3-none-any.whl      # wheel 包 (推荐)
└── alicia_d_sdk-6.0.0.tar.gz                # 源码包
```

---

## 安装方式

### 本地安装

```bash
# 安装 wheel 包 (推荐)
pip install dist/alicia_d_sdk-6.0.0-py3-none-any.whl

# 或安装源码包
pip install dist/alicia_d_sdk-6.0.0.tar.gz
```

### 分发给他人

1. 将 `dist/` 目录下的 `.whl` 文件发送给他人
2. 对方使用以下命令安装:

```bash
pip install alicia_d_sdk-6.0.0-py3-none-any.whl
```

### 创建离线安装包

如果目标机器没有网络连接,可以创建包含所有依赖的离线包:

```bash
# 1. 下载所有依赖
mkdir offline_packages
pip download -r requirements.txt -d offline_packages/

# 2. 将 offline_packages/ 和 dist/ 一起打包
tar -czf alicia_d_sdk_offline.tar.gz dist/ offline_packages/

# 3. 在离线机器上解压并安装
tar -xzf alicia_d_sdk_offline.tar.gz
pip install --no-index --find-links=offline_packages dist/alicia_d_sdk-*.whl
```

---

## 手动打包 (不使用脚本)

### 安装打包工具

```bash
pip install setuptools wheel build
```

### 构建分发包

```bash
# 方式 1: 使用 build 模块 (推荐)
python -m build

# 方式 2: 使用 setuptools
python setup.py sdist bdist_wheel

# 仅构建 wheel
python setup.py bdist_wheel

# 仅构建源码包
python setup.py sdist
```

---

## 上传到 PyPI

如果您想将包发布到 PyPI 供全球用户使用:

### 1. 安装 twine

```bash
pip install twine
```

### 2. 注册 PyPI 账号

访问 https://pypi.org 注册账号

### 3. 上传包

```bash
# 上传到测试服务器 (可选)
twine upload --repository testpypi dist/*

# 上传到正式 PyPI
twine upload dist/*
```

### 4. 从 PyPI 安装

上传成功后,任何人都可以通过以下命令安装:

```bash
pip install alicia-d-sdk
```

---

## 版本管理

版本号在 `alicia_d_sdk/__init__.py` 中定义:

```python
__version__ = "6.0.0"
```

修改版本号后重新打包即可生成新版本的安装包。

---

## 故障排查

### 问题 1: 找不到 setuptools/wheel

**解决方案:**
```bash
pip install --upgrade setuptools wheel build
```

### 问题 2: Git 依赖无法解析

如果 `requirements.txt` 中有 Git 依赖 (如 robocore),确保:
- Git 已安装
- 可以访问 GitHub
- 或者在离线环境中提前下载这些依赖

### 问题 3: 构建失败

**解决方案:**
```bash
# 清理旧的构建文件
rm -rf build dist *.egg-info

# 重新构建
python build_package.py
```

---

## 最佳实践

1. **使用 wheel 格式**: wheel 包安装更快,推荐分发 `.whl` 文件
2. **版本控制**: 每次发布前更新版本号
3. **测试安装**: 在干净的虚拟环境中测试安装包
4. **文档齐全**: 确保 README.md 包含完整的使用说明
5. **依赖锁定**: 在 `requirements.txt` 中指定具体版本号

---

## 示例工作流

```bash
# 1. 更新版本号
vim alicia_d_sdk/__init__.py  # 修改 __version__

# 2. 清理并构建
python build_package.py

# 3. 在新环境中测试
conda create -n test_env python=3.8
conda activate test_env
pip install dist/alicia_d_sdk-6.0.0-py3-none-any.whl

# 4. 测试功能
python -c "from alicia_d_sdk import create_robot; print('Import successful!')"

# 5. 分发或上传
# 分发: 发送 dist/alicia_d_sdk-6.0.0-py3-none-any.whl
# 或上传: twine upload dist/*
```

---

## 参考资源

- [Python Packaging Guide](https://packaging.python.org/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
- [Wheel Format](https://wheel.readthedocs.io/)
- [Twine Documentation](https://twine.readthedocs.io/)
