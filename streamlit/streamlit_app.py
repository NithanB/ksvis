import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Pokémon Data Fog/Cloud Visualization 📊")
st.markdown("Visualizing data locally while running core services in the Docker 'Cloud'.")

@st.cache_data
def load_data():
    """Loads the Pokémon dataset from the mounted volume path."""
    try:
        # File is accessed via the volume mount path defined in docker-compose.yml
        df = pd.read_csv('/app/data/pokemonSet.csv') 
        df['Name_Clean'] = df['Name'].apply(lambda x: x.split('Mega')[0].strip())
        return df
    except FileNotFoundError:
        st.error("Error: 'pokemonSet.csv' not found at /app/data/. Check your volume mount.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.subheader("Data Preview")
    st.dataframe(df.head())

    def plot_total_stats_distribution(data):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data['Total'], bins=20, kde=True, ax=ax, color='skyblue')
        ax.set_title('Distribution of Pokémon Total Stats')
        ax.set_xlabel('Total Stats')
        ax.set_ylabel('Count')
        return fig

    def plot_attack_vs_defense(data):
        fig, ax = plt.subplots(figsize=(8, 8))
        sns.scatterplot(x='Attack', y='Defense', data=data, hue='Legendary', style='Legendary', palette='viridis', s=100, ax=ax)
        ax.set_title('Attack vs. Defense by Legendary Status')
        ax.set_xlabel('Attack Stat')
        ax.set_ylabel('Defense Stat')
        return fig

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Total Stat Distribution")
        st.pyplot(plot_total_stats_distribution(df))

    with col2:
        st.subheader("Attack vs. Defense")
        st.pyplot(plot_attack_vs_defense(df))