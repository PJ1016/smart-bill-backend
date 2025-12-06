import os
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import AnalyzedDocument
from semantic_kernel.functions import kernel_function

# Load environment variables once
load_dotenv()


# ---------------------------
#  Client & Config
# ---------------------------

def get_document_intelligence_client() -> DocumentIntelligenceClient:
    """
    Create and return a DocumentIntelligenceClient using env variables:
    - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    - AZURE_DOCUMENT_INTELLIGENCE_KEY
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Missing AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT or "
            "AZURE_DOCUMENT_INTELLIGENCE_KEY in environment."
        )

    return DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )


# ---------------------------
#  Core Analyze Function
# ---------------------------

def analyze_document(
    file_path: str,
    model_id: str = "prebuilt-layout",
    content_type: str = "application/octet-stream",
):
    """
    Analyze a document with Azure Document Intelligence and return the result object.

    :param file_path: Path to the local PDF/image.
    :param model_id: Model to use (e.g., 'prebuilt-layout', 'prebuilt-document').
    :param content_type: MIME type (default 'application/octet-stream' works for PDF).
    """
    client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=model_id,
            body=f,
            content_type=content_type,
        )
        result = poller.result()

    return result


# ---------------------------
#  Extraction Helpers
# ---------------------------

def extract_lines(result) -> List[str]:
    """
    Extract all text lines from the analysis result.
    """
    lines: List[str] = []
    for page in getattr(result, "pages", []) or []:
        for line in getattr(page, "lines", []) or []:
            if line.content:
                lines.append(line.content)
    return lines


def extract_plain_text(result) -> str:
    """
    Join all lines into a single plain-text string.
    """
    return "\n".join(extract_lines(result))


def _extract_direct_key_value_pairs(result) -> Dict[str, str]:
    """Extract key-value pairs directly from result object."""
    kv_dict: Dict[str, str] = {}
    
    for kv in result.key_value_pairs:
        key_text = kv.key.content if kv.key else ""
        value_text = kv.value.content if kv.value else ""
        if key_text:
            kv_dict[key_text] = value_text
    
    return kv_dict


def _extract_document_fields(result) -> Dict[str, str]:
    """Extract key-value pairs from document fields."""
    kv_dict: Dict[str, str] = {}
    
    for doc in getattr(result, "documents", []) or []:
        if not isinstance(doc, AnalyzedDocument) or not doc.fields:
            continue
            
        for name, field in doc.fields.items():
            kv_dict[name] = field.value if hasattr(field, "value") else str(field.value)  # type: ignore
    
    return kv_dict


def extract_key_value_pairs(result) -> Dict[str, str]:
    """
    Extract key-value pairs as a dict from the result (mainly useful with 'prebuilt-document').
    """
    if hasattr(result, "key_value_pairs") and result.key_value_pairs:
        return _extract_direct_key_value_pairs(result)
    
    return _extract_document_fields(result)


def extract_tables(result) -> List[List[List[str]]]:
    """
    Extract tables as a list of tables, where each table is a list of rows, and each row is a list of cell contents.

    Returns:
        List[table] where table = List[row], row = List[cell_content]
    """
    all_tables: List[List[List[str]]] = []

    for table in getattr(result, "tables", []) or []:
        # Build a dict of (row_index -> {col_index: content})
        grid: Dict[int, Dict[int, str]] = {}
        for cell in table.cells:
            row_idx = cell.row_index
            col_idx = cell.column_index
            grid.setdefault(row_idx, {})
            grid[row_idx][col_idx] = cell.content

        # Convert grid to ordered list of rows
        rows: List[List[str]] = []
        for row_idx in sorted(grid.keys()):
            row_dict = grid[row_idx]
            # sort columns by index
            row_cells = [row_dict[col_idx] for col_idx in sorted(row_dict.keys())]
            rows.append(row_cells)

        all_tables.append(rows)

    return all_tables


# ---------------------------
#  Debug / Print Helpers
# ---------------------------

def print_basic_debug(result) -> None:
    """
    Print basic info: lines, key-values, first table.
    Useful for debugging on CLI.
    """
    print("\n===== LINES =====\n")
    for line in extract_lines(result):
        print(line)

    print("\n===== KEY VALUE PAIRS =====\n")
    kv = extract_key_value_pairs(result)
    if kv:
        for k, v in kv.items():
            print(f"{k}: {v}")
    else:
        print("(No key-value pairs found)")

    print("\n===== FIRST TABLE (IF ANY) =====\n")
    tables = extract_tables(result)
    if tables:
        first = tables[0]
        for r_idx, row in enumerate(first):
            print(f"Row {r_idx}: {row}")
    else:
        print("(No tables found)")
