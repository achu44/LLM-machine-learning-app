from openai import OpenAI
import streamlit as st
import pandas as pd
import plotly.express as px
#from conversation_history import display_master_conversation

def load_data():
    df = pd.read_csv('AnalysisData.csv')
    #quantiles = df['CumOil12Month'].quantile([0.33, 0.66])
    #df['CumOilCategory'] = pd.cut(df['CumOil12Month'],
    #                              bins=[-float('inf'), quantiles[0.33], quantiles[0.66], float('inf')],
    #                              labels=['Low', 'Medium', 'High'])
    return df

if 'df' not in st.session_state:
    st.session_state['df'] = load_data()

def setup_page():
    st.title('Main Page')
    st.write('This is the main page of the application.')

# setup_page()

pages = {
    "Data Exploration No gpt": "01_data_exploration_no_gpt",
    "Data Preprocessing": "02_data_preprocessing",
    "Train Models": "03_train_models",
    "Model Evaluation": "04_model_evaluation",
    "Data Exploration Using gpt": "05_data_exploration_using_gpt",
    "Entire Conversation": "06_entire_conversation",
    "Auto Execute Code": "07_auto_execute_code"
}

# Create a radio button in the sidebar for page selection
selected_page = st.sidebar.radio("Select a section", list(pages.keys()))

# Dynamically import the selected page module and render its content
page = __import__(f"pages.{pages[selected_page]}", fromlist=["app"])
page.app()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.session_state['client'] = client

if 'initialized' not in st.session_state:
    st.session_state['initialized'] = True
    initial_message = {
        'role': 'system',
        'content': '''
        Here is the schema for a dataset for 6098 wells from the Midland Basin, with 1 row per well. The columns in the dataset are as follows:
        Column Name	Column Units	Description Column	Group
        SurfaceLongitude	Decimal Degrees	The Longitude of the surface hole location	Location
        SurfaceLatitude	Decimal Degrees	The Latitude of the surface hole location	Location
        BottomHoleLongitude	Decimal Degrees	The Longitude of the bottom hole location	Location
        BottomHoleLatitude	Decimal Degrees	The Latitude of the bottom hole location	Location
        Operator	None (string)	Company that operates the well	Completion
        CompletionDate	None (date)	Date in which the well was completed	Completion
        Reservoir	None (string)	Geologic formation that the well is targeting	Geology
        LateralLength_FT	Feet	Completed length of the horizontal well	Completion
        ProppantIntensity_LBSPerFT	Pounds / Feet	Amount of proppant (frac sand) per lateral foot used to complete the well	Completion
        FluidIntensity_BBLPerFT	Barrels / Feet	Amount of fluid per lateral foot used to complete the well	Completion
        HzDistanceToNearestOffsetAtDrill	Feet	Horizontal distance to the nearest offset well - measured at the time the well was completed	Well spacing
        HzDistanceToNearestOffsetCurrent	Feet	Horizontal distance to the nearest offset well - measured at current time	Well spacing
        VtDistanceToNearestOffsetCurrent	Feet	Vertical distance to the nearest offset well - measured at the time the well was completed	Well spacing
        VtDistanceToNearestOffsetAtDrill	Feet	Vertical distance to the nearest offset well - measured at current time	Well spacing
        WellDepth	Feet	Depth of the horizontal well	Geology
        ReservoirThickness	Feet	Thickness of the targeted reservoir	Geology
        OilInPlace	Million barrels of oil / square mile	Amount of oil in place for the target reservoir	Geology
        Porosity	Percent	Porosity of the target reservoir	Geology
        ReservoirPressure	PSI	Pressure of the target reservoir	Geology
        WaterSaturation	Percent	% saturation of water in the target reservoir fluid	Geology
        StructureDerivative	Percent	% change in depth of the target formation - proxy for geologic faults	Geology
        TotalOrganicCarbon	Percent	% of total organic carbon of the target formation	Geology
        ClayVolume	Percent	% clay of the target reservoir	Geology
        CarbonateVolume	Percent	% carbonate of the target reservoir	Geology
        Maturity	Percent	Maturity of the target reservoir	Geology
        TotalWellCost_USDMM	Millions of dollars	Total cost of the horizontal well	Completion
        CumOil12Month	Barrels of oil	Amount of oil produced in the first 12 months of production	Production
        rowID	None (ID)	unique identifier for each well	ID
        '''
        # CumOilCategory
    }
    st.session_state['messages'] = [initial_message] 

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# method generate_code is NOT USED
# Function to generate code using gpt-3.5-turbo
def generate_code(prompt, messages):
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

st.markdown("""
<style>
.big-font {
    font-size:30px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Last 4 Messages of Conversation:</p>', unsafe_allow_html=True)

num_messages_to_display = 4
recent_messages = st.session_state.messages[-num_messages_to_display:]

for message in recent_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

