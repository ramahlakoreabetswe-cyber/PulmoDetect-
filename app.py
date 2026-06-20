import streamlit as st
from pyairtable import Table
from datetime import datetime

# Page setup
st.set_page_config(page_title="PulmoDetect", layout="centered")
# Connect to Airtable
   
   
airtable = Table(
       st.secrets["AIRTABLE_TOKEN"],
       st.secrets["AIRTABLE_BASE_ID"],
       "Predictions"
   )
   


# Title + Credits
st.title("PulmoDetect: TB Risk Screening")
st.caption("Developed by: Reabetswe")
         
# Tabs = your menu bar
tab1, tab2, tab3 = st.tabs(["Risk Screening", "What is TB?", "Credits"])
         
with tab1:
    st.header("TB Risk Screening")
    st.subheader("Which region are you from?")
    st.caption("No personal data will be stored. Region selection used for anonymous usage stats only.")

# 9 Limpopo regions with Tzaneen included
region_options = [
    "Polokwane",
    "Tzaneen", 
    "Makhado",
    "Thohoyandou",
    "Lephalale",
    "Burgersfort",
    "Groblersdal",
    "Giyani",
    "Mokopane"
]

region = st.radio(
    "Select your region:",
    options=region_options + ["Other"],
    index=None,
    key="region_select"  # Adding key prevents widget reset issues
)

# Show text box only if "Other" is picked
if region == "Other":
    other_region = st.text_input("Please specify your region:")
    region = other_region if other_region.strip() else "Other"
# Log button
if region:  # only show if they picked a region
    if st.button("Submit Region"):
        try:
            airtable.create({
                "Timestamp": str(datetime.now()),
                "Region": region
            })
            st.success(f"Thank you! Anoymously Logged: {region}")
        except Exception as e:
            st.error("Could not log. Check Airtable setup.")             
         
st.subheader("Tick all symptoms that apply:")
st.caption("No personal data is will be stored.")
col1, col2 = st.columns(2)
    
    # 25-point total system
with col1:
    coughing = 2 if st.checkbox("Coughing") else 0
    constant_cough_2weeks = 4 if st.checkbox("Constant cough for 2 weeks or more") else 0 
    fever = 2 if st.checkbox("Fever") else 0
    sweats = 2 if st.checkbox("Night sweats") else 0
    weight = 2 if st.checkbox("Unexplained weight loss") else 0
with col2:
    fatigue = 1 if st.checkbox("Tiredness or fatigue") else 0
    chest_pain = 2 if st.checkbox("Often experience chest pain") else 0
    blood_or_sputum = 4 if st.checkbox("Coughing up blood or sputum") else 0
    appetite = 2 if st.checkbox("Loss of appetite") else 0
    contact = 4 if st.checkbox("Had recent contact with someone infected with TB") else 0
        
if st.button("calculate My Risk", type="primary"):
        
    score = sum([coughing, constant_cough_2weeks, fever, sweats, weight, fatigue, chest_pain, blood_or_sputum, appetite, contact])
    st.divider()
    if score == 0:
                 st.success(f"You reported no TB symptoms. Keep monitoring your health.")
    elif score >= 20:
                st.warning(f"HIGH RISK!! Please visit a clinic for TB screening as soon as possible")
    elif score >=10:
                st.warning(f"Moderate risk. Although you are not at high risk, you should pay attention to any new symptoms that may develop or consider visiting a clinic for TB testing.")
    else:
                 st.warning(f"Low risk. Stay aware :)")
            
    st.caption("Disclaimer: This is not a medical diagnosis. Please consult a healthcare professional for TB testing and advice")

with tab2:
    st.header("What is TB?")
    st.markdown("""
    **WHAT IS TUBERCULOSIS (TB)?**
    

    Tuberculosis (TB) is a serious contagious infection cause by Mycobacterium tuberculosis bacteria that primarily attacks the lungs (pulmonary TB), but can attack other parts of the body.

    **HOW DOES TB SPREAD?**
    
    
    Tuberculosis is spread through the air from person to person when someone with active lung or throat TB coughs, sneezes, speaks or sings. These bacteria can remain suspended in the air for several hours, infecting others who breathe them in, particularly in enclosed, poorly ventilated or crowd spaces.

    **FACTORS AFFECTING SPREAD**
    
    
    Close contact: People with active TB are most likely to spread it to those they spend time with everyday, such as family members, friends, coworkers, or schoolmates 
    
    Duration: Prolonged exposure to an infected person increases the risk of infection.
    
    Immune system: People with weak immune systems (e.g., HIV, malnutrition, diabetes) are at higher risk of developing active TB if exposed.

    **COMMON SYMPTOMS:**
    
    
    -Coughing lasting up to 2 weeks or more
    
    -Unexplained weight loss
    
    -Night sweats and fever
    
    -COUGHING UP BLOOD OR PHLEGM
    
    -Chest pain and weakness

    **WHY IS IT SERIOUS IN SOUTH AFRICA?**
    
    
    Tuberculosis (TB) is one of the most pressing public health challenges in South Africa. SA is on the top three lists of 30 high burden countries for TB and
    HIV-associated TB (TB/HIV) [South African Department of Health]. About 56,000 people die from TB each year in South Africa.

    **PREVENTING THE SPREAD**
    
    
    Treatment: People with active TB usually stop being contagious 2 to 3 weeeks after starting proper treatment.
    
    Ventilation: Using fans or opening windows to ensure fresh air moves around can reduce transmission risk.
    
    Hygiene: Covering the mouth when coughing or sneezing and wearing a mask  can help reduce the release of bacteria.

    **THE GOOD NEWS:**
    
    
    TB IS CURABLE!! With a standard 6-month course of four antimicrobial drugs. Treatment for active TB is highly effective when followed correctly, preventing further infection and resistance. Drug-resistant TB requires longer, more complex, and specialised treatment regimens.

    **WHEN TO GET TESTED:**
    
    
    If you have a cough for 2+ weeks OR any 2+ symptoms above, visit your nearest clinic for a FREE TB test.


    **Information from:**
    
    https://www.mayoclinic.org
    
    https://www.cdc.gov > tb > signs-symptoms
    
    https://www.health.gov.za
    
    Please visit the National Department of Health, Mayo Clinic or Centers for Disease Control and Prevention websites for more information regarding Tuberculosis.""")

with tab3:
    st.header("Credits")
    st.info("""
TB Risk Screening Tool
Created for Tritech 2026

Developer: Reabetswe Ramahlako

Location: Limpopo

Built with: Python + Tkinter

Scoring based on WHO TB Guidelines

Disclaimer: This is an educational tool only.
Not a substitute for professional medical diagnosis.

\u00A9 PulmoDetect""")
                                       

