"""Reject publication entries that Hugo would silently skip or misread."""

from pathlib import Path


def validate_publication_files(directory):
    """Validate source filenames and YAML boundaries before listing Hugo pages."""
    directory = Path(directory)
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory)
        if not path.is_file() or any(part.startswith(".") for part in relative.parts):
            continue
        if path.suffix != ".md":
            suggestion = path.name + ".md" if not path.suffix else path.with_suffix(".md").name
            raise ValueError(
                f"Publication file {path}: publication entries must have a .md filename. "
                f"Rename it to {suggestion!r} (for example, 'trafficflex.md') and wrap "
                "the title, authors, venue, and year in opening and closing '---' lines. "
                "Hugo otherwise skips this entry."
            )
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0] != "---":
            raise ValueError(
                f"Publication file {path}: missing opening '---'. "
                "Put '---' on the first line, followed by the publication fields, "
                "then another '---' on its own line."
            )
        if "---" not in lines[1:]:
            raise ValueError(
                f"Publication file {path}: missing closing '---'. "
                "Add '---' on its own line after the publication fields "
                "and before any abstract."
            )
