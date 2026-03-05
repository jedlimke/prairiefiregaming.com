#!/usr/bin/env python3
"""
Remove hard-wrapping from role-brief fields in badge-briefs.yaml
"""

import re
from pathlib import Path

def unwrap_paragraph(lines):
    """Take a list of lines and join them into a single paragraph, preserving intentional breaks."""
    if not lines:
        return []
    
    paragraphs = []
    current = []
    
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            # Empty line = paragraph break
            if current:
                paragraphs.append(' '.join(current))
                current = []
            paragraphs.append('')  # Preserve blank line
        else:
            current.append(stripped)
    
    if current:
        paragraphs.append(' '.join(current))
    
    return paragraphs

def main():
    badge_file = Path("/Users/jedlimke/code/prairiefiregaming.com/rules/den-of-wolves-2026/temp-assets/badge-briefs.yaml")
    
    with open(badge_file, 'r') as f:
        lines = f.readlines()
    
    output = []
    i = 0
    in_role_brief = False
    role_brief_lines = []
    base_indent = ""
    
    while i < len(lines):
        line = lines[i]
        
        # Check if we're starting a role-brief block
        if re.match(r'^(\s+)role-brief: \|', line):
            in_role_brief = True
            base_indent = re.match(r'^(\s+)role-brief:', line).group(1)
            content_indent = base_indent + '  '
            output.append(line)
            role_brief_lines = []
            i += 1
            
            # Collect all the role-brief content lines
            while i < len(lines):
                if lines[i].startswith(content_indent) or lines[i].strip() == '':
                    if lines[i].strip():  # Non-empty line
                        role_brief_lines.append(lines[i][len(content_indent):].rstrip())
                    else:
                        role_brief_lines.append('')  # Preserve blank lines
                    i += 1
                else:
                    # End of role-brief block
                    break
            
            # Unwrap and write the role-brief content
            unwrapped = unwrap_paragraph(role_brief_lines)
            for para_line in unwrapped:
                if para_line == '':
                    output.append('\n')
                else:
                    output.append(f'{content_indent}{para_line}\n')
            
            in_role_brief = False
            continue
        
        output.append(line)
        i += 1
    
    with open(badge_file, 'w') as f:
        f.writelines(output)
    
    print("Unwrapped all role-brief fields")

if __name__ == '__main__':
    main()
