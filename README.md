# Dataset Tag Editor Standalone - KisaRo Edition

[日本語 Readme](README-JP.md)

This is a forked and enhanced version of [Dataset Tag Editor Standalone](https://github.com/toshiaki1729/dataset-tag-editor-standalone) by toshiaki1729.

It is a WebUI tool designed to edit training datasets for Text2Image Models, optimized for comma-separated captions.

## KisaRo Edition Enhancements
- **Multi-language Support (JP/EN)**: The UI can now be toggled between Japanese and English. This can be configured in the "Settings" tab.
- **Main Tab (Single Image Tagger)**: Added a dedicated tab where you can quickly extract and verify tags for a single image via drag-and-drop.
- **Refined UI/UX**: Various minor improvements for a more seamless tagging workflow.

## Original Project
This tool is based on the original work by [toshiaki1729](https://github.com/toshiaki1729).  
Original Repository: [https://github.com/toshiaki1729/dataset-tag-editor-standalone](https://github.com/toshiaki1729/dataset-tag-editor-standalone)

---

## Requirements
All requirements are listed in `requirements.txt`.
**Please install the followings first:**
- [Python](https://www.python.org/) >= 3.9 (Developed on 3.10.11)
- [PyTorch](https://pytorch.org/) with CUDA >= 1.10.0

## Installation
### Windows
Just run `install.bat`.

### Linux (or manual install on Windows)
Run following commands on the root directory of this repo:
```sh
python3 -m venv --system-site-packages venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

## Launch
### Windows
Just run `launch_user.bat`.

### Linux
```sh
source ./venv/bin/activate
python scripts/launch.py [arguments]
```

## Features (Brief)
- Edit captions in text or JSON format.
- Multi-tag filtering (AND/OR/NOT).
- Batch search/replace/append (supports Regex).
- Supports various interrogators (BLIP, DeepDanbooru, WDv1.4 Tagger v1/v2/v3, etc.).
- Move/Delete files directly from the UI.
