LIGHT = dict(bg="#ffffff", sidebar="#f9f9f9", surface="#f4f4f4", border="#e5e5e5",
             text="#0d0d0d", muted="#6b6b6b", hover="#ececec",
             accent="#0d0d0d", accent_text="#ffffff", code="#f6f6f6")
DARK = dict(bg="#212121", sidebar="#171717", surface="#2f2f2f", border="#3b3b3b",
            text="#ececec", muted="#a3a3a3", hover="#2a2a2a",
            accent="#ececec", accent_text="#171717", code="#181818")


def _vars(p: dict) -> str:
    return ";".join(f"--{k}:{v}" for k, v in p.items())


BASE = """
html, body, .stApp { font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { visibility: hidden; }
[data-testid="stElementContainer"]:has(iframe[height="0"]) { display: none; }

/* ── Surfaces ─────────────────────────────────────────── */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] { background: var(--bg) !important; color: var(--text); }
[data-testid="stHeader"] { background: transparent !important; }
/* always-visible "open sidebar" button when the sidebar is collapsed */
[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {
    position: fixed; top: .6rem; left: .6rem; z-index: 1000002;
    background: var(--surface); border: 1px solid var(--border); border-radius: 10px; }
[data-testid="stExpandSidebarButton"] *, [data-testid="stSidebarCollapsedControl"] *,
[data-testid="collapsedControl"] *, [data-testid="stSidebarCollapseButton"] *,
[data-testid="stSidebarHeader"] button * { color: var(--text) !important; }
[data-testid="stSidebar"], [data-testid="stSidebar"] > div { background: var(--sidebar) !important; border-right: 1px solid var(--border); }
.stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
[data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] p, .stTabs button { color: var(--text); }
[data-testid="stCaptionContainer"], .stApp small { color: var(--muted) !important; }
hr { border-color: var(--border) !important; }
.block-container { max-width: 50rem; padding: 3rem 1rem 7rem; }
.stApp p, .stApp li { font-size: var(--fs); line-height: 1.65; }

/* ── Inputs / popovers / dialogs ──────────────────────── */
[data-baseweb="input"] > div, [data-baseweb="base-input"], [data-baseweb="textarea"],
[data-baseweb="select"] > div, [data-testid="stFileUploaderDropzone"] {
    background: var(--surface) !important; border-color: var(--border) !important;
    color: var(--text) !important; border-radius: 12px !important; }
input, textarea { color: var(--text) !important; }
[data-baseweb="popover"] > div, [data-baseweb="menu"], [role="dialog"], [data-testid="stPopoverBody"] {
    background: var(--bg) !important; color: var(--text); border: 1px solid var(--border); border-radius: 14px; }
[data-baseweb="menu"] li:hover { background: var(--hover) !important; }
button[data-baseweb="tab"] { color: var(--muted); }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--text); }
pre, [data-testid="stCode"] pre { background: var(--code) !important; border: 1px solid var(--border); border-radius: 12px; }
table, th, td { border-color: var(--border) !important; color: var(--text); }

/* ── Buttons ──────────────────────────────────────────── */
.stButton > button, .stDownloadButton > button, [data-testid="stPopover"] > button {
    background: transparent; color: var(--text); border: 1px solid var(--border);
    border-radius: 10px; transition: background .15s, border-color .15s; }
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stPopover"] > button:hover {
    background: var(--hover); border-color: var(--border); color: var(--text); }
.stButton > button[kind="primary"] { background: var(--accent); color: var(--accent_text); border-color: var(--accent); }
.stButton > button[kind="primary"] p { color: var(--accent_text); }

/* ── Sidebar ──────────────────────────────────────────── */
[data-testid="stSidebarUserContent"] { padding-top: .5rem; }
[data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlock"] { min-height: calc(100vh - 4rem); }
.st-key-sb_bottom { margin-top: auto; }
.brand { display: flex; align-items: center; gap: .55rem; font-weight: 600; font-size: 1.05rem; padding: .2rem .3rem .6rem; }
.brand .logo { width: 28px; height: 28px; border-radius: 8px; background: var(--accent); color: var(--accent_text);
               display: grid; place-items: center; font-size: .9rem; }
.side-heading { font-size: .75rem; font-weight: 600; color: var(--muted); letter-spacing: .04em;
                text-transform: uppercase; padding: .9rem .4rem .1rem; }
.group-label { font-size: .72rem; color: var(--muted); padding: .7rem .5rem .2rem; }
.st-key-history { overflow-y: auto; max-height: calc(100vh - 380px); }
[data-testid="stSidebar"] .stButton > button {
    border: none !important; box-shadow: none !important; justify-content: flex-start; text-align: left;
    min-height: 2.1rem; padding: .25rem .6rem; }
[data-testid="stSidebar"] .stButton > button[kind="secondary"] { background: transparent !important; }
[data-testid="stSidebar"] .stButton > button:hover { background: var(--hover) !important; }
[data-testid="stSidebar"] .st-key-new_chat button { border: 1px solid var(--border) !important; justify-content: center; }
.st-key-history [data-testid="stVerticalBlock"] { gap: .1rem; }
[class*="st-key-row_"] [data-testid="stPopover"] > button { border: none !important; background: transparent !important; }
[data-testid="stSidebar"] .st-key-new_chat button { border: 1px solid var(--border); justify-content: center; }
[class*="st-key-row_"] button p { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
[class*="st-key-row_"] button[kind="primary"] { background: var(--hover); color: var(--text); }
[class*="st-key-row_"] [data-testid="stPopover"] > button { border: none; padding: 0 .4rem; }
[class*="st-key-row_"] [data-testid="stPopover"] { opacity: 0; transition: opacity .15s; }
[class*="st-key-row_"]:hover [data-testid="stPopover"], [class*="st-key-row_"]:focus-within [data-testid="stPopover"] { opacity: 1; }
@media (hover: none) { [class*="st-key-row_"] [data-testid="stPopover"] { opacity: 1; } }
[class*="st-key-row_"] [data-testid="stPopover"] button [data-testid="stIconMaterial"],
[class*="st-key-row_"] [data-testid="stPopover"] button svg { display: none; }
.profile { display: flex; align-items: center; gap: .6rem; padding: .3rem .2rem; font-weight: 500; }
.avatar { width: 30px; height: 30px; border-radius: 50%; background: var(--accent); color: var(--accent_text);
          display: grid; place-items: center; font-size: .8rem; font-weight: 600; }

/* keep rows on one line, even on mobile */
[class*="st-key-row_"] [data-testid="stHorizontalBlock"], .st-key-topbar [data-testid="stHorizontalBlock"],
[class*="st-key-actions_"] [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: .25rem; }
[class*="st-key-actions_"] [data-testid="stColumn"] { flex: 0 0 auto !important; width: auto !important; min-width: 0 !important; }

/* ── Top bar ──────────────────────────────────────────── */
.st-key-topbar { position: sticky; top: 0; z-index: 50; background: var(--bg); padding: .6rem 0 .4rem 2.6rem;
                 border-bottom: 1px solid var(--border); margin-bottom: .5rem; }
.chat-title { font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.st-key-topbar [data-testid="stPopover"] > button { border: none; }
.st-key-topbar [data-testid="stPopover"] button [data-testid="stIconMaterial"] { display: none; }

/* ── Messages ─────────────────────────────────────────── */
[data-testid="stChatMessage"] { background: transparent; padding: var(--gap) 0; }
[data-testid^="stChatMessageAvatar"] { background: var(--surface); color: var(--text); border: 1px solid var(--border); }
/* user turn: right side, bubble. AI turn: left side, plain */
[data-testid="stChatMessage"]:has([class*="st-key-umsg_"]) { flex-direction: row-reverse; }
[data-testid="stChatMessage"]:has([class*="st-key-umsg_"]) [data-testid="stChatMessageContent"] {
    flex: 0 1 auto; width: fit-content; max-width: 82%; background: var(--surface);
    border-radius: 1.25rem; padding: .65rem 1.05rem; }

/* action bar under AI answers */
[class*="st-key-actions_"] button { border: none; min-height: 2rem; padding: 0 .45rem; color: var(--muted); }
[class*="st-key-actions_"] button[kind="primary"] { background: var(--hover); color: var(--text); }
[class*="st-key-actions_"] [data-testid="stPopover"] > button { border: none; }
[class*="st-key-actions_"] [data-testid="stPopover"] button [data-testid="stIconMaterial"]:last-child { display: none; }

/* typing animation + stop button */
.typing { display: flex; align-items: center; gap: 5px; padding: .4rem 0; }
.typing span:not(.think-label) { width: 7px; height: 7px; border-radius: 50%; background: var(--muted);
                                  animation: blink 1.2s infinite ease-in-out; }
.typing span:nth-child(2) { animation-delay: .15s; } .typing span:nth-child(3) { animation-delay: .3s; }
.think-label { margin-left: .5rem; color: var(--muted); font-size: .85rem; }
@keyframes blink { 0%,80%,100% { opacity: .25; transform: scale(.8); } 40% { opacity: 1; transform: scale(1); } }
.st-key-stopbar button { border-radius: 999px; font-size: .82rem; padding: .15rem .9rem; margin-bottom: .4rem; }

/* ── Composer ─────────────────────────────────────────── */
[data-testid="stChatInput"] { background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 1.6rem; box-shadow: 0 4px 24px rgba(0,0,0,.07); }
[data-testid="stChatInput"] textarea { background: transparent !important; color: var(--text) !important; }
[data-testid="stChatInputSubmitButton"] { background: var(--accent) !important; color: var(--accent_text) !important; border-radius: 50%; }

/* ── Welcome ──────────────────────────────────────────── */
.welcome { text-align: center; margin: 16vh 0 1.5rem; }
.welcome h1 { font-size: 2rem; font-weight: 600; margin-bottom: .3rem; }
.welcome p { color: var(--muted) !important; }
.st-key-cards button { height: auto; padding: .9rem 1rem; text-align: left; justify-content: flex-start;
                       border-radius: 14px; background: var(--surface); border: 1px solid var(--border); }
.st-key-cards button:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(0,0,0,.08); }
.empty-state { text-align: center; color: var(--muted); padding: 1rem .5rem; font-size: .85rem; }
"""


def build_css(theme: str, font_size: str, compact: bool, show_avatars: bool) -> str:
    if theme == "Light":
        root = f":root{{{_vars(LIGHT)}}}"
    elif theme == "Dark":
        root = f":root{{{_vars(DARK)}}}"
    else:   # System: follow the OS
        root = f":root{{{_vars(LIGHT)}}} @media (prefers-color-scheme: dark){{:root{{{_vars(DARK)}}}}}"
    fs = {"Small": "0.9rem", "Default": "1rem", "Large": "1.1rem"}.get(font_size, "1rem")
    gap = ".15rem" if compact else ".7rem"
    avatars = "" if show_avatars else '[data-testid^="stChatMessageAvatar"]{display:none!important}'
    return (f"<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');"
            f"{root}:root{{--fs:{fs};--gap:{gap}}}{BASE}{avatars}</style>")