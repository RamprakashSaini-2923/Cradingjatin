import os

CARDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "assets", "cards")
os.makedirs(CARDS_DIR, exist_ok=True)

# Common SVG elements: EMV chip and contactless waves
def get_chip():
    return """
    <g transform="translate(42, 105)">
        <rect width="44" height="34" rx="6" fill="url(#goldChip)" stroke="#b8860b" stroke-width="1.2"/>
        <line x1="0" y1="17" x2="44" y2="17" stroke="#996515" stroke-width="1"/>
        <line x1="22" y1="0" x2="22" y2="34" stroke="#996515" stroke-width="1"/>
        <circle cx="22" cy="17" r="6" fill="none" stroke="#996515" stroke-width="1"/>
    </g>
    <g transform="translate(100, 114)" stroke="rgba(255,255,255,0.7)" stroke-width="2" fill="none">
        <path d="M0,4 A8,8 0 0,1 0,16"/>
        <path d="M5,1 A13,13 0 0,1 5,19"/>
        <path d="M10,-2 A18,18 0 0,1 10,22"/>
    </g>
    """

def create_card_svg(filename, brand, title, denomination, gradient_colors, brand_svg, accent_color="#00f0ff"):
    g1, g2, g3 = gradient_colors
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="100%" height="100%">
  <defs>
    <linearGradient id="cardGrad_{filename}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{g1}"/>
      <stop offset="50%" stop-color="{g2}"/>
      <stop offset="100%" stop-color="{g3}"/>
    </linearGradient>
    <linearGradient id="goldChip" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffd700"/>
      <stop offset="50%" stop-color="#e6b800"/>
      <stop offset="100%" stop-color="#b8860b"/>
    </linearGradient>
    <linearGradient id="gloss" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="rgba(255,255,255,0.25)"/>
      <stop offset="30%" stop-color="rgba(255,255,255,0.05)"/>
      <stop offset="100%" stop-color="rgba(255,255,255,0)"/>
    </linearGradient>
    <radialGradient id="meshGlow" cx="85%" cy="15%" r="65%">
      <stop offset="0%" stop-color="{accent_color}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{accent_color}" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="15" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>

  <!-- Card Base -->
  <rect width="476" height="296" x="2" y="2" rx="22" fill="url(#cardGrad_{filename})" stroke="rgba(255,255,255,0.18)" stroke-width="2" filter="url(#cardShadow)"/>
  <rect width="476" height="296" x="2" y="2" rx="22" fill="url(#meshGlow)"/>

  <!-- Glossy Sheen Overlay -->
  <path d="M 2,2 Q 240,120 476,2 L 476,296 Q 240,180 2,296 Z" fill="url(#gloss)" opacity="0.4" clip-path="inset(0 round 22px)"/>

  <!-- Brand & Logo Top Header -->
  <g transform="translate(40, 36)">
    <text x="0" y="20" font-family="'Space Grotesk', 'Outfit', sans-serif" font-size="22" font-weight="900" fill="#ffffff" letter-spacing="2">
      {brand.upper()}
    </text>
    <text x="0" y="38" font-family="'Outfit', sans-serif" font-size="11" font-weight="600" fill="rgba(255,255,255,0.7)" letter-spacing="1.5">
      OFFICIAL DIGITAL PASS
    </text>
  </g>

  <!-- Brand Graphic on Right -->
  <g transform="translate(360, 32)">
    {brand_svg}
  </g>

  <!-- EMV Gold Chip & Contactless -->
  {get_chip()}

  <!-- Card Number & Masked Format -->
  <g transform="translate(42, 185)">
    <text x="0" y="0" font-family="'Courier New', monospace" font-size="19" font-weight="bold" fill="#ffffff" letter-spacing="4" opacity="0.95">
      •••• •••• •••• 9412
    </text>
  </g>

  <!-- Bottom Details: Denomination & Title -->
  <g transform="translate(42, 248)">
    <text x="0" y="-8" font-family="'Outfit', sans-serif" font-size="10" font-weight="600" fill="rgba(255,255,255,0.6)" letter-spacing="1">
      VOUCHER VALUE
    </text>
    <text x="0" y="16" font-family="'Space Grotesk', sans-serif" font-size="20" font-weight="800" fill="{accent_color}">
      {denomination}
    </text>
  </g>

  <!-- Holographic Shield Badge -->
  <g transform="translate(370, 215)">
    <circle cx="28" cy="28" r="26" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
    <circle cx="28" cy="28" r="19" fill="none" stroke="{accent_color}" stroke-width="1" stroke-dasharray="3,3"/>
    <path d="M 28,15 L 39,20 L 39,28 C 39,36 28,41 28,41 C 28,41 17,36 17,28 L 17,20 Z" fill="{accent_color}" opacity="0.85"/>
    <path d="M 24,28 L 27,31 L 33,24" stroke="#000" stroke-width="2" fill="none" stroke-linecap="round"/>
  </g>
</svg>"""

    filepath = os.path.join(CARDS_DIR, f"{filename}.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    return filepath

# Brand SVGs (Custom clean vector graphics for each brand)
steam_logo = """
<circle cx="36" cy="36" r="32" fill="#1b2838" stroke="#66c0f4" stroke-width="2.5"/>
<path d="M 36,18 A 8,8 0 1,0 44,26 L 31,39 A 12,12 0 1,1 18,34 L 28,29 A 8,8 0 0,0 36,18 Z" fill="#ffffff"/>
<circle cx="36" cy="26" r="4" fill="#1b2838"/>
<circle cx="26" cy="42" r="6" fill="#1b2838"/>
"""

play_logo = """
<circle cx="36" cy="36" r="32" fill="rgba(0,0,0,0.4)" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
<polygon points="22,18 52,36 22,54" fill="#00e676"/>
<polygon points="22,18 36,36 22,54" fill="#00b0ff"/>
<polygon points="36,36 52,36 22,18" fill="#ffea00"/>
<polygon points="36,36 52,36 22,54" fill="#ff3d00"/>
"""

valorant_logo = """
<circle cx="36" cy="36" r="32" fill="#0f1923" stroke="#ff4655" stroke-width="2"/>
<polygon points="22,24 34,24 24,48 16,48" fill="#ff4655"/>
<polygon points="36,24 54,24 48,48 30,48" fill="#ff4655"/>
"""

bgmi_logo = """
<circle cx="36" cy="36" r="32" fill="#1e180a" stroke="#f1a80a" stroke-width="2.5"/>
<text x="36" y="44" font-family="'Impact', sans-serif" font-size="22" font-weight="bold" fill="#f1a80a" text-anchor="middle">UC</text>
"""

xbox_logo = """
<circle cx="36" cy="36" r="32" fill="#107c10" stroke="#ffffff" stroke-width="2"/>
<path d="M 22,24 Q 36,36 50,24 Q 40,48 36,54 Q 32,48 22,24 Z" fill="#ffffff"/>
"""

ps_logo = """
<circle cx="36" cy="36" r="32" fill="#003791" stroke="#ffffff" stroke-width="2"/>
<path d="M 33,18 L 33,52 L 40,49 L 40,24 Q 40,21 44,23 L 44,47 L 50,44 L 50,22 Q 50,16 38,17 Z" fill="#ffffff"/>
<ellipse cx="26" cy="46" rx="14" ry="6" fill="#00439c" opacity="0.6"/>
"""

netflix_logo = """
<circle cx="36" cy="36" r="32" fill="#000000" stroke="#e50914" stroke-width="2.5"/>
<path d="M 24,18 L 30,18 L 30,54 L 24,54 Z" fill="#b81d24"/>
<path d="M 42,18 L 48,18 L 48,54 L 42,54 Z" fill="#b81d24"/>
<polygon points="24,18 31,18 48,54 41,54" fill="#e50914"/>
"""

spotify_logo = """
<circle cx="36" cy="36" r="32" fill="#1ed760"/>
<path d="M 20,28 A 18,18 0 0,1 50,25" stroke="#121212" stroke-width="4.5" stroke-linecap="round" fill="none"/>
<path d="M 23,36 A 14,14 0 0,1 47,34" stroke="#121212" stroke-width="3.5" stroke-linecap="round" fill="none"/>
<path d="M 26,43 A 10,10 0 0,1 44,42" stroke="#121212" stroke-width="2.8" stroke-linecap="round" fill="none"/>
"""

amazon_logo = """
<circle cx="36" cy="36" r="32" fill="#131921" stroke="#ff9900" stroke-width="2"/>
<text x="36" y="38" font-family="'Space Grotesk', sans-serif" font-size="24" font-weight="900" fill="#ffffff" text-anchor="middle">a</text>
<path d="M 22,44 Q 36,52 50,44" stroke="#ff9900" stroke-width="3" fill="none" stroke-linecap="round"/>
"""

youtube_logo = """
<circle cx="36" cy="36" r="32" fill="#282828" stroke="#ff0000" stroke-width="2.5"/>
<polygon points="30,24 46,36 30,48" fill="#ff0000"/>
"""

apple_logo = """
<circle cx="36" cy="36" r="32" fill="#1c1c1e" stroke="rgba(255,255,255,0.4)" stroke-width="2"/>
<path d="M 37,20 C 37,16 41,14 41,14 C 39,17 36,19 33,19 C 33,19 32,15 37,20 Z M 26,35 C 26,45 33,52 38,52 C 40,52 42,50 45,50 C 48,50 49,52 52,52 C 57,52 61,45 61,45 C 61,45 54,41 54,34 C 54,27 60,24 60,24 C 57,20 52,19 49,19 C 45,19 43,21 41,21 C 38,21 35,19 32,19 C 26,20 21,26 21,35 Z" fill="#ffffff" transform="translate(-10, -5) scale(0.9)"/>
"""

windows_logo = """
<circle cx="36" cy="36" r="32" fill="#001d3d" stroke="#00a4ef" stroke-width="2"/>
<rect x="20" y="20" width="13" height="13" fill="#00a4ef"/>
<rect x="37" y="20" width="13" height="13" fill="#00a4ef"/>
<rect x="20" y="37" width="13" height="13" fill="#00a4ef"/>
<rect x="37" y="37" width="13" height="13" fill="#00a4ef"/>
"""

cards_data = [
    ("steam_500", "Steam", "Steam Wallet ₹500", "₹500 Balance", ("#0e1b2b", "#172b43", "#0b121c"), steam_logo, "#66c0f4"),
    ("steam_1000", "Steam", "Steam Wallet ₹1,000", "₹1,000 Balance", ("#091322", "#132338", "#080d16"), steam_logo, "#66c0f4"),
    ("valorant_vp", "Valorant", "Valorant 1,000 VP", "1,000 VP", ("#221017", "#3b1723", "#12080d"), valorant_logo, "#ff4655"),
    ("bgmi_uc", "BGMI", "BGMI 660 UC Pass", "660 UC Credits", ("#231c07", "#3d2f0a", "#141004"), bgmi_logo, "#f1a80a"),
    ("xbox_pass", "Xbox", "Xbox Game Pass", "1 Month Ultimate", ("#06230f", "#0c451d", "#03170a"), xbox_logo, "#107c10"),
    ("playstation_1000", "PlayStation", "PS Store ₹1,000", "₹1,000 Balance", ("#051838", "#0a2e6e", "#030e24"), ps_logo, "#0070d1"),
    ("netflix_uhd", "Netflix", "Netflix UHD 4K", "1 Month Premium", ("#260408", "#42070f", "#120204"), netflix_logo, "#e50914"),
    ("spotify_prem", "Spotify", "Spotify Premium", "3 Months Pass", ("#042111", "#084021", "#02140a"), spotify_logo, "#1ed760"),
    ("amazon_prime", "Amazon", "Prime Video", "3 Months Access", ("#0a1928", "#122d4a", "#050e18"), amazon_logo, "#00a8e1"),
    ("youtube_prem", "YouTube", "YouTube Premium", "3 Months Pass", ("#29080c", "#470c14", "#140406"), youtube_logo, "#ff0000"),
    ("play_500", "Google Play", "Play Store Card ₹500", "₹500 Code", ("#0a2228", "#123d48", "#051317"), play_logo, "#00e676"),
    ("play_1000", "Google Play", "Play Store Card ₹1,000", "₹1,000 Code", ("#081d22", "#0f363f", "#040f12"), play_logo, "#00e676"),
    ("amazon_500", "Amazon", "Shopping Voucher ₹500", "₹500 Voucher", ("#1f1807", "#362a0c", "#120e04"), amazon_logo, "#ff9900"),
    ("apple_1000", "Apple", "App Store Card ₹1,000", "₹1,000 Code", ("#1c1c1e", "#2c2c2e", "#0c0c0e"), apple_logo, "#f5f5f7"),
    ("windows_11", "Microsoft", "Windows 11 Pro", "Retail License", ("#061a33", "#0c3263", "#030d1a"), windows_logo, "#00a4ef"),
    ("office_365", "Microsoft", "Office 365 Pro", "1 Year License", ("#240e06", "#451a0b", "#140703"), windows_logo, "#d83b01")
]

for card in cards_data:
    create_card_svg(*card)

print(f"Generated {len(cards_data)} vector card graphics in {CARDS_DIR}")
