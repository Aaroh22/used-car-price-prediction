from pathlib import Path
import base64

import joblib
import pandas as pd
import streamlit as st


# Project files

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "Models" / "final_pipeline.joblib"
DATA_PATH = BASE_DIR / "data" / "cleaned_cardekho_dataset.csv"
HERO_IMAGE_PATH = BASE_DIR / "assets" / "asset1.png"
PAGE_ICON_PATH  = BASE_DIR / "assets" / "favicon-W-darkblue.ico"


# Page setup

st.set_page_config(
    page_title="WheelWorth",
    page_icon= str(PAGE_ICON_PATH) ,
    layout="wide"
)


# Model and data loading

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def format_indian_currency(value):
    """Format a numeric value using Indian lakh/crore digit grouping."""
    digits = str(int(round(abs(value))))

    if len(digits) > 3:
        final_three = digits[-3:]
        remaining = digits[:-3]
        groups = []

        while remaining:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        digits = ",".join([*groups, final_three])

    sign = "-" if value < 0 else ""
    return f"{sign}₹{digits}"


model = load_model()
df = load_data()


# Hero image

def get_base64_image(image_path):

    with open(image_path, "rb") as image_file:

        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    return encoded_image


hero_image = get_base64_image(
    HERO_IMAGE_PATH
)


# Page styles

css = """
<style>


/* Page layout */

.stApp {

    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(42, 93, 255, 0.12),
            transparent 25%
        ),
        linear-gradient(
            180deg,
            #060b16 0%,
            #091221 55%,
            #060b16 100%
        );

    color: white;
}


.block-container {

    max-width: 1280px;

    padding-top: 2rem;

    padding-bottom: 4rem;
}


/* Hide Streamlit default elements */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    visibility: hidden;
}

[data-testid="stDecoration"] {
    display: none;
}


/* Logo */

.wheelworth-logo {

    font-size: 2.5rem;

    font-weight: 800;

    letter-spacing: -0.5px;

    margin-bottom: 1.4rem;
}


.wheelworth-logo span {

    color: #4f82ff;
}


/* Hero */

.hero {

    min-height: 300px;

    padding: 55px;

    border-radius: 22px;

    border:
        1px solid rgba(255, 255, 255, 0.08);


    background-image:

        linear-gradient(
            90deg,
            rgba(4, 10, 20, 0.99) 0%,
            rgba(4, 10, 20, 0.94) 30%,
            rgba(4, 10, 20, 0.72) 48%,
            rgba(4, 10, 20, 0.28) 68%,
            rgba(4, 10, 20, 0.05) 100%
        ),

        url("data:image/png;base64,__HERO_IMAGE__");


    background-size: cover;

    background-position: center;

    background-repeat: no-repeat;


    display: flex;

    align-items: center;


    box-shadow:
        0px 20px 60px
        rgba(0, 0, 0, 0.30);


    margin-bottom: 38px;

    overflow: hidden;

    position: relative;
}


.hero-content {

    max-width: 620px;

    position: relative;

    z-index: 2;
}


.hero-badge {

    display: inline-block;

    padding: 7px 13px;

    border-radius: 100px;


    background:
        rgba(68, 116, 255, 0.11);


    border:
        1px solid
        rgba(86, 132, 255, 0.30);


    color: #7aa5ff;


    font-size: 0.75rem;

    font-weight: 600;

    margin-bottom: 18px;
}


.hero-title {

    color: white;

    font-size: 3rem;

    line-height: 1.05;

    letter-spacing: -2px;

    font-weight: 800;

    margin-bottom: 18px;
}


.hero-title span {

    background:
        linear-gradient(
            90deg,
            #75a4ff,
            #477cff
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


.hero-subtitle {

    max-width: 530px;

    color: #a1aec1;

    font-size: 1rem;

    line-height: 1.7;
}


/* Section heading */

.section-title {

    font-size: 1.45rem;

    font-weight: 700;

    color: white;

    margin-bottom: 4px;
}


.section-subtitle {

    color: #8290a5;

    font-size: 0.9rem;

    margin-bottom: 22px;
}


/* Form fields */

div[data-baseweb="select"] > div {

    background-color:
        #101a2b !important;

    border:
        1px solid
        #25344b !important;

    border-radius:
        10px !important;

    min-height: 48px;
}


div[data-baseweb="input"] {

    background-color:
        #101a2b !important;

    border:
        1px solid
        #25344b !important;

    border-radius:
        10px !important;
}


div[data-baseweb="input"] input {

    color:
        white !important;
}


/* Keep number-input keyboard instructions below the value field. */

[data-testid="stNumberInput"] div[data-baseweb="input"] {

    overflow: visible !important;
}


[data-testid="stNumberInput"] [data-testid="InputInstructions"] {

    top: calc(100% + 4px) !important;
    bottom: auto !important;
    left: 2px !important;

    color: #718097 !important;

    font-size: 0.68rem !important;
    line-height: 1 !important;

    white-space: nowrap;
}


/* Widget labels */

[data-testid="stWidgetLabel"] {

    color:
        #dce5f3;
}


/* Estimate button */

.stButton > button {

    width: 100%;

    min-height: 55px;

    margin-top: 15px;


    border:
        1px solid
        rgba(173, 216, 255, 0.36);

    border-radius: 11px;


    background:
        linear-gradient(
            135deg,
            rgba(126, 190, 255, 0.22),
            rgba(74, 144, 255, 0.13)
        );

    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);


    color: white;

    font-size: 1.15rem;

    font-weight: 400;


    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.20),
        0 10px 30px rgba(73, 154, 255, 0.13);


    transition: 0.2s;
}


.stButton > button p {

    font-size: 1.15rem !important;

    font-weight: 400 !important;

    line-height: 1.2 !important;
}


.stButton > button:hover {

    transform:
        translateY(-1px);

    color:
        white;

    border-color:
        rgba(195, 226, 255, 0.56);

    background:
        linear-gradient(
            135deg,
            rgba(147, 204, 255, 0.31),
            rgba(91, 159, 255, 0.20)
        );


    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.28),
        0 14px 35px rgba(73, 154, 255, 0.20);
}


.stButton > button:active {

    transform:
        translateY(0px);
}


/* Valuation result */

.result-card {

    min-height: 430px;

    padding: 38px;

    border-radius: 20px;


    border:
        1px solid
        rgba(79, 130, 255, 0.22);


    background:

        radial-gradient(
            circle at 85% 10%,
            rgba(49, 105, 255, 0.17),
            transparent 32%
        ),

        linear-gradient(
            145deg,
            rgba(15, 27, 47, 0.96),
            rgba(8, 17, 31, 0.96)
        );


    box-shadow:
        0 20px 60px
        rgba(0, 0, 0, 0.22);
}


.result-label {

    color: #8d9bb0;

    font-size: 0.78rem;

    font-weight: 600;

    letter-spacing: 1.2px;

    text-transform: uppercase;

    margin-bottom: 12px;
}


.result-price {

    color: white;

    font-size: 3rem;

    font-weight: 800;

    letter-spacing: -2px;

    margin-bottom: 12px;
}


.result-description {

    color: #8d9bb0;

    font-size: 0.9rem;

    line-height: 1.6;
}


.result-divider {

    border-top:
        1px solid
        rgba(255, 255, 255, 0.08);

    margin:
        28px 0 22px 0;
}


.result-summary {

    color: #8998ad;

    font-size: 0.9rem;

    line-height: 1.9;
}


.result-summary strong {

    color: #dce5f3;

    font-size: 1.05rem;
}


.empty-result {

    color: #66758c;

    margin-top: 120px;

    text-align: center;

    line-height: 1.7;
}


.empty-result span {

    color: #8998ad;
}


/* Disclaimer */

.model-note {

    color: #64748b;

    font-size: 0.78rem;

    text-align: center;

    margin-top: 45px;

    line-height: 1.6;
}


/* Small screens */

@media (max-width: 800px) {

    .block-container {

        padding-left: 1rem;

        padding-right: 1rem;
    }


    .hero {

        padding: 35px 25px;

        min-height: 280px;


        background-position:
            65% center;


        background-image:

            linear-gradient(
                90deg,
                rgba(4, 10, 20, 0.98) 0%,
                rgba(4, 10, 20, 0.88) 55%,
                rgba(4, 10, 20, 0.30) 100%
            ),

            url("data:image/png;base64,__HERO_IMAGE__");
    }


    .hero-title {

        font-size: 2.3rem;
    }


    .hero-subtitle {

        font-size: 0.92rem;
    }


    .result-price {

        font-size: 2.4rem;
    }

}

</style>
"""


# Add the hero image to the stylesheet

css = css.replace(
    "__HERO_IMAGE__",
    hero_image
)


st.markdown(
    css,
    unsafe_allow_html=True
)


# Logo

st.markdown(
    """<div class="wheelworth-logo">Wheel<span>Worth</span></div>""",
    unsafe_allow_html=True
)


# Hero

st.markdown(
    """<div class="hero"><div class="hero-content"><div class="hero-badge">ML-POWERED CAR VALUATION</div><div class="hero-title">Find Your Car's <span>True Value.</span></div><div class="hero-subtitle">Get an estimated resale value using a machine learning model trained on thousands of used-car listings.</div></div></div>""",
    unsafe_allow_html=True
)


# Car details heading

st.markdown(
    """<div class="section-title">Car Details</div><div class="section-subtitle">Enter your vehicle details to estimate its resale value.</div>""",
    unsafe_allow_html=True
)


# Input and result columns

input_panel, result_panel = st.columns(
    [1.08, 0.92],
    gap="large"
)


# Vehicle details form

with input_panel:


    # Make and model

    col1, col2 = st.columns(2)


    with col1:

        brands = sorted(
            df["brand"]
            .dropna()
            .unique()
        )


        brand = st.selectbox(
            "Brand",
            brands
        )


    with col2:

        available_models = sorted(
            df.loc[
                df["brand"] == brand,
                "model"
            ]
            .dropna()
            .unique()
        )


        car_model = st.selectbox(
            "Model",
            available_models
        )


    # Age and distance

    col1, col2 = st.columns(2)


    with col1:

        vehicle_age = st.number_input(
            "Vehicle Age (Years)",
            min_value=0,
            max_value=40,
            value=5,
            step=1
        )


    with col2:

        km_driven = st.number_input(
            "Kilometres Driven",
            min_value=0,
            max_value=2_000_000,
            value=50_000,
            step=1_000
        )


    # Fuel and transmission

    col1, col2 = st.columns(2)


    with col1:

        fuel_type = st.selectbox(
            "Fuel Type",
            sorted(
                df["fuel_type"]
                .dropna()
                .unique()
            )
        )


    with col2:

        transmission_type = st.selectbox(
            "Transmission",
            sorted(
                df["transmission_type"]
                .dropna()
                .unique()
            )
        )


    # Seller and seating

    col1, col2 = st.columns(2)


    with col1:

        seller_type = st.selectbox(
            "Seller Type",
            sorted(
                df["seller_type"]
                .dropna()
                .unique()
            )
        )


    with col2:

        seats = st.selectbox(
            "Seats",
            sorted(
                df["seats"]
                .dropna()
                .astype(int)
                .unique()
            )
        )


    # Technical details

    col1, col2, col3 = st.columns(3)


    with col1:

        mileage = st.number_input(
            "Mileage (km/l)",
            min_value=1.0,
            max_value=50.0,
            value=18.0,
            step=0.1
        )


    with col2:

        engine = st.number_input(
            "Engine (cc)",
            min_value=500.0,
            max_value=8_000.0,
            value=1_200.0,
            step=50.0
        )


    with col3:

        max_power = st.number_input(
            "Power (bhp)",
            min_value=20.0,
            max_value=1_000.0,
            value=100.0,
            step=1.0
        )


    # Submit the valuation

    predict_button = st.button(
        "Estimate Car Value",
        width="stretch"
    )


# Run the prediction

prediction = None


if predict_button:


    # Keep these feature names aligned with the training data.

    input_data = pd.DataFrame(
        {
            "brand": [brand],
            "model": [car_model],
            "vehicle_age": [vehicle_age],
            "km_driven": [km_driven],
            "seller_type": [seller_type],
            "fuel_type": [fuel_type],
            "transmission_type": [transmission_type],
            "mileage": [mileage],
            "engine": [engine],
            "max_power": [max_power],
            "seats": [seats]
        }
    )


    # The saved pipeline handles preprocessing and prediction.

    prediction = model.predict(
        input_data
    )[0]


    prediction = max(
        float(prediction),
        0
    )


# Valuation result

with result_panel:


    # Empty state

    if prediction is None:


        st.markdown(
            """<div class="result-card"><div class="result-label">Estimated Market Value</div><div class="empty-result">Your estimated value will appear here.<br><span>Enter the car details and click Estimate Car Value.</span></div></div>""",
            unsafe_allow_html=True
        )


    # Predicted value

    else:


        formatted_price = format_indian_currency(
            prediction
        )


        st.markdown(
            f"""<div class="result-card"><div class="result-label">Estimated Market Value</div><div class="result-price">{formatted_price}</div><div class="result-description">Estimated resale value based on the vehicle characteristics you provided.</div><div class="result-divider"></div><div class="result-summary"><strong>{brand} {car_model}</strong><br>{vehicle_age} years old &nbsp; • &nbsp; {km_driven:,.0f} km<br>{fuel_type} &nbsp; • &nbsp; {transmission_type} &nbsp; • &nbsp; {seats} seats<br>{engine:,.0f} cc &nbsp; • &nbsp; {max_power:,.0f} bhp</div></div>""",
            unsafe_allow_html=True
        )


# Disclaimer

st.markdown(
    """<div class="model-note">WheelWorth provides a machine-learning based estimate using historical used-car listing data. Actual resale prices may vary depending on condition, location and current market factors.</div>""",
    unsafe_allow_html=True
)
