"""Draws the SVG artwork for this repository.

    python3 dev/make-assets.py
"""

from pathlib import Path

BG = "#0f1720"
PANEL = "#16202b"
BORDER = "#28394a"
TEXT = "#e6edf3"
MUTED = "#9fb0c0"
HA = "#41BDF5"
VIOLET = "#7C7CF5"
GREEN = "#3ddc97"
FONT = "ui-sans-serif, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"
OUT = Path("assets")


def escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def frame(width: int, height: int, label: str, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{HA}"/>
      <stop offset="1" stop-color="{VIOLET}"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" rx="16" fill="{BG}"/>
  <g font-family="{FONT}">
{body}  </g>
</svg>
"""


def text(x, y, value, fill=TEXT, size=14, weight=None, anchor=None, family=None):
    parts = [f'    <text x="{x}" y="{y}" fill="{fill}" font-size="{size}"']
    if weight:
        parts.append(f' font-weight="{weight}"')
    if anchor:
        parts.append(f' text-anchor="{anchor}"')
    if family:
        parts.append(f' font-family="{family}"')
    parts.append(f">{escape(str(value))}</text>\n")
    return "".join(parts)


def card(x, y, w, h, r=14, fill=PANEL, stroke=BORDER):
    return f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>\n'


def envelope(x, y, scale=1.0, colour="#fff", width=2.2):
    w, h = 26 * scale, 19 * scale
    return (
        f'    <g stroke="{colour}" stroke-width="{width}" fill="none" stroke-linejoin="round">\n'
        f'      <rect x="{x}" y="{y}" width="{w:.1f}" height="{h:.1f}" rx="{3 * scale:.1f}"/>\n'
        f'      <path d="M{x} {y + 4 * scale:.1f} {x + w / 2:.1f} {y + h - 4 * scale:.1f} {x + w:.1f} {y + 4 * scale:.1f}"/>\n'
        f"    </g>\n"
    )


def banner() -> str:
    body = (
        '    <circle cx="1040" cy="90" r="180" fill="url(#accent)" opacity="0.10"/>\n'
        + card(72, 96, 72, 72, 22, "url(#accent)", "none")
        + envelope(95, 120, 1.0)
        + text(172, 132, "Mail Archiver", TEXT, 34, "700")
        + text(172, 162, "Home Assistant App (Add-on)", HA, 20, "600")
        + text(72, 224, "Runs the mail backup on Home Assistant OS itself. Appears in the sidebar", MUTED, 17)
        + text(72, 250, "through ingress - in the browser and in the Home Assistant app.", MUTED, 17)
        + card(72, 288, 214, 42, 21, PANEL, BORDER)
        + text(96, 315, "aarch64 · amd64", HA, 14, "600")
        + card(302, 288, 190, 42, 21, PANEL, BORDER)
        + text(326, 315, "Ingress, no login", VIOLET, 14, "600")
        + card(508, 288, 214, 42, 21, PANEL, BORDER)
        + text(532, 315, "Backups included", GREEN, 14, "600")
        + f'    <g stroke="{HA}" stroke-width="4" fill="none" stroke-linejoin="round">\n'
        + '      <path d="M1000 210 1075 140 1150 210"/>\n'
        + '      <path d="M1020 200v70h110v-70"/>\n'
        + '      <path d="M1060 270v-26a15 15 0 0 1 30 0v26"/>\n'
        + "    </g>\n"
    )
    return frame(1200, 400, "Mail Archiver as a Home Assistant add-on", body)


def sidebar() -> str:
    items = ["Übersicht", "Energie", "Verlauf", "Mail Archiver", "Entwickler", "Einstellungen"]
    body = (
        text(60, 62, "In the sidebar", TEXT, 22, "700")
        + text(60, 92, "Ingress puts the interface inside Home Assistant, phone included.", MUTED, 15)
        + card(60, 130, 260, 380)
    )
    y = 176
    for item in items:
        active = item == "Mail Archiver"
        if active:
            body += card(76, y - 22, 228, 36, 10, "#1d3a4d", "none")
        body += text(112, y, item, HA if active else MUTED, 14, "600" if active else None)
        body += (
            f'    <circle cx="94" cy="{y - 5}" r="6" fill="none" stroke="{HA if active else MUTED}" stroke-width="1.6"/>\n'
        )
        y += 52

    body += card(344, 130, 796, 380)
    body += card(344, 130, 796, 56, 14, "#101a24", "none")
    body += text(372, 165, "Mail Archiver", TEXT, 16, "600")
    body += text(1116, 165, "Übersicht", MUTED, 13, anchor="end")
    body += card(372, 214, 350, 96)
    body += text(396, 246, "NACHRICHTEN", MUTED, 10)
    body += text(396, 278, "48.213", TEXT, 24, "600")
    body += card(746, 214, 366, 96)
    body += text(770, 246, "ARCHIVGRÖSSE", MUTED, 10)
    body += text(770, 278, "1,84 GB", TEXT, 24, "600")
    body += card(372, 334, 740, 140)
    body += text(396, 368, "Status der Konten", TEXT, 15, "600")
    body += text(396, 406, "Privat", MUTED, 13)
    body += text(1088, 406, "12.480 · 612 MB", MUTED, 13, anchor="end")
    body += text(396, 440, "Arbeit", MUTED, 13)
    body += text(1088, 440, "35.733 · 1,24 GB", MUTED, 13, anchor="end")
    return frame(1200, 560, "The add-on interface inside the Home Assistant sidebar", body)


def install() -> str:
    steps = [
        ("1", "Repository", "Settings, Add-ons, Add-on store, three dots, Repositories."),
        ("2", "Add", "Paste the URL of this repository and add it."),
        ("3", "Install", "Install Mail Archiver and set a master password."),
        ("4", "Start", "Start it and open Mail Archiver from the sidebar."),
    ]
    body = text(60, 62, "Installation", TEXT, 22, "700")
    x = 60
    for number, title, description in steps:
        body += card(x, 100, 258, 200)
        body += f'    <circle cx="{x + 44}" cy="146" r="22" fill="url(#accent)"/>\n'
        body += text(x + 44, 153, number, "#0f1720", 18, "700", anchor="middle")
        body += text(x + 24, 206, title, TEXT, 17, "600")
        line, lines = "", []
        for word in description.split():
            if len(line) + len(word) > 30:
                lines.append(line)
                line = word
            else:
                line = f"{line} {word}".strip()
        lines.append(line)
        for index, entry in enumerate(lines[:4]):
            body += text(x + 24, 234 + index * 20, entry, MUTED, 13)
        x += 282
    return frame(1200, 340, "The four installation steps", body)


def storage() -> str:
    body = (
        text(60, 62, "Where things are kept", TEXT, 22, "700")
        + text(60, 92, "Both survive an update of the add-on, and both are part of a Home Assistant backup.", MUTED, 15)
        + card(60, 136, 520, 200)
        + text(88, 178, "/data/config", HA, 16, "600", family=MONO)
        + text(88, 210, "Encrypted configuration and the index", MUTED, 13)
        + text(88, 234, "database. Small, a few megabytes.", MUTED, 13)
        + text(88, 274, "Managed by the supervisor,", MUTED, 13)
        + text(88, 298, "not visible in the file editor.", MUTED, 13)
        + card(620, 136, 520, 200)
        + text(648, 178, "/share/mail-archive", VIOLET, 16, "600", family=MONO)
        + text(648, 210, "One .eml per message, in the folder", MUTED, 13)
        + text(648, 234, "tree of the mailbox. As big as the", MUTED, 13)
        + text(648, 258, "mailbox itself.", MUTED, 13)
        + text(648, 298, "Readable from any other add-on.", MUTED, 13)
        + card(60, 366, 1080, 74, 14, "#1c2a1f", "#2c4a33")
        + text(88, 400, "Careful", GREEN, 14, "600")
        + text(88, 424, "Everything outside /share, /media and /backup lives inside the container and is gone with the next update.", MUTED, 13)
    )
    return frame(1200, 480, "Where the add-on keeps its configuration and the archive", body)


def social() -> str:
    body = (
        '    <circle cx="1120" cy="120" r="260" fill="url(#accent)" opacity="0.12"/>\n'
        + card(96, 150, 96, 96, 28, "url(#accent)", "none")
        + envelope(126, 186, 1.3)
        + text(224, 200, "Mail Archiver", TEXT, 46, "700")
        + text(224, 244, "Home Assistant App (Add-on)", HA, 26, "600")
        + text(96, 330, "IMAP mailboxes backed up to files you own —", MUTED, 22)
        + text(96, 366, "in the sidebar, on Home Assistant OS.", MUTED, 22)
        + card(96, 420, 250, 52, 26, PANEL, BORDER)
        + text(221, 453, "Ingress, no login", HA, 17, "600", anchor="middle")
        + card(362, 420, 232, 52, 26, PANEL, BORDER)
        + text(478, 453, "aarch64 · amd64", VIOLET, 17, "600", anchor="middle")
        + f'    <g stroke="{HA}" stroke-width="7" fill="none" stroke-linejoin="round">\n'
        + '      <path d="M900 330 1010 230 1120 330"/>\n'
        + '      <path d="M930 316v110h160v-110"/>\n'
        + '      <path d="M985 426v-42a25 25 0 0 1 50 0v42"/>\n'
        + "    </g>\n"
    )
    return frame(1280, 640, "Mail Archiver as a Home Assistant add-on", body)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "banner.svg").write_text(banner())
    (OUT / "sidebar.svg").write_text(sidebar())
    (OUT / "install.svg").write_text(install())
    (OUT / "storage.svg").write_text(storage())
    (OUT / "social-preview.svg").write_text(social())
    print("wrote", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
