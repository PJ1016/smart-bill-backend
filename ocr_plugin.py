# ocr_plugin.py

from typing import Dict, Any, List

from semantic_kernel.functions import kernel_function

from ocr_utils import (
    analyze_document,
    extract_plain_text,
    extract_key_value_pairs,
    extract_tables,
)


class OcrPlugin:
    """
    Semantic Kernel plugin for OCR / Document Intelligence.
    Exposes high-level functions that SK (or agents) can call.
    """

    @kernel_function(
        name="analyze_pdf_to_text",
        description="Analyze a PDF using Azure Document Intelligence and return extracted plain text.",
    )
    def analyze_pdf_to_text(self, file_path: str) -> str:
        """
        Analyze the given PDF and return all extracted text as a single string.
        """
        result = analyze_document(file_path, model_id="prebuilt-layout")
        text = extract_plain_text(result)
        return text

    @kernel_function(
        name="analyze_pdf_to_kv_and_tables",
        description="Analyze a PDF and return key-value fields and tables as structured data.",
    )
    def analyze_pdf_to_kv_and_tables(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze the given PDF and return structured data:
        {
            "key_values": { ... },
            "tables": [ [ [cells...] ], ... ]
        }
        """
        # For KV pairs, prebuilt-document is usually better
        result = analyze_document(file_path, model_id="prebuilt-document")

        kv = extract_key_value_pairs(result)
        tables = extract_tables(result)

        return {
            "key_values": kv,
            "tables": tables,
        }

    @kernel_function(
        name="get_pdf_tables",
        description="Extract only tables from a PDF document.",
    )
    def get_pdf_tables(self, file_path: str) -> List[List[List[str]]]:
        """
        Analyze the given PDF and return tables only.
        """
        result = analyze_document(file_path, model_id="prebuilt-layout")
        tables = extract_tables(result)
        return tables
