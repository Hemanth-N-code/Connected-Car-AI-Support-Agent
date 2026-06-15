import os
import chromadb

client = chromadb.PersistentClient(
    path="vector_store"
)

collection = client.get_or_create_collection(
    name="automotive_kb"
)

KB_PATH = "data/kb"

for filename in os.listdir(KB_PATH):

    filepath = os.path.join(
        KB_PATH,
        filename
    )

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        content = file.read()

    collection.add(
        documents=[content],
        ids=[filename]
    )

print("Knowledge Base Indexed Successfully")