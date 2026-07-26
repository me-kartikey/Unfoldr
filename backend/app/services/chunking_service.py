import re
from typing import List, Dict


class ChunkingService:
    @staticmethod
    def chunk_document(document: str) -> List[Dict]:
        """
        Split a markdown document into chunks based on headings.

        Args:
            document: Markdown documentation content.

        Returns:
            List of chunks with id, title and content.
        """

        if not document or not document.strip():
            return []

        sections = re.split(
            r"(?=^#{1,2}\s)",
            document.strip(),
            flags=re.MULTILINE,
        )

        chunks = []

        for section in sections:
            section = section.strip()

            if not section:
                continue

            lines = section.splitlines()
            heading = lines[0]

            title = heading.lstrip("#").strip()

            chunk_id = (
                title.lower()
                .replace(" ", "_")
                .replace("/", "_")
                .replace("-", "_")
            )

            chunks.append(
                {
                    "id": chunk_id,
                    "title": title,
                    "content": section,
                }
            )

        return chunks