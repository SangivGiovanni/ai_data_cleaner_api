# 🧹 AI-Powered Data Cleaner for Underwriting Spreadsheets

## Overview

In the London specialty insurance market, underwriters frequently receive messy, non-standard Excel spreadsheets from brokers. These files often require significant manual effort to clean, standardize, and prepare for pricing models or analysis. This Flask-based API aims to **automate that data wrangling process** by leveraging **OpenAI's GPT models** to identify header rows, map columns, and clean data intelligently.

This tool allows underwriters to upload a template and messy file, and get back a cleaned dataset—with rejected rows saved separately for review.

---

## 🚀 Features

- 📤 Upload both messy and template Excel files
- 🤖 Automatically detect header rows in messy data using GPT
- 🔁 AI-driven column mapping based on semantic similarity
- 🧽 Drop rows with excessive missing values (configurable threshold)
- 📥 Download cleaned output and rejected rows
- 📋 Logging built-in for debugging and operational visibility

---

## 🧠 How It Works

1. **Upload a Template File**  
   This file defines the expected structure (column names) of the final cleaned dataset.

2. **Upload a Messy File**  
   This file represents the broker-provided data in its raw, often unstructured form.

3. **AI Cleansing Begins**
   - The messy sheet is previewed and sent to GPT to detect which row contains the header.
   - GPT is then asked to map each template column to the closest-matching column in the messy file using natural language understanding.
   - Rows with too many missing values are dropped.
   - Cleaned data and rejected rows are saved as separate Excel files.

4. **Results Returned**
   - Cleaned output (`cleaned_output.xlsx`)
   - Rejected rows (`rejected_rows.xlsx`)

---

## 🧾 API Endpoints

### `/upload_template` – `POST`
Upload your template Excel file (e.g. from pricing model).

### `/upload_messy` – `POST`
Upload the raw broker spreadsheet.

### `/map_and_clean` – `GET`
Trigger the data cleaning process. Returns a JSON summary of results.

### `/download_cleaned` – `GET`
Download the cleaned Excel file.

---

## 🛠️ Tech Stack

- **Flask** (Python micro web framework)
- **Pandas** (for data manipulation)
- **OpenAI GPT (via Azure)** – used to detect headers and perform column mapping
- **httpx** – for robust HTTP requests with SSL handling
- **dotenv** – to manage API keys and settings
- **Excel file support** – via `openpyxl`

---

## 🔐 Environment Variables

Create a `.env` file with your Azure OpenAI credentials:

```ini
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-04-01-preview
AZURE_OPENAI_API_DEPLOYMENT_NAME=your_deployment_name
```

---

## 📦 Installation & Usage

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-org/ai-data-cleaner.git
   cd ai-data-cleaner
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** with your Azure OpenAI credentials.

5. **Run the Flask server**
   ```bash
   python run.py
   ```

6. **Use tools like Postman or curl to test the endpoints**, or integrate into an internal UI for underwriters.

---

## 📁 Project Structure

```
├── app/
│   ├── routes/
│   │   ├── upload_routes.py      # File upload endpoints
│   │   └── process_routes.py     # Trigger cleaning and download
│   ├── services/
│   │   └── data_cleaning.py      # Core AI cleaning logic
│   └── __init__.py               # App factory with logging config
├── uploads/                      # Uploaded & output Excel files
├── run.py                        # Entry point
├── requirements.txt              # Dependencies
├── .env                          # API keys (not committed)
```

---

## 🧪 Example Prompts Used in GPT

To detect header row:
```
You're a data analyst. Below is a preview of an Excel sheet.
Each row is a list of column values. Identify the row index (0-based)
that most likely contains the column headers.
```

To map columns:
```
Map the following template columns to the most appropriate messy dataset columns.
Return a JSON dictionary with template column names as keys, and messy column names as values.
Do NOT include any explanations.
```

---

## 🛡️ Disclaimer

This project is a **prototype** and should be thoroughly validated before being used in production for critical underwriting or actuarial workflows.

---

## 📬 Future Enhancements

- Web front-end for non-technical users
- Support for batch processing
- Integration into pricing models or document management systems
- More sophisticated row cleaning (e.g. fuzzy matching, type inference)

---

## 👤 Author

**[Your Name]** – Data Engineering / Analytics at [Your Company]

---

## 📄 License

MIT License (or your company’s license policy)