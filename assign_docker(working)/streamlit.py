import streamlit as st
import requests
import pandas as pd
import plotly.express as px


def main():
    #title and index 
    st.set_page_config(page_title="Hugging face models WEB UI", page_icon="🐦", layout="centered", initial_sidebar_state="auto", menu_items=None)
    st.title("Calculate Vectara and toxicity values for your string 🐦")
    

    sent_string=st.text_input("Enter your string in format (sentence1. sentence2) Add atleast 1 fullstop")
    
    #handling string input
    if st.button("Submit"):
        if sent_string:            
            try:
                response = requests.post(url = f"http://127.0.0.1:8000/call_model/{sent_string}")
                json_data = response.json()
                st.write(f'Received text: “{json_data["Received text:"]}”')
                st.write("Response:")
                st.write(f'Vectara: {json_data["Vectara"]}')
                st.write(f'Toxicity: {json_data["Toxicity"]}')
                
            except Exception as e:
                json_data = {"error":"String entered in wrong format or incorrect type"}
                st.write(json_data)

    #sidebar for graph, table output
    with st.sidebar:      
        st.title("Print Graph and table:")
        
        #create graph
        if st.button("Fetch Graph"):
            response = requests.get(url = "http://127.0.0.1:8000/table_graph")
            if response.status_code == 200:
                json_data = response.json()
                df = pd.json_normalize(json_data)
                fig = px.scatter(df, x="vectara", y="toxicity", color_discrete_sequence=['red'],title="Scatter plot for vectara vs toxicity")
                
                #updating graph background and plot color
                fig.update_layout(
                    plot_bgcolor="white",  
                    paper_bgcolor="black",     
                    font=dict(color="black")   
                )
                
                st.plotly_chart(fig)
            else:
                st.error("Error fetching graph data.")



        #create table
        if st.button("Fetch Table Data"):
            response = requests.get(url = "http://127.0.0.1:8000/table_graph")

            if response.status_code == 200:
                json_data = response.json()     
                df = pd.json_normalize(json_data)     
                st.dataframe(df, hide_index=True) 
            else:
                st.error("Error fetching table data.")

if __name__ == "__main__":
     main()
