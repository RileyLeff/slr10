import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import norm

st.title('Riley\'s Seawater Inundation Rate Calculator')

# User inputs
st.sidebar.header('Parameters')
htf = st.sidebar.slider('High Tide Flood Threshold', 0.0, 5.0, 2.5, 0.1)
std_dev = st.sidebar.slider('Standard Dev In Annual Distribution Of Daily High Tide', 0.1, 5.0, 1.0, 0.1)

# User-entered range for mean
st.sidebar.header('Mean Sea Level Increase')
mean_min = st.sidebar.number_input('Current Sea Level', value=0.0, step=0.1)
mean_max = st.sidebar.number_input('Maximum Future Sea Level Of Interest', value=5.0, step=0.1)

# Ensure mean_max is always greater than mean_min
if mean_max <= mean_min:
    mean_max = mean_min + 0.1
    st.sidebar.warning('Maximum Sea Level Cannot Be Less Than Current/Minimum.')

# Calculate flood rate
@st.cache_data
def calculate_flood_rate(mean, htf, std_dev):
    return 1 - norm.cdf(htf, mean, std_dev)

# Generate data
means = np.linspace(mean_min, mean_max, 100)
flood_rates = [calculate_flood_rate(mean, htf, std_dev) for mean in means]

# Create DataFrame
df = pd.DataFrame({'Change In Mean High Sea Level': means, 'Inundation Frequency': flood_rates})

# Create plot
fig = px.line(df, x='Change In Mean High Sea Level', y='Inundation Frequency', 
              title=f'Inundation Frequency vs. Change In Mean High Tide (HTF={htf}, σ={std_dev})')
fig.update_layout(yaxis_range=[0, 1])

# Display plot
st.plotly_chart(fig)