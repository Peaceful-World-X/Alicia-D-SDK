from setuptools import setup, find_packages
import os

def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Python SDK for controlling the Alicia D robotic arm."

# --- UPDATED FUNCTION TO PARSE REQUIREMENTS ---
def parse_requirements(filename):
    """
    Load requirements from a pip requirements file and separate them into
    install_requires and dependency_links.
    """
    install_requires = []
    dependency_links = []

    requirements_path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(requirements_path):
        return [], []

    base_dir = os.path.dirname(__file__)

    with open(requirements_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if line.startswith('git+'):
                    # The package name (after #egg=) goes into install_requires
                    pkg_name = line.split('#egg=')[-1]
                    install_requires.append(pkg_name)
                    # The full URL goes into dependency_links
                    dependency_links.append(line)
                elif '@' in line:
                    # Handle package @ URL or file path format
                    # e.g., "synriard @ ./bin/Synria-Robot-Descriptions.zip"
                    parts = line.split('@', 1)
                    pkg_name = parts[0].strip()
                    path_or_url = parts[1].strip()

                    # Convert relative file path to absolute path with file:// URL
                    if path_or_url.startswith('./') or path_or_url.startswith('../'):
                        # Relative path: convert to absolute
                        abs_path = os.path.abspath(os.path.join(base_dir, path_or_url))
                        if os.path.exists(abs_path):
                            file_url = f"file://{abs_path}"
                            install_requires.append(f"{pkg_name} @ {file_url}")
                        else:
                            print(f"Warning: File not found: {abs_path}, skipping dependency")
                    elif path_or_url.startswith('file://'):
                        # Already a file:// URL, use as-is
                        install_requires.append(line)
                    elif not path_or_url.startswith(('http://', 'https://', 'git+')):
                        # Assume it's a relative path without ./
                        abs_path = os.path.abspath(os.path.join(base_dir, path_or_url))
                        if os.path.exists(abs_path):
                            file_url = f"file://{abs_path}"
                            install_requires.append(f"{pkg_name} @ {file_url}")
                        else:
                            print(f"Warning: File not found: {abs_path}, skipping dependency")
                    else:
                        # Already a URL (http/https/git+), use as-is
                        install_requires.append(line)
                else:
                    # Standard PyPI packages go into install_requires
                    install_requires.append(line)

    return install_requires, dependency_links

# 从 __init__.py 读取版本号
def get_version():
    init_py_path = os.path.join(os.path.dirname(__file__), 'alicia_d_sdk', '__init__.py')
    version_line = ''
    if os.path.exists(init_py_path):
        with open(init_py_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    version_line = line
                    break
    # 从 __version__ = "x.y.z" 中提取版本号
    if version_line:
        return version_line.split('=')[-1].strip().strip('"').strip("'")
    return "0.1.0" # 默认版本

# Parse the requirements.txt file to get the lists
install_requires, dependency_links = parse_requirements('requirements.txt')

setup(
    name='alicia_d_sdk',
    version=get_version(),
    author='Synria Robotics',
    author_email='support@synriarobotics.ai',
    description='Python SDK for controlling the Alicia D robotic arm',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Synria-Robotics/Alicia-D-SDK',
    packages=find_packages(exclude=['tests*', 'examples*']),

    # --- USE THE CORRECTLY PARSED REQUIREMENTS ---
    install_requires=install_requires,
    dependency_links=dependency_links,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
    python_requires='>=3.6',
    keywords='robotic arm, alicia d, sdk, serial communication, robotics',
)