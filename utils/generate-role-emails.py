#!/usr/bin/env python3
"""
Generate role-assignment email templates for Den of Wolves 2026.
Also renames brief PDFs with random 4-char hex suffixes for privacy.

Usage:
    python utils/generate-role-emails.py
"""

import os
import random
import string
import textwrap

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://prairiefiregaming.com"
ASSETS_URL = f"{BASE_URL}/assets/megagames"
RULES_URL = f"{BASE_URL}/rules/den-of-wolves-2026"
BRIEFS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "rules", "den-of-wolves-2026", "briefs"
)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..")
DISCORD_INVITE = "https://discord.gg/yRbakKZk"

# ---------------------------------------------------------------------------
# Team data
# ---------------------------------------------------------------------------

TEAMS = [
    # ── SHIPS ─────────────────────────────────────────────────────────────
    {
        "id": "aegis",
        "ship_name": "ICSS Aegis",
        "nation": "ICSS",
        "flag_img": "dow--nation--icss.png",
        "ship_img": "dow--ship--aegis--black.png",
        "brief_base": "brief--aegis",
        "roles": [
            "Admiral",
            "XO",
            "CAG",
            "Comms Officer",
            "Logistics Officer",
            "Council Liaison",
        ],
        "flavor": "The fleet's only battleship—and humanity's last shield against the Wolves. Your crew carries the weight of every soul in the fleet on its shoulders.",
        "type": "ship",
    },
    {
        "id": "star-alpha",
        "ship_name": "Star Alpha",
        "nation": "Interstellar Council",
        "flag_img": "dow--nation--isc.png",
        "ship_img": "dow--ship--star-alpha--black.png",
        "brief_base": "brief--star-alpha",
        "roles": [
            "President",
            "Vice President",
            "Chief of Staff",
            "Parliamentarian",
        ],
        "flavor": "The seat of executive power—the last government humanity has. The fleet survives on law, compromise, and the fragile thread of legitimacy your crew represents.",
        "type": "ship",
    },
    {
        "id": "dione",
        "ship_name": "Dione",
        "nation": "Federated Atlantic Syndicate (FAS)",
        "flag_img": "dow--nation--fas.png",
        "ship_img": "dow--ship--dione--black.png",
        "brief_base": "brief--dione",
        "roles": [
            "Captain",
            "First Officer",
            "Chief Engineer",
            "Council Member",
        ],
        "flavor": "The largest civilian vessel in the fleet—home to ten thousand refugees and the Interstellar Council itself. The political heart of the fleet beats aboard your ship.",
        "type": "ship",
    },
    {
        "id": "shepherd",
        "ship_name": "Shepherd",
        "nation": "Rosal",
        "flag_img": "dow--nation--rosal.png",
        "ship_img": "dow--ship--shepherd--black.png",
        "brief_base": "brief--shepherd",
        "roles": [
            "Captain",
            "First Officer",
            "Chief Engineer",
            "Council Member",
        ],
        "flavor": "The ship that feeds the fleet. Without the Shepherd's food production, people starve—and everyone knows it. That's leverage. Use it wisely.",
        "type": "ship",
    },
    {
        "id": "lucas",
        "ship_name": "Lucas",
        "nation": "South American Nations (SAN)",
        "flag_img": "dow--nation--san.png",
        "ship_img": "dow--ship--lucas--black.png",
        "brief_base": "brief--lucas",
        "roles": [
            "Captain",
            "First Officer",
            "Chief Engineer",
            "Council Member",
        ],
        "flavor": "The fleet's main water supplier and home to SAN's engineering university. Quiet, essential, and more formidable than anyone gives you credit for.",
        "type": "ship",
    },
    {
        "id": "icebreaker",
        "ship_name": "Icebreaker",
        "nation": "Confederated Peoples of Asia (CPA)",
        "flag_img": "dow--nation--cpa.png",
        "ship_img": "dow--ship--icebreaker--black.png",
        "brief_base": "brief--icebreaker",
        "roles": [
            "Captain",
            "First Officer",
            "Chief Engineer",
            "Council Member",
        ],
        "flavor": "The fleet's primary mining ship—its industrial backbone. The CPA lost more than anyone in the Attack. Grief and fury fuel your crew in equal measure.",
        "type": "ship",
    },
    {
        "id": "refinery-124",
        "ship_name": "Refinery 124",
        "nation": "Gliese",
        "flag_img": "dow--nation--gliese.png",
        "ship_img": "dow--ship--refinery-124--black.png",
        "brief_base": "brief--refinery-124",
        "roles": [
            "Captain",
            "First Officer",
            "Chief Engineer",
            "Council Member",
        ],
        "flavor": "Without strytium fuel, the fleet stops moving. Your ship produces it. Quiet, essential, underestimated—and absolutely indispensable.",
        "type": "ship",
    },
    {
        "id": "quellon",
        "ship_name": "Quellon",
        "nation": "Proxima",
        "flag_img": "dow--nation--proxima.png",
        "ship_img": "dow--ship--quellon--black.png",
        "brief_base": "brief--quellon",
        "roles": [
            "Captain",
            "First Officer",
            "Chief Engineer",
            "Council Member",
        ],
        "flavor": "Proxima's primary vessel—a significant water producer and fighter carrier. Self-sufficiency isn't just a philosophy here. It's survival.",
        "type": "ship",
    },
    {
        "id": "endeavour",
        "ship_name": "Endeavour",
        "nation": "Rosal",
        "flag_img": "dow--nation--rosal.png",
        "ship_img": "dow--ship--endeavour--black.png",
        "brief_base": "brief--endeavour",
        "roles": [
            "Captain",
            "Chief Scientist",
        ],
        "flavor": "The most scientifically important ship in the fleet. If something can be figured out, it gets figured out here. Humanity's ingenuity lives aboard the Endeavour.",
        "type": "ship",
    },
    {
        "id": "salvador",
        "ship_name": "Salvador",
        "nation": "South American Nations (SAN)",
        "flag_img": "dow--nation--san.png",
        "ship_img": "dow--ship--salvador--black.png",
        "brief_base": "brief--salvador",
        "roles": [
            "Captain",
            "Head Surgeon",
        ],
        "flavor": "The only dedicated medical vessel in the fleet. People live or die based on what happens here. The Salvador is indispensable—and so are you.",
        "type": "ship",
    },
    {
        "id": "vulcan",
        "ship_name": "Vulcan",
        "nation": "Proxima",
        "flag_img": "dow--nation--proxima.png",
        "ship_img": "dow--ship--vulcan--black.png",
        "brief_base": "brief--vulcan",
        "roles": [
            "Captain",
            "Warden",
        ],
        "flavor": "A prison transport with weapon batteries and 413 prisoners. Controversial, powerful, and Proxima's most complicated contribution to the fleet.",
        "type": "ship",
    },
    {
        "id": "hephaestus",
        "ship_name": "Hephaestus",
        "nation": "Helvetii",
        "flag_img": "dow--nation--helvetii.png",
        "ship_img": "dow--ship--hephaestus--black.png",
        "brief_base": "brief--hephaestus",
        "roles": [
            "Captain",
            "First Officer",
            "Chief Engineer",
            "Diplomat",
        ],
        "flavor": "A patchwork industrial jack-of-all-trades crewed by reformed criminals in Helvetii's rehabilitation program. Rowdy, capable, and ready to prove they belong at the table.",
        "type": "ship",
    },
    {
        "id": "baltar",
        "ship_name": "Baltar",
        "nation": "Helvetii",
        "flag_img": "dow--nation--helvetii.png",
        "ship_img": "dow--ship--baltar--black.png",
        "brief_base": "brief--baltar",
        "roles": [
            "Captain",
            "Chief Scientist",
        ],
        "flavor": "Helvetii's state-of-the-art research ship—purpose-built for scanning, prospecting, and discovery. Your multinational crew doesn't feel bound by anyone's neutrality.",
        "type": "ship",
    },
    {
        "id": "javelin",
        "ship_name": "ICSS Javelin",
        "nation": "ICSS",
        "flag_img": "dow--nation--icss.png",
        "ship_img": "dow--ship--javelin--black.png",
        "brief_base": "brief--javelin",
        "roles": [
            "Captain",
            "XO",
            "Chief Engineer",
            "Staff Sergeant",
        ],
        "flavor": "The fleet's newest missile boat—green crew, prototype weapons, and a burning desire to hit back at the Wolves. You were still on shakedown cruise when Old Earth burned.",
        "type": "ship",
    },
    {
        "id": "fuerza-leon",
        "ship_name": "Fuerza Leon",
        "nation": "Confederated Peoples of Asia (CPA)",
        "flag_img": "dow--nation--cpa.png",
        "ship_img": "dow--ship--fuerza-leon--black.png",
        "brief_base": "brief--fuerza-leon",
        "roles": [
            "Captain",
            "First Officer",
        ],
        "flavor": "A CPA bulk hauler with vast cargo capacity and several highly skilled specialists aboard. Emergency jumps scattered your manifest—but that means you have flexibility. Turn the chaos into leverage.",
        "type": "ship",
    },
    # ── INC (NEWS MEDIA) ──────────────────────────────────────────────────
    {
        "id": "inc",
        "ship_name": "Interstellar News Corporation",
        "nation": "INC — Independent",
        "flag_img": "dow--news--inc.png",
        "ship_img": None,
        "brief_base": "brief--inc",
        "roles": [
            "Editor-in-Chief",
            "Lead Anchor",
            "Fleet Correspondent",
            "Military Correspondent",
            "Political Correspondent",
        ],
        "flavor": "The only independent press in the Survivor Fleet. Unrestricted freedom of movement. Broadcast power is real power. Your team shapes morale across the entire fleet—use it seriously, not sensationally.",
        "type": "press",
    },
    # ── WILDCARDS ─────────────────────────────────────────────────────────
    {
        "id": "wildcard--arbourist",
        "ship_name": "The Arbourist",
        "nation": "Unaffiliated",
        "flag_img": None,
        "ship_img": None,
        "brief_base": "brief--wildcard--arbourist",
        "roles": ["Arbourist"],
        "flavor": "The Prophet of the Universal Arbour—a rapidly growing new religion. Weeks ago you had dozens of followers. Now you have hundreds. You roam the entire fleet freely. What kind of prophet will you be?",
        "type": "wildcard",
    },
    {
        "id": "wildcard--inquisitor",
        "ship_name": "The Inquisitor",
        "nation": "Proxima",
        "flag_img": "dow--nation--proxima.png",
        "ship_img": None,
        "brief_base": "brief--wildcard--inquisitor",
        "roles": ["Inquisitor"],
        "flavor": "The last Inquisitor General in the fleet—Proxima's surviving judicial authority, and the only one of any kind. Judge, jury, and prosecutor. Your power is technically unlimited but practically tenuous. Root out Wolf agents. Keep justice alive.",
        "type": "wildcard",
    },
    {
        "id": "wildcard--firebrand",
        "ship_name": "The Firebrand",
        "nation": "Gliese",
        "flag_img": "dow--nation--gliese.png",
        "ship_img": None,
        "brief_base": "brief--wildcard--firebrand",
        "roles": ["Firebrand"],
        "flavor": "A political prisoner—populist, charismatic, and just released after a decade of imprisonment. A stencil of your face is a symbol of resistance. Once free, your voice could reshape the fleet's politics.",
        "type": "wildcard",
    },
]

# ---------------------------------------------------------------------------
# Generate random hex suffixes & rename briefs
# ---------------------------------------------------------------------------


def generate_hex(n=4):
    return "".join(random.choices("0123456789abcdef", k=n))


def rename_briefs(teams):
    """Rename brief PDFs with hex suffixes. Returns a mapping of brief_base → hex."""
    mapping = {}
    briefs_dir = os.path.normpath(BRIEFS_DIR)

    for team in teams:
        base = team["brief_base"]
        old_path = os.path.join(briefs_dir, f"{base}.pdf")

        # Check if already renamed (glob for existing hex-suffixed file)
        already_renamed = False
        if os.path.isdir(briefs_dir):
            for f in os.listdir(briefs_dir):
                if f.startswith(base + "----") and f.endswith(".pdf"):
                    # Extract existing hex
                    hex_part = f.replace(base + "----", "").replace(".pdf", "")
                    mapping[base] = hex_part
                    already_renamed = True
                    print(f"  ✓ {f} (already renamed)")
                    break

        if not already_renamed:
            hex_code = generate_hex()
            new_name = f"{base}----{hex_code}.pdf"
            new_path = os.path.join(briefs_dir, new_name)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                print(f"  → {base}.pdf  ➜  {new_name}")
            else:
                print(f"  ⚠ {base}.pdf not found — will use hex {hex_code} anyway")
            mapping[base] = hex_code

    return mapping


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

STYLES = """\
        body {
            font-family: "LT Tofino", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #222;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
        }
        a {
            color: #FF6600;
            text-decoration: underline;
            font-weight: bold;
        }
        a:hover {
            color: #FF0066;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
        }
        .hero {
            margin: 0 0 10px 0;
        }
        .flag-banner {
            margin: 0 0 20px 0;
        }
        .callout {
            background-color: #FFCC00;
            color: #222;
            padding: 15px 20px;
            margin: 0 0 25px 0;
            border-radius: 4px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }
        h1 {
            font-size: 26px;
            margin: 20px 0 10px 0;
            color: #222;
        }
        h2 {
            font-size: 20px;
            margin: 30px 0 10px 0;
            color: #FF6600;
        }
        p {
            margin: 14px 0;
        }
        .event-meta {
            font-size: 14px;
            color: #999;
            margin: 10px 0 20px 0;
        }
        table.roster {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        table.roster th,
        table.roster td {
            padding: 10px 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        table.roster th {
            background-color: #f5f5f5;
            font-weight: bold;
        }
        .discord-box {
            padding: 15px 20px 15px 0;
            border-top: 8px solid #5865F2;
            border-right: 8px dashed #5865F2;
            border-bottom: 8px solid #5865F2;
            margin: 25px 0;
        }
        .discord-box strong {
            color: #5865F2;
        }
        .discord-btn {
            display: inline-block;
            background-color: #5865F2;
            color: #fff !important;
            padding: 12px 28px;
            font-size: 16px;
            font-weight: bold;
            text-decoration: none;
            border-radius: 4px;
            margin: 12px 0 0 0;
        }
        .discord-btn:hover {
            background-color: #FF0066;
            color: #fff !important;
            text-decoration: none;
        }
        .resources {
            background-color: #FFCC0022;
            padding: 15px 20px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .resources ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .resources li {
            margin: 8px 0;
        }
        .bumper {
            margin-top: 40px;
            padding: 15px 20px;
            border-top: 1px solid #22222222;
            font-size: 14px;
            color: #777;
        }
        .bumper strong {
            color: #FF6600;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #22222222;
            font-size: 14px;
            color: #999;
            text-align: center;
        }
        .footer img {
            max-width: 200px;
            margin: 20px auto 0 auto;
        }
"""


def build_flag_banner_html(team):
    """Build a full-width flag banner image, like the hero."""
    flag = team.get("flag_img")
    if not flag:
        return ""
    return f"""\
    <img src="{ASSETS_URL}/{flag}" alt="{team['nation']}" class="flag-banner">
"""


def build_ship_image_html(team):
    """Build a centered 50%-width ship image."""
    ship = team.get("ship_img")
    if not ship:
        return ""
    return f"""\
    <p style="text-align: center;">
        <img src="{ASSETS_URL}/{ship}" alt="{team['ship_name']}" style="width: 50%; height: auto; margin: 0 auto;">
    </p>
"""


def build_roster_table(roles):
    """Build the crew roster table with placeholder names."""
    rows = ""
    for role in roles:
        rows += f"""\
            <tr>
                <td>{role}</td>
                <td style="color: #999;"><em>[Player Name]</em></td>
            </tr>
"""
    return f"""\
    <table class="roster">
        <thead>
            <tr>
                <th>Suggested Role</th>
                <th>Teammate</th>
            </tr>
        </thead>
        <tbody>
{rows}        </tbody>
    </table>
"""


def build_email(team, hex_mapping):
    brief_base = team["brief_base"]
    hex_code = hex_mapping.get(brief_base, "0000")
    brief_url = f"{RULES_URL}/briefs/{brief_base}----{hex_code}.pdf"
    is_wildcard = team["type"] == "wildcard"
    is_press = team["type"] == "press"
    ship_name = team["ship_name"]
    title_prefix = ship_name

    # --- Callout text ---
    if is_wildcard:
        callout = f"Your role: {ship_name}"
        greeting = f"You've been cast as <strong>{ship_name}</strong>."
    elif is_press:
        callout = "You've been assigned to the INC News Team!"
        greeting = "You're part of the <strong>Interstellar News Corporation</strong>—the fleet's only independent press."
    else:
        callout = f"Welcome aboard the {ship_name}!"
        greeting = f"You've been assigned to the <strong>{ship_name}</strong>."

    # --- Flag banner (full-width, like the hero) ---
    flag_banner = build_flag_banner_html(team)
    # --- Ship image (50% centered, placed after intro) ---
    ship_image = build_ship_image_html(team)

    # --- Roster section ---
    if len(team["roles"]) > 1:
        if is_wildcard:
            roster_section = ""
        elif is_press:
            roster_heading = "Your Team &amp; Suggested Roles"
            roster_section = f"""\
    <h2>{roster_heading}</h2>

    <p>Here's your newsroom lineup and suggested assignments. These are based on survey preferences, but you're free to shuffle roles within the team if everyone agrees!</p>

{build_roster_table(team["roles"])}

    <p style="font-size: 14px; color: #777;"><em>Role suggestions are based on the preferences you expressed in the survey. If you'd like to swap with a teammate, that's totally fine—just coordinate with each other.</em></p>
"""
        else:
            roster_heading = "Your Crew &amp; Suggested Roles"
            roster_section = f"""\
    <h2>{roster_heading}</h2>

    <p>Here's your ship roster and suggested role assignments. These are based on survey preferences, but you're free to shuffle roles within the crew if everyone agrees!</p>

{build_roster_table(team["roles"])}

    <p style="font-size: 14px; color: #777;"><em>Role suggestions are based on the preferences you expressed in the survey. If you'd like to swap with a crewmate, that's totally fine—just coordinate with each other.</em></p>
"""
    else:
        roster_section = ""

    # --- Discord section ---
    if is_wildcard:
        discord_channel_text = "I'll get you set up with your own private channel right away"
    elif is_press:
        discord_channel_text = "I'll get you assigned to the <strong>INC private channel</strong> right away"
    else:
        discord_channel_text = f"I'll get you assigned to the <strong>{ship_name} private channel</strong> right away"

    discord_section = f"""\
    <div class="discord-box">
        <h2 style="margin: 0 0 10px 0;"><strong>Join the PFG Discord Server</strong></h2>
        <p>This is where {"your team" if is_press else "your crew" if not is_wildcard else "we'll"} {"" if is_wildcard else "will "}coordinate before game day. Join the server and send a DM to <strong>Jed (@coppergearbox)</strong>—{discord_channel_text} so you can start planning{"" if is_wildcard else " together"}.</p>
        <p style="font-size: 13px; color: #777;">Even if you're not a Discord regular, it takes 30 seconds to join and it's the easiest way for {"your team" if is_press else "your crew" if not is_wildcard else "us"} to stay connected. That said, all your essential materials are linked below—you won't miss anything critical.</p>
        <p style="text-align: center;"><a href="{DISCORD_INVITE}" class="discord-btn">JOIN THE SERVER ►</a></p>
    </div>
"""

    # --- Resources section ---
    brief_label = "Your Team Brief" if is_press else "Your Ship Brief" if not is_wildcard else "Your Role Brief"
    resources_section = f"""\
    <h2>Prepare for Launch</h2>

    <div class="resources">
        <p><strong>Game resources:</strong></p>
        <ul>
            <li><a href="{RULES_URL}/">Event Overview &amp; Rules Hub</a> — rules primer, background guide, and survival guide all in one place</li>
            <li><a href="{brief_url}"><strong>{brief_label} (private link)</strong></a> — this is for your eyes only, please don't share it with other {"teams" if is_press else "ships" if not is_wildcard else "players"}</li>
        </ul>
        <p style="font-size: 13px; color: #777;">We recommend reading the <strong>Rules Primer</strong> and <strong>Background Guide</strong> first, then your {"team" if is_press else "ship" if not is_wildcard else "role"} brief. You don't need to memorize everything—the survival guide is a handy reference you can bring on game day.</p>
    </div>
"""

    # --- Body copy ---
    if is_wildcard:
        body_intro = f"""\
    <h1>{greeting}</h1>

    <p class="event-meta">Saturday, March 7th · Fargo, ND · 6 Hours</p>

    <p>{team["flavor"]}</p>

    <p>This is a <strong>solo wildcard role</strong>—you won't have a ship crew, but you'll have the entire fleet as your playground. Your brief has everything you need to hit the ground running.</p>

    <p>Let's get you connected and prepared!</p>

{ship_image}
"""
    else:
        other_word = "teammates" if is_press else "crewmates"
        body_intro = f"""\
    <h1>{greeting}</h1>

    <p class="event-meta">Saturday, March 7th · Fargo, ND · 6 Hours</p>

    <p>{team["flavor"]}</p>

    <p>This email is going out to your {other_word} (CC'd above) so you can start getting to know each other. You'll be working together on game day, and a little coordination beforehand goes a long way!</p>

    <p>Let's get you connected and prepared!</p>

{ship_image}
"""

    # --- Bumper ---
    bumper = f"""\
    <div class="bumper">
        <p>Know someone who'd love this? <strong>We only have about 10 spots left!</strong> Send them to <a href="{BASE_URL}/megagames/den-of-wolves-2026/">the event page</a> — and the code <strong>BUDDYSYSTEM</strong> still works at checkout.</p>
    </div>
"""

    # --- Footer ---
    footer = f"""\
    <p style="margin-top: 40px;">
        <strong>— Jed @ Prairie Fire Gaming</strong><br>
        <span style="color: #999; font-size: 14px;">See you in the fleet!</span>
    </p>

    <div class="footer">
        <p>Questions? Contact us at <a href="mailto:info@prairiefiregaming.com">info@prairiefiregaming.com</a></p>
        <p>March 7th, 2026 · West Acres · Fargo, ND</p>
        <a href="{BASE_URL}/">
            <img src="{BASE_URL}/assets/prairiefiregaming.png" alt="Prairie Fire Gaming">
        </a>
    </div>
"""

    # --- Assemble ---
    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your {"Role" if is_wildcard else "Team" if is_press else "Ship"} Assignment: {title_prefix} — Den of Wolves 2026</title>
    <style>
{STYLES}
    </style>
</head>
<body>
    <a href="{BASE_URL}/megagames/den-of-wolves-2026/">
        <img src="{ASSETS_URL}/dow--hero-banner-3.png" alt="Den of Wolves: Infinite Domain" class="hero">
    </a>

{flag_banner}
    <div class="callout">
        {callout}
    </div>

{body_intro}
{roster_section}
{discord_section}
{resources_section}
{bumper}
{footer}
</body>
</html>
"""
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("═══════════════════════════════════════════════════════════")
    print("  Den of Wolves 2026 — Role Assignment Email Generator")
    print("═══════════════════════════════════════════════════════════")
    print()

    # Step 1: Rename briefs
    print("📂 Renaming brief PDFs with hex suffixes…")
    hex_mapping = rename_briefs(TEAMS)
    print()

    # Step 2: Generate email templates
    print("📧 Generating email templates…")
    output_dir = os.path.normpath(OUTPUT_DIR)
    for team in TEAMS:
        filename = f"email-template-dow-2026-role--{team['id']}.html"
        filepath = os.path.join(output_dir, filename)
        html = build_email(team, hex_mapping)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ {filename}")

    print()
    print(f"✅ Done! {len(TEAMS)} templates generated.")
    print()
    print("Hex mapping for briefs:")
    for base, hex_code in sorted(hex_mapping.items()):
        print(f"  {base}  →  {hex_code}")
    print()
    print("Next steps:")
    print("  1. Fill in [Player Name] placeholders in each template")
    print("  2. CC the team members when sending")
    print("  3. Verify brief links resolve correctly after deploy")


if __name__ == "__main__":
    main()
