from urllib.parse import quote

# Atom One Dark / Atom One Light palettes
DARK = dict(bg="#282c34", sidebar="#21252b", surface="#2c313a", border="#3e4451",
            text="#abb2bf", bright="#d7dae0", muted="#7f848e", hover="#2c313a", active="#333945",
            accent="#61afef", accent_text="#1e2227", label="#c678dd", red="#e06c75", code="#282c34")
LIGHT = dict(bg="#fafafa", sidebar="#eeeeef", surface="#f0f0f1", border="#dbdbdc",
             text="#383a42", bright="#232324", muted="#696c77", hover="#e6e6e7", active="#dcdcdd",
             accent="#4078f2", accent_text="#ffffff", label="#a626a4", red="#e45649", code="#f0f0f1")


def _vars(p: dict) -> str:
    return ";".join(f"--{k}:{v}" for k, v in p.items())


# ── Lucide icons (drawn with CSS masks so they inherit the text colour) ──────────
ICONS = {
    "plus": "<path d='M5 12h14'/><path d='M12 5v14'/>",
    "search": "<circle cx='11' cy='11' r='8'/><path d='m21 21-4.3-4.3'/>",
    "message-square": "<path d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'/>",
    "chevrons-left": "<path d='m11 17-5-5 5-5'/><path d='m18 17-5-5 5-5'/>",
    "chevrons-right": "<path d='m6 17 5-5-5-5'/><path d='m13 17 5-5-5-5'/>",
    "settings": ("<path d='M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z'/>"
                 "<circle cx='12' cy='12' r='3'/>"),
    "pencil": "<path d='M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z'/><path d='m15 5 4 4'/>",
    "trash": ("<path d='M3 6h18'/><path d='M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6'/>"
              "<path d='M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2'/><path d='M10 11v6'/><path d='M14 11v6'/>"),
    "sparkle": "<path d='M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z'/>",
}


def _icon(name: str) -> str:
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' "
           f"stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>{ICONS[name]}</svg>")
    return f'url("data:image/svg+xml;utf8,{quote(svg)}")'


def _mask(selector: str, name: str, size: int = 18) -> str:
    m = _icon(name)
    return (f"{selector}::before{{content:'';flex:none;width:{size}px;height:{size}px;background:currentColor;"
            f"-webkit-mask:{m} center/contain no-repeat;mask:{m} center/contain no-repeat}}")


ICON_CSS = "".join([
    _mask(".st-key-new_chat button", "plus", 18),
    _mask(".st-key-sb_collapse button", "chevrons-left", 20),
    _mask(".st-key-sb_expand button", "chevrons-right", 20),
    _mask('[class*="st-key-chat_"] button', "message-square", 16),
    _mask(".st-key-open_settings_btn button", "settings", 18),
    _mask('[class*="st-key-rename_"] button', "pencil", 16),
    _mask('[class*="st-key-delc_"] button', "trash", 16),
    _mask(".brand .logo", "sparkle", 18),
])

SEARCH_CSS = (
    ".st-key-search_wrap [data-baseweb='input']{position:relative}"
    ".st-key-search_wrap [data-baseweb='input']::before{content:'';position:absolute;left:.8rem;top:50%;"
    "transform:translateY(-50%);width:16px;height:16px;background:var(--muted);z-index:1;pointer-events:none;"
    f"-webkit-mask:{_icon('search')} center/contain no-repeat;mask:{_icon('search')} center/contain no-repeat}}"
    ".st-key-search_wrap [data-baseweb='input']::after{content:'Ctrl K';position:absolute;right:.6rem;top:50%;"
    "transform:translateY(-50%);font-size:.7rem;color:var(--accent);border:1px solid var(--border);"
    "border-radius:6px;padding:.05rem .4rem;pointer-events:none}"
    ".st-key-search_wrap input{padding-left:2.4rem!important;padding-right:4rem!important}"
)

BASE = """
html, body, .stApp { font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { visibility: hidden; }
[data-testid="stElementContainer"]:has(iframe[height="0"]) { display: none; }
button:focus-visible, input:focus-visible, textarea:focus-visible { outline: 2px solid var(--accent) !important; outline-offset: 1px; }

/* ── Surfaces ─────────────────────────────────────────── */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] { background: var(--bg) !important; color: var(--text); }
[data-testid="stHeader"] { background: transparent !important; }
.stApp p, .stApp li, .stApp label, [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] p, .stTabs button { color: var(--text); }
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp strong { color: var(--bright); }
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
button[data-baseweb="tab"][aria-selected="true"] { color: var(--bright); }
pre, [data-testid="stCode"] pre { background: var(--code) !important; border: 1px solid var(--border); border-radius: 12px; }
table, th, td { border-color: var(--border) !important; color: var(--text); }

/* ── Buttons ──────────────────────────────────────────── */
.stButton > button, .stDownloadButton > button, [data-testid="stPopover"] > button {
    background: transparent; color: var(--text); border: 1px solid var(--border);
    border-radius: 10px; transition: background .15s, border-color .15s, color .15s; }
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stPopover"] > button:hover {
    background: var(--hover); border-color: var(--border); color: var(--bright); }
.stButton > button[kind="primary"] { background: var(--accent); color: var(--accent_text); border-color: var(--accent); }
.stButton > button[kind="primary"] p { color: var(--accent_text); }

/* ── Sidebar shell (260px, animated collapse) ─────────── */
[data-testid="stSidebarCollapseButton"], [data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] {
    transform: none !important; margin-left: 0 !important; visibility: visible !important;
    width: 260px !important; min-width: 260px !important; max-width: 260px !important;
    background: var(--sidebar) !important; border-right: 1px solid var(--border);
    transition: width .25s ease, min-width .25s ease, max-width .25s ease; }
section[data-testid="stSidebar"] > div { background: var(--sidebar) !important; }
@media (max-width: 768px) {
    section[data-testid="stSidebar"] { width: 85vw !important; min-width: 0 !important; max-width: 85vw !important; } }
[data-testid="stSidebarUserContent"] { padding: .9rem .6rem .6rem; }
[data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlock"] { min-height: calc(100vh - 2.5rem); gap: .65rem; }
.st-key-sb_bottom { margin-top: auto; }

/* generic sidebar buttons: flat, no boxes */
[data-testid="stSidebar"] .stButton > button {
    background: transparent; border: none !important; box-shadow: none !important; color: var(--text);
    justify-content: flex-start; gap: .65rem; min-height: 2.3rem; padding: .3rem .7rem; border-radius: 10px; }
[data-testid="stSidebar"] .stButton > button:hover { background: var(--hover); color: var(--bright); }
[data-testid="stSidebar"] .stButton > button [data-testid="stMarkdownContainer"] { min-width: 0; flex: 1 1 auto; text-align: left; }
[data-testid="stSidebar"] .stButton > button p { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-align: left; margin: 0; }

/* header */
.brand { display: flex; align-items: center; gap: .65rem; font-weight: 600; font-size: 1.15rem; color: var(--bright); }
.brand .logo { width: 32px; height: 32px; border-radius: 10px; background: var(--accent); color: var(--accent_text);
               display: grid; place-items: center; flex: none; }
.st-key-sb_collapse button, .st-key-sb_expand button { justify-content: center !important; padding: 0 !important; min-width: 2.2rem; color: var(--muted); }
.st-key-sb_collapse [data-testid="stIconMaterial"], .st-key-sb_expand [data-testid="stIconMaterial"],
.st-key-sb_collapse [data-testid="stButtonIcon"], .st-key-sb_expand [data-testid="stButtonIcon"] { display: none; }
.st-key-sb_expand { position: fixed; top: .7rem; left: .7rem; z-index: 1000002; width: auto !important; }
.st-key-sb_expand button { background: var(--surface) !important; border: 1px solid var(--border) !important; }

/* prominent New Chat */
[data-testid="stSidebar"] .st-key-new_chat button {
    background: var(--accent); color: var(--accent_text); font-weight: 600; min-height: 2.7rem;
    border-radius: 12px; padding-left: 1rem; }
[data-testid="stSidebar"] .st-key-new_chat button:hover { background: var(--accent); color: var(--accent_text); filter: brightness(1.08); }
[data-testid="stSidebar"] .st-key-new_chat button p { color: var(--accent_text); }

/* history */
.side-heading { font-size: .72rem; font-weight: 600; color: var(--muted); letter-spacing: .05em;
                text-transform: uppercase; padding: .3rem .6rem 0; }
.group-label { font-size: .85rem; font-weight: 500; color: var(--label); padding: .8rem .6rem .25rem; }
.st-key-history { overflow-y: auto; max-height: calc(100vh - 400px); }
.st-key-history [data-testid="stVerticalBlock"] { gap: .1rem; }
[class*="st-key-row_"] { border-radius: 10px; transition: background .15s; }
[class*="st-key-row_"]:hover { background: var(--hover); }
[class*="st-key-row_on_"] { background: var(--active) !important; }
[class*="st-key-row_"] [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0 !important; align-items: center; }
[class*="st-key-row_"] [data-testid="stColumn"]:first-child { min-width: 0 !important; }
[class*="st-key-chat_"] button { font-weight: 400; background: transparent !important; }
[class*="st-key-row_on_"] [class*="st-key-chat_"] button { color: var(--bright); }
[class*="st-key-row_"] [data-testid="stPopover"] > button { border: none !important; background: transparent !important; color: var(--muted); padding: 0 .5rem; }
[class*="st-key-row_"] [data-testid="stPopover"] { opacity: 0; transition: opacity .15s; }
[class*="st-key-row_"]:hover [data-testid="stPopover"], [class*="st-key-row_"]:focus-within [data-testid="stPopover"],
[class*="st-key-row_on_"] [data-testid="stPopover"] { opacity: 1; }
@media (hover: none) { [class*="st-key-row_"] [data-testid="stPopover"] { opacity: 1; } }
[class*="st-key-row_"] [data-testid="stPopover"] button [data-testid="stIconMaterial"],
[class*="st-key-row_"] [data-testid="stPopover"] button svg { display: none; }
[class*="st-key-delc_"] button, [class*="st-key-delc_"] button p { color: var(--red) !important; }
.empty-state { text-align: center; color: var(--muted); padding: 1rem .5rem; font-size: .85rem; }
.skel { height: 2rem; border-radius: 10px; margin: .3rem 0;
        background: linear-gradient(90deg, var(--hover), var(--active), var(--hover)); background-size: 200% 100%;
        animation: shimmer 1.2s infinite linear; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* footer */
[data-testid="stSidebar"] .st-key-open_settings_btn button { padding: .5rem .7rem; }
.profile { display: flex; align-items: center; gap: .7rem; padding: .35rem .5rem; }
.avatar { width: 38px; height: 38px; border-radius: 50%; background: var(--accent); color: var(--accent_text);
          display: grid; place-items: center; font-size: .85rem; font-weight: 700; flex: none; }
.pname { display: flex; flex-direction: column; min-width: 0; line-height: 1.25; }
.pname b { color: var(--bright); font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pname span { color: var(--muted); font-size: .78rem; }

/* ── Messages: user = right bubble, assistant = plain ─── */
[data-testid="stChatMessage"] { background: transparent; padding: var(--gap) 0; gap: 0; }
[data-testid^="stChatMessageAvatar"] { display: none !important; }
[data-testid="stChatMessage"]:has([class*="st-key-umsg_"]) { flex-direction: row-reverse; }
[data-testid="stChatMessage"]:has([class*="st-key-umsg_"]) [data-testid="stChatMessageContent"] {
    flex: 0 1 auto; width: fit-content; max-width: 82%; margin-left: auto; margin-right: -.6rem;
    background: var(--surface); border-radius: 1.25rem; padding: .65rem 1.05rem; }
.chip { display: inline-flex; align-items: center; gap: .4rem; padding: .25rem .6rem; border: 1px solid var(--border);
        border-radius: 999px; font-size: .8rem; color: var(--muted); margin-bottom: .3rem; }

/* action bar under AI answers */
[class*="st-key-actions_"] [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: .25rem; }
[class*="st-key-actions_"] [data-testid="stColumn"] { flex: 0 0 auto !important; width: auto !important; min-width: 0 !important; }
[class*="st-key-actions_"] button { border: none; min-height: 2rem; padding: 0 .45rem; color: var(--muted); }
[class*="st-key-actions_"] button[kind="primary"] { background: var(--hover); color: var(--bright); }
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
    border-radius: 1.6rem; box-shadow: 0 4px 24px rgba(0,0,0,.18); }
[data-testid="stChatInput"] textarea { background: transparent !important; color: var(--text) !important; }
[data-testid="stChatInputSubmitButton"] { background: var(--accent) !important; color: var(--accent_text) !important; border-radius: 50%; }

/* ── Welcome ──────────────────────────────────────────── */
.welcome { text-align: center; margin: 16vh 0 1.5rem; }
.welcome h1 { font-size: 2rem; font-weight: 600; margin-bottom: .3rem; }
.welcome p { color: var(--muted) !important; }

/* ── Atom One refinement ─────────────────────────────── */
.stApp [data-testid="stMain"] { background: var(--bg) !important; }
.st-key-search_wrap [data-baseweb="input"] > div {
    min-height: 42px; border-radius: 10px !important;
}
.st-key-search_wrap input::placeholder { color: var(--muted) !important; opacity: 1; }
.st-key-search_wrap [data-baseweb="input"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}
.st-key-sb_collapse button { border-radius: 9px !important; }
.st-key-history { scrollbar-width: thin; scrollbar-color: var(--border) transparent; }
.st-key-history::-webkit-scrollbar { width: 6px; }
.st-key-history::-webkit-scrollbar-thumb { background: var(--border); border-radius: 8px; }
.st-key-history::-webkit-scrollbar-track { background: transparent; }
.st-key-history [data-testid="stVerticalBlock"] { padding-bottom: .2rem; }
[class*="st-key-row_"] [data-testid="stPopover"] > button {
    min-width: 30px; min-height: 30px; border-radius: 8px !important;
}
[data-testid="stPopoverBody"] button { min-height: 2.25rem; }
[data-testid="stPopoverBody"] button p { white-space: nowrap; }
.st-key-open_settings_btn button { min-height: 2.5rem !important; }
.st-key-sb_bottom { padding-top: .25rem; }
.st-key-sb_bottom hr { margin: .35rem 0 .55rem; }
.profile { min-height: 48px; }
.st-key-new_chat button { letter-spacing: .01em; }
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        width: min(86vw, 300px) !important;
        min-width: min(86vw, 300px) !important;
        max-width: min(86vw, 300px) !important;
    }
    .block-container { padding: 2rem .9rem 6rem; }
    .welcome { margin-top: 12vh; }
    .welcome h1 { font-size: clamp(1.45rem, 5vw, 2rem); }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { scroll-behavior: auto !important; animation-duration: .01ms !important;
        animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
}

"""



def build_css(theme: str, font_size: str, compact: bool, sidebar_open: bool = True) -> str:
    if theme == "Light":
        root = f":root{{{_vars(LIGHT)}}}"
    elif theme == "Dark":
        root = f":root{{{_vars(DARK)}}}"
    else:
        root = f":root{{{_vars(LIGHT)}}} @media (prefers-color-scheme: dark){{:root{{{_vars(DARK)}}}}}"
    fs = {"Small": "0.9rem", "Default": "1rem", "Large": "1.1rem"}.get(font_size, "1rem")
    gap = ".15rem" if compact else ".7rem"
    side = "" if sidebar_open else (
        "section[data-testid='stSidebar']{width:0!important;min-width:0!important;max-width:0!important;"
        "border-right:0!important;overflow:hidden!important;visibility:visible!important}"
    )
    return (
        "<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');"
        + root
        + f":root{{--fs:{fs};--gap:{gap}}}"
        + BASE + ICON_CSS + SEARCH_CSS
        + """
/* ── Sidebar precision overrides for current Streamlit DOM ── */
section[data-testid="stSidebar"],
[data-testid="stSidebar"] {
    background: var(--sidebar) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    background: var(--sidebar) !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: .35rem !important;
}
[data-testid="stSidebar"] .st-key-new_chat button,
[data-testid="stSidebar"] .st-key-open_settings_btn button,
[data-testid="stSidebar"] [class*="st-key-chat_"] button,
[data-testid="stSidebar"] .st-key-sb_collapse button,
[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] > button {
    box-shadow: none !important;
}
[data-testid="stSidebar"] .st-key-new_chat button {
    background: var(--accent) !important;
    color: var(--accent_text) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    justify-content: flex-start !important;
    padding: 0 14px !important;
}
[data-testid="stSidebar"] .st-key-new_chat button p {
    color: var(--accent_text) !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .st-key-open_settings_btn button {
    background: transparent !important;
    color: var(--text) !important;
    border: 0 !important;
    border-radius: 9px !important;
    min-height: 40px !important;
    justify-content: flex-start !important;
    padding: 0 10px !important;
}
[data-testid="stSidebar"] .st-key-open_settings_btn button p {
    color: var(--text) !important;
}
[data-testid="stSidebar"] .st-key-open_settings_btn button:hover {
    background: var(--hover) !important;
    color: var(--bright) !important;
}
[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"],
[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div,
[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .st-key-search_wrap input {
    background: transparent !important;
    color: var(--text) !important;
    min-height: 40px !important;
}
[data-testid="stSidebar"] .st-key-search_wrap input::placeholder {
    color: var(--muted) !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"]:focus-within,
[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}
[data-testid="stSidebar"] .st-key-history {
    overflow-x: hidden !important;
    overflow-y: auto !important;
    max-height: calc(100vh - 330px) !important;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
}
[data-testid="stSidebar"] .st-key-history > div,
[data-testid="stSidebar"] .st-key-history [data-testid="stVerticalBlock"] {
    gap: .12rem !important;
    overflow-x: hidden !important;
}
[data-testid="stSidebar"] [class*="st-key-row_"] {
    background: transparent !important;
    border-radius: 8px !important;
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] [class*="st-key-row_"]:hover,
[data-testid="stSidebar"] [class*="st-key-row_on_"] {
    background: var(--active) !important;
}
[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 0 !important;
    min-width: 0 !important;
}
[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="column"]:first-child,
[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stColumn"]:first-child {
    flex: 1 1 0 !important;
    width: 0 !important;
    min-width: 0 !important;
}
[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="column"]:last-child,
[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stColumn"]:last-child {
    flex: 0 0 34px !important;
    width: 34px !important;
    min-width: 34px !important;
}
[data-testid="stSidebar"] [class*="st-key-chat_"] {
    min-width: 0 !important;
    width: 100% !important;
}
[data-testid="stSidebar"] [class*="st-key-chat_"] button {
    width: 100% !important;
    min-width: 0 !important;
    min-height: 36px !important;
    height: 36px !important;
    padding: 0 9px !important;
    background: transparent !important;
    color: var(--text) !important;
    border: 0 !important;
    border-radius: 8px !important;
    justify-content: flex-start !important;
}
[data-testid="stSidebar"] [class*="st-key-chat_"] button p {
    color: inherit !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    text-align: left !important;
    font-size: .88rem !important;
}
[data-testid="stSidebar"] [class*="st-key-row_on_"] [class*="st-key-chat_"] button {
    color: var(--bright) !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] {
    width: 34px !important;
    opacity: 0 !important;
    transition: opacity .15s ease !important;
}
[data-testid="stSidebar"] [class*="st-key-row_"]:hover [data-testid="stPopover"],
[data-testid="stSidebar"] [class*="st-key-row_"]:focus-within [data-testid="stPopover"],
[data-testid="stSidebar"] [class*="st-key-row_on_"] [data-testid="stPopover"] {
    opacity: 1 !important;
}
[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] > button {
    min-width: 30px !important;
    width: 30px !important;
    min-height: 30px !important;
    padding: 0 !important;
    background: transparent !important;
    border: 0 !important;
    color: var(--muted) !important;
}
[data-testid="stSidebar"] .group-label {
    padding: .55rem .55rem .18rem !important;
    font-size: .78rem !important;
}
[data-testid="stSidebar"] .side-heading {
    padding: .2rem .55rem 0 !important;
}
[data-testid="stSidebar"] .st-key-sb_bottom {
    margin-top: auto !important;
}
[data-testid="stSidebar"] .st-key-sb_bottom [data-testid="stVerticalBlock"] {
    gap: .25rem !important;
}
[data-testid="stSidebar"] .st-key-sb_collapse button {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    min-height: 36px !important;
    min-width: 36px !important;
}
[data-testid="stSidebar"] .brand .logo {
    background: transparent !important;
    color: var(--bright) !important;
}
[data-testid="stSidebar"] .st-key-search_wrap,
[data-testid="stSidebar"] .st-key-history {
    width: 100% !important;
    min-width: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    min-width: 0 !important;
}
@media (hover: none) {
    [data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] {
        opacity: 1 !important;
    }
}
@media (max-width: 768px) {
    [data-testid="stSidebar"] .st-key-history {
        max-height: calc(100vh - 310px) !important;
    }
}"""
        + '\n/* ── Sidebar: fixed header/footer; only chat history scrolls ── */\nsection[data-testid="stSidebar"] {\n    position: relative !important;\n    height: 100vh !important;\n    max-height: 100vh !important;\n    overflow: hidden !important;\n}\nsection[data-testid="stSidebar"] > div,\nsection[data-testid="stSidebar"] [data-testid="stSidebarContent"],\nsection[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {\n    height: 100vh !important;\n    max-height: 100vh !important;\n    min-height: 0 !important;\n    overflow: hidden !important;\n    padding-top: 0 !important;\n    padding-bottom: 0 !important;\n    scrollbar-width: none !important;\n}\nsection[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlock"] {\n    height: 100vh !important;\n    max-height: 100vh !important;\n    min-height: 0 !important;\n    overflow: hidden !important;\n    padding: 0 !important;\n    gap: .2rem !important;\n    display: flex !important;\n    flex-direction: column !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_top {\n    flex: 0 0 auto !important;\n    width: 100% !important;\n    padding: 0 .55rem !important;\n    margin: 0 !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_top [data-testid="stVerticalBlock"] {\n    gap: .32rem !important;\n}\nsection[data-testid="stSidebar"] .brand { margin: 0 !important; padding: 0 !important; }\nsection[data-testid="stSidebar"] .st-key-search_wrap { margin: 0 !important; }\nsection[data-testid="stSidebar"] .st-key-history {\n    display: block !important;\n    width: calc(100% - 12px) !important;\n    height: calc(100vh - 350px) !important;\n    max-height: calc(100vh - 350px) !important;\n    min-height: 100px !important;\n    margin: 0 6px 112px !important;\n    padding: 0 4px 8px 0 !important;\n    overflow-y: auto !important;\n    overflow-x: hidden !important;\n    overscroll-behavior: contain !important;\n    scrollbar-width: thin !important;\n    scrollbar-color: var(--border) transparent !important;\n}\nsection[data-testid="stSidebar"] .st-key-history::-webkit-scrollbar {\n    display: block !important; width: 6px !important;\n}\nsection[data-testid="stSidebar"] .st-key-history::-webkit-scrollbar-thumb {\n    background: var(--border) !important; border-radius: 8px !important;\n}\nsection[data-testid="stSidebar"] .st-key-history > div,\nsection[data-testid="stSidebar"] .st-key-history [data-testid="stVerticalBlock"] {\n    overflow: visible !important;\n    min-height: min-content !important;\n    gap: .16rem !important;\n}\n/* Pin Settings and account profile to the sidebar bottom. */\nsection[data-testid="stSidebar"] .st-key-sb_bottom {\n    position: absolute !important;\n    left: 0 !important; right: 0 !important; bottom: 0 !important;\n    z-index: 100 !important;\n    width: 100% !important;\n    margin: 0 !important;\n    padding: .35rem .7rem .65rem !important;\n    background: var(--sidebar) !important;\n    border-top: 1px solid var(--border) !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_bottom [data-testid="stVerticalBlock"] {\n    gap: .18rem !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_bottom hr { display: none !important; }\nsection[data-testid="stSidebar"] .st-key-open_settings_btn button {\n    min-height: 38px !important; padding: .3rem .65rem !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_bottom .profile {\n    min-height: 48px !important; padding: .2rem .5rem !important;\n}\n@media (max-height: 760px) {\n    section[data-testid="stSidebar"] .st-key-history {\n        height: calc(100vh - 300px) !important;\n        max-height: calc(100vh - 300px) !important;\n        margin-bottom: 105px !important;\n    }\n}\n/* Inset chat rows slightly; reserve a narrow trailing column for the menu. */\nsection[data-testid="stSidebar"] [class*="st-key-row_"] {\n    width: calc(100% - 8px) !important;\n    max-width: 232px !important;\n    min-height: 38px !important;\n    margin: 1px auto !important;\n    padding: 0 2px !important;\n    border-radius: 9px !important;\n    overflow: visible !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stHorizontalBlock"] {\n    width: 100% !important; min-height: 36px !important;\n    flex-wrap: nowrap !important; align-items: center !important; gap: 0 !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stColumn"]:first-child {\n    flex: 1 1 0% !important; width: 0 !important; min-width: 0 !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stColumn"]:last-child {\n    flex: 0 0 32px !important; width: 32px !important; min-width: 32px !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] { width: 100% !important; min-width: 0 !important; }\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button {\n    width: 100% !important; min-width: 0 !important; height: 36px !important; min-height: 36px !important;\n    padding: 0 7px !important; border: 0 !important; border-radius: 8px !important;\n    background: transparent !important; box-shadow: none !important; justify-content: flex-start !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button p {\n    overflow: hidden !important; white-space: nowrap !important; text-overflow: ellipsis !important;\n    text-align: left !important;\n}\n/* Three-dot popover trigger: visible on hover/focus; no white square. */\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] {\n    display: block !important; flex: 0 0 32px !important; width: 32px !important; min-width: 32px !important;\n    opacity: 0 !important; visibility: hidden !important; pointer-events: none !important;\n    transition: opacity .15s ease, visibility .15s ease !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"]:hover [data-testid="stPopover"],\nsection[data-testid="stSidebar"] [class*="st-key-row_"]:focus-within [data-testid="stPopover"],\nsection[data-testid="stSidebar"] [class*="st-key-row_on_"] [data-testid="stPopover"] {\n    opacity: 1 !important; visibility: visible !important; pointer-events: auto !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] button {\n    display: flex !important; align-items: center !important; justify-content: center !important;\n    width: 30px !important; min-width: 30px !important; height: 30px !important; min-height: 30px !important;\n    padding: 0 !important; margin: 0 !important; color: var(--text) !important;\n    background: transparent !important; border: 0 !important; border-radius: 7px !important;\n    box-shadow: none !important; font-size: 20px !important; line-height: 1 !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] button:hover {\n    color: var(--bright) !important; background: var(--hover) !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] button svg,\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] button [data-testid="stIconMaterial"] {\n    display: inline-flex !important; visibility: visible !important; color: var(--text) !important;\n    fill: currentColor !important; width: 18px !important; height: 18px !important;\n}\n'
        + '\n/* ── Sidebar final structure: one scroll region + pinned account footer ── */\nsection[data-testid="stSidebar"] {\n    height: 100vh !important;\n    max-height: 100vh !important;\n    overflow: hidden !important;\n}\nsection[data-testid="stSidebar"] > div,\nsection[data-testid="stSidebar"] [data-testid="stSidebarContent"],\nsection[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {\n    height: 100vh !important;\n    max-height: 100vh !important;\n    min-height: 0 !important;\n    overflow: hidden !important;\n    padding: 0 !important;\n    scrollbar-width: none !important;\n}\nsection[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlock"] {\n    display: flex !important;\n    flex-direction: column !important;\n    height: 100vh !important;\n    max-height: 100vh !important;\n    min-height: 0 !important;\n    overflow: hidden !important;\n    padding: 0 !important;\n    gap: 0 !important;\n}\n/* Header + New Chat + Search + Your Chats + history share this single scrollbar. */\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll {\n    flex: 1 1 0% !important;\n    min-height: 0 !important;\n    height: auto !important;\n    max-height: none !important;\n    width: 100% !important;\n    overflow-y: auto !important;\n    overflow-x: hidden !important;\n    overscroll-behavior: contain !important;\n    scrollbar-width: thin !important;\n    scrollbar-color: var(--border) transparent !important;\n    padding: 0 .45rem .45rem !important;\n    margin: 0 !important;\n}\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll::-webkit-scrollbar {\n    width: 6px !important;\n}\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll::-webkit-scrollbar-thumb {\n    background: var(--border) !important;\n    border-radius: 8px !important;\n}\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll > div,\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll [data-testid="stVerticalBlock"] {\n    overflow: visible !important;\n    min-height: min-content !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_top {\n    width: 100% !important;\n    margin: 0 !important;\n    padding: 0 !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_top [data-testid="stVerticalBlock"] {\n    gap: .25rem !important;\n}\nsection[data-testid="stSidebar"] .brand {\n    margin: 0 !important;\n    padding: 0 !important;\n}\nsection[data-testid="stSidebar"] .st-key-history {\n    width: 100% !important;\n    height: auto !important;\n    max-height: none !important;\n    min-height: 0 !important;\n    overflow: visible !important;\n    margin: 0 !important;\n    padding: 0 0 .4rem !important;\n}\n/* Settings + profile stay outside the scroll area and remain pinned to bottom. */\nsection[data-testid="stSidebar"] .st-key-sb_bottom {\n    position: relative !important;\n    flex: 0 0 auto !important;\n    width: 100% !important;\n    left: auto !important;\n    right: auto !important;\n    bottom: auto !important;\n    z-index: 10 !important;\n    margin: 0 !important;\n    padding: .4rem .75rem .9rem !important;\n    background: var(--sidebar) !important;\n    border-top: 1px solid var(--border) !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_bottom [data-testid="stVerticalBlock"] {\n    gap: .12rem !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_bottom .profile {\n    min-height: 48px !important;\n    padding: .2rem .5rem .55rem !important;\n    margin-bottom: .15rem !important;\n}\n/* Restore chat-row width to the full inner sidebar width. */\nsection[data-testid="stSidebar"] [class*="st-key-row_"] {\n    width: 100% !important;\n    max-width: none !important;\n    min-height: 34px !important;\n    height: auto !important;\n    margin: 0 !important;\n    padding: 0 !important;\n    border-radius: 8px !important;\n    overflow: visible !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stHorizontalBlock"] {\n    width: 100% !important;\n    min-height: 33px !important;\n    height: auto !important;\n    flex-wrap: nowrap !important;\n    align-items: center !important;\n    gap: 0 !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stColumn"]:first-child {\n    flex: 1 1 0% !important;\n    width: 0 !important;\n    min-width: 0 !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stColumn"]:last-child {\n    flex: 0 0 32px !important;\n    width: 32px !important;\n    min-width: 32px !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button {\n    width: 100% !important;\n    min-width: 0 !important;\n    min-height: 32px !important;\n    height: 32px !important;\n    padding: 0 7px !important;\n    border: 0 !important;\n    border-radius: 7px !important;\n    background: transparent !important;\n    box-shadow: none !important;\n    justify-content: flex-start !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button p {\n    overflow: hidden !important;\n    white-space: nowrap !important;\n    text-overflow: ellipsis !important;\n    text-align: left !important;\n}\n/* Reveal three-dot action menu on row hover or keyboard focus. */\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] {\n    display: block !important;\n    flex: 0 0 32px !important;\n    width: 32px !important;\n    min-width: 32px !important;\n    opacity: 0 !important;\n    visibility: hidden !important;\n    pointer-events: none !important;\n    transition: opacity .14s ease, visibility .14s ease !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"]:hover [data-testid="stPopover"],\nsection[data-testid="stSidebar"] [class*="st-key-row_"]:focus-within [data-testid="stPopover"],\nsection[data-testid="stSidebar"] [class*="st-key-row_on_"] [data-testid="stPopover"] {\n    opacity: 1 !important;\n    visibility: visible !important;\n    pointer-events: auto !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] > button {\n    display: flex !important;\n    align-items: center !important;\n    justify-content: center !important;\n    width: 30px !important;\n    min-width: 30px !important;\n    height: 30px !important;\n    min-height: 30px !important;\n    padding: 0 !important;\n    margin: 0 !important;\n    color: var(--text) !important;\n    background: transparent !important;\n    border: 0 !important;\n    border-radius: 7px !important;\n    box-shadow: none !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stPopover"] > button:hover {\n    color: var(--bright) !important;\n    background: var(--hover) !important;\n}\n'
        + '\n/* ── Final top-gap + single-scrollbar correction ── */\nsection[data-testid="stSidebar"] {\n    position: relative !important;\n    height: 100vh !important;\n    max-height: 100vh !important;\n    overflow: hidden !important;\n}\nsection[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {\n    display: none !important;\n    height: 0 !important;\n    min-height: 0 !important;\n    padding: 0 !important;\n    margin: 0 !important;\n    overflow: hidden !important;\n}\nsection[data-testid="stSidebar"] > div,\nsection[data-testid="stSidebar"] [data-testid="stSidebarContent"] {\n    height: 100vh !important;\n    max-height: 100vh !important;\n    min-height: 0 !important;\n    padding: 0 !important;\n    margin: 0 !important;\n    overflow: hidden !important;\n    scrollbar-width: none !important;\n}\nsection[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {\n    position: relative !important;\n    height: 100vh !important;\n    max-height: 100vh !important;\n    min-height: 0 !important;\n    padding: 0 !important;\n    margin: 0 !important;\n    overflow: hidden !important;\n    scrollbar-width: none !important;\n}\nsection[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > [data-testid="stVerticalBlock"] {\n    position: relative !important;\n    height: 100vh !important;\n    max-height: 100vh !important;\n    min-height: 0 !important;\n    padding: 0 !important;\n    margin: 0 !important;\n    gap: 0 !important;\n    overflow: hidden !important;\n}\n/* Brand, New Chat, Search and history scroll together from the very top. */\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll {\n    position: absolute !important;\n    top: 0 !important;\n    left: 0 !important;\n    right: 0 !important;\n    bottom: 112px !important;\n    width: 100% !important;\n    height: auto !important;\n    max-height: none !important;\n    min-height: 0 !important;\n    margin: 0 !important;\n    padding: 0 .45rem .6rem !important;\n    overflow-y: scroll !important;\n    overflow-x: hidden !important;\n    overscroll-behavior: contain !important;\n    scrollbar-width: thin !important;\n    scrollbar-color: var(--border) transparent !important;\n}\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll::-webkit-scrollbar {\n    display: block !important;\n    width: 7px !important;\n}\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll::-webkit-scrollbar-track {\n    background: transparent !important;\n}\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll::-webkit-scrollbar-thumb {\n    background: var(--border) !important;\n    border-radius: 10px !important;\n    border: 1px solid transparent !important;\n    background-clip: padding-box !important;\n}\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll > div,\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll [data-testid="stVerticalBlock"] {\n    min-height: min-content !important;\n    overflow: visible !important;\n}\n/* Remove all top margin/padding from the first nested block. */\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll > div,\nsection[data-testid="stSidebar"] .st-key-sidebar_scroll [data-testid="stElementContainer"]:first-child,\nsection[data-testid="stSidebar"] .st-key-sb_top,\nsection[data-testid="stSidebar"] .st-key-sb_top > div {\n    margin-top: 0 !important;\n    padding-top: 0 !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_top [data-testid="stVerticalBlock"] {\n    gap: .25rem !important;\n}\nsection[data-testid="stSidebar"] .brand {\n    margin-top: 0 !important;\n    padding-top: 0 !important;\n}\n/* History is part of sidebar_scroll, not a second nested scroll area. */\nsection[data-testid="stSidebar"] .st-key-history {\n    height: auto !important;\n    max-height: none !important;\n    min-height: 0 !important;\n    margin: 0 !important;\n    padding: 0 0 .5rem !important;\n    overflow: visible !important;\n}\n/* Footer remains pinned and gets a little breathing room below the profile. */\nsection[data-testid="stSidebar"] .st-key-sb_bottom {\n    position: absolute !important;\n    left: 0 !important;\n    right: 0 !important;\n    bottom: 0 !important;\n    width: 100% !important;\n    height: 112px !important;\n    min-height: 112px !important;\n    margin: 0 !important;\n    padding: .35rem .75rem .85rem !important;\n    z-index: 100 !important;\n    background: var(--sidebar) !important;\n    border-top: 1px solid var(--border) !important;\n}\nsection[data-testid="stSidebar"] .st-key-sb_bottom .profile {\n    padding: .2rem .5rem .7rem !important;\n    margin-bottom: .1rem !important;\n}\n'
        + '\n/* ── Final chat alignment and date-group spacing ── */\n/* Keep every conversation title flush-left within its full-width row. */\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [data-testid="stColumn"]:first-child,\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] {\n    text-align: left !important;\n    justify-content: flex-start !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button {\n    display: flex !important;\n    align-items: center !important;\n    justify-content: flex-start !important;\n    text-align: left !important;\n    padding-left: 7px !important;\n    padding-right: 7px !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button [data-testid="stMarkdownContainer"],\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button p {\n    width: 100% !important;\n    text-align: left !important;\n    margin-left: 0 !important;\n}\n/* A small, consistent gap separates Today / Yesterday / Previous 7 Days\n   labels from the first chat in each date group. */\nsection[data-testid="stSidebar"] .group-label {\n    display: block !important;\n    width: 100% !important;\n    text-align: left !important;\n    padding: .72rem .6rem .42rem !important;\n    margin: 0 0 .12rem !important;\n    line-height: 1.25 !important;\n}\nsection[data-testid="stSidebar"] .st-key-history [data-testid="stVerticalBlock"] {\n    gap: .12rem !important;\n}\n'
        + '\n/* ── Chat title alignment: icon followed by left-aligned title ── */\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button {\n    display: flex !important;\n    flex-direction: row !important;\n    align-items: center !important;\n    justify-content: flex-start !important;\n    text-align: left !important;\n    gap: .55rem !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button > div,\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button [data-testid="stMarkdownContainer"] {\n    display: block !important;\n    flex: 1 1 0% !important;\n    width: 0 !important;\n    min-width: 0 !important;\n    max-width: 100% !important;\n    margin: 0 !important;\n    padding: 0 !important;\n    text-align: left !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-chat_"] button p {\n    display: block !important;\n    width: 100% !important;\n    margin: 0 !important;\n    padding: 0 !important;\n    text-align: left !important;\n}\n/* Slightly more breathing room between date headings and the first chat row. */\nsection[data-testid="stSidebar"] .group-label {\n    display: block !important;\n    text-align: left !important;\n    padding: .72rem .6rem .52rem !important;\n    margin: 0 0 .22rem !important;\n    line-height: 1.25 !important;\n}\n'
        + '\n/* ── Restore visible chat titles (keep icon + title in one row) ── */\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [class*="st-key-chat_"] {\n    width: 100% !important;\n    min-width: 0 !important;\n    overflow: hidden !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [class*="st-key-chat_"] button {\n    display: flex !important;\n    flex-direction: row !important;\n    align-items: center !important;\n    justify-content: flex-start !important;\n    width: 100% !important;\n    min-width: 0 !important;\n    overflow: hidden !important;\n    color: var(--text) !important;\n    text-align: left !important;\n    white-space: nowrap !important;\n    gap: .55rem !important;\n}\n/* Streamlit renders button labels inside this markdown wrapper.\n   Do not give it width:0: that collapsed the chat title in the previous patch. */\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [class*="st-key-chat_"] button [data-testid="stMarkdownContainer"] {\n    display: block !important;\n    flex: 1 1 auto !important;\n    width: auto !important;\n    min-width: 0 !important;\n    max-width: calc(100% - 24px) !important;\n    overflow: hidden !important;\n    visibility: visible !important;\n    opacity: 1 !important;\n    color: inherit !important;\n    text-align: left !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [class*="st-key-chat_"] button p {\n    display: block !important;\n    width: 100% !important;\n    min-width: 0 !important;\n    margin: 0 !important;\n    padding: 0 !important;\n    overflow: hidden !important;\n    color: inherit !important;\n    text-align: left !important;\n    text-overflow: ellipsis !important;\n    white-space: nowrap !important;\n}\n/* Date headings get a clear but compact gap before their first conversation. */\nsection[data-testid="stSidebar"] .group-label {\n    display: block !important;\n    width: 100% !important;\n    margin: 0 0 .38rem !important;\n    padding: .78rem .6rem .42rem !important;\n    line-height: 1.3 !important;\n    text-align: left !important;\n}\n'
        + '\n/* ── Final fix: prevent chat label wrapper from collapsing ── */\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [class*="st-key-chat_"] button > div {\n    display: block !important;\n    flex: 1 1 auto !important;\n    width: auto !important;\n    min-width: 0 !important;\n    max-width: calc(100% - 24px) !important;\n    overflow: hidden !important;\n    visibility: visible !important;\n    opacity: 1 !important;\n    text-align: left !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [class*="st-key-chat_"] button > div > div,\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [class*="st-key-chat_"] button [data-testid="stMarkdownContainer"] {\n    display: block !important;\n    flex: 1 1 auto !important;\n    width: auto !important;\n    min-width: 0 !important;\n    max-width: 100% !important;\n    overflow: hidden !important;\n    visibility: visible !important;\n    opacity: 1 !important;\n    text-align: left !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-row_"] [class*="st-key-chat_"] button p {\n    display: block !important;\n    width: 100% !important;\n    min-width: 0 !important;\n    margin: 0 !important;\n    overflow: hidden !important;\n    color: var(--text) !important;\n    text-align: left !important;\n    text-overflow: ellipsis !important;\n    white-space: nowrap !important;\n}\n/* Add a slightly larger gap between each date heading and its first chat. */\nsection[data-testid="stSidebar"] .group-label {\n    display: block !important;\n    text-align: left !important;\n    padding: .82rem .6rem .58rem !important;\n    margin: 0 0 .32rem !important;\n    line-height: 1.3 !important;\n}\n'
        + '\n/* ── Search + composer: soft Atom dark input surfaces ── */\n:root {\n    --input-surface-soft: #3a3f46;\n    --input-text-soft: #edf0f4;\n    --input-placeholder-soft: #c2c8d0;\n}\n/* Sidebar search field */\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"] {\n    background: var(--input-surface-soft) !important;\n    border: 1px solid #515862 !important;\n    border-radius: 10px !important;\n    box-shadow: none !important;\n}\nsection[data-testid="stSidebar"] .st-key-search_wrap input {\n    background: transparent !important;\n    color: var(--input-text-soft) !important;\n    caret-color: var(--input-text-soft) !important;\n}\nsection[data-testid="stSidebar"] .st-key-search_wrap input::placeholder {\n    color: var(--input-placeholder-soft) !important;\n    opacity: 1 !important;\n}\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"]:focus-within,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div:focus-within {\n    border-color: #626b77 !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\n/* Main message composer: match search field\'s light-grey dark surface. */\n[data-testid="stChatInput"] {\n    background: var(--input-surface-soft) !important;\n    border: 1px solid #515862 !important;\n    border-radius: 1.6rem !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\n[data-testid="stChatInput"]:focus,\n[data-testid="stChatInput"]:focus-within {\n    background: var(--input-surface-soft) !important;\n    border-color: #626b77 !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\n[data-testid="stChatInput"] textarea,\n[data-testid="stChatInput"] textarea:focus,\n[data-testid="stChatInput"] textarea:focus-visible {\n    background: transparent !important;\n    color: var(--input-text-soft) !important;\n    caret-color: var(--input-text-soft) !important;\n    outline: none !important;\n    box-shadow: none !important;\n    border: 0 !important;\n}\n[data-testid="stChatInput"] textarea::placeholder {\n    color: var(--input-placeholder-soft) !important;\n    opacity: 1 !important;\n}\n/* Remove Streamlit/browser tab-focus rectangle from the composer only. */\n[data-testid="stChatInput"] :focus,\n[data-testid="stChatInput"] :focus-visible {\n    outline: none !important;\n    box-shadow: none !important;\n}\n'
        + '\n/* ── Search + main prompt: consistent Atom One Dark grey inputs ── */\n:root {\n    --atom-input-bg: #3a3f46;\n    --atom-input-border: #515862;\n    --atom-input-text: #f0f2f5;\n    --atom-input-placeholder: #c5cbd3;\n}\n/* Search chat text_input: target the Streamlit widget and all BaseWeb layers. */\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="stTextInput"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"] > div {\n    background: var(--atom-input-bg) !important;\n    background-color: var(--atom-input-bg) !important;\n    border-color: var(--atom-input-border) !important;\n    box-shadow: none !important;\n}\nsection[data-testid="stSidebar"] .st-key-search_wrap input,\nsection[data-testid="stSidebar"] .st-key-search_wrap input:focus {\n    background: transparent !important;\n    background-color: transparent !important;\n    color: var(--atom-input-text) !important;\n    -webkit-text-fill-color: var(--atom-input-text) !important;\n    caret-color: var(--atom-input-text) !important;\n    outline: none !important;\n    box-shadow: none !important;\n}\nsection[data-testid="stSidebar"] .st-key-search_wrap input::placeholder {\n    color: var(--atom-input-placeholder) !important;\n    -webkit-text-fill-color: var(--atom-input-placeholder) !important;\n    opacity: 1 !important;\n}\n/* Hide Streamlit\'s keyboard/submit hint ("Press Enter to apply") for search only. */\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="InputInstructions"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="InputInstructions"] *,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="stInputInstructions"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="stInputInstructions"] *,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] [role="tooltip"] {\n    display: none !important;\n    visibility: hidden !important;\n}\n/* Do not show an accent/red focus ring when typing in search. */\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"]:focus-within,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div:focus-within,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="stTextInput"]:focus-within {\n    border-color: var(--atom-input-border) !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\n/* Main chat composer: same grey background and readable near-white text. */\n[data-testid="stChatInput"],\n[data-testid="stChatInput"] > div,\n[data-testid="stChatInput"] form,\n[data-testid="stChatInput"] [data-baseweb="textarea"],\n[data-testid="stChatInput"] [data-baseweb="base-input"],\n[data-testid="stChatInput"] textarea {\n    background: var(--atom-input-bg) !important;\n    background-color: var(--atom-input-bg) !important;\n    border-color: var(--atom-input-border) !important;\n    box-shadow: none !important;\n}\n[data-testid="stChatInput"] textarea,\n[data-testid="stChatInput"] textarea:focus,\n[data-testid="stChatInput"] textarea:focus-visible {\n    color: var(--atom-input-text) !important;\n    -webkit-text-fill-color: var(--atom-input-text) !important;\n    caret-color: var(--atom-input-text) !important;\n    outline: none !important;\n}\n[data-testid="stChatInput"] textarea::placeholder {\n    color: var(--atom-input-placeholder) !important;\n    -webkit-text-fill-color: var(--atom-input-placeholder) !important;\n    opacity: 1 !important;\n}\n[data-testid="stChatInput"]:focus,\n[data-testid="stChatInput"]:focus-within,\n[data-testid="stChatInput"] form:focus-within,\n[data-testid="stChatInput"] [data-baseweb="textarea"]:focus-within {\n    border-color: var(--atom-input-border) !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\n[data-testid="stChatInput"] :focus,\n[data-testid="stChatInput"] :focus-visible {\n    outline: none !important;\n    box-shadow: none !important;\n}\n'
        + '\n/* ── Match Search Chats exactly to the main composer surface ── */\n:root {\n    --atom-input-bg: #3a3f46;\n    --atom-input-border: #515862;\n    --atom-input-text: #f0f2f5;\n    --atom-input-placeholder: #c5cbd3;\n}\n/* Apply grey directly to the input as well as BaseWeb wrappers.\n   This avoids the white default input showing through on some Streamlit versions. */\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] [data-testid="stTextInput"],\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] [data-baseweb="input"],\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] [data-baseweb="base-input"],\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] [data-baseweb="input"] > div,\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] input {\n    background: var(--atom-input-bg) !important;\n    background-color: var(--atom-input-bg) !important;\n    border-color: var(--atom-input-border) !important;\n    box-shadow: none !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] input,\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] input:focus {\n    color: var(--atom-input-text) !important;\n    -webkit-text-fill-color: var(--atom-input-text) !important;\n    caret-color: var(--atom-input-text) !important;\n    outline: none !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] input::placeholder {\n    color: var(--atom-input-placeholder) !important;\n    -webkit-text-fill-color: var(--atom-input-placeholder) !important;\n    opacity: 1 !important;\n}\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] [data-baseweb="input"]:focus-within,\nsection[data-testid="stSidebar"] [class*="st-key-search_wrap"] [data-testid="stTextInput"]:focus-within {\n    border-color: var(--atom-input-border) !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\n/* Slightly rounder composer corners while retaining the existing proportions. */\n[data-testid="stChatInput"],\n[data-testid="stChatInput"] > div,\n[data-testid="stChatInput"] form {\n    border-radius: 2rem !important;\n}\n'
        + '\n/* ── Search focus state: never switch to white ── */\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"] > div,\nsection[data-testid="stSidebar"] .st-key-search_wrap input,\nsection[data-testid="stSidebar"] .st-key-search_wrap input:focus,\nsection[data-testid="stSidebar"] .st-key-search_wrap input:active {\n    background: #3a3f46 !important;\n    background-color: #3a3f46 !important;\n    color: #f0f2f5 !important;\n    -webkit-text-fill-color: #f0f2f5 !important;\n    border-color: #515862 !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\nsection[data-testid="stSidebar"] .st-key-search_wrap input::placeholder {\n    color: #c5cbd3 !important;\n    -webkit-text-fill-color: #c5cbd3 !important;\n    opacity: 1 !important;\n}\n/* Make the add/attachment plus icon in the composer white. */\n[data-testid="stChatInput"] button,\n[data-testid="stChatInput"] button svg,\n[data-testid="stChatInput"] button [data-testid="stIconMaterial"],\n[data-testid="stChatInput"] [data-testid*="Attach"] button,\n[data-testid="stChatInput"] [data-testid*="FileUploader"] button {\n    color: #f0f2f5 !important;\n}\n[data-testid="stChatInput"] button svg {\n    stroke: #f0f2f5 !important;\n    fill: none !important;\n}\n[data-testid="stChatInput"] button:hover {\n    color: #ffffff !important;\n}\n[data-testid="stChatInput"] button:hover svg {\n    stroke: #ffffff !important;\n}\n/* Keep send arrow styling unchanged. */\n[data-testid="stChatInputSubmitButton"],\n[data-testid="stChatInputSubmitButton"] svg {\n    color: var(--accent_text) !important;\n    stroke: var(--accent_text) !important;\n}\n'
        + '\n/* ── Search border: slightly lighter, including keyboard/mouse focus ── */\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="stTextInput"] {\n    border: 1px solid #788391 !important;\n    border-color: #788391 !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"]:focus-within,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div:focus-within,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="stTextInput"]:focus-within {\n    border-color: #788391 !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\n/* ── Composer add / upload controls: white glyphs, no square button chrome ── */\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]),\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):hover,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):active,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):focus,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):focus-visible {\n    background: transparent !important;\n    background-color: transparent !important;\n    border: 0 !important;\n    border-color: transparent !important;\n    outline: none !important;\n    box-shadow: none !important;\n    border-radius: 50% !important;\n    color: #ffffff !important;\n    -webkit-tap-highlight-color: transparent !important;\n}\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) svg,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) [data-testid="stIconMaterial"],\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) span {\n    color: #ffffff !important;\n    fill: none !important;\n    stroke: #ffffff !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\n/* Some Streamlit releases wrap the upload trigger in its own focusable element. */\n[data-testid="stChatInput"] [data-testid*="FileUploader"],\n[data-testid="stChatInput"] [data-testid*="FileUploader"] *,\n[data-testid="stChatInput"] [data-testid*="Attach"],\n[data-testid="stChatInput"] [data-testid*="Attach"] * {\n    outline: none !important;\n    box-shadow: none !important;\n}\n[data-testid="stChatInput"] [data-testid*="FileUploader"] button,\n[data-testid="stChatInput"] [data-testid*="Attach"] button {\n    background: transparent !important;\n    border: 0 !important;\n    border-color: transparent !important;\n    color: #ffffff !important;\n}\n'
        + '\n/* ── Native chat composer attachment controls: plain icons, no focus boxes ── */\n/* Keep Streamlit\'s actual add/attachment and upload controls; only remove their\n   decorative square button chrome and focus/tap highlights. */\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]),\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):hover,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):active,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):focus,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):focus-visible,\n[data-testid="stChatInput"] button[aria-label*="attach" i],\n[data-testid="stChatInput"] button[aria-label*="upload" i],\n[data-testid="stChatInput"] button[aria-label*="file" i] {\n    appearance: none !important;\n    -webkit-appearance: none !important;\n    background: transparent !important;\n    background-color: transparent !important;\n    border: none !important;\n    outline: 0 !important;\n    box-shadow: none !important;\n    filter: none !important;\n    text-decoration: none !important;\n    -webkit-tap-highlight-color: transparent !important;\n}\n\n/* Remove outlines/shadows applied to the icon or internal wrapper itself. */\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) *,\n[data-testid="stChatInput"] button[aria-label*="attach" i] *,\n[data-testid="stChatInput"] button[aria-label*="upload" i] *,\n[data-testid="stChatInput"] button[aria-label*="file" i] {\n    outline: 0 !important;\n    box-shadow: none !important;\n    filter: none !important;\n    text-shadow: none !important;\n}\n\n/* Retain the normal plus/upload glyphs in white; do not replace or hide them. */\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) svg,\n[data-testid="stChatInput"] button[aria-label*="attach" i] svg,\n[data-testid="stChatInput"] button[aria-label*="upload" i] svg,\n[data-testid="stChatInput"] button[aria-label*="file" i] svg {\n    color: #ffffff !important;\n    stroke: currentColor !important;\n    fill: none !important;\n    background: transparent !important;\n    border: 0 !important;\n    outline: 0 !important;\n    box-shadow: none !important;\n}\n\n/* Also neutralize focus rings on Streamlit\'s file-upload wrappers. */\n[data-testid="stChatInput"] [data-testid*="FileUploader"],\n[data-testid="stChatInput"] [data-testid*="FileUploader"] *,\n[data-testid="stChatInput"] [data-testid*="Attach"],\n[data-testid="stChatInput"] [data-testid*="Attach"] *,\n[data-testid="stChatInput"] [data-testid*="Upload"],\n[data-testid="stChatInput"] [data-testid*="Upload"] * {\n    outline: 0 !important;\n    box-shadow: none !important;\n    filter: none !important;\n}\n\n/* The blue send control is intentionally untouched. */\n'
        + '\n/* ── Composer add / upload controls: circular hit area, white icon, no fill ── */\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]),\n[data-testid="stChatInput"] button[aria-label*="attach" i],\n[data-testid="stChatInput"] button[aria-label*="upload" i],\n[data-testid="stChatInput"] button[aria-label*="file" i],\n[data-testid="stChatInput"] [data-testid*="FileUploader"] button,\n[data-testid="stChatInput"] [data-testid*="Attach"] button,\n[data-testid="stChatInput"] [data-testid*="Upload"] button {\n    appearance: none !important;\n    -webkit-appearance: none !important;\n    width: 34px !important;\n    min-width: 34px !important;\n    height: 34px !important;\n    min-height: 34px !important;\n    padding: 0 !important;\n    display: inline-flex !important;\n    align-items: center !important;\n    justify-content: center !important;\n    border-radius: 50% !important;\n    background: transparent !important;\n    background-color: transparent !important;\n    border: 0 !important;\n    outline: 0 !important;\n    box-shadow: none !important;\n    color: #ffffff !important;\n    -webkit-tap-highlight-color: transparent !important;\n}\n\n/* Keep the native plus/upload glyph, but render it white without a square frame. */\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) svg,\n[data-testid="stChatInput"] button[aria-label*="attach" i] svg,\n[data-testid="stChatInput"] button[aria-label*="upload" i] svg,\n[data-testid="stChatInput"] button[aria-label*="file" i] svg,\n[data-testid="stChatInput"] [data-testid*="FileUploader"] button svg,\n[data-testid="stChatInput"] [data-testid*="Attach"] button svg,\n[data-testid="stChatInput"] [data-testid*="Upload"] button svg {\n    width: 20px !important;\n    height: 20px !important;\n    color: #ffffff !important;\n    stroke: #ffffff !important;\n    fill: none !important;\n    background: transparent !important;\n    border: 0 !important;\n    outline: 0 !important;\n    box-shadow: none !important;\n}\n\n/* Neutralize browser/Streamlit focus and hover decoration on attachment controls. */\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):hover,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):active,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):focus,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):focus-visible,\n[data-testid="stChatInput"] [data-testid*="FileUploader"],\n[data-testid="stChatInput"] [data-testid*="FileUploader"] *,\n[data-testid="stChatInput"] [data-testid*="Attach"],\n[data-testid="stChatInput"] [data-testid*="Attach"] *,\n[data-testid="stChatInput"] [data-testid*="Upload"],\n[data-testid="stChatInput"] [data-testid*="Upload"] * {\n    background-color: transparent !important;\n    border-color: transparent !important;\n    outline: 0 !important;\n    box-shadow: none !important;\n    filter: none !important;\n}\n\n/* Preserve the blue send button unchanged. */\n'
        + '\n/* ── Clean native composer icons: plain plus and arrow, no square glyphs ── */\n\n/* Attachment/add button: retain Streamlit\'s real button behavior, replace only\n   its square-plus artwork with a plain white plus sign. */\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) {\n    position: relative !important;\n    width: 34px !important;\n    min-width: 34px !important;\n    height: 34px !important;\n    min-height: 34px !important;\n    padding: 0 !important;\n    border: 0 !important;\n    border-radius: 50% !important;\n    background: transparent !important;\n    box-shadow: none !important;\n    outline: none !important;\n    color: #ffffff !important;\n}\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) svg,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) [data-testid="stIconMaterial"],\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]) span {\n    display: none !important;\n}\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"])::after {\n    content: "+" !important;\n    display: block !important;\n    color: #ffffff !important;\n    font-family: Arial, sans-serif !important;\n    font-size: 27px !important;\n    font-weight: 300 !important;\n    line-height: 1 !important;\n    background: transparent !important;\n    border: 0 !important;\n    box-shadow: none !important;\n}\n\n/* Send/upload action: keep its existing blue circular button, but replace the\n   square upload-arrow artwork with a plain white upward arrow. */\n[data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"] {\n    position: relative !important;\n    width: 36px !important;\n    min-width: 36px !important;\n    height: 36px !important;\n    min-height: 36px !important;\n    padding: 0 !important;\n    border-radius: 50% !important;\n    border: 0 !important;\n    outline: none !important;\n    box-shadow: none !important;\n    background: #61b0ed !important;\n    color: #ffffff !important;\n}\n[data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"] svg,\n[data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"] [data-testid="stIconMaterial"],\n[data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"] span {\n    display: none !important;\n}\n[data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"]::after {\n    content: "↑" !important;\n    display: block !important;\n    color: #ffffff !important;\n    font-family: Arial, sans-serif !important;\n    font-size: 25px !important;\n    font-weight: 400 !important;\n    line-height: 1 !important;\n    background: transparent !important;\n    border: 0 !important;\n    box-shadow: none !important;\n}\n\n/* No square/focus decoration in any interaction state. */\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):hover,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):active,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):focus,\n[data-testid="stChatInput"] button:not([data-testid="stChatInputSubmitButton"]):focus-visible,\n[data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"]:hover,\n[data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"]:active,\n[data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"]:focus,\n[data-testid="stChatInput"] [data-testid="stChatInputSubmitButton"]:focus-visible {\n    outline: none !important;\n    box-shadow: none !important;\n    filter: none !important;\n}\n'
        + '\n/* ── Final Search Chats border tone: soft neutral grey ── */\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="stTextInput"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"],\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"] > div,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"] > div,\nsection[data-testid="stSidebar"] .st-key-search_wrap input {\n    border: 1px solid #68717d !important;\n    border-color: #68717d !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"]:hover,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="input"]:focus-within,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-baseweb="base-input"]:focus-within,\nsection[data-testid="stSidebar"] .st-key-search_wrap [data-testid="stTextInput"]:focus-within {\n    border-color: #68717d !important;\n    box-shadow: none !important;\n    outline: none !important;\n}\n'
        + '\n\n\n/* ── Atom One Dark editor-style code blocks ── */\n.stMarkdown pre,\n.stMarkdown pre code,\n[data-testid="stMarkdownContainer"] pre,\n[data-testid="stMarkdownContainer"] pre code,\n[data-testid="stCodeBlock"],\n[data-testid="stCodeBlock"] *,\n[data-testid="stCode"],\n[data-testid="stCode"] *,\n.stCodeBlock,\n.stCodeBlock *,\npre:has(code),\npre:has(code) * {\n    background-color: #282c34 !important;\n    box-shadow: none !important;\n    text-shadow: none !important;\n}\n.stMarkdown pre,\n[data-testid="stMarkdownContainer"] pre,\n[data-testid="stCodeBlock"] pre,\n[data-testid="stCode"] pre,\n.stCodeBlock pre,\npre:has(code) {\n    display: block !important;\n    box-sizing: border-box !important;\n    width: 100% !important;\n    max-width: 100% !important;\n    margin: 0 !important;\n    padding: 1rem !important;\n    color: #abb2bf !important;\n    border: 1px solid #3e4451 !important;\n    border-radius: 9px !important;\n    overflow-x: auto !important;\n}\n.stMarkdown pre code,\n[data-testid="stMarkdownContainer"] pre code,\n[data-testid="stCodeBlock"] pre code,\n[data-testid="stCode"] pre code,\n.stCodeBlock pre code,\npre:has(code) code {\n    display: block !important;\n    width: 100% !important;\n    min-width: max-content !important;\n    padding: 0 !important;\n    margin: 0 !important;\n    color: #abb2bf !important;\n    background: #282c34 !important;\n    font-family: "JetBrains Mono", "Fira Code", Consolas, monospace !important;\n    font-size: .9rem !important;\n    line-height: 1.65 !important;\n    white-space: pre !important;\n}\n/* Atom One Dark syntax colors (Pygments, Highlight.js and common token classes). */\npre .k, pre .kc, pre .kd, pre .kn, pre .kp, pre .kr, pre .kt,\npre .hljs-keyword, pre .hljs-selector-tag, pre .hljs-literal,\npre .token.keyword, pre .token.atrule {\n    color: #c678dd !important;\n}\npre .s, pre .s1, pre .s2, pre .sa, pre .sb, pre .sc, pre .sd,\npre .se, pre .sh, pre .si, pre .sr, pre .ss,\npre .hljs-string, pre .hljs-attr, pre .hljs-regexp,\npre .token.string, pre .token.char {\n    color: #98c379 !important;\n}\npre .m, pre .mb, pre .mf, pre .mh, pre .mi, pre .mo,\npre .hljs-number, pre .token.number {\n    color: #d19a66 !important;\n}\npre .c, pre .c1, pre .cm, pre .cp, pre .cpf, pre .cs,\npre .hljs-comment, pre .hljs-quote, pre .token.comment {\n    color: #5c6370 !important;\n    font-style: italic !important;\n}\npre .nf, pre .fm, pre .nc, pre .hljs-title,\npre .hljs-function .hljs-title, pre .token.function {\n    color: #61afef !important;\n}\npre .nb, pre .bp, pre .nd, pre .hljs-built_in, pre .hljs-type,\npre .token.builtin, pre .token.class-name {\n    color: #e5c07b !important;\n}\npre .na, pre .nn, pre .hljs-variable, pre .hljs-params,\npre .token.parameter {\n    color: #e06c75 !important;\n}\npre .o, pre .ow, pre .p, pre .hljs-operator,\npre .hljs-punctuation, pre .token.operator, pre .token.punctuation {\n    color: #abb2bf !important;\n}\npre .err, pre .hljs-error, pre .token.error {\n    color: #e06c75 !important;\n    background-color: #282c34 !important;\n}\n/* Inline code in assistant prose stays a separate, subtle grey chip. */\n[data-testid="stMarkdownContainer"] p code,\n[data-testid="stMarkdownContainer"] li code,\n.stMarkdown p code,\n.stMarkdown li code {\n    background: #3a3f46 !important;\n    color: #e5c07b !important;\n    border: 1px solid #515862 !important;\n    border-radius: 5px !important;\n    padding: .12em .38em !important;\n}\n\n'
        + '\n/* ── Slightly brighter chat text: assistant answers + user prompts ── */\n[data-testid="stChatMessage"] [data-testid="stChatMessageContent"],\n[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] p,\n[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] li,\n[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] blockquote,\n[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] td,\n[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] th {\n    color: #c8cdd5 !important;\n}\n/* Keep user prompt text clearly readable inside its right-aligned bubble. */\n[data-testid="stChatMessage"]:has([class*="st-key-umsg_"]) [data-testid="stChatMessageContent"],\n[data-testid="stChatMessage"]:has([class*="st-key-umsg_"]) [data-testid="stChatMessageContent"] * {\n    color: #d5d9e0 !important;\n}\n/* Preserve Atom One Dark code syntax colors inside assistant responses. */\n[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] pre,\n[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] pre code {\n    color: #abb2bf !important;\n}\n'
        + '\n/* ── Brighter Atom One Dark code palette + soft grey code surface ── */\n.stMarkdown pre,\n.stMarkdown pre code,\n[data-testid="stMarkdownContainer"] pre,\n[data-testid="stMarkdownContainer"] pre code,\n[data-testid="stCodeBlock"],\n[data-testid="stCodeBlock"] *,\n[data-testid="stCode"],\n[data-testid="stCode"] *,\n.stCodeBlock,\n.stCodeBlock *,\npre:has(code),\npre:has(code) * {\n    background-color: #303640 !important;\n}\n.stMarkdown pre,\n[data-testid="stMarkdownContainer"] pre,\n[data-testid="stCodeBlock"] pre,\n[data-testid="stCode"] pre,\n.stCodeBlock pre,\npre:has(code) {\n    background: #303640 !important;\n    color: #c8cdd5 !important;\n    border-color: #454d59 !important;\n}\n.stMarkdown pre code,\n[data-testid="stMarkdownContainer"] pre code,\n[data-testid="stCodeBlock"] pre code,\n[data-testid="stCode"] pre code,\n.stCodeBlock pre code,\npre:has(code) code {\n    background: #303640 !important;\n    color: #c8cdd5 !important;\n}\n/* Brighter, higher-contrast Atom One Dark syntax tokens. */\npre .k, pre .kc, pre .kd, pre .kn, pre .kp, pre .kr, pre .kt,\npre .hljs-keyword, pre .hljs-selector-tag, pre .hljs-literal,\npre .token.keyword, pre .token.atrule {\n    color: #d18be0 !important;\n}\npre .s, pre .s1, pre .s2, pre .sa, pre .sb, pre .sc, pre .sd,\npre .se, pre .sh, pre .si, pre .sr, pre .ss,\npre .hljs-string, pre .hljs-attr, pre .hljs-regexp,\npre .token.string, pre .token.char {\n    color: #a8d18d !important;\n}\npre .m, pre .mb, pre .mf, pre .mh, pre .mi, pre .mo,\npre .hljs-number, pre .token.number {\n    color: #e0ae78 !important;\n}\npre .c, pre .c1, pre .cm, pre .cp, pre .cpf, pre .cs,\npre .hljs-comment, pre .hljs-quote, pre .token.comment {\n    color: #858e9c !important;\n    font-style: italic !important;\n}\npre .nf, pre .fm, pre .nc, pre .hljs-title,\npre .hljs-function .hljs-title, pre .token.function {\n    color: #79baf0 !important;\n}\npre .nb, pre .bp, pre .nd, pre .hljs-built_in, pre .hljs-type,\npre .token.builtin, pre .token.class-name {\n    color: #edd08b !important;\n}\npre .na, pre .nn, pre .hljs-variable, pre .hljs-params,\npre .token.parameter {\n    color: #ed858e !important;\n}\npre .o, pre .ow, pre .p, pre .hljs-operator,\npre .hljs-punctuation, pre .token.operator, pre .token.punctuation {\n    color: #c8cdd5 !important;\n}\npre .err, pre .hljs-error, pre .token.error {\n    color: #ed858e !important;\n    background-color: #303640 !important;\n}\n'
        + '\n/* Message actions: retain Copy + make Regenerate clearly visible. */\n[class*="st-key-actions_"] [data-testid="stHorizontalBlock"] {\n    display: flex !important;\n    align-items: center !important;\n    gap: .4rem !important;\n}\n[class*="st-key-actions_"] [data-testid="stColumn"] {\n    flex: 0 0 auto !important;\n    width: auto !important;\n    min-width: 34px !important;\n}\n[class*="st-key-regen_"] button {\n    display: inline-flex !important;\n    align-items: center !important;\n    justify-content: center !important;\n    width: 34px !important;\n    min-width: 34px !important;\n    height: 34px !important;\n    min-height: 34px !important;\n    padding: 0 !important;\n    opacity: 1 !important;\n    visibility: visible !important;\n    color: #c8cdd5 !important;\n    background: transparent !important;\n    border: 1px solid transparent !important;\n    border-radius: 9px !important;\n    box-shadow: none !important;\n}\n[class*="st-key-regen_"] button:hover {\n    color: #ffffff !important;\n    background: #3a404a !important;\n    border-color: #4b5360 !important;\n}\n[class*="st-key-regen_"] button svg {\n    color: currentColor !important;\n    fill: none !important;\n    opacity: 1 !important;\n}\n'
        + '\n/* ── Hard-hide legacy feedback/share controls in assistant message toolbars ── */\n[data-testid="stChatMessageActions"],\n[data-testid="stChatMessageToolbar"],\n[data-testid="stFeedback"],\nbutton[aria-label*="Like" i],\nbutton[aria-label*="Dislike" i],\nbutton[aria-label*="Good response" i],\nbutton[aria-label*="Bad response" i],\nbutton[aria-label*="Share" i],\nbutton[title*="Good response" i],\nbutton[title*="Bad response" i],\nbutton[title*="Share" i],\n[data-testid*="thumb"],\n[data-testid*="share"] {\n    display: none !important;\n    visibility: hidden !important;\n    width: 0 !important;\n    min-width: 0 !important;\n    height: 0 !important;\n    padding: 0 !important;\n    margin: 0 !important;\n}\n/* Keep the custom Copy icon bright and visually consistent with Regenerate. */\n[class*="st-key-actions_"] iframe {\n    opacity: 1 !important;\n    filter: none !important;\n}\n[class*="st-key-actions_"] iframe html,\n[class*="st-key-actions_"] iframe body {\n    background: transparent !important;\n}\n[class*="st-key-regen_"] button,\n[class*="st-key-regen_"] button svg {\n    color: #c8cdd5 !important;\n    opacity: 1 !important;\n}\n[class*="st-key-regen_"] button:hover {\n    color: #ffffff !important;\n}\n'
        + side
        + "</style>"
    )