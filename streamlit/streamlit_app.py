import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Pokémon Data Visualizer")
st.markdown("Visualizing data locally while running core services in the Docker 'Cloud'.")



TYPE_COLORS = {
    'Normal': '#A8A878', 'Fire': '#F08030', 'Water': '#6890F0', 'Grass': '#78C850',
    'Electric': '#F8D030', 'Ice': '#98D8D8', 'Fighting': '#C03028', 'Poison': '#A040A0',
    'Ground': '#E0C068', 'Flying': '#A890F0', 'Psychic': '#F85888', 'Bug': '#A8B820',
    'Rock': '#B8A038', 'Ghost': '#705898', 'Dragon': '#7038F8', 'Steel': '#B8B8D0',
    'Dark': '#705848', 'Fairy': '#EE99AC', 'NaN': '#DCDCDC' # Default color for NaN/missing type
}



def color_type_cells(val):
    val_str = str(val) if pd.notna(val) else 'NaN'

    color = TYPE_COLORS.get(val_str, TYPE_COLORS['NaN'])

    return f'background-color: {color}; color: #000000; font-weight: bold; border-radius: 5px; text-align: center;'


@st.cache_data
def load_data():
    """Loads the Pokémon dataset from the mounted volume path."""
    try:
        # File is accessed via the volume mount path defined in docker-compose.yml
        # Note: We set pandas options *before* reading the file to ensure the full DF is loaded 
        # for inspection later, although st.dataframe() handles display limits well.
        
        # Load the data
        df = pd.read_csv('/app/data/pokemonSet.csv') 
        
        # Data cleaning/preparation
        df['Name_Clean'] = df['Name'].apply(lambda x: x.split('Mega')[0].strip())
        
        return df
    except FileNotFoundError:
        st.error("Error: 'pokemonSet.csv' not found at /app/data/. Check your volume mount.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.subheader("Data Preview")
    
    
   
    df_display = df.copy()
    df_display['Legendary'] = df_display['Legendary'].map({True: '👑', False: '🚫'})


    styled_df = df.style.applymap(color_type_cells, subset = ['Type 1', 'Type 2'])

    st.dataframe(styled_df)



   

    def plot_total_stats_distribution(data):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data['Total'], bins=20, kde=True, ax=ax, color='red')
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
    
    def plot_element_distribution(data):
        fig, ax = plt.subplots(figsize=(12, 6))
        type1_counts = data['Type 1'].value_counts()
        
        # Create a palette that matches the order of the types
        palette = [TYPE_COLORS.get(t, TYPE_COLORS['NaN']) for t in type1_counts.index]
        
        sns.barplot(x=type1_counts.index, y=type1_counts.values, palette=palette, ax=ax)
        
        ax.set_title('Distribution of Primary Pokémon Types')
        ax.set_xlabel('Type')
        ax.set_ylabel('Count')
        
        # Rotate labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        return fig
    

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Total Stat Distribution")
        st.pyplot(plot_total_stats_distribution(df))

    with col2:
        st.subheader("Attack vs. Defense")
        st.pyplot(plot_attack_vs_defense(df))


    st.markdown("---")
    st.subheader("Element Type Distribution")
    st.pyplot(plot_element_distribution(df))


