import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import os

st.set_page_config(page_title="Data Dashboard", layout="wide")

CSV_PATH = "/Users/omartharwat/Desktop/Eplison/mid-project/bodyPerformance_cleaned.csv"
CACHE_PATH = CSV_PATH + ".parquet"  # or .pkl if you prefer pickle

def load_body_performance():
    if os.path.exists(CACHE_PATH) and os.path.getmtime(CACHE_PATH) >= os.path.getmtime(CSV_PATH):
        return pd.read_parquet(CACHE_PATH)  # or pd.read_pickle
    df = pd.read_csv(CSV_PATH)
    df.to_parquet(CACHE_PATH)  # cache for next time
    return df

df = load_body_performance()

st.title("Blood Pressure & BMI Explorer")
st.caption("Interactively explore vitals, BMI, and performance classes from the bodyPerformance dataset.")

tab_overview, tab_bmi, physical_analysis, tab_quality,strength_enduranc = st.tabs(
    ["Overview", "BMI", "physical_analysis", "Segmentation", "Strength & Endurance"]
)

# ---------------- Sidebar filters ---------------- #
with st.sidebar:
    st.header("Filter Options")
    gender_filter = st.multiselect("Gender", sorted(df["gender"].unique()),
                                   default=sorted(df["gender"].unique()))
    class_filter = st.multiselect("Class", sorted(df["class"].unique()),
                                  default=sorted(df["class"].unique()))
    age_range = st.slider(
        "Age range",
        float(df["age"].min()), float(df["age"].max()),
        (float(df["age"].min()), float(df["age"].max()))
    )
    bmi_range = st.slider(
        "BMI range",
        float(df["BMI"].min()), float(df["BMI"].max()),
        (float(df["BMI"].min()), float(df["BMI"].max()))
    )
    exerices_filter = st.multiselect("Exercises", sorted(df.columns[7:11]),
                                  default=sorted(df.columns[7:11]))

# ------------- Filter DataFrame ------------------ #
filtered = df[
    df["gender"].isin(gender_filter)
    & df["class"].isin(class_filter)
    & df["age"].between(*age_range)
    & df["BMI"].between(*bmi_range)
    & df[exerices_filter].notnull().all(axis=1)
]

# ------------- OVERVIEW TAB ---------------------- #
with tab_overview:
    st.subheader("KPI Data Overview")

    col2, col3, col4 = st.columns(3)
    col2.metric("Avg Systolic BP", f"{filtered['systolic'].mean():.2f}")
    col3.metric("Avg Diastolic BP", f"{filtered['diastolic'].mean():.2f}")
    col4.metric("Avg BMI", f"{filtered['BMI'].mean():.2f}")

    st.subheader("Strength & Endurance Trends BY age")

    chart_col1,chart_col2 = st.columns(2)

    grip_force_fig = px.bar(
        filtered.groupby(["age_group", "age"])["gripForce"].mean().reset_index(),
        x="age",
        y="gripForce",
        color="age_group",
        template="plotly_dark",
  
    )

    situps_fig = px.scatter(
        filtered.groupby(['age','age_group'])['sit-ups counts'].mean().reset_index(),
        x="age",
        y="sit-ups counts",
        color="age_group",
        template="plotly_dark",
   
    )
    board_fig=px.scatter(
        filtered.groupby(['age','age_group'])['broad jump_cm'].mean().reset_index(),
        x="age",
        y="broad jump_cm",
        color="age_group",
        template="plotly_dark",
    )
    sit_and_becnh_fig = px.histogram(
        filtered.groupby(['age','age_group'])['sit and bend forward_cm'].mean().reset_index(),
        x="age",
        y="sit and bend forward_cm",
        color="age_group",
        template="plotly_dark",
    )

    with chart_col1:
        st.subheader("Sit-ups Counts by Age")
        st.plotly_chart(situps_fig, use_container_width=True)

    with chart_col2:
        st.subheader("Grip Force by Age Group")
        st.plotly_chart(grip_force_fig, use_container_width=True)
    with chart_col1:
        st.subheader("Broad Jump by Age")
        st.plotly_chart(board_fig, use_container_width=True)   
    with chart_col2:
        st.subheader("Sit and Reach by Age")
        st.plotly_chart(sit_and_becnh_fig, use_container_width=True)     
# ------------- BMI TAB ---------------------- #
with tab_bmi:
    st.subheader("BMI Analysis")

    col1,col2,col3 = st.columns(3)

    chart_col1,chart_col2 = st.columns(2)
    #---------------KPI----------------------#
    col1.metric("BMI Avrage", f"{filtered['BMI'].mean():.2f}")
    col2.metric("systolic Average", f"{df['systolic'].mean():.2f}")
    col3.metric("diastolic Average", f"{df['diastolic'].mean():.2f}")
    # ---------------Figures---------------------#
    

    #----------fig1-------------------#
    bmi_fig = px.histogram(
        filtered.groupby(['BMI','bmi_category'])['systolic'].mean().reset_index(),
        x="bmi_category",
        y='systolic',
        color="bmi_category",
        nbins=30,
        template="plotly_dark",
        title="BMI Distribution by Performance Class & systolic Blood Pressure",
    )
    bmi_fig.update_layout(bargap=0.1 ,
    xaxis_title="BMI",
    yaxis_title="Systolic Blood Pressure")
    #-----------fig2--------------------------#
    bmi_fig2=px.histogram(filtered.groupby(['BMI','bmi_category'])['diastolic'].mean().reset_index(),
    x='bmi_category',
    y='diastolic',
    color='bmi_category'
    ,template="plotly_dark"
    ,title="BMI vs Diastolic Blood Pressure",
    nbins=30)

    bmi_fig2.update_layout(bargap=0.1 ,
    xaxis_title="BMI",
    yaxis_title="Diastolic Blood Pressure")
# ---------------fig3---------------------#
    bmi_fig3=px.line(filtered.groupby('age_group')['BMI'].mean().reset_index(),
    x='age_group',
    y='BMI'
,template="plotly_dark")
#---------------fig4----------------------#
    bmi_fig4=px.scatter(filtered,x='BMI',y='systolic',color='bmi_category',template="plotly_dark")
    #---------fig5---------------------#
    
    #----------------plotting------------------#
    with chart_col1:
        st.plotly_chart(bmi_fig, use_container_width=True)
    with chart_col2:
        st.plotly_chart(bmi_fig2, use_container_width=True)
    with chart_col1:
        st.plotly_chart(bmi_fig3, use_container_width=True)
    with chart_col2:
        st.plotly_chart(bmi_fig4, use_container_width=True) 
      

# ------------- physical_analysis TAB ---------------------- #    
with physical_analysis:
    st.subheader("Physical Analysis")
    col1,col2,col3,col4 = st.columns(4)
    chart_col1,chart_col2 = st.columns(2)
    #---------------KPI----------------------#
    col1.metric("Avg Grip Force", f"{filtered['gripForce'].mean():.2f}")
    col2.metric("Avg Sit-ups Counts", f"{filtered['sit-ups counts'].mean():.2f}")
    col3.metric("Avg Broad Jump (cm)", f"{filtered['broad jump_cm'].mean():.2f}")
    col4.metric("Avg Sit and Bend Forward (cm)", f"{filtered['sit and bend forward_cm'].mean():.2f}")
    # ---------------Figures---------------------#
    #----------fig1-------------------#
    grip_fig=px.histogram(filtered.groupby(['gender','age_group'])['gripForce'].mean().reset_index(),
                        x='age_group',y='gripForce',
                        color='gender',
                        title='gripForce chart',
                        template="plotly_dark")
    #-----------fig2--------------------------#
    situps_fig=px.histogram(filtered.groupby(['gender','age_group'])['sit-ups counts'].mean().reset_index(),
                       x='age_group',y='sit-ups counts'
                       ,color='gender',
                       title='sit-up counts chart',
                       template="plotly_dark")
    # ---------------fig3---------------------#
    board_fig=px.line(filtered.groupby(['age_group','gender'])['broad jump_cm'].mean().reset_index(),
                      x='age_group',y='broad jump_cm'
                           ,color='gender',
                           template="plotly_dark"
                           ,title='broad jump chart')
    #---------------fig4----------------------#
    sit_bind=px.line(filtered.groupby(['age_group','gender'])['sit and bend forward_cm'].mean().reset_index(),
                        x='age_group',y='sit and bend forward_cm',
                        color='gender'
                        ,template="plotly_dark"
                        ,title='sit and bend forward chart')
    deep_analysis=filtered.groupby(['bmi_category','body fat_%'])[['gripForce','sit-ups counts','sit and bend forward_cm','broad jump_cm']].mean().reset_index()
    fig5=px.bar(filtered,x='body fat_%',y='gripForce',color='bmi_category',template="plotly_dark",title='Body Fat % vs Grip Force by BMI Category')

    with chart_col1:
        st.plotly_chart(grip_fig, use_container_width=True)
    with chart_col2:
        st.plotly_chart(board_fig, use_container_width=True)    
    with chart_col2:
        st.plotly_chart(situps_fig, use_container_width=True)
    with chart_col1:
        st.plotly_chart(sit_bind, use_container_width=True)
         
# ------------- Segmentation TAB ---------------------- #    
with tab_quality:
    col1,col2 = st.columns(2)
    chart_col1,chart_col2 = st.columns(2)
    class_fig=px.pie(filtered,names='class',title='Performance Class Distribution',template="plotly_dark")
    age_group_fig=px.pie(filtered,names='age_group',title='Age Group Distribution',template="plotly_dark")
    gender_fig=px.pie(filtered,names='gender',title='gender distribution',template="plotly_dark")
    bmi_fig=px.pie(filtered,names='bmi_category',title='BMI Category Distribution',template="plotly_dark")
    with chart_col1:
        st.plotly_chart(class_fig, use_container_width=True)
    with chart_col2:
        st.plotly_chart(age_group_fig, use_container_width=True)
    with chart_col1:
        st.plotly_chart(gender_fig, use_container_width=True)
    with chart_col2:
        st.plotly_chart(bmi_fig, use_container_width=True)
# ------------- Strength & Endurance TAB ---------------------- #
with strength_enduranc:
    st.subheader("Strength & Endurance Analysis")
    col1,col2,col3,col4 = st.columns(4)
    chart_col1,chart_col2 = st.columns(2)
    #---------------KPI----------------------#

    metric_options = {"Grip Force": "gripForce",
                        "Sit-ups Counts": "sit-ups counts",
                        "Broad Jump (cm)": "broad jump_cm",
                        "Sit and Bend Forward (cm)": "sit and bend forward_cm" 
                        }
    group_options = ["gender", "age_group", "class","bmi_category"]

    metric_label = st.selectbox("Exercise Metric", list(metric_options.keys()))
    group_by = st.radio("Compare by", group_options, horizontal=True)

    metric_col = metric_options[metric_label]
    kpi_df = (
        filtered.groupby(group_by)[metric_col]
        .mean()
        .reset_index()
        .rename(columns={metric_col: "value"})
    )
    col1.metric(
        f"{metric_label} ({group_by})",
        f"{kpi_df['value'].mean():.2f}",
        help="Average of selected exercise metric across the filtered data",
    )
    col2.metric(
        f"Max {metric_label} ({group_by})",
        f"{kpi_df['value'].max():.2f}",
        help="Maximum of selected exercise metric across the filtered data",
    )
    col3.metric(
        f"Min {metric_label} ({group_by})",
        f"{kpi_df['value'].min():.2f}",
        help="Minimum of selected exercise metric across the filtered data",
    )
     # ---------------Figures---------------------#
     #----------fig1-------------------#
     # Bar chart for average metric by selected group
    fig = px.bar(
        kpi_df,
        x=group_by,
        y="value",
        color=group_by,
        template="plotly_dark",
        title=f"Average {metric_label} by {group_by.capitalize()}",

    )
    bodyfat_by_group = (
        filtered.groupby(group_by)["body fat_%"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        bodyfat_by_group,
        x=group_by,
        y="body fat_%",
        color=group_by,  # <- use group_by, not "gender"
        template="plotly_dark",
        title=f"Average Body Fat % by {group_by.capitalize()}",
    )

    with chart_col1:
        st.plotly_chart(fig, use_container_width=True)
    with chart_col2:
        st.plotly_chart(fig2, use_container_width=True)    