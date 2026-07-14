#!/usr/bin/env python3
"""Create a realistic demo_storage tree for a personal file server.

The script is idempotent: running it again will reuse existing files and
only create missing directories and placeholder content.
"""

from __future__ import annotations

from pathlib import Path
import textwrap

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover - optional dependency
    Image = None
    ImageDraw = None

ROOT = Path(__file__).resolve().parent
STORAGE_ROOT = ROOT / "demo_storage"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text_file(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def create_pdf(path: Path, content: str) -> None:
    if path.exists():
        return

    lines = content.splitlines() or [""]
    escaped_lines = []
    for line in lines:
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        escaped_lines.append(escaped)

    content_stream_parts = []
    y = 760
    for line in escaped_lines:
        content_stream_parts.append(f"BT /F1 12 Tf 72 {y} Td ({line}) Tj ET")
        y -= 14
    content_stream = "\n".join(content_stream_parts).encode("latin-1")

    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n",
        f"4 0 obj\n<< /Length {len(content_stream)} >>\nstream\n".encode("latin-1") + content_stream + b"\nendstream\nendobj\n",
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
    ]

    pdf_bytes = b"%PDF-1.4\n"
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf_bytes))
        pdf_bytes += obj

    xref_offset = len(pdf_bytes)
    pdf_bytes += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    pdf_bytes += b"0000000000 65535 f \n"
    for offset in offsets[1:]:
        pdf_bytes += f"{offset:010d} 00000 n \n".encode("ascii")
    pdf_bytes += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    path.write_bytes(pdf_bytes)


def create_placeholder_image(path: Path, label: str, size=(320, 180), fmt: str = "PNG") -> None:
    if path.exists() and Image is not None:
        try:
            with Image.open(path) as img:
                return
        except Exception:
            pass

    if path.exists() and Image is None:
        return

    if Image is None or ImageDraw is None:
        path.write_text(f"Placeholder image: {label}\n", encoding="utf-8")
        return

    img = Image.new("RGB", size, color=(241, 245, 249))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, size[0] - 1, size[1] - 1), outline=(148, 163, 184), width=4)
    draw.rectangle((16, 16, size[0] - 16, size[1] - 16), outline=(59, 130, 246), width=2)
    draw.text((24, 28), label, fill=(15, 23, 42))
    draw.text((24, 70), "Demo placeholder", fill=(71, 85, 105))
    if fmt.upper() == "JPG":
        img.save(path, format="JPEG", quality=90)
    else:
        img.save(path, format="PNG")


def create_placeholder_video(path: Path) -> None:
    if path.exists():
        return
    path.write_bytes(b"\x00\x00\x00")


def create_readme(path: Path, title: str, summary: str) -> None:
    if path.exists():
        return
    write_text_file(path, f"# {title}\n\n{summary}\n")


def build_structure() -> None:
    ensure_dir(STORAGE_ROOT)

    # Root folders
    directories = [
        STORAGE_ROOT / "Documents" / "Semester_Notes",
        STORAGE_ROOT / "Documents" / "Receipts",
        STORAGE_ROOT / "Pictures" / "Vacation",
        STORAGE_ROOT / "Pictures" / "Family",
        STORAGE_ROOT / "Pictures" / "Nature",
        STORAGE_ROOT / "Pictures" / "Wallpapers",
        STORAGE_ROOT / "Videos" / "Tutorials",
        STORAGE_ROOT / "Music" / "Album1",
        STORAGE_ROOT / "Music" / "Album2",
        STORAGE_ROOT / "Music" / "Podcasts",
        STORAGE_ROOT / "Projects" / "Portfolio",
        STORAGE_ROOT / "Projects" / "DjangoApp",
        STORAGE_ROOT / "Projects" / "Docker",
        STORAGE_ROOT / "Projects" / "Python",
        STORAGE_ROOT / "Downloads",
        STORAGE_ROOT / "Archives" / "2024",
        STORAGE_ROOT / "Archives" / "2025",
    ]
    for directory in directories:
        ensure_dir(directory)

    # Text files
    write_text_file(
        STORAGE_ROOT / "Documents" / "Meeting_Notes.txt",
        textwrap.dedent(
            """\
            Meeting Notes
            -------------
            - Review the project timeline and confirm milestones.
            - Prepare a short status summary for the team.
            - Share the updated roadmap before Friday.
            """
        ).strip()
        + "\n",
    )

    write_text_file(
        STORAGE_ROOT / "Documents" / "Shopping_List.txt",
        textwrap.dedent(
            """\
            Grocery Shopping List
            ---------------------
            - Eggs
            - Milk
            - Bread
            - Pasta
            - Apples
            - Coffee
            """
        ).strip()
        + "\n",
    )

    # PDFs
    create_pdf(
        STORAGE_ROOT / "Documents" / "Resume.pdf",
        "Resume\nPersonal Summary\nSoftware developer with experience in Django, Linux, and automation.",
    )
    create_pdf(
        STORAGE_ROOT / "Documents" / "Project_Proposal.pdf",
        "Project Proposal\nHome Server Demo\nA lightweight personal file server to organize documents, media, and projects.",
    )
    create_pdf(
        STORAGE_ROOT / "Documents" / "Semester_Notes" / "DBMS_Notes.pdf",
        "DBMS Notes\nNormalization, joins, indexing, and transaction basics.",
    )
    create_pdf(
        STORAGE_ROOT / "Documents" / "Semester_Notes" / "OS_Notes.pdf",
        "OS Notes\nProcesses, threads, memory management, and scheduling policies.",
    )
    create_pdf(
        STORAGE_ROOT / "Documents" / "Semester_Notes" / "Networks_Notes.pdf",
        "Networks Notes\nTCP/IP, DNS, routing, and basic network troubleshooting.",
    )
    create_pdf(
        STORAGE_ROOT / "Documents" / "Receipts" / "Electricity_Bill.pdf",
        "Electricity Bill\nInvoice #10021\nAmount Due: $42.75",
    )
    create_pdf(
        STORAGE_ROOT / "Documents" / "Receipts" / "Internet_Bill.pdf",
        "Internet Bill\nInvoice #2044\nAmount Due: $59.99",
    )

    # Images
    create_placeholder_image(STORAGE_ROOT / "Pictures" / "Vacation" / "Beach.png", "Vacation / Beach", fmt="PNG")
    create_placeholder_image(STORAGE_ROOT / "Pictures" / "Family" / "Family_Portrait.jpg", "Family Portrait", fmt="JPG")
    create_placeholder_image(STORAGE_ROOT / "Pictures" / "Nature" / "Forest.jpg", "Nature / Forest", fmt="JPG")
    create_placeholder_image(STORAGE_ROOT / "Pictures" / "Wallpapers" / "Abstract.png", "Wallpaper / Abstract", fmt="PNG")
    create_placeholder_image(STORAGE_ROOT / "Pictures" / "Wallpapers" / "Sunset.png", "Wallpaper / Sunset", fmt="PNG")

    # Videos
    create_placeholder_video(STORAGE_ROOT / "Videos" / "Demo_Video.mp4")
    create_placeholder_video(STORAGE_ROOT / "Videos" / "Screen_Recording.mp4")
    create_placeholder_video(STORAGE_ROOT / "Videos" / "Tutorials" / "Intro_Tutorial.mp4")

    # README files
    create_readme(
        STORAGE_ROOT / "Documents" / "README.md",
        "Documents",
        "This folder contains resumes, notes, receipts, and other personal documents.",
    )
    create_readme(
        STORAGE_ROOT / "Pictures" / "README.md",
        "Pictures",
        "Sample image folders for vacation shots, family photos, nature scenes, and wallpapers.",
    )
    create_readme(
        STORAGE_ROOT / "Music" / "README.md",
        "Music",
        "A small collection of albums and podcasts for the demo storage server.",
    )
    create_readme(
        STORAGE_ROOT / "Projects" / "README.md",
        "Projects",
        "Example project folders for portfolio work, Django applications, Docker experiments, and Python scripts.",
    )
    create_readme(
        STORAGE_ROOT / "Archives" / "README.md",
        "Archives",
        "Archive folders for older files grouped by year.",
    )


def main() -> None:
    build_structure()
    print(f"Created demo storage at {STORAGE_ROOT}")


if __name__ == "__main__":
    main()
