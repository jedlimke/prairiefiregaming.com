#!/usr/bin/env python3
"""
Convert Watch the Skies survey TSV to readable HTML
"""

import csv
import html

# Read the TSV file
input_file = '/Users/jedlimke/Downloads/wtsfargo-surveyresponses-processed - Form Responses 1.tsv'
output_file = '/Users/jedlimke/code/prairiefiregaming.com/wts-survey-responses.html'

# Column indices for the data we want (0-based)
# Multi-column table fields (short responses)
short_fields = [
    (1, 'Did you have fun?'),
    (2, 'Would you play again?'),
    (3, 'Compared to expectations'),
    (4, 'Good value?'),
    (5, 'Team of...'),
    (9, 'Which role/team?'),
    (10, 'Did your role suit you?'),
    (11, 'Different role(s) you\'d pick'),
    (12, 'Play same role again?'),
    (13, 'Able to make meaningful decisions?'),
    (14, 'Influence over narrative'),
    (15, 'Breaking news alerts influence'),
    (16, 'Printed news influence'),
]

# Full-width fields (long responses)
long_fields = [
    (22, 'What would you do differently?'),
    (23, 'What did you like the least?'),
    (24, 'What did you like the most?'),
    (25, 'What could we have done better?'),
    (26, 'Anything else we should know?'),
]

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Watch the Skies - Survey Responses</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 {
            color: #222;
            border-bottom: 3px solid #FFCC00;
            padding-bottom: 10px;
        }
        article {
            background: white;
            margin: 30px 0;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #FFCC00;
            color: #222;
            font-weight: bold;
        }
        .response-section {
            margin: 20px 0;
        }
        .response-section h3 {
            color: #FF6600;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
        }
        .response-text {
            padding: 10px;
            background: #f9f9f9;
            border-left: 3px solid #FF6600;
            margin-bottom: 10px;
        }
        .empty {
            color: #999;
            font-style: italic;
        }
        hr {
            border: none;
            border-top: 2px solid #FFCC00;
            margin: 30px 0;
        }
        .yes-cell {
            background: #d4edda !important;
            color: #155724;
            font-weight: bold;
        }
        .no-cell {
            background: #f8d7da !important;
            color: #721c24;
            font-weight: bold;
        }
    </style>
<script>
// Highlight Yes/No cells in tables
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('table td').forEach(function(td) {
        if (td.textContent.trim() === 'Yes') {
            td.classList.add('yes-cell');
        } else if (td.textContent.trim() === 'No') {
            td.classList.add('no-cell');
        }
    });
});
</script>
</head>
<body>
    <h1>Watch the Skies - Post-Game Survey Responses</h1>
"""

def format_narrative_influence(value):
    """Convert numeric rating (0-10) to filled/unfilled circles"""
    try:
        rating = int(value)
        if rating < 0 or rating > 10:
            return html.escape(value)
        filled = '⚫' * rating
        unfilled = '⚪' * (10 - rating)
        return f'{filled}{unfilled} ({rating}/10)'
    except (ValueError, TypeError):
        return html.escape(str(value)) if value else '<span class="empty">(no response)</span>'

# Read and process TSV
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    headers = next(reader)  # Skip header row
    
    response_count = 0
    for row in reader:
        if len(row) < 27:  # Skip incomplete rows (need through column 26, 0-based)
            continue
            
        response_count += 1
        html_content += f'\n    <article>\n        <h2>Response #{response_count}</h2>\n'
        
        # Short response table
        html_content += '        <table>\n'
        for col_idx, label in short_fields:
            value = row[col_idx].strip() if col_idx < len(row) else ''
            
            # Special formatting for narrative influence rating
            if label == 'Influence over narrative':
                formatted_value = format_narrative_influence(value)
            elif not value:
                formatted_value = '<span class="empty">(no response)</span>'
            else:
                formatted_value = html.escape(value)
            
            html_content += f'            <tr><th>{label}</th><td>{formatted_value}</td></tr>\n'
        html_content += '        </table>\n'
        
        # Long response sections
        for col_idx, label in long_fields:
            value = row[col_idx].strip() if col_idx < len(row) else ''
            html_content += f'        <div class="response-section">\n'
            html_content += f'            <h3>{label}</h3>\n'
            if value:
                html_content += f'            <div class="response-text">{html.escape(value)}</div>\n'
            else:
                html_content += '            <div class="response-text empty">(no response)</div>\n'
            html_content += '        </div>\n'
        
        html_content += '    </article>\n'

html_content += """
</body>
</html>
"""

# Write output
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✓ Converted {response_count} survey responses")
print(f"✓ Output written to: {output_file}")
