import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import matplotlib.ticker as mtick
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Data Cleaned.csv')

def display_introduction():
    st.subheader("Introduction")
    st.markdown("""
    This dataset contains information about the salaries of employees at a company. 
    Each row represents a different employee, and the columns include information such as age, gender, education level, job title, years of experience, and salary.

    **Columns:**

    - **Age:** This column represents the age of each employee in years. The values in this column are numeric.

    - **Gender:** This column contains the gender of each employee, which can be either male or female. The values in this column are categorical.

    - **Education Level:** This column contains the educational level of each employee, which can be high school, bachelor's degree, master's degree, or PhD. The values in this column are categorical.

    - **Job Title:** This column contains the job title of each employee. The job titles can vary depending on the company and may include positions such as manager, analyst, engineer, or administrator. The values in this column are categorical.

    - **Years of Experience:** This column represents the number of years of work experience of each employee. The values in this column are numeric.

    - **Salary:** This column represents the annual salary of each employee in US dollars. The values in this column are numeric and can vary depending on factors such as job title, years of experience, and education level.
    """)

def display_data_section():
    st.subheader("Dataset")
    st.write("""
    This is the data section.
    You can provide options to interact with your data here.
    """)
    st.dataframe(df)

def display_gender_distribution():
    st.write("Choose colors for bars:")
    col1, col2 = st.columns([1, 9])
    with col1:
        male_color = st.color_picker("Male bars", "#1f77b4")
    with col2:
        female_color = st.color_picker("Female bars", "#ff7f0e")

    st.subheader("Gender Distribution")
    gender_counts = df['Gender'].value_counts()
    colors = [male_color, female_color]
    explode = (0.1, 0)
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('none') # Set the facecolor of the plot to 'none'
    gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=colors, explode=explode, ax=ax)
    ax.set_title('Perbandingan Jumlah Laki-laki dan Perempuan', color='white') # Change the title color to white
    ax.tick_params(axis='both', labelcolor='white') # Change the tick label color to white
    st.pyplot(fig, bbox_inches='tight', pad_inches=0)

    st.write("""
    This is the data section.
    You can provide options to interact with your data here.
    """)

def filter_data_by_age(df, age):
    return df[df['Age'] == age]

def age_slider():
    st.title('Education Level Distribution by Gender and Age')

    age = st.slider('Select Age', min_value=23, max_value=53, value=30)
    filtered_data = filter_data_by_age(df, age)
    display_education_by_gender(filtered_data, age)

def display_education_by_gender(filtered_df=None, age=None):
    st.subheader("Education Level Distribution by Gender and Age")
    if filtered_df is None or age is None:
        return
    else:
        male_counts = filtered_df[filtered_df['Gender'] == 'Male']['Education Level'].value_counts()
        female_counts = filtered_df[filtered_df['Gender'] == 'Female']['Education Level'].value_counts()

        levels = ["Bachelor's", "Master's", 'PhD']
        bar_width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))

        male_bars = ax.bar(np.arange(len(levels)), [male_counts.get(level, 0) for level in levels], bar_width, label='Male', color='yellow')
        female_bars = ax.bar(np.arange(len(levels)) + bar_width, [female_counts.get(level, 0) for level in levels], bar_width, label='Female', color='red')

        ax.set_xlabel('Education Level')
        ax.set_ylabel('Count')
        ax.set_title(f'Education Level Distribution at Age {age}')
        ax.set_xticks(np.arange(len(levels)) + bar_width / 2)
        ax.set_xticklabels(levels)
        ax.legend()

        for i in range(len(levels)):
            ax.text(male_bars[i].get_x() + male_bars[i].get_width() / 2., male_bars[i].get_height(),
                    male_counts.get(levels[i], 0), ha='center', va='bottom')
            ax.text(female_bars[i].get_x() + female_bars[i].get_width() / 2., female_bars[i].get_height(),
                    female_counts.get(levels[i], 0), ha='center', va='bottom')

        plt.tight_layout()

        st.pyplot(fig)

def display_age_education_distribution(df):
    st.subheader("Education Level Distribution by Age")

    st.write("Choose colors for bars:")
    col1, col2 = st.columns([1, 9])
    with col1:
        male_color = st.color_picker("Male bars", "#1f77b4")
    with col2:
        female_color = st.color_picker("Female bars", "#ff7f0e")

    education_counts = df.groupby(['Education Level', 'Gender']).size()
    education_counts = education_counts.reset_index(name='Count')
    chart = alt.Chart(education_counts).mark_bar().encode(
        x='Education Level:N',
        y='Count:Q',
        color=alt.Color('Gender:N', scale=alt.Scale(domain=['Male', 'Female'], range=[male_color, female_color])),
        tooltip=['Education Level', 'Gender', 'Count']
    ).properties(
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=14
    )

    st.altair_chart(chart, use_container_width=True)

def display_age_x_salary():
    df_filtered = df.dropna(subset=['Age', 'Salary', 'Years of Experience'])

    # Scatter Plot
    st.subheader('Scatter Plot: Hubungan Antara Usia dan Pendapatan')
    min_salary = df_filtered['Salary'].min()
    max_salary = df_filtered['Salary'].max()
    min_age = df_filtered['Age'].min()
    max_age = df_filtered['Age'].max()

    selected_salary = st.slider('Pilih Gaji:', min_salary, max_salary, (min_salary, max_salary))
    selected_age = st.slider('Pilih Usia:', min_age, max_age, (min_age, max_age))

    filtered_data = df_filtered[
        (df_filtered['Salary'] >= selected_salary[0]) & (df_filtered['Salary'] <= selected_salary[1]) &
        (df_filtered['Age'] >= selected_age[0]) & (df_filtered['Age'] <= selected_age[1])
    ]

    x = filtered_data['Age'].values
    y = filtered_data['Salary'].values

    fig, ax = plt.subplots()
    ax.scatter(x, y, s=50, c='blue', alpha=0.5)
    ax.set_xlabel('Usia')
    ax.set_ylabel('Pendapatan')
    st.pyplot(fig)

    # Bubble Chart
    st.subheader('Bubble Chart: Hubungan Antara Tahun Pengalaman dan Pendapatan')
    min_experience = df_filtered['Years of Experience'].min()
    max_experience = df_filtered['Years of Experience'].max()

    selected_experience = st.slider('Pilih Tahun Pengalaman:', min_experience, max_experience, (min_experience, max_experience))

    filtered_data_bubble = df_filtered[
        (df_filtered['Salary'] >= selected_salary[0]) & (df_filtered['Salary'] <= selected_salary[1]) &
        (df_filtered['Years of Experience'] >= selected_experience[0]) & (df_filtered['Years of Experience'] <= selected_experience[1])
    ]

    z = filtered_data_bubble['Years of Experience'].values
    y_bubble = filtered_data_bubble['Salary'].values

    fig, ax = plt.subplots()
    ax.scatter(z, y_bubble, s=50, c='red', alpha=0.5)
    ax.set_xlabel('Tahun Pengalaman')
    ax.set_ylabel('Pendapatan')
    ax.set_title('Ukuran gelembung: Tahun Pengalaman')
    st.pyplot(fig)

def display_salary_by_gender(df):
    # Filter data for male and female
    male_data = df[df['Gender'] == 'Male']
    female_data = df[df['Gender'] == 'Female']

    # Create a line chart
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(male_data['Years of Experience'], male_data['Salary'], label='Male', color='blue')
    ax.plot(female_data['Years of Experience'], female_data['Salary'], label='Female', color='orange')

    # Set chart title and labels
    ax.set_title('Salary by Years of Experience and Gender')
    ax.set_xlabel('Years of Experience')
    ax.set_ylabel('Salary')
    ax.legend()

    # Set limits for x and y axis
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 250000)

    # Display the chart
    st.pyplot(fig)

def display_education_level(df):
    # Filter out rows with missing values
    df_filtered = df.dropna(subset=['Education Level'])

    # Count the number of individuals for each education level
    education_counts = df_filtered['Education Level'].value_counts()

    # Plotting
    plt.figure(figsize=(8, 8))
    plt.pie(education_counts, labels=education_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Education Levels')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot()

def display_composition(df):
    # Select the columns you're interested in
    columns_of_interest = ['Gender', 'Education Level', 'Job Title']

    # Iterate over each column and plot a bar chart
    for column in columns_of_interest:
        plt.figure(figsize=(10, 6))
        plt.title(f'Composition of {column}')
        plt.xlabel(column)
        plt.ylabel('Count')
        df[column].value_counts().plot(kind='bar')
        st.pyplot()

def main():
    st.sidebar.title("Job Salary")

    section = st.sidebar.radio("Navigate", ("Introduction", "Data", "Gender Distribution", 
    "Age Distribution", "Education Distribution","Age and Salary Relation", 
    "Gender by Salary Comparison", "Education Levels", "Composition" ))

    if section == "Introduction":
        display_introduction()
        st.write("You are viewing the Introduction section.")
    elif section == "Data":
        display_data_section()
        st.write("You are viewing the Data section.")
    elif section == "Gender Distribution":
        display_gender_distribution()
        st.write("You are viewing the Gender Distribution section.")
    elif section == "Age Distribution":
        age_slider()
        st.write("You are viewing the Age Distribution section.")
    elif section == "Education Distribution":
        display_age_education_distribution(df)
        st.write("You are viewing the Age Distribution section.")
    elif section == "Age and Salary Relation":
        display_age_x_salary()
        st.write("You are viewing the Age and Salary Relation section.")
    elif section =="Gender by Salary Comparison":
        display_salary_by_gender(df)
        st.write("You are viewing the Gender and Salary Comparison section.")
    elif section == "Education Levels":
        st.write(display_education_level(df))
    elif section == "Composition":
        display_composition(df)
        st.write("You are viewing the Composition section.")

if __name__ == "__main__":
    main()
