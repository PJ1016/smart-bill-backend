# test_ocr_plugin.py

import asyncio

from semantic_kernel import Kernel
from ocr_plugin import OcrPlugin


async def main():
    kernel = Kernel()

    # 1. Add OCR plugin instance
    ocr_plugin = OcrPlugin()
    kernel.add_plugin(ocr_plugin, plugin_name="ocr")

    # 2. Call the plugin functions via the kernel
    file_path = "./dummy_statement.pdf"  # or sample_bank_statement.pdf

    # a) Get plain text
    text_result = await kernel.invoke(
        plugin_name="ocr",
        function_name="analyze_pdf_to_text",
        arguments={"file_path": file_path},
    )
    print("\n=== TEXT OUTPUT ===\n")
    print(text_result)

    # b) Get KV + tables
    kv_tables_result = await kernel.invoke(
        plugin_name="ocr",
        function_name="analyze_pdf_to_kv_and_tables",
        arguments={"file_path": file_path},
    )
    print("\n=== KV + TABLES OUTPUT ===\n")
    print(kv_tables_result)


if __name__ == "__main__":
    asyncio.run(main())
