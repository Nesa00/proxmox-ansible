# -*- coding: utf-8 -*-
"""Custom filters for documentation generation - strip ANSI codes and format output."""

import re
def strip_ansi(text):
    """Remove ANSI escape sequences from text for clean report output."""
    if text is None or not isinstance(text, str):
        return text or ""
    # Remove ANSI escape sequences: \033[...m, \x1b[...m, and 8-bit/24-bit color codes
    ansi_escape = re.compile(
        r'\x1b\[[0-9;]*m|'  # Standard ANSI
        r'\x1b\[[0-9;]*[a-zA-Z]|'  # ANSI with letter
        r'\x1b\[[?0-9;]*[hl]|'  # Alternative
        r'\033\[[0-9;]*m'  # Octal form
    )
    return ansi_escape.sub('', text)


def text_to_markdown_table(text, header_sep='  '):
    """
    Convert tabular text (space-aligned columns) to Markdown table.
    First line is treated as header.
    """
    if text is None or not isinstance(text, str) or not text.strip():
        return text or ""
    lines = [l for l in text.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return text
    # Split by multiple spaces (2+)
    def split_row(line):
        return [c.strip() for c in re.split(r'\s{2,}', line) if c.strip()]
    rows = [split_row(l) for l in lines]
    if not rows:
        return text
    # Use first row as header
    header = rows[0]
    col_count = len(header)
    # Build markdown table
    sep = ' | '
    header_line = '| ' + sep.join(header) + ' |'
    separator = '|' + '|'.join(['---'] * col_count) + '|'
    body_lines = []
    for row in rows[1:]:
        # Pad row to match header columns
        padded = (row + [''] * col_count)[:col_count]
        body_lines.append('| ' + sep.join(padded) + ' |')
    return '\n'.join([header_line, separator] + body_lines)


def format_section(title, content, level=2):
    """Format content with a markdown section header."""
    if content is None or not str(content).strip():
        return ""
    prefix = '#' * level
    return f"{prefix} {title}\n\n{strip_ansi(str(content).strip())}\n"


class FilterModule:
    """Ansible filter plugin for documentation."""

    def filters(self):
        return {
            'strip_ansi': strip_ansi,
            'text_to_markdown_table': text_to_markdown_table,
            'format_section': format_section,
        }
