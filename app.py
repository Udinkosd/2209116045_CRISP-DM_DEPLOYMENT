import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import matplotlib.ticker as mtick
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt


df = pd.read_csv('Data Cleaned.csv')

def display_introduction():
    st.subheader("Pengenalan")
    st.markdown("""
    Dataset ini berisi informasi tentang gaji karyawan di sebuah perusahaan. 
    Setiap baris mewakili seorang karyawan yang berbeda, dan kolom-kolomnya mencakup informasi 
    seperti usia, jenis kelamin, tingkat pendidikan, jabatan, tahun pengalaman, dan gaji.

    **Kolom:**

    - Usia: Kolom ini menunjukkan usia setiap karyawan dalam tahun. Nilai-nilai dalam kolom ini bersifat numerik.

    - Jenis Kelamin: Kolom ini berisi jenis kelamin setiap karyawan, yang dapat berupa laki-laki atau perempuan. 
    Nilai-nilai dalam kolom ini bersifat kategorikal.

    - Tingkat Pendidikan: Kolom ini berisi tingkat pendidikan setiap karyawan, yang dapat berupa 
    sekolah menengah, gelar sarjana, gelar magister, atau gelar doktor. Nilai-nilai dalam kolom ini 
    bersifat kategorikal.

    - Jabatan: Kolom ini berisi jabatan setiap karyawan. Jabatan-jabatan dapat bervariasi 
    tergantung pada perusahaan dan dapat mencakup posisi seperti manajer, analis, insinyur, 
    atau administrator. Nilai-nilai dalam kolom ini bersifat kategorikal.

    - Pengalaman Kerja: Kolom ini mewakili jumlah tahun pengalaman kerja setiap karyawan. 
    Nilai-nilai dalam kolom ini bersifat numerik.

    - Gaji: Kolom ini mewakili gaji tahunan setiap karyawan dalam dolar AS. Nilai-nilai 
    dalam kolom ini bersifat numerik dan dapat bervariasi tergantung pada faktor seperti 
    jabatan, tahun pengalaman, dan tingkat pendidikan.
    """)

def display_data_section():
    st.subheader("Dataset")
    st.dataframe(df)
    st.markdown("""
    Berikut adalah rangkuman dari dataset:

    Jumlah responden berdasarkan tingkat pendidikan dan jenis kelamin:
    | Gender | Tingkat Pendidikan | Jumlah |
    |--------|--------------------|--------|
    | Female | Sarjana            | 103    |
    |        | Magister           | 50     |
    |        | Doktor             | 26     |
    | Male   | Sarjana            | 121    |
    |        | Magister           | 48     |
    |        | Doktor             | 25     |
    ---------------------------------------
    - Usia Tertua: 53
    - Usia Termuda: 23
    - Usia Rata-rata: 37
    ---------------------------------------
    - Gaji Tertinggi: $250,000
    - Gaji Terendah: $350
    - Gaji Rata-rata: $100,577
    ---------------------------------------
    - Pengalaman Kerja Tertinggi: 25 tahun
    - Pengalaman Kerja Terendah: 0 tahun
    - Rata-rata Pengalaman Kerja: 10.03 tahun
    """)

def display_gender_distribution():
    st.subheader("Distribusi Jenis Kelamin")
    st.write("Choose colors for bars:")
    col1, col2 = st.columns([1, 9])
    with col1:
        male_color = st.color_picker("Male bars", "#1f77b4")
    with col2:
        female_color = st.color_picker("Female bars", "#ff7f0e")

    gender_counts = df['Gender'].value_counts()
    colors = [male_color, female_color]
    explode = (0.1, 0)
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('none') 
    gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=colors, explode=explode, ax=ax)
    ax.set_title('Perbandingan Jumlah Laki-laki dan Perempuan', color='white')
    ax.tick_params(axis='both', labelcolor='white')
    st.pyplot(fig, bbox_inches='tight', pad_inches=0)
    st.markdown("""
    Pie Chart

    Dalam diagram tersebut, menunjukkan jumlah responden dalam dataset, 
    terdapat 48% wanita dan sisanya yaitu 52% adalah pria.

    ---------------------------------------
    """)

def filter_data_by_age(df, age):
    return df[df['Age'] == age]
        
def age_slider():
    st.subheader("Distribusi Pendidikan berdasarkan Jenis Kelamin dan Umur")
    age = st.slider('Select Age', min_value=23, max_value=53, value=30)
    filtered_data = filter_data_by_age(df, age)
    display_education_by_gender(filtered_data, age)

def display_education_by_gender(filtered_df=None, age=None):
    if filtered_df is None or age is None:
        return
    else:
        st.write("Choose colors for bars:")
        col1, col2 = st.columns([1, 9])
        with col1:
            male_color = st.color_picker("Male bars", "#1f77b2")
        with col2:
            female_color = st.color_picker("Female bars", "#ff7f0c")
        male_counts = filtered_df[filtered_df['Gender'] == 'Male']['Education Level'].value_counts()
        female_counts = filtered_df[filtered_df['Gender'] == 'Female']['Education Level'].value_counts()

        levels = ["Bachelor's", "Master's", 'PhD']
        bar_width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))

        male_bars = ax.bar(np.arange(len(levels)), [male_counts.get(level, 0) for level in levels], bar_width, label='Male', color=male_color)
        female_bars = ax.bar(np.arange(len(levels)) + bar_width, [female_counts.get(level, 0) for level in levels], bar_width, label='Female', color=female_color)

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
    st.write("Choose colors for bars:")
    col1, col2 = st.columns([1, 9])
    with col1:
        male_color = st.color_picker("Male bars", "#1f77b3")
    with col2:
        female_color = st.color_picker("Female bars", "#ff7f0a")

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

    st.markdown("""
    | Gender | Tingkat Pendidikan | Jumlah |
    |--------|--------------------|--------|
    | Female | Sarjana            | 103    |
    |        | Magister           | 50     |
    |        | Doktor             | 26     |
    | Male   | Sarjana            | 121    |
    |        | Magister           | 48     |
    |        | Doktor             | 25     |
    """)
    st.markdown("""
    ---------------------------------------
    Dalam diagram Bar tersebut, erlihat bahwa mayoritas responden 
    memiliki gelar sarjana (Bachelor's), diikuti oleh gelar master (Master's) dan gelar doktor (PhD). 
    Meskipun demikian, terdapat perbedaan kecil antara jumlah laki-laki dan 
    perempuan dalam setiap tingkat pendidikan. Pada tingkat pendidikan sarjana, 
    terdapat sedikit lebih banyak laki-laki daripada perempuan, sementara pada 
    tingkat pendidikan master dan doktor, jumlah perempuan sedikit lebih banyak daripada laki-laki.
    """)
    st.markdown("""
    ---------------------------------------
    """)

def display_age_x_salary():
    df_filtered = df.dropna(subset=['Age', 'Salary', 'Years of Experience'])

    # Scatter Plot
    st.subheader('Hubungan Antara Usia dan Pendapatan')
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
    ax.set_ylabel('Pendapatan Per Tahun')
    st.pyplot(fig)
    st.markdown("""
        ---------------------------------------
        Dalam scatter plot di atas, terlihat bahwa usia 23 tahun adalah yang paling muda, 
        sementara usia 53 tahun adalah yang tertua. Di rentang usia 23 hingga 25 tahun, 
        terdapat 5 responden dengan gaji di bawah 50 ribu USD per tahun. Salah satu dari responden 
        berusia 25 tahun memiliki gaji paling rendah di rentang tersebut, yaitu sebesar 30 ribu USD. 
        Di rentang usia di atas 50 tahun hingga 53 tahun, terdapat 9 responden. 
        Gaji terendah adalah 140 ribu USD dan yang tertinggi adalah 250 ribu USD, 
        dengan salah satu responden berusia 52 tahun.        
        """)
    st.markdown("""
    ---------------------------------------
    """)

    st.subheader('Hubungan Antara Tahun Pengalaman dan Pendapatan')
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
    ax.set_ylabel('Pendapatan Per Tahun')
    ax.set_title('Ukuran gelembung: Tahun Pengalaman')
    st.pyplot(fig)

    st.markdown("""
        ---------------------------------------
        Dalam bubble plot di atas, yang menggambarkan hubungan antara tahun pengalaman 
        dan gaji per tahun, terlihat bahwa pengalaman terendah adalah 0 tahun dan yang tertinggi 
        adalah 25 tahun. Di rentang 0 tahun hingga 5 tahun, terdapat 36 responden. 
        Seorang responden dengan pengalaman 1 tahun memiliki gaji di bawah 20 ribu USD, 
        sementara yang tertinggi adalah seorang responden dengan pengalaman 5 tahun yang 
        memiliki gaji di atas 80 ribu USD per tahun.

        - Gaji Tertinggi: $250,000
        - Gaji Terendah: $350
        - Gaji Rata-rata: $100,577
        ---------------------------------------
        - Pengalaman Kerja Tertinggi: 25 tahun
        - Pengalaman Kerja Terendah: 0 tahun
        - Rata-rata Pengalaman Kerja: 10.03 tahun 
        """)
    st.markdown("""
    ---------------------------------------
    """)

def display_salary_by_gender(df):
    st.subheader('Perbandingan Gaji berdasarkan Jenis Kelamin')
    min_salary = df['Salary'].min()
    max_salary = df['Salary'].max()
    min_experience = df['Years of Experience'].min()
    max_experience = df['Years of Experience'].max()

    selected_salary = st.slider('Pilih Gaji:', min_salary, max_salary, (min_salary, max_salary))
    selected_experience = st.slider('Pilih Tahun Pengalaman:', min_experience, max_experience, (min_experience, max_experience))

    filtered_data = df[
        (df['Salary'] >= selected_salary[0]) & (df['Salary'] <= selected_salary[1]) &
        (df['Years of Experience'] >= selected_experience[0]) & (df['Years of Experience'] <= selected_experience[1])
    ]

    avg_salary = filtered_data.groupby(['Gender', 'Years of Experience'])['Salary'].mean().unstack()

    col1, col2 = st.columns([1, 9])
    with col1:
        male_color = st.color_picker("Male bars", "#1f77b4")
    with col2:
        female_color = st.color_picker("Female bars", "#ff7f0e")

    fig, ax = plt.subplots(figsize=(12, 8))

    male_data = avg_salary.loc['Male']
    ax.plot(male_data.index, male_data, marker='o', label='Male', color=male_color)

    female_data = avg_salary.loc['Female']
    ax.plot(female_data.index, female_data, marker='o', label='Female', color=female_color)

    ax.set_title('Average Salary by Gender and Years of Experience')
    ax.set_xlabel('Years of Experience')
    ax.set_ylabel('Average Salary ($)')
    ax.legend()
    ax.grid(True)
    ax.set_xticklabels(ax.get_xticks(), rotation=45)
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    st.pyplot(fig)
    
    st.markdown("""
        ---------------------------------------
        Pada data di atas, terlihat bahwa rata-rata gaji berdasarkan pengalaman kerja menunjukkan 
        variasi yang signifikan. Gaji tertinggi mencapai USD250,000 pertahun, 
        sementara yang terendah berada di bawah USD50,000 pertahun. Data ini menunjukkan bahwa 
        semakin tinggi pengalaman kerja seseorang, semakin tinggi pula gaji yang diterima, baik 
        untuk perempuan maupun laki-laki. Selain itu, tidak terdapat perbedaan gaji yang signifikan 
        antara jenis kelamin dalam dataset ini. 
        
        Namun, perlu diperhatikan bahwa meskipun terlihat 
        perbedaan gaji meski memiliki pengalaman yang sama, hal itu dipengaruhi oleh perbedaan posisi 
        yang dipegang oleh responden di perusahaan masing-masing. Sebagai contoh, dalam data tersebut, 
        terlihat bahwa laki-laki memiliki gaji lebih tinggi dibandingkan dengan perempuan. Perbedaan ini 
        dipengaruhi oleh faktor seperti gelar lulusan dan posisi dalam perusahaan, di mana laki-laki 
        mungkin menduduki posisi CEO sedangkan perempuan adalah Direktur.
        """)
    st.markdown("""
    ---------------------------------------
    """)
    
def display_education_level(df):
    df_filtered = df.dropna(subset=['Education Level'])

    education_counts = df_filtered['Education Level'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(education_counts, labels=education_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Education Levels')
    plt.axis('equal')
    st.pyplot()

def display_composition(df):
    st.subheader('Diagram Komposisi Dataset')
    columns_of_interest = ['Gender', 'Education Level']

    for column in columns_of_interest:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(f'Composition of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Count')
        df[column].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    st.dataframe(df)
    st.markdown("""
    ---------------------------------------
    | Gender | Tingkat Pendidikan | Jumlah |
    |--------|--------------------|--------|
    | Female | Sarjana            | 103    |
    |        | Magister           | 50     |
    |        | Doktor             | 26     |
    | Male   | Sarjana            | 121    |
    |        | Magister           | 48     |
    |        | Doktor             | 25     |
    ---------------------------------------
    - Usia Tertua: 53
    - Usia Termuda: 23
    - Usia Rata-rata: 37
    ---------------------------------------
    - Gaji Tertinggi: $250,000
    - Gaji Terendah: $350
    - Gaji Rata-rata: $100,577
    ---------------------------------------
    - Pengalaman Kerja Tertinggi: 25 tahun
    - Pengalaman Kerja Terendah: 0 tahun
    - Rata-rata Pengalaman Kerja: 10.03 tahun
        """)
    st.markdown("""
    ---------------------------------------
    """)

def display_kmeans(df):
    df.dropna(inplace=True)

    label_encoder = LabelEncoder()
    df['Gender'] = label_encoder.fit_transform(df['Gender'])
    df['Education Level'] = label_encoder.fit_transform(df['Education Level'])
    df['Job Title'] = label_encoder.fit_transform(df['Job Title'])

    X = df[['Age', 'Gender', 'Education Level', 'Years of Experience', 'Salary']]

    k = 3

    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)

    plt.figure(figsize=(10, 6))
    plt.scatter(X.iloc[:, 0], X.iloc[:, 4], c=df['Cluster'], cmap='viridis')
    plt.title('K-means Clustering')
    plt.xlabel('Age')
    plt.ylabel('Salary')
    plt.colorbar(label='Cluster')
    st.pyplot(plt)

    st.markdown("""
    ---------------------------------------
    """)

    st.subheader('Tabel Cluster')

    selected_cluster = st.slider('Pilih Cluster:', 0, k-1, 0)

    filtered_df = df[df['Cluster'] == selected_cluster]

    st.write(filtered_df)
    st.markdown("""
    Dalam diagram k-means clustering tersebut, terdapat tiga cluster yaitu cluster 0, 1 dan 2.
    """)
    st.markdown("""
    ---------------------------------------
    """)

    st.subheader('Statistik Cluster')

    cluster_stats = filtered_df.groupby('Cluster').agg(
        Usia_Tertua=('Age', 'max'),
        Usia_Termuda=('Age', 'min'),
        Usia_Rata_rata=('Age', 'mean'),
        Jumlah_Perempuan=('Gender', 'sum'),
        Jumlah_Laki_laki=('Gender', lambda x: x.eq(0).sum()),
        Jumlah_Pendidikan_S1=('Education Level', lambda x: x.eq(0).sum()),
        Jumlah_Pendidikan_S2=('Education Level', lambda x: x.eq(1).sum()),
        Jumlah_Pendidikan_S3=('Education Level', lambda x: x.eq(2).sum()),
        Tahun_Pengalaman_Tertinggi=('Years of Experience', 'max'),
        Tahun_Pengalaman_Terendah=('Years of Experience', 'min'),
        Tahun_Pengalaman_Rata_rata=('Years of Experience', 'mean'),
        Gaji_Tertinggi=('Salary', 'max'),
        Gaji_Terendah=('Salary', 'min'),
        Gaji_Rata_rata=('Salary', 'mean')
    )

    st.write(cluster_stats.iloc[:, :3])
    st.write(cluster_stats.iloc[:, 3:6])
    st.write(cluster_stats.iloc[:, 6:9])
    st.write(cluster_stats.iloc[:, 9:])

    st.markdown("""
    Dalam tabel tersebut, kita dapat melihat beberapa statistik penting terkait 
    dengan cluster data. Misalnya, kita bisa melihat usia tertua dan termuda, rata-rata usia, 
    tahun pengalaman, dan gaji rata-rata. Pada kasus ini, pada cluster 1 terlihat bahwa usia 
    tertua adalah 40 tahun, sementara yang termuda adalah 23 tahun. Rata-rata usia pada 
    cluster 1 sendiri adalah 30 tahun. Selain itu, terdapat informasi 
    tentang jumlah perempuan dan laki-laki dalam setiap cluster, 
    di mana dalam cluster tersebut terdapat 67 perempuan dan 68 laki-laki. 
    Selain itu, terdapat beberapa statistik clustering lainnya yang dapat 
    dilihat pada tabel statistik cluster tersebut
    """)
    st.markdown("""
    ---------------------------------------
    """)

def main():
    st.sidebar.title("Selamat Datang!")

    sections = ["Pengenalan", "Data", "Distribusi", "Hubungan", "Perbandingan", "Komposisi", "Clustering"]
    selected_section = st.sidebar.radio("Pilih Halaman", sections)

    st.title("Job Salary Dashboard")

    if selected_section == "Pengenalan":
        display_introduction()
        st.write("You are viewing the Introduction section.")
    elif selected_section == "Data":
        display_data_section()
        st.write("You are viewing the Data section.")
    elif selected_section == "Distribusi":
        display_gender_distribution()
        age_slider()
        display_age_education_distribution(df)
        st.write("You are viewing the Distribution section.")
    elif selected_section == "Hubungan":
        display_age_x_salary()
        st.write("You are viewing the Relation section.")
    elif selected_section == "Perbandingan":
        display_salary_by_gender(df)
        st.write("You are viewing the Comparison section.")
    elif selected_section == "Komposisi":
        display_composition(df)
        st.write("You are viewing the Composition section.")
    elif selected_section == "Clustering":
        display_kmeans(df)
        st.write("You are viewing the Clustering section.")

if __name__ == "__main__":
    main()
