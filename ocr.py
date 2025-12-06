import os
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

# Get Azure values from environment
endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

# 2. Create client
client=DocumentIntelligenceClient(endpoint=endpoint,credential=AzureKeyCredential(key))

# 3. Path to your local PDF
file_path="./dummy_statement.pdf"

with open(file_path, "rb") as f:
    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        body=f,
        content_type="application/octet-stream"
    )
    result = poller.result()
# 4. Print full raw result structure (optional, very verbose)
# print(result)
for page in result.pages:
    for line in page.lines:
        print(line.content)
# # 5. Print extracted plain text
# print("\n===== EXTRACTED TEXT =====\n")
# for page in result.pages:
#     if page.lines:
#         for line in page.lines:
#             print(line.content)

# 6. Print key-value pairs if any
print("\n===== KEY VALUE PAIRS =====\n")
if result.key_value_pairs:
    for kv in result.key_value_pairs:
        key_text = kv.key.content if kv.key else ""
        value_text = kv.value.content if kv.value else ""
        print(f"{key_text}: {value_text}")

# 7. Print first table (if exists)
print("\n===== FIRST TABLE (IF ANY) =====\n")
if result.tables:
    table = result.tables[0]
    for cell in table.cells:
        print(f"Row {cell.row_index}, Col {cell.column_index}: {cell.content}")