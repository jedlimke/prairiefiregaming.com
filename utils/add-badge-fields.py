#!/usr/bin/env python3
"""
Add duty-brief and nation-brief fields to all role briefs in badge-briefs.yaml
"""

import re
import sys
from pathlib import Path

# Mapping of team names to nations
TEAM_TO_NATION = {
    # ICS ships
    "Aegis": "ICS",
    "Star Alpha": "ICS",
    "Javelin": "ICS",
    
    # INC
    "INC": "INC",
    
    # FAS
    "Dione": "FAS",
    
    # CPA
    "Icebreaker": "CPA",
    "Fuerza Leon": "CPA",
    
    # SAN
    "Lucas": "SAN",
    "Salvador": "SAN",
    
    # Rosal
    "Shepherd": "Rosal",
    "Endeavor": "Rosal",
    
    # Proxima
    "Quellon": "Proxima",
    "Vulcan": "Proxima",
    
    # Gliese
    "Refinery 124": "Gliese",
    
    # Helvetii
    "Hephaestus": "Helvetii",
    "Baltar": "Helvetii",
    
    # Solo roles - no nation
    "Solo Roles": None
}

# Mapping of role names to duty keys
ROLE_TO_DUTY = {
    # Aegis
    "Admiral": "admiral",
    "XO": "xo",
    "FWCO": "fwco",
    "Comms Officer": "comms-officer",
    "Logs Officer": "logs-officer",
    "Council Liaison": "council-liaison",
    
    # Star Alpha
    "President": "president",
    "Vice President": "vice-president",
    "Chief of Staff": "chief-of-staff",
    "Parliamentarian": "parliamentarian",
    
    # Common ship roles
    "Captain": "captain",
    "First Officer": "first-officer",
    "Chief Engineer": "chief-engineer",
    
    # Council members
    "Council Member": "council-member",
    "Diplomat (Council Member)": "diplomat",
    
    # Specialists
    "Chief Scientist": "chief-scientist",
    "Head Surgeon": "head-surgeon",
    "Warden": "warden",
    "Staff Sergeant": "staff-sergeant",
    
    # Media
    "Editor-in-Chief": "editor-in-chief",
    "Lead Anchor": "lead-anchor",
    "Fleet Correspondent": "fleet-correspondent",
    "Military Correspondent": "military-correspondent",
    "Political Correspondent": "political-correspondent",
    
    # Solo roles
    "Arbourist": "arbourist",
    "Inquisitor": "inquisitor",
    "Firebrand": "firebrand"
}

def main():
    badge_file = Path("/Users/jedlimke/code/prairiefiregaming.com/rules/den-of-wolves-2026/temp-assets/badge-briefs.yaml")
    
    # Read the file
    with open(badge_file, 'r') as f:
        content = f.read()
    
    # Split into sections
    lines = content.split('\n')
    output_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        output_lines.append(line)
        
        # Check if this is a "- name:" line (start of a brief)
        if re.match(r'^\s+- name: (.+)$', line):
            role_name = re.match(r'^\s+- name: (.+)$', line).group(1)
            indent = len(line) - len(line.lstrip())
            base_indent = ' ' * (indent + 2)
            
            # Collect the team name from the next few lines
            team = None
            j = i + 1
            while j < len(lines) and j < i + 10:
                team_match = re.match(r'^\s+team: (.+)$', lines[j])
                if team_match:
                    team = team_match.group(1)
                    break
                j += 1
            
            # Skip forward to after role-brief
            i += 1
            while i < len(lines):
                output_lines.append(lines[i])
                # Check if we're at the end of role-brief block
                if re.match(r'^\s+role-brief: \|', lines[i]):
                    # Skip the multi-line content
                    i += 1
                    while i < len(lines) and (lines[i].startswith(base_indent) or lines[i].strip() == ''):
                        output_lines.append(lines[i])
                        i += 1
                    
                    # Now add duty-brief and nation-brief
                    if role_name in ROLE_TO_DUTY:
                        duty_key = ROLE_TO_DUTY[role_name]
                        output_lines.append(f'{base_indent}duty-brief:')
                        output_lines.append(f'{base_indent}  $ref: "#/duties/{duty_key}"')
                    else:
                        print(f"Warning: No duty mapping for role '{role_name}'", file=sys.stderr)
                    
                    # Add nation-brief if applicable
                    nation = TEAM_TO_NATION.get(team) if team else None
                    if nation is not None:
                        output_lines.append(f'{base_indent}nation-brief:')
                        output_lines.append(f'{base_indent}  $ref: "#/nations/{nation}"')
                    
                    break
                i += 1
            continue
        
        i += 1
    
    # Write back
    with open(badge_file, 'w') as f:
        f.write('\n'.join(output_lines))
    
    print("Updated badge-briefs.yaml with duty-brief and nation-brief fields")

if __name__ == '__main__':
    main()
