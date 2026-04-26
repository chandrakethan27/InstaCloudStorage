# 📸 InstaCloudStorage

**InstaCloudStorage** is a robust Python-based CLI tool designed to automate the backup and synchronization of local photo collections to Instagram. It functions as a "Personal Cloud" storage bridge, allowing you to systematically upload images while ensuring no duplicates are ever posted.

---

## ✨ Features

- **🚀 Automated Batch Uploads**: Simply point to a folder and let it handle the rest.
- **🛡️ Duplicate Prevention**: Uses MD5 hashing to track uploaded files in a local SQLite database. Even if you rename a file, it won't be re-uploaded.
- **🔄 Session Persistence**: Stores login settings in `session.json` to avoid repeated logins and reduce the risk of account flags.
- **⏳ Smart Rate Limiting**: Includes randomized delays (30-60s) between uploads and automatic retry logic for rate-limited requests.
- **📁 Broad Compatibility**: Supports `.jpg`, `.jpeg`, and `.png` formats.
- **📊 Detailed Tracking**: Maintains a complete history of uploads including timestamps and original file paths.

---

## 🛠️ Tech Stack

- **Python 3.11** (Recommended)
- **[instagrapi](https://github.com/adw0rd/instagrapi)**: A powerful unofficial Instagram Private API wrapper.
- **SQLite3**: For lightweight, reliable local tracking.
- **python-dotenv**: For secure credential management.

---

## 📋 Prerequisites

- **Python Version**: Python 3.11 is required. (Wheels for certain dependencies like `pydantic-core` may not yet be available for newer versions like 3.14).
- **Instagram Account**: A valid Instagram account (it is recommended to use a dedicated "backup" or "storage" account).

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/InstaCloudStorage.git
cd InstaCloudStorage
```

### 2. Install Dependencies
It is highly recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration
Copy the template environment file and fill in your Instagram credentials:
```bash
cp .env.example .env
```
Edit `.env`:
```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

---

## 🖥️ Usage

To start uploading photos from a specific folder, run:

```bash
python main.py --folder /path/to/your/photos
```

### What happens during execution:
1. **Scanning**: The tool identifies all valid images in the target directory.
2. **Verification**: It checks the local `uploaded.db` to see if the file's MD5 hash exists.
3. **Upload**: If new, the photo is uploaded with a randomized delay to simulate human behavior.
4. **Recording**: Once successful, the file is logged in the database to prevent future re-uploads.

---

## 🗺️ Roadmap (v2 and beyond)

- [ ] **Photo Retrieval**: Command to download all photos from the account back to local storage.
- [ ] **Metadata Preservation**: Store original MD5 and size in Instagram captions for verification during retrieval.
- [ ] **Recursive Scanning**: Support for nested subdirectories.
- [ ] **Video Support**: Enable backup for `.mp4` and `.mov` files.
- [ ] **GUI Dashboard**: A desktop interface to monitor upload progress and manage settings.

---

## ⚠️ Disclaimer

This tool uses an unofficial API. Use it at your own risk. Frequent or high-volume uploads may lead to account restrictions or bans. Always adhere to Instagram's Community Guidelines.

---

## 📄 License

This project is licensed under the MIT License.
