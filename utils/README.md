# Utils

One-off scripts used to prepare megagame content. None of these are part of the Jekyll build — they're run locally as needed.

## Scripts

### convert-docx.py

Batch converts `.docx` files in `rules/<game>/temp-assets/` to markdown. Normalizes smart quotes, preserves bold/italic/headings, handles lists. Images get replaced with a `❌` placeholder you'll need to fix by hand.

**Requires:** `python-docx`

### unwrap-briefs.py

Strips hard line-wrapping from multiline YAML fields in `badge-briefs.yaml`. Run this after pasting content from Google Docs or Word — those copy as hard-wrapped paragraphs and the YAML ends up ugly.

### add-badge-fields.py

Enriches `badge-briefs.yaml` with `$ref` fields for duties and nations based on role-title and team-name mappings. The mappings are hardcoded to Den of Wolves roles (Admiral → admiral, Captain → captain, etc.) so you'd need to update them for a different game.

### generate-role-emails.py

The big one. Generates per-team role-assignment email templates and renames brief PDFs with random hex suffixes (so URLs aren't guessable). For Den of Wolves 2026 this produced 19 HTML emails — one per ship, one for the INC press team, and three for wildcard roles.

All team data (ship names, nations, flag/ship images, role lists, flavor text) is defined in a `TEAMS` array at the top of the script. Styling matches the PFG email conventions: LT Tofino font, `#FF6600` orange links, highlight boxes with solid/dashed border style.

The brief-renaming step is idempotent — it detects already-renamed files and skips them.

**Workflow for next game:**
1. Duplicate the script and update `TEAMS`, paths, and copy
2. Put brief PDFs in the briefs directory with `brief--{team-id}.pdf` names
3. Run once to rename briefs and generate templates
4. Fill in `[Player Name]` and `[email@address]` placeholders
5. CC the team members together when sending

### convert-survey.py

Converts a Google Forms TSV export into a styled HTML report. Hardcoded to the Watch the Skies 2017 survey columns. You'd need to remap the column indices for a different survey, but the layout/styling code is reusable.

**Output:** `wts-survey-responses.html` (also in this directory)

## General Notes

- These scripts use only stdlib plus `python-docx` (for the docx converter). No other external deps.
- `temp-assets/` directories (where raw source files live during game prep) get cleaned out before commit to keep player info out of git.
- The YAML file `badge-briefs.yaml` that several scripts reference lives in `rules/<game>/temp-assets/` during prep and gets removed after.
