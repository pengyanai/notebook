#!/usr/bin/env python3
"""
Migrate article metadata from markdown blockquotes to Jekyll front matter.
Converts:
  > Author: **name**
  > Labels: **label**
  > Created: **date**
  > Link and comments: <url>
To front matter format.
"""

import re
from pathlib import Path

POSTS_DIR = Path("posts")


def extract_metadata_from_content(content):
    """Extract metadata from markdown blockquotes."""
    author = None
    labels = None
    date = None
    link = None

    # Match blockquote patterns
    author_match = re.search(r'>\s*Author:\s*\*\*([^*]+)\*\*', content)
    labels_match = re.search(r'>\s*Labels:\s*\*\*([^*]+)\*\*', content)
    date_match = re.search(r'>\s*Created:\s*\*\*([^*]+)\*\*', content)
    link_match = re.search(r'>\s*Link and comments:\s*<([^>]+)>', content)

    if author_match:
        author = author_match.group(1).strip()
    if labels_match:
        labels = labels_match.group(1).strip()
    if date_match:
        date = date_match.group(1).strip()
    if link_match:
        link = link_match.group(1).strip()

    return author, labels, date, link


def extract_title(content):
    """Extract title from first h1 heading."""
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    return None


def remove_metadata_blockquotes(content):
    """Remove metadata blockquotes and title from content."""
    # Remove title (first h1 heading)
    content = re.sub(r'^#\s+.+?\n+', '', content, flags=re.MULTILINE)

    # Remove metadata blockquote section (Author, Labels, Created, Link)
    lines = content.split('\n')
    new_lines = []
    skip_blockquote = False

    for i, line in enumerate(lines):
        # Check if this is a metadata blockquote line
        if re.match(r'>\s*(Author|Labels|Created|Link and comments):', line):
            skip_blockquote = True
            continue

        # Check if we're still in blockquote section
        if skip_blockquote:
            if line.strip() == '' or not line.startswith('>'):
                skip_blockquote = False
            else:
                continue

        new_lines.append(line)

    content = '\n'.join(new_lines)

    # Remove extra blank lines at the start
    content = re.sub(r'^\n+', '', content)

    return content.strip()


def migrate_article(file_path):
    """Migrate a single article file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already migrated (has author/date in front matter)
    if 'author:' in content.split('---')[0] if '---' in content else '':
        print(f"  Skipping {file_path.name} (already migrated)")
        return False

    # Extract existing front matter
    front_matter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    existing_fm = {}
    if front_matter_match:
        fm_content = front_matter_match.group(1)
        for line in fm_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                existing_fm[key.strip()] = value.strip()
        content_after_fm = content[front_matter_match.end():]
    else:
        content_after_fm = content

    # Extract metadata from blockquotes
    author, labels, date, link = extract_metadata_from_content(content_after_fm)
    title = extract_title(content_after_fm)

    if not author and not date:
        print(f"  Skipping {file_path.name} (no metadata found)")
        return False

    # Remove metadata blockquotes and title
    clean_content = remove_metadata_blockquotes(content_after_fm)

    # Build new front matter
    front_matter = ["---"]
    front_matter.append("layout: default")

    if title:
        front_matter.append(f'title: "{title}"')
    if author:
        front_matter.append(f"author: {author}")
    if labels:
        front_matter.append(f"labels: {labels}")
    if date:
        front_matter.append(f"date: {date}")
    if link:
        front_matter.append(f"link: {link}")

    # Preserve other existing front matter
    for key, value in existing_fm.items():
        if key not in ['layout', 'title', 'author', 'labels', 'date', 'link']:
            front_matter.append(f"{key}: {value}")

    front_matter.append("---")

    # Write migrated content
    new_content = "\n".join(front_matter) + "\n\n" + clean_content + "\n"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  Migrated {file_path.name}")
    return True


def main():
    """Process all posts in the posts directory."""
    if not POSTS_DIR.exists():
        print(f"Error: {POSTS_DIR} directory not found")
        return

    md_files = list(POSTS_DIR.glob("*.md"))
    print(f"Found {len(md_files)} article files")

    migrated_count = 0
    for md_file in sorted(md_files):
        if migrate_article(md_file):
            migrated_count += 1

    print(f"\nMigration complete: {migrated_count} files migrated")


if __name__ == "__main__":
    main()
