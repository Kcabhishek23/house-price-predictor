import streamlit as st

from main import predict_price


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FI House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# OPTIONS
# These must match the categories in data/house_price.csv exactly.
# The model's OneHotEncoder ignores unseen values, so a mismatched
# option would silently have no effect on the prediction.
# ============================================================

MUNICIPALITIES = [
    "Helsinki",
    "Espoo",
    "Vantaa",
    "Tampere",
    "Turku",
    "Oulu",
    "Jyväskylä",
    "Kuopio",
    "Lahti",
    "Pori"
]

PROPERTY_TYPES = [
    "Apartment",
    "Terraced house",
    "Semi-detached house",
    "Detached house"
]

HEATING_SYSTEMS = [
    "District heating",
    "Electric heating",
    "Geothermal",
    "Air-source heat pump",
    "Oil heating",
    "Wood heating"
]

CONDITIONS = [
    "New",
    "Excellent",
    "Good",
    "Fair",
    "Needs renovation"
]

ENERGY_RATINGS = ["A", "B", "C", "D", "E", "F", "G"]


def html(markup):
    """Render an HTML snippet.

    Streamlit's markdown parser ends an HTML block at the first blank
    line and treats 4+ space indentation as a code block, so both are
    stripped before rendering.
    """
    cleaned = "\n".join(
        line.strip() for line in markup.splitlines() if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)



# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #0b0d0f;
        --panel: #111418;
        --field: #181c21;
        --border: rgba(255,255,255,0.08);
        --border-strong: #292e35;
        --text: #f2f3f5;
        --muted: #858b95;
        --faint: #4a5058;
        --accent: #8fa8ff;
        --nav-h: 64px;
        --scroll-h: clamp(300px, calc(100vh - 320px), 480px);
    }


    /* ---------- GLOBAL ---------- */

    html,
    [data-testid="stMain"],
    section.main {
        scroll-behavior: smooth;
    }

    html,
    body,
    .stApp,
    .stApp p,
    .stApp label,
    .stApp input,
    .stApp button,
    .stApp [data-baseweb="select"],
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] *,
    [data-baseweb="popover"] {
        font-family: 'Space Grotesk', sans-serif !important;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1200px;
        padding: var(--nav-h) 24px 0 24px;
    }

    [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
        gap: 0;
    }

    /* Hide Streamlit chrome */
    #MainMenu,
    footer,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        display: none !important;
    }


    /* ---------- NAVBAR (fixed) ---------- */

    .fi-nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;

        height: var(--nav-h);

        background: rgba(11,13,15,0.88);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);

        border-bottom: 1px solid var(--border);
    }

    .fi-nav-inner {
        max-width: 1200px;
        height: 100%;
        margin: 0 auto;
        padding: 0 24px;

        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .fi-brand {
        font-size: 17px;
        font-weight: 600;
        letter-spacing: -0.3px;
        color: var(--text);
    }

    .fi-nav-link,
    .fi-nav-link:visited {
        font-size: 14px;
        color: var(--muted) !important;
        text-decoration: none !important;
        transition: color 0.2s ease;
    }

    .fi-nav-link:hover {
        color: var(--text) !important;
    }


    /* ---------- WORKSPACE (vertically centred) ---------- */

    .st-key-workspace {
        min-height: calc(100vh - var(--nav-h));
        justify-content: center;
        padding: 32px 0;
    }

    .st-key-workspace [data-testid="stHorizontalBlock"] {
        align-items: stretch;
    }

    .st-key-workspace [data-testid="stColumn"] {
        display: flex;
        flex-direction: column;
    }

    .st-key-workspace [data-testid="stColumn"] > [data-testid="stVerticalBlock"] {
        flex: 1;
    }

    .st-key-workspace [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"] {
        flex: 1;
    }


    /* ---------- PANELS ---------- */

    .st-key-input-panel,
    .st-key-result-panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        gap: 1rem;

        flex: 1;
        align-items: stretch !important;
    }

    .panel-title {
        font-size: 17px;
        font-weight: 600;
        letter-spacing: -0.2px;
        line-height: 1.3;
    }

    .panel-subtitle {
        font-size: 13px;
        color: var(--muted);
        margin-top: 2px;
    }


    /* ---------- INPUT SCROLL AREA ---------- */

    .st-key-input-scroll {
        height: var(--scroll-h);
        flex: none;
        overflow-y: auto;
        padding: 16px 10px 8px 2px;
        align-items: stretch !important;

        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
    }

    .st-key-input-scroll::-webkit-scrollbar {
        width: 5px;
    }

    .st-key-input-scroll::-webkit-scrollbar-track {
        background: transparent;
    }

    .st-key-input-scroll::-webkit-scrollbar-thumb {
        background: #30343a;
        border-radius: 10px;
    }

    .st-key-input-scroll {
        scrollbar-width: thin;
        scrollbar-color: #30343a transparent;
    }


    /* ---------- WIDGETS ---------- */

    [data-testid="stWidgetLabel"] p,
    .stCheckbox label p {
        color: #bfc4cc !important;
        font-size: 13px !important;
    }

    [data-testid="stNumberInputContainer"],
    [data-baseweb="input"],
    [data-baseweb="base-input"],
    [data-baseweb="select"] > div {
        background: var(--field) !important;
        border-color: var(--border-strong) !important;
        border-radius: 9px !important;
    }

    [data-baseweb="input"] input,
    [data-baseweb="select"] div,
    [data-baseweb="select"] input {
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text);
    }

    [data-baseweb="select"] svg,
    [data-testid="stNumberInputStepDown"] svg,
    [data-testid="stNumberInputStepUp"] svg {
        color: var(--muted) !important;
        fill: var(--muted) !important;
    }

    [data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInputStepUp"] {
        background: transparent !important;
    }

    [data-testid="stNumberInputContainer"]:focus-within,
    [data-baseweb="input"]:focus-within,
    [data-baseweb="select"] > div:focus-within {
        border-color: var(--accent) !important;
    }

    /* Dropdown menu (rendered in a portal outside the app tree) */
    [data-baseweb="popover"] [data-baseweb="menu"],
    [data-baseweb="popover"] ul {
        background: var(--field) !important;
    }

    [data-baseweb="popover"] li {
        background: transparent !important;
        color: var(--text) !important;
    }

    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] li[aria-selected="true"] {
        background: #23282f !important;
    }

    /* Checkboxes */
    .stCheckbox [data-baseweb="checkbox"] > span:first-child {
        background-color: var(--field) !important;
        border-color: #3a4048 !important;
        border-radius: 5px !important;
    }

    .stCheckbox label:has(input:checked) > span:first-child {
        background-color: var(--accent) !important;
        border-color: var(--accent) !important;
    }


    /* ---------- BUTTON ---------- */

    [data-testid="stElementContainer"]:has(.stButton),
    .stButton {
        width: 100% !important;
    }

    .stButton {
        margin-top: 4px;
    }

    .stButton button {
        width: 100%;
        padding: 10px 18px;

        background: #ffffff;
        color: var(--bg);

        border: none;
        border-radius: 10px;

        transition: background 0.2s ease;
    }

    .stButton button p {
        font-size: 14px;
        font-weight: 600;
        color: var(--bg) !important;
    }

    .stButton button:hover,
    .stButton button:focus:not(:active) {
        background: #dfe4ff;
        color: var(--bg);
        border: none;
    }


    /* ---------- RESULT PANEL ---------- */

    .st-key-result-panel {
        justify-content: center;
        text-align: center;
    }

    .result-label {
        font-size: 13px;
        color: var(--muted);
        letter-spacing: 0.02em;
    }

    .result-price {
        font-size: clamp(44px, 5.5vw, 72px);
        font-weight: 600;
        letter-spacing: -0.04em;
        line-height: 1.05;

        margin: 14px 0 18px;
    }

    .result-price.is-empty {
        color: #3a3f46;
    }

    .result-hint {
        font-size: 13px;
        color: var(--muted);
    }

    .result-summary {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 6px 18px;

        font-size: 13px;
        color: var(--muted);
    }

    .result-summary span + span::before {
        content: "";
        display: inline-block;
        width: 3px;
        height: 3px;
        margin-right: 18px;
        vertical-align: middle;

        background: var(--faint);
        border-radius: 50%;
    }


    /* ---------- OUR MODEL ---------- */

    .fi-model {
        box-sizing: border-box;
        min-height: calc(100vh - var(--nav-h));
        padding: 96px 0 64px;
        scroll-margin-top: var(--nav-h);

        border-top: 1px solid var(--border);
    }

    .fi-model-title {
        font-size: 36px;
        font-weight: 600;
        letter-spacing: -0.04em;
        line-height: 1.1;

        margin-bottom: 14px;
    }

    .fi-model-text {
        max-width: 640px;
        margin-bottom: 20px;

        font-size: 15px;
        line-height: 1.7;
        color: var(--muted);
    }

    .fi-model-name {
        margin-bottom: 40px;

        font-size: 13px;
        color: var(--muted);
    }

    .fi-model-name strong {
        color: var(--accent);
        font-weight: 500;
    }

    .fi-metrics {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;

        margin-bottom: 40px;
    }

    .fi-metric {
        padding: 18px 20px;

        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    .fi-metric-value {
        font-size: 24px;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    .fi-metric-label {
        margin-top: 4px;

        font-size: 12px;
        color: var(--muted);
    }

    .fi-note {
        max-width: 640px;
        padding-left: 16px;

        border-left: 2px solid var(--accent);

        font-size: 13px;
        line-height: 1.7;
        color: var(--muted);
    }


    /* ---------- RESPONSIVE ---------- */

    @media (max-width: 900px) {

        :root {
            --scroll-h: 420px;
        }

        [data-testid="stMainBlockContainer"] {
            padding-left: 16px;
            padding-right: 16px;
        }

        .fi-nav-inner {
            padding: 0 16px;
        }

        .st-key-workspace {
            min-height: auto;
            padding: 24px 0 56px;
        }

        /* Stack: input panel on top, prediction panel below */
        .st-key-workspace > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"],
        .st-key-workspace > [data-testid="stHorizontalBlock"] {
            flex-direction: column;
            gap: 1rem;
        }

        .st-key-workspace [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 100% !important;
        }

        .st-key-result-panel {
            min-height: 280px;
        }

        .fi-model {
            min-height: auto;
            padding: 72px 0 56px;
        }

        .fi-metrics {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 520px) {

        .fi-model-title {
            font-size: 30px;
        }

        .fi-brand {
            font-size: 15px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# NAVBAR
# ============================================================

html(
    """
    <nav class="fi-nav">
        <div class="fi-nav-inner">
            <span class="fi-brand">FI House Price Predictor</span>
            <a class="fi-nav-link" href="#our-model">Our Model</a>
        </div>
    </nav>
    """
)


# ============================================================
# WORKSPACE
# ============================================================

with st.container(key="workspace"):

    left, right = st.columns([1.15, 1], gap="large")


    # --------------------------------------------------------
    # LEFT — PROPERTY INPUTS
    # --------------------------------------------------------

    with left:

        with st.container(key="input-panel"):

            html(
                """
                <div>
                    <div class="panel-title">Property Information</div>
                    <div class="panel-subtitle">Enter the details of the property.</div>
                </div>
                """
            )

            # Only this area scrolls; the title and button stay in view.
            with st.container(key="input-scroll"):

                c1, c2 = st.columns(2)
                house_size = c1.number_input(
                    "House size (m²)", min_value=20, max_value=300, value=75, step=1
                )
                rooms = c2.number_input(
                    "Rooms", min_value=1, max_value=9, value=3, step=1
                )

                c1, c2 = st.columns(2)
                floor = c1.number_input(
                    "Floor", min_value=0, max_value=13, value=2, step=1
                )
                house_age = c2.number_input(
                    "House age (years)", min_value=0, max_value=100, value=20, step=1
                )

                c1, c2 = st.columns(2)
                bathrooms = c1.number_input(
                    "Bathrooms", min_value=1, max_value=3, value=1, step=1
                )
                toilets = c2.number_input(
                    "Toilets", min_value=1, max_value=5, value=1, step=1
                )

                c1, c2 = st.columns(2)
                parking_spaces = c1.number_input(
                    "Parking spaces", min_value=0, max_value=3, value=1, step=1
                )
                distance_to_city_center = c2.number_input(
                    "Distance to city centre (km)",
                    min_value=0.0, max_value=30.0, value=5.0, step=0.5,
                    format="%.1f"
                )

                c1, c2 = st.columns(2)
                municipality = c1.selectbox("Municipality", MUNICIPALITIES)
                property_type = c2.selectbox("Property type", PROPERTY_TYPES)

                c1, c2 = st.columns(2)
                heating_system = c1.selectbox("Heating system", HEATING_SYSTEMS)
                condition = c2.selectbox("Condition", CONDITIONS, index=2)

                c1, c2 = st.columns(2)
                plot_size = c1.number_input(
                    "Plot size (m²)",
                    min_value=0, max_value=5000, value=0, step=10
                )
                energy_rating = c2.selectbox("Energy rating", ENERGY_RATINGS, index=2)

                c1, c2 = st.columns(2)
                open_kitchen = c1.checkbox("Open kitchen")
                garden = c2.checkbox("Garden")

                c1, c2 = st.columns(2)
                sauna = c1.checkbox("Sauna")
                balcony_terrace = c2.checkbox("Balcony / terrace")

            predict_button = st.button("Predict Price")


    # --------------------------------------------------------
    # PREDICTION
    # Runs before the right panel renders so the result appears
    # immediately. The model itself is trained once, inside main.py,
    # when it is first imported. Nothing is retrained here.
    # --------------------------------------------------------

    if predict_button:

        prediction = predict_price(
            house_size=house_size,
            rooms=rooms,
            floor=floor,
            open_kitchen=int(open_kitchen),
            parking_spaces=parking_spaces,
            house_age=house_age,
            garden=int(garden),
            bathrooms=bathrooms,
            toilets=toilets,
            distance_to_city_center=distance_to_city_center,
            municipality=municipality,
            property_type=property_type,
            sauna=int(sauna),
            balcony_terrace=int(balcony_terrace),
            heating_system=heating_system,
            condition=condition,
            plot_size=plot_size,
            energy_rating=energy_rating
        )

        # Keep the result and the inputs it was made from, so the
        # displayed summary never disagrees with the displayed price.
        st.session_state["prediction"] = prediction
        st.session_state["summary"] = {
            "rooms": rooms,
            "municipality": municipality,
            "size": house_size
        }


    # --------------------------------------------------------
    # RIGHT — RESULT
    # --------------------------------------------------------

    with right:

        with st.container(key="result-panel"):

            prediction = st.session_state.get("prediction")
            summary = st.session_state.get("summary")

            if prediction is not None:

                # The model predicts in thousands of euros. Rounded to the
                # nearest €1,000, since the model's error is ~€19k.
                price = round(prediction) * 1000
                rooms_label = "room" if summary["rooms"] == 1 else "rooms"

                html(
                    f"""
                    <div>
                        <div class="result-label">Estimated Price</div>
                        <div class="result-price">€{price:,.0f}</div>
                        <div class="result-summary">
                            <span>{summary["rooms"]} {rooms_label}</span>
                            <span>{summary["municipality"]}</span>
                            <span>{summary["size"]} m²</span>
                        </div>
                    </div>
                    """
                )

            else:

                html(
                    """
                    <div>
                        <div class="result-label">Estimated Price</div>
                        <div class="result-price is-empty">€ —</div>
                        <div class="result-hint">Enter property information and predict.</div>
                    </div>
                    """
                )


# ============================================================
# OUR MODEL
# ============================================================

html(
    """
    <section id="our-model" class="fi-model">

        <div class="fi-model-title">Our Model</div>

        <div class="fi-model-text">
            FI House Price Predictor is a machine learning project built
            for learning and experimentation. The model uses property
            characteristics such as location, size, condition and other
            features to estimate house prices.
        </div>

        <div class="fi-model-name">
            Model: <strong>Random Forest Regressor</strong>
        </div>

        <div class="fi-metrics">
            <div class="fi-metric">
                <div class="fi-metric-value">10,000</div>
                <div class="fi-metric-label">Training records</div>
            </div>
            <div class="fi-metric">
                <div class="fi-metric-value">0.943</div>
                <div class="fi-metric-label">R² Score</div>
            </div>
            <div class="fi-metric">
                <div class="fi-metric-value">€19.38k</div>
                <div class="fi-metric-label">MAE</div>
            </div>
            <div class="fi-metric">
                <div class="fi-metric-value">910.50</div>
                <div class="fi-metric-label">MSE</div>
            </div>
        </div>

        <div class="fi-note">
            This project uses a synthetic Finnish-style dataset created for
            machine learning practice. It does not represent actual Finnish
            housing market transactions.
        </div>

    </section>
    """
)
