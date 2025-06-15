import os
import pandas as pd
import logging
import json
import httpx
import re
from dotenv import load_dotenv
from openai import AzureOpenAI
from app.config import UPLOAD_FOLDER

logger = logging.getLogger(__name__)

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    http_client=httpx.Client(verify=False)
)


def detect_header_row_gpt(raw_df):
    prompt = f"""
        You're a data analyst. Below is a preview of an Excel sheet.
        Each row is a list of column values. Identify the row index (0-based) that most likely contains the column headers.

        Data Preview:
        {raw_df.to_string(index=True)}

        Respond only with a single integer.
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_API_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=10
        )
        result = response.choices[0].message.content.strip()
        return int(result)
    except Exception as e:
        logging.error(f"❌ Header row detection failed: {e}")
        return 0


def get_column_mapping_gpt(template_columns, messy_columns):
    prompt = f"""
        You are a data assistant. Map the following template columns to the most appropriate messy dataset columns.

        Template Columns:
        {template_columns}

        Messy Columns:
        {messy_columns}

        Return a JSON dictionary with template column names as keys, and messy column names as values.
        Do NOT include any explanations. Only return raw JSON.
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_API_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        raw = response.choices[0].message.content.strip()
        
        # 🧽 Clean up markdown code block
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\\s*", "", raw)
            raw = re.sub(r"\\s*```$", "", raw)

        # 🧼 Remove trailing note or anything after the JSON
        json_part = re.search(r'{.*}', raw, re.DOTALL)
        if json_part:
            cleaned = json_part.group().strip()
        else:
            raise ValueError("Could not extract JSON from GPT response.")

        mapping = json.loads(cleaned)
        if not isinstance(mapping, dict):
            raise ValueError("Response is not a valid dictionary.")

        logger.debug(f"🛠️ Column mapping: {mapping}")
        return mapping

    except Exception as e:
        logging.error(f"❌ Column mapping failed: {e}")
        return {}


def drop_sparse_rows(df, threshold=0.4):
    max_na = int(len(df.columns) * threshold)
    cleaned = df[df.isnull().sum(axis=1) <= max_na]
    rejected = df[df.isnull().sum(axis=1) > max_na]
    return cleaned, rejected


def map_and_clean_data():
    template_path = os.path.join(UPLOAD_FOLDER, 'template.xlsx')
    messy_path = os.path.join(UPLOAD_FOLDER, 'messy.xlsx')

    messy_preview = pd.read_excel(messy_path, header=None, nrows=15)
    header_index = detect_header_row_gpt(messy_preview)
    logger.info(f"✅ Detected header row at index {header_index}")

    template_df = pd.read_excel(template_path)
    messy_df = pd.read_excel(messy_path, header=header_index)

    mapping = get_column_mapping_gpt(list(template_df.columns), list(messy_df.columns))

    mapped_df = pd.DataFrame()
    for col in template_df.columns:
        mapped_df[col] = messy_df[mapping.get(col)] if mapping.get(col) in messy_df.columns else None

    cleaned_df, rejected_df = drop_sparse_rows(mapped_df)

    cleaned_path = os.path.join(UPLOAD_FOLDER, 'cleaned_output.xlsx')
    rejected_path = os.path.join(UPLOAD_FOLDER, 'rejected_rows.xlsx')

    logger.info(f"💾 Saving cleaned data to {cleaned_path}, rejected rows to {rejected_path}")
    if os.path.exists(cleaned_path):
        os.remove(cleaned_path)
    cleaned_df.to_excel(cleaned_path, index=False)
    rejected_df.to_excel(rejected_path, index=False)

    return {
        "message": "Data mapped and cleaned successfully",
        "saved_as": cleaned_path,
        "rejected_rows_saved_as": rejected_path,
        "cleaned_row_count": len(cleaned_df),
        "rejected_row_count": len(rejected_df)
    }
