import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page config
st.set_page_config(page_title='Data Visualizer',
                   layout='centered',
                   page_icon='📊')

# Title
st.title('📊  Data Visualizer')

working_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the folder where your CSV files are located
folder_path = f"{working_dir}/data"  # Update this to your folder path

# List all files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Dropdown to select multiple files
selected_files = st.multiselect('Select files', files)

if selected_files:
    combined_df = pd.DataFrame()  # Initialize an empty dataframe

    for selected_file in selected_files:
        # Construct the full path to the file
        file_path = os.path.join(folder_path, selected_file)

        try:
            # Read the selected CSV file with error handling for encoding issues
            df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Try different encodings if needed
        except UnicodeDecodeError:
            st.error(f"Error loading {selected_file}. Please check the file encoding.")
            continue

        # Merge columns by concatenating all files into one dataframe (ignores index for proper concatenation)
        combined_df = pd.concat([combined_df, df], axis=0, ignore_index=True)

    if not combined_df.empty:
        # Once the files are merged, show the combined data
        st.write("Combined Data:")
        st.write(combined_df.head())

        # Get the merged column list
        columns = combined_df.columns.tolist()

        col1, col2 = st.columns(2)

        with col1:
            # Allow the user to select columns for plotting from the merged columns
            x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
            y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

        with col2:
            plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
            # Allow the user to select the type of plot
            plot_type = st.selectbox('Select the type of plot', options=plot_list)

        # Generate the plot based on user selection
        if st.button('Generate Plot'):

            fig, ax = plt.subplots(figsize=(6, 4))

            if plot_type == 'Line Plot':
                sns.lineplot(x=combined_df[x_axis], y=combined_df[y_axis], ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(x=combined_df[x_axis], y=combined_df[y_axis], ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=combined_df[x_axis], y=combined_df[y_axis], ax=ax)
            elif plot_type == 'Distribution Plot':
                sns.histplot(combined_df[x_axis], kde=True, ax=ax)
                y_axis = 'Density'
            elif plot_type == 'Count Plot':
                sns.countplot(x=combined_df[x_axis], ax=ax)
                y_axis = 'Count'

            # Adjust label sizes
            ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
            ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

            # Adjust title and axis labels with a smaller font size
            plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
            plt.xlabel(x_axis, fontsize=10)
            plt.ylabel(y_axis, fontsize=10)

            # Show the results
            st.pyplot(fig)
