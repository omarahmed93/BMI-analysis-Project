import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import os

st.set_page_config(page_title="Data Dashboard", layout="wide")



df=pd.read_csv("/Users/omartharwat/Desktop/Eplison/mid-project/body_performance.csv")

st.title("Blood Pressure & BMI Explorer")