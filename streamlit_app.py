
import os
import streamlit as st

# Load API keys from Streamlit Cloud Secrets
try:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
except Exception:
    pass

from agent.agent import run_agent

st.set_page_config(
    page_title="EventEase",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f5f3ff;
    color: #25213b;
}

/* Main content width */
.block-container {
    max-width: 850px;
    padding-top: 1rem;
}

/* Streamlit header */
header[data-testid="stHeader"] {
    background-color: #ffffff;
}

/* Full-width EventEase header */

.app-header {
    width: 100vw;
    margin-left: calc(50% - 50vw);
    min-height: 75px;
    padding: 10px 5%;
    box-sizing: border-box;
    background-color: #ffffff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: visible;
}

.app-header .brand {
    font-size: 22px;
    font-weight: 700;
    line-height: normal;
    color: #25213b;
    margin: 0;
    padding: 0;
    display: block;
    overflow: visible;
}

.app-header .brand span {
    color: #6c4ce3;
}

.app-header .tagline {
    color: #777777;
    font-size: 14px;
    line-height: normal;
    margin: 0;
}

/* Hero section */
.hero {
    text-align: center;
    margin: 30px 0 40px;
}

.hero h1 {
    color: #34245f;
    font-size: 32px;
    margin-bottom: 12px;
}

.hero p {
    color: #777777;
    font-size: 15px;
}

/* White input and recommendation cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important;
    border: 1px solid #e5e5e5;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    padding: 8px;
}

/* Section headings */
h1, h2, h3 {
    color: #49348b;
}

/* Text area */
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #25213b !important;
    border: 1px solid #dddddd;
    border-radius: 10px;
    font-size: 15px;
}

.stTextArea textarea:focus {
    border-color: #8062eb;
}

/* Generate button */
.stButton button {
    background-color: #6c4ce3;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 22px;
    transition: 0.3s;
}

.stButton button:hover {
    background-color: #5134bd;
    color: #ffffff;
}

/* Footer */
.footer {
    text-align: center;
    padding: 25px;
    color: #888888;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# Header
st.markdown(
    '<div class="app-header">'
    '<div class="brand"><span>Event</span>Ease</div>'
    '<div class="tagline">AI-Powered Event Planner</div>'
    '</div>',
    unsafe_allow_html=True
)


# Hero section
st.markdown("""
<div class="hero">
    <h1>Plan Your Perfect Event</h1>
    <p>Tell us what you're planning. Let AI take care of the recommendations.</p>
</div>
""", unsafe_allow_html=True)



# Event input section
with st.container(border=True):

    st.subheader("Describe Your Event")

    user_query = st.text_area(
        "Event requirements",
        placeholder=(
            "Example: I want to organize a birthday party "
            "in Hyderabad for 100 guests with a budget of ₹50,000..."
        ),
        height=120,
        label_visibility="collapsed"
    )

    generate = st.button("Generate Recommendations")


# Store recommendations across Streamlit reruns
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None


# Connect Streamlit directly with Agentic RAG
if generate:

    if not user_query.strip():
        st.warning("Please enter your event requirements.")

    else:
        try:
            with st.spinner("Generating your event recommendations..."):

                result = run_agent(user_query)

                st.session_state.recommendations = result.model_dump()

        except Exception as error:
            st.error(f"Unable to generate recommendations: {error}")


# AI Recommendations
st.subheader("AI Recommendations")

data = st.session_state.recommendations

if data:

    # Event Overview
    with st.container(border=True):
        st.markdown("**:violet[Event Overview]**")
        st.write(data.get("event_overview", "Not available"))

    # Venue Recommendations
    with st.container(border=True):
        st.markdown("**:violet[Venue Recommendations]**")

        venues = data.get("venue_recommendations", [])

        if venues:
            for venue in venues:

                with st.container(border=True):

                    if venue.get("image_url"):
                        st.image(venue["image_url"], width=300)

                    st.subheader(venue.get("name", "Venue"))

                    st.write("Address:", venue.get("address") or "Not available")
                    st.write("Capacity:", venue.get("capacity") or "Not available")
                    st.write("Facilities:", ", ".join(venue.get("facilities", [])) or "Not available")
                    st.write("Price:", venue.get("price") or "Not available")

                    if venue.get("rating"):
                        st.write("Rating:", venue["rating"])

                    if venue.get("source_url"):
                        st.link_button(
                            "View Original Venue Website",
                            venue["source_url"]
                        )
        else:
            st.write("No venue recommendations available.")

    # Other recommendation sections
    sections = [
        ("Food & Catering", "food_recommendations"),
        ("Decoration", "decoration_recommendations"),
        ("Additional Recommendations", "additional_recommendations"),
        ("Estimated Budget Breakdown", "budget_breakdown"),
        ("Information Sources", "information_sources")
    ]

    for heading, field in sections:

        with st.container(border=True):
            st.markdown(f"**:violet[{heading}]**")
            st.write(data.get(field, "Not available"))

else:

    sections = [
        ("Event Overview", "Your event overview will appear here."),
        ("Venue Recommendations", "Venue suggestions will appear here."),
        ("Food & Catering", "Food recommendations will appear here."),
        ("Decoration", "Decoration suggestions will appear here."),
        ("Additional Recommendations", "Additional suggestions will appear here."),
        ("Estimated Budget Breakdown", "Estimated costs will appear here."),
        ("Information Sources", "Sources will appear here.")
    ]

    for heading, description in sections:
        with st.container(border=True):
            st.markdown(f"**:violet[{heading}]**")
            st.write(description)


# Footer
st.markdown(
    '<div class="footer">Powered by AI | AI Event Planner</div>',
    unsafe_allow_html=True
)
