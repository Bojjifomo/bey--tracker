import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="BX Combo Builder",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── DARK THEME OVERRIDE ───────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stMetricValue"] { font-size: 1.6rem !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { font-size: 0.72rem !important; color: #9995c0 !important; }
.metric-neg [data-testid="stMetricValue"] { color: #ff6b6b !important; }
.metric-pos [data-testid="stMetricValue"] { color: #51cf66 !important; }
.stSelectbox label, .stRadio label { font-size: 0.78rem !important; }
div[data-testid="stExpander"] { border: 1px solid #2a2a38 !important; }
</style>
""", unsafe_allow_html=True)

# ─── PART DATA ─────────────────────────────────────────────────────────────────

BLADES = [
    {"name":"Sword Dran (A1 B25)",          "do":48.00, "di":30.0,  "mass":34.8},
    {"name":"Sword Dran (B1 D25)",           "do":48.00, "di":30.0,  "mass":34.6},
    {"name":"Sword Dran (A1 K24)",           "do":48.00, "di":30.0,  "mass":34.9},
    {"name":"Sword Dran (A4 B24)",           "do":48.00, "di":30.0,  "mass":35.1},
    {"name":"Infinity Miku",                 "do":45.63, "di":30.0,  "mass":38.0},
    {"name":"Cobalt Dragoon (E24)",          "do":45.63, "di":30.0,  "mass":37.8},
    {"name":"Cobalt Dragoon (B25)",          "do":45.63, "di":30.0,  "mass":38.3},
    {"name":"Lightning L Drago (upper F24)","do":47.88, "di":30.0,  "mass":33.9},
    {"name":"Dragoon Storm (A1 B25)",        "do":48.75, "di":30.0,  "mass":25.5},
    {"name":"Storm Pegasis (A3 B25)",        "do":47.30, "di":30.0,  "mass":31.6},
    {"name":"Victory Valkyrie (B25 4STAR)",  "do":48.60, "di":27.6,  "mass":33.5},
    {"name":"Wizard Rod (A2)",               "do":49.60, "di":33.3,  "mass":35.8},
    {"name":"Wizard Rod (A1 E25 A4)",        "do":49.60, "di":33.3,  "mass":35.8},
    {"name":"Samurai Saber (A5 A25)",        "do":47.355,"di":27.2,  "mass":36.7},
    {"name":"Pheonix Wing (Blue Mold 3)",    "do":47.65, "di":27.55, "mass":38.8},
    {"name":"Hells Chain (A1 E25)",          "do":47.50, "di":31.31, "mass":33.2},
    {"name":"Impact Drake (l24)",            "do":49.01, "di":28.33, "mass":39.3},
    {"name":"Ghost Circle (A7 E25)",         "do":44.40, "di":29.0,  "mass":26.8},
    {"name":"Hover Wyvern (A3 A5)",          "do":46.95, "di":30.8,  "mass":35.1},
    {"name":"Gale Wyvern (A1 K24)",          "do":46.65, "di":30.5,  "mass":31.6},
    {"name":"Silver Wolf (A3 C25 A3)",       "do":49.45, "di":27.39, "mass":37.0},
    {"name":"Dagger Dran (A2 I24)",          "do":46.97, "di":27.7,  "mass":36.0},
    {"name":"Wizard Arrow (A1 K23)",         "do":47.23, "di":27.6,  "mass":31.6},
    {"name":"Cowl Sphinx (L24)",             "do":46.00, "di":32.5,  "mass":33.1},
    {"name":"Obsidian Shell (I24)",          "do":46.00, "di":30.0,  "mass":32.2},
    {"name":"Helm Knight (A3 I23 A1)",       "do":47.40, "di":31.0,  "mass":32.2},
    {"name":"Buster Dran (A4 F24 A8)",       "do":47.52, "di":33.23, "mass":36.7},
    {"name":"Tide Whale (B25)",              "do":48.00, "di":28.1,  "mass":37.9},
    {"name":"Leon Claw (F24)",               "do":47.70, "di":28.2,  "mass":31.6},
    {"name":"Leon Crest (A4 L24 A6)",        "do":47.50, "di":27.7,  "mass":34.9},
    {"name":"Gill Shark (A4 L24)",           "do":45.438,"di":27.5,  "mass":29.9},
    {"name":"Gill Shark (A2 G25)",           "do":45.438,"di":27.5,  "mass":29.7},
    {"name":"Shelter Drake (A4 G25)",        "do":45.438,"di":27.5,  "mass":32.3},
    {"name":"Weiss Tiger (A2 L24)",          "do":47.20, "di":27.4,  "mass":34.6},
    {"name":"Thanos (C1 D24)",              "do":46.22, "di":32.2,  "mass":29.6},
    {"name":"Iron Man (A4 D24 A1)",         "do":47.40, "di":31.0,  "mass":32.2},
    {"name":"Tackle Goat (E25)",            "do":46.00, "di":30.0,  "mass":31.6},
    {"name":"Keel Shark (B24 A1)",          "do":45.77, "di":27.5,  "mass":34.4},
    {"name":"Steel Samurai (E24)",          "do":47.70, "di":28.2,  "mass":31.2},
    {"name":"Clock Mirage (F25)",           "do":52.00, "di":27.5,  "mass":37.8},
    {"name":"Shinobi Shadow (C25)",         "do":47.60, "di":27.7,  "mass":27.8},
    {"name":"Golum Rock (A4 H25 A8)",       "do":46.00, "di":30.3,  "mass":34.5},
    {"name":"Golum Rock (A4 D25 A5)",       "do":46.00, "di":30.3,  "mass":43.3},
    {"name":"Red Hulk (S3 E25)",            "do":47.50, "di":34.45, "mass":36.25},
    {"name":"Captain America (F1 C25)",     "do":48.00, "di":30.0,  "mass":32.5},
    {"name":"Rhino Horn (H25)",             "do":43.70, "di":28.0,  "mass":32.8},
]

RATCHETS = [
    {"name":"0-60",  "od":40.00,   "di":9, "mass":6.9},
    {"name":"1-60",  "od":36.967,  "di":9, "mass":6.0},
    {"name":"1-80",  "od":36.967,  "di":9, "mass":6.7},
    {"name":"2-60",  "od":36.829,  "di":9, "mass":6.1},
    {"name":"2-70",  "od":36.829,  "di":9, "mass":6.2},
    {"name":"3-60",  "od":38.00,   "di":9, "mass":6.3},
    {"name":"3-70",  "od":38.00,   "di":9, "mass":6.5},
    {"name":"3-80",  "od":38.00,   "di":9, "mass":7.0},
    {"name":"3-85",  "od":38.00,   "di":9, "mass":4.7},
    {"name":"4-55",  "od":38.00,   "di":9, "mass":4.7},
    {"name":"4-60",  "od":38.00,   "di":9, "mass":6.2},
    {"name":"4-70",  "od":38.00,   "di":9, "mass":6.4},
    {"name":"4-80",  "od":38.00,   "di":9, "mass":6.9},
    {"name":"5-60",  "od":38.60,   "di":9, "mass":6.6},
    {"name":"5-70",  "od":38.60,   "di":9, "mass":6.7},
    {"name":"5-80",  "od":38.60,   "di":9, "mass":7.2},
    {"name":"6-60",  "od":38.335,  "di":9, "mass":6.2},
    {"name":"6-80",  "od":38.335,  "di":9, "mass":6.8},
    {"name":"7-60",  "od":38.19,   "di":9, "mass":7.1},
    {"name":"7-70",  "od":38.19,   "di":9, "mass":7.3},
    {"name":"7-80",  "od":37.00,   "di":9, "mass":7.7},
    {"name":"9-60",  "od":37.00,   "di":9, "mass":6.2},
    {"name":"M-85",  "od":38.335,  "di":19.5,"mass":10.7},
]

BITS = [
    {"name":"F",        "od":16, "mass":2.2,  "mu":0.11,  "eff":7.2,  "teeth":12},
    {"name":"E",        "od":24, "mass":3.3,  "mu":0.135, "eff":3.0,  "teeth":12},
    {"name":"C",        "od":16, "mass":2.1,  "mu":0.135, "eff":5.78, "teeth":12},
    {"name":"R",        "od":16, "mass":2.0,  "mu":0.11,  "eff":6.2,  "teeth":10},
    {"name":"RA (new)", "od":21, "mass":3.2,  "mu":0.20,  "eff":7.2,  "teeth":16},
    {"name":"RA (used)","od":21, "mass":3.2,  "mu":0.20,  "eff":3.7,  "teeth":16},
    {"name":"GF",       "od":16, "mass":2.2,  "mu":0.135, "eff":7.9,  "teeth":12},
    {"name":"LO",       "od":9,  "mass":1.9,  "mu":0.11,  "eff":1.5,  "teeth":12},
    {"name":"FB",       "od":9,  "mass":1.9,  "mu":0.11,  "eff":2.0,  "teeth":12},
    {"name":"LR",       "od":16, "mass":1.9,  "mu":0.11,  "eff":6.2,  "teeth":10},
    {"name":"K",        "od":16, "mass":2.1,  "mu":0.135, "eff":6.9,  "teeth":12},
    {"name":"V",        "od":16, "mass":2.1,  "mu":0.11,  "eff":6.75, "teeth":12},
    {"name":"O",        "od":16, "mass":2.1,  "mu":0.11,  "eff":1.5,  "teeth":12},
    {"name":"LF",       "od":16, "mass":2.1,  "mu":0.11,  "eff":7.2,  "teeth":12},
    {"name":"N",        "od":16, "mass":2.0,  "mu":0.11,  "eff":1.2,  "teeth":12},
    {"name":"B",        "od":16, "mass":2.0,  "mu":0.11,  "eff":2.0,  "teeth":12},
    {"name":"Q",        "od":16, "mass":2.2,  "mu":0.15,  "eff":7.9,  "teeth":12},
    {"name":"DB",       "od":16, "mass":3.1,  "mu":0.11,  "eff":2.0,  "teeth":12},
    {"name":"T",        "od":16, "mass":2.1,  "mu":0.11,  "eff":3.29, "teeth":12},
    {"name":"U",        "od":16, "mass":2.2,  "mu":0.135, "eff":1.5,  "teeth":12},
    {"name":"L",        "od":16, "mass":2.6,  "mu":0.135, "eff":1.9,  "teeth":16},
    {"name":"H",        "od":16, "mass":2.5,  "mu":0.135, "eff":1.9,  "teeth":16},
    {"name":"P",        "od":16, "mass":2.1,  "mu":0.135, "eff":1.8,  "teeth":12},
    {"name":"GN",       "od":16, "mass":2.0,  "mu":0.11,  "eff":1.6,  "teeth":12},
    {"name":"GB",       "od":16, "mass":2.0,  "mu":0.11,  "eff":2.0,  "teeth":12},
    {"name":"W",        "od":16, "mass":1.9,  "mu":0.11,  "eff":1.8,  "teeth":10},
    {"name":"D",        "od":16, "mass":2.0,  "mu":0.11,  "eff":2.5,  "teeth":12},
    {"name":"A",        "od":16, "mass":2.6,  "mu":0.11,  "eff":7.2,  "teeth":16},
    {"name":"TR",       "od":16, "mass":12.5, "mu":0.135, "eff":1.3,  "teeth":16},
    {"name":"OP",       "od":16, "mass":13.9, "mu":0.135, "eff":1.3,  "teeth":14},
    {"name":"GR",       "od":16, "mass":2.1,  "mu":0.135, "eff":6.8,  "teeth":10},
    {"name":"HN",       "od":16, "mass":2.1,  "mu":0.11,  "eff":1.2,  "teeth":12},
]

CHIPS = [
    {"name":"Pegasis", "do":16.87, "di":0, "mass":1.7},
    {"name":"Emperor", "do":16.87, "di":0, "mass":4.7},
    {"name":"Dran",    "do":16.87, "di":0, "mass":1.7},
    {"name":"Wizard",  "do":16.87, "di":0, "mass":1.7},
    {"name":"Hells",   "do":16.87, "di":0, "mass":1.7},
    {"name":"Perceus", "do":16.87, "di":0, "mass":1.7},
    {"name":"Fox",     "do":16.87, "di":0, "mass":1.7},
]

CX_BLADES = [
    {"name":"Blast",  "do":47.00, "di":27.7, "mass":32.6},
    {"name":"Might",  "do":49.78, "di":27.7, "mass":32.8},
    {"name":"Brave",  "do":47.00, "di":27.7, "mass":31.4},
    {"name":"Arc",    "do":50.00, "di":27.7, "mass":29.4},
    {"name":"Reaper", "do":48.00, "di":27.7, "mass":29.4},
    {"name":"Dark",   "do":48.25, "di":27.7, "mass":30.8},
    {"name":"Brush",  "do":49.00, "di":27.7, "mass":30.2},
]

ASSISTS = [
    {"name":"Assult", "do":44.3, "di":19.6, "mass":5.0},
    {"name":"Heavy",  "do":46.0, "di":30.6, "mass":7.8},
    {"name":"Slash",  "do":45.6, "di":19.6, "mass":4.8},
    {"name":"Round",  "do":47.0, "di":19.6, "mass":4.6},
    {"name":"Turn",   "do":45.0, "di":19.6, "mass":5.8},
    {"name":"Bumper", "do":47.5, "di":19.6, "mass":5.2},
    {"name":"Jaggy",  "do":44.6, "di":19.6, "mass":4.6},
]

# ─── PHYSICS CONSTANTS ─────────────────────────────────────────────────────────
G          = 9806.65   # mm/s²
LAUNCH_RPM = 7000
TOOTH_PITCH = 2.2      # mm — verified from SwitchPro dash calc sheet
TS_FACTOR  = 184.1     # mm/s per mm eff_OD at 7000 RPM

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def get_by_name(lst, name):
    return next((x for x in lst if x["name"] == name), None)

def inertia(mass, od, di=0.0):
    """Moment of inertia: M*(Ro² + Ri²)/2  →  M*(Do² + Di²)/8"""
    return mass * (od**2 + di**2) / 8.0

def calc_cx_assembly(chip, cx_blade, assist):
    I_chip   = inertia(chip["mass"],     chip["do"],     chip["di"])
    I_blade  = inertia(cx_blade["mass"], cx_blade["do"], cx_blade["di"])
    I_assist = inertia(assist["mass"],   assist["do"],   assist["di"])
    I_total  = I_chip + I_blade + I_assist
    M_total  = chip["mass"] + cx_blade["mass"] + assist["mass"]
    eff_area = I_total / M_total
    eff_do   = np.sqrt(8.0 * eff_area)
    return {
        "mass": M_total, "I": I_total,
        "eff_do": eff_do, "eff_area": eff_area,
        "I_chip": I_chip, "I_blade": I_blade, "I_assist": I_assist,
    }

def calc_combo(blade_do, blade_di, blade_mass, blade_I, ratchet, bit):
    I_ratchet = inertia(ratchet["mass"], ratchet["od"], ratchet["di"])
    I_bit     = inertia(bit["mass"],     bit["od"],     0.0)
    Ma        = blade_mass + ratchet["mass"] + bit["mass"]
    I_total   = blade_I + I_ratchet + I_bit
    omega0    = LAUNCH_RPM * 2 * np.pi / 60.0
    fric      = bit["mu"] * Ma * G * (bit["eff"] / 2.0)
    spin_time = (I_total * omega0 / fric) if fric > 0 else 999.0
    top_speed = TS_FACTOR * bit["eff"]
    dash_speed = (LAUNCH_RPM / 60.0) * bit["teeth"] * TOOTH_PITCH
    return {
        "Ma": Ma, "I_total": I_total,
        "I_ratchet": I_ratchet, "I_bit": I_bit,
        "spin_time": spin_time,
        "top_speed": top_speed,
        "avg_speed": top_speed / 2,
        "dash_speed": dash_speed,
        "dash_avg_speed": dash_speed / 2,
    }

def calc_collision(stats, Mb):
    Ma         = stats["Ma"]
    cf         = (Ma - Mb) / (Ma + Mb)
    af         = 2 * Ma    / (Ma + Mb)
    ts, ds     = stats["top_speed"], stats["dash_speed"]
    return {
        "max_recoil":      cf * ts,
        "avg_recoil":      cf * ts / 2,
        "dash_max_recoil": cf * ds,
        "dash_avg_recoil": cf * ds / 2,
        "max_atk":         af * ts,
        "avg_atk":         af * ts / 2,
        "dash_max_atk":    af * ds,
        "dash_avg_atk":    af * ds / 2,
        "collision_factor": cf,
        "atk_factor": af,
    }

# ─── LOOKUP DICTS ─────────────────────────────────────────────────────────────
blade_names   = [b["name"]   for b in BLADES]
ratchet_names = [r["name"]   for r in RATCHETS]
bit_names     = [b["name"]   for b in BITS]
chip_names    = [c["name"]   for c in CHIPS]
cx_blade_names= [b["name"]   for b in CX_BLADES]
assist_names  = [a["name"]   for a in ASSISTS]

DEFENDER_PRESETS = {
    "Wizard Rod 1-60 H":     ("Wizard Rod (A2)", "1-60", "H"),
    "Cobalt Dragoon 9-60 E": ("Cobalt Dragoon (B25)", "9-60", "E"),
    "Impact Drake 7-70 L":   ("Impact Drake (l24)", "7-70", "L"),
    "Silver Wolf 3-80 FB":   ("Silver Wolf (A3 C25 A3)", "3-80", "FB"),
    "Custom":                 (None, None, None),
}

# ══════════════════════════════════════════════════════════════════════════════
#   SIDEBAR — ATTACKER BUILDER
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌀 BX Combo Builder")
    st.caption("Physics engine · SwitchPro Friction & Inertia Estimator")
    st.divider()

    combo_mode = st.radio("Combo type", ["Regular", "CX"], horizontal=True)

    if combo_mode == "Regular":
        st.markdown("**Blade**")
        blade_choice = st.selectbox(
            "Blade", blade_names,
            index=blade_names.index("Golum Rock (A4 H25 A8)"),
            label_visibility="collapsed",
        )
        blade_obj = get_by_name(BLADES, blade_choice)
        st.caption(f"OD: {blade_obj['do']} mm · ID: {blade_obj['di']} mm · {blade_obj['mass']} g")
    else:
        st.markdown("**Chip**")
        chip_choice = st.selectbox("Chip", chip_names,
            index=chip_names.index("Fox"), label_visibility="collapsed")
        chip_obj = get_by_name(CHIPS, chip_choice)
        st.caption(f"{chip_obj['mass']} g")

        st.markdown("**CX Blade**")
        cx_blade_choice = st.selectbox("CX Blade", cx_blade_names,
            index=cx_blade_names.index("Brush"), label_visibility="collapsed")
        cx_blade_obj = get_by_name(CX_BLADES, cx_blade_choice)
        st.caption(f"OD: {cx_blade_obj['do']} mm · {cx_blade_obj['mass']} g")

        st.markdown("**Assist**")
        assist_choice = st.selectbox("Assist", assist_names,
            index=assist_names.index("Heavy"), label_visibility="collapsed")
        assist_obj = get_by_name(ASSISTS, assist_choice)
        st.caption(f"OD: {assist_obj['do']} mm · {assist_obj['mass']} g")

    st.divider()
    st.markdown("**Ratchet**")
    ratchet_choice = st.selectbox("Ratchet", ratchet_names,
        index=ratchet_names.index("3-85"), label_visibility="collapsed")
    ratchet_obj = get_by_name(RATCHETS, ratchet_choice)
    st.caption(f"OD: {ratchet_obj['od']} mm · {ratchet_obj['mass']} g")

    st.markdown("**Bit**")
    bit_choice = st.selectbox("Bit", bit_names,
        index=bit_names.index("H"), label_visibility="collapsed")
    bit_obj = get_by_name(BITS, bit_choice)
    st.caption(
        f"Eff OD: {bit_obj['eff']} mm · {bit_obj['teeth']} teeth · "
        f"μ={bit_obj['mu']} · {bit_obj['mass']} g"
    )

    st.divider()
    st.markdown("**Defender**")
    preset_choice = st.selectbox(
        "Preset", list(DEFENDER_PRESETS.keys()),
        index=0, label_visibility="collapsed",
    )
    pre_bl, pre_rt, pre_bt = DEFENDER_PRESETS[preset_choice]

    if preset_choice == "Custom":
        def_blade_choice   = st.selectbox("Def. Blade",   blade_names,   index=0)
        def_ratchet_choice = st.selectbox("Def. Ratchet", ratchet_names, index=0)
        def_bit_choice     = st.selectbox("Def. Bit",     bit_names,     index=20)
    else:
        def_blade_choice   = pre_bl
        def_ratchet_choice = pre_rt
        def_bit_choice     = pre_bt

    def_blade_obj   = get_by_name(BLADES,   def_blade_choice)
    def_ratchet_obj = get_by_name(RATCHETS, def_ratchet_choice)
    def_bit_obj     = get_by_name(BITS,     def_bit_choice)
    Mb = def_blade_obj["mass"] + def_ratchet_obj["mass"] + def_bit_obj["mass"]
    st.caption(f"Defender total mass: **{Mb:.1f} g**")

# ══════════════════════════════════════════════════════════════════════════════
#   COMPUTE
# ══════════════════════════════════════════════════════════════════════════════
cx_data = None

if combo_mode == "Regular":
    b_do, b_di = blade_obj["do"], blade_obj["di"]
    b_mass     = blade_obj["mass"]
    b_I        = inertia(b_mass, b_do, b_di)
    blade_label = blade_choice
else:
    cx_data    = calc_cx_assembly(chip_obj, cx_blade_obj, assist_obj)
    b_do, b_di = cx_data["eff_do"], 0.0
    b_mass     = cx_data["mass"]
    b_I        = cx_data["I"]
    blade_label = f"{chip_choice} / {cx_blade_choice} / {assist_choice} (CX)"

stats = calc_combo(b_do, b_di, b_mass, b_I, ratchet_obj, bit_obj)
coll  = calc_collision(stats, Mb)

Ma         = stats["Ma"]
mass_diff  = Ma - Mb
I_blade_val = b_I
I_ratchet_val = stats["I_ratchet"]
I_bit_val  = stats["I_bit"]

# ══════════════════════════════════════════════════════════════════════════════
#   MAIN PANEL
# ══════════════════════════════════════════════════════════════════════════════
st.title("🌀 Beyblade X Combo Builder")
st.caption(
    f"**Attacker:** {blade_label}  ·  {ratchet_choice}  ·  {bit_choice}  "
    f"→  vs  **{preset_choice}** ({Mb:.1f} g)"
)

# ── ROW 1: KEY METRICS ────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

diff_str = f"{'↑' if mass_diff >= 0 else '↓'} {abs(mass_diff):.1f}g vs def"
c1.metric("Attacker mass (Ma)", f"{Ma:.1f} g", diff_str,
          delta_color="inverse")
c2.metric("Total inertia",      f"{stats['I_total']:.0f} g·mm²")
c3.metric("Spin time",
          f"{min(stats['spin_time'], 500):.1f} s" + ("+" if stats["spin_time"] > 500 else ""))
c4.metric("Top speed",          f"{stats['top_speed']:.1f} mm/s")
c5.metric("Dash speed",         f"{stats['dash_speed']:.0f} mm/s",
          f"{bit_obj['teeth']} teeth")

st.divider()

# ── ROW 2: COLLISION STATS ────────────────────────────────────────────────────
tab_col, tab_dash = st.tabs(["Normal Spin", "Dash (X-Line)"])

with tab_col:
    ca, cb, cc, cd = st.columns(4)
    ca.metric("Max ATK",    f"{coll['max_atk']:.2f} mm/s")
    cb.metric("Avg ATK",    f"{coll['avg_atk']:.2f} mm/s")
    cc.metric("Max recoil", f"{coll['max_recoil']:.2f} mm/s",
              "bounce back" if coll["max_recoil"] < 0 else "keeps going")
    cd.metric("Avg recoil", f"{coll['avg_recoil']:.2f} mm/s")

with tab_dash:
    da, db, dc, dd = st.columns(4)
    da.metric("Dash max ATK",    f"{coll['dash_max_atk']:.2f} mm/s")
    db.metric("Dash avg ATK",    f"{coll['dash_avg_atk']:.2f} mm/s")
    dc.metric("Dash max recoil", f"{coll['dash_max_recoil']:.2f} mm/s",
              "bounce back" if coll["dash_max_recoil"] < 0 else "keeps going")
    dd.metric("Dash avg recoil", f"{coll['dash_avg_recoil']:.2f} mm/s")

st.divider()

# ── ROW 3: CHARTS ─────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.markdown("#### Collision comparison")

    cats   = ["Max ATK", "Avg ATK", "Max Recoil", "Avg Recoil",
              "Dash Max ATK", "Dash Avg ATK", "Dash Max Recoil", "Dash Avg Recoil"]
    vals   = [
        coll["max_atk"], coll["avg_atk"],
        coll["max_recoil"], coll["avg_recoil"],
        coll["dash_max_atk"], coll["dash_avg_atk"],
        coll["dash_max_recoil"], coll["dash_avg_recoil"],
    ]
    colors = [
        "#51cf66","#94d82d","#ff6b6b","#ff6b6b",
        "#ffa94d","#ffec99","#ff6b6b","#ff6b6b",
    ]

    fig_bar = go.Figure(go.Bar(
        x=vals, y=cats, orientation="h",
        marker_color=colors,
        text=[f"{v:.1f}" for v in vals],
        textposition="outside",
        textfont=dict(size=11),
    ))
    fig_bar.update_layout(
        height=320, margin=dict(l=0, r=60, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8e6ff", size=11),
        xaxis=dict(gridcolor="#2a2a38", zerolinecolor="#3a3a4e"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        showlegend=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with right_col:
    st.markdown("#### Inertia breakdown")
    i_labels = ["Blade / CX", "Ratchet", "Bit"]
    i_vals   = [I_blade_val, I_ratchet_val, I_bit_val]
    i_cols   = ["#6c63ff", "#a29bfe", "#74c0fc"]

    fig_pie = go.Figure(go.Pie(
        labels=i_labels, values=i_vals,
        marker=dict(colors=i_cols),
        hole=0.5,
        textinfo="label+percent",
        textfont=dict(size=12, color="#e8e6ff"),
        hovertemplate="%{label}: %{value:.0f} g·mm² (%{percent})<extra></extra>",
    ))
    fig_pie.update_layout(
        height=290, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8e6ff"),
        showlegend=True,
        legend=dict(font=dict(color="#9995c0", size=11)),
    )
    fig_pie.add_annotation(
        text=f"{stats['I_total']:.0f}<br><span style='font-size:10px'>g·mm²</span>",
        x=0.5, y=0.5, font=dict(size=14, color="#e8e6ff"),
        showarrow=False,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ── CX BREAKDOWN ──────────────────────────────────────────────────────────────
if combo_mode == "CX" and cx_data:
    st.markdown("#### CX Assembly breakdown")
    cx_rows = [
        {"Part": f"Chip · {chip_choice}", "OD (mm)": f"{chip_obj['do']}", "ID (mm)": "0",
         "Mass (g)": chip_obj["mass"], "Inertia (g·mm²)": round(cx_data["I_chip"], 1)},
        {"Part": f"Blade · {cx_blade_choice}", "OD (mm)": f"{cx_blade_obj['do']}",
         "ID (mm)": f"{cx_blade_obj['di']}", "Mass (g)": cx_blade_obj["mass"],
         "Inertia (g·mm²)": round(cx_data["I_blade"], 1)},
        {"Part": f"Assist · {assist_choice}", "OD (mm)": f"{assist_obj['do']}",
         "ID (mm)": f"{assist_obj['di']}", "Mass (g)": assist_obj["mass"],
         "Inertia (g·mm²)": round(cx_data["I_assist"], 1)},
        {"Part": "🔵 CX Assembly (effective)", "OD (mm)": f"{cx_data['eff_do']:.2f}",
         "ID (mm)": "0", "Mass (g)": round(cx_data["mass"], 2),
         "Inertia (g·mm²)": round(cx_data["I"], 1)},
    ]
    st.dataframe(pd.DataFrame(cx_rows), use_container_width=True, hide_index=True)
    st.caption("Effective OD = √(8 × I_total / M_total)  —  SwitchPro formula")
    st.divider()

# ── FULL PART TABLE ────────────────────────────────────────────────────────────
st.markdown("#### Full combo breakdown")
part_rows = [
    {"Part": f"{'Blade' if combo_mode == 'Regular' else 'CX Assembly'}",
     "Name": blade_label[:45],
     "OD (mm)": f"{b_do:.2f}", "ID (mm)": f"{b_di:.2f}",
     "Mass (g)": round(b_mass, 2), "Inertia (g·mm²)": round(I_blade_val, 1)},
    {"Part": "Ratchet", "Name": ratchet_choice,
     "OD (mm)": ratchet_obj["od"], "ID (mm)": ratchet_obj["di"],
     "Mass (g)": ratchet_obj["mass"], "Inertia (g·mm²)": round(I_ratchet_val, 1)},
    {"Part": "Bit", "Name": bit_choice,
     "OD (mm)": bit_obj["od"], "ID (mm)": "0",
     "Mass (g)": bit_obj["mass"], "Inertia (g·mm²)": round(I_bit_val, 1)},
    {"Part": "TOTAL", "Name": "—",
     "OD (mm)": "—", "ID (mm)": "—",
     "Mass (g)": round(Ma, 2), "Inertia (g·mm²)": round(stats["I_total"], 1)},
]
st.dataframe(pd.DataFrame(part_rows), use_container_width=True, hide_index=True)

# ── FORMULA EXPANDER ──────────────────────────────────────────────────────────
with st.expander("📐 Physics formulas"):
    st.markdown(f"""
**Inertia:** `I = M × (OD² + ID²) / 8`  *(hollow cylinder polar moment)*

**Spin time:** `T = I·ω₀ / (μ · M · g · r_bit)`  where ω₀ = {LAUNCH_RPM} RPM, g = {G:.2f} mm/s²

**Top speed:** `V = {TS_FACTOR} × eff_OD`  mm/s  *(empirical from SwitchPro sim at {LAUNCH_RPM} RPM)*

**Dash speed:** `V_dash = (RPM/60) × teeth × {TOOTH_PITCH}`  mm/s  *(X-Line tooth pitch = {TOOTH_PITCH} mm)*

**ATK on defender:** `ATK = 2·Ma / (Ma + Mb) × V_impact`

**Recoil on attacker:** `Recoil = (Ma − Mb) / (Ma + Mb) × V_impact`

**CX Effective OD:** `OD_eff = √(8 × I_cx / M_cx)`

---
Current values:
- Collision factor cf = `{coll['collision_factor']:.4f}` → attacker {'bounces back' if coll['collision_factor'] < 0 else 'keeps going'}
- ATK factor af = `{coll['atk_factor']:.4f}`
- Ma = `{Ma:.2f} g`  ·  Mb = `{Mb:.2f} g`  ·  Δ = `{mass_diff:+.2f} g`
    """)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.caption("Data source: SwitchPro's Beyblade Friction Sim & Inertia Estimator (v1.25.2026)  ·  All values ±0.1g / ±0.05mm")
