import streamlit as st
import pandas as pd
import mysql.connector

# MySQL connection
myconnection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='1441',
    database='redbusscrape'
)
mycursor = myconnection.cursor()

# Load the DataFrame
df = pd.read_csv("C:/Users/nsjag/Downloads/redbusdatanew.csv")

# Streamlit title
st.title("RED BUS")

# Sidebar navigation
r = st.sidebar.radio("Redbus", ["About us", "Home"])

if r == "About us":
    st.write("Visit us at: https://www.redbus.in/")
    tab1, tab2 = st.tabs(["USERS", "FAMILY"])
    tab1.image(r'C:\Users\nsjag\OneDrive\Pictures\Screenshots\Screenshot 2024-10-23 163204.png')
    tab2.image(r'C:\Users\nsjag\OneDrive\Pictures\Screenshots\Screenshot 2024-10-23 163214.png')
    st.markdown(":bus: Enjoy a Cozy and Memorable Bus Travel with redbus :bus:")
    st.success("Have a memorable journey")
    st.balloons()

elif r == "Home":
    # Sidebar inputs
    col1 = st.sidebar.selectbox("Route Name", df["route_name"].unique())
    col2 = st.sidebar.selectbox("Bus Type", ["A/C Sleeper and Seater", "Non A/C Sleeper and Seater", "A/C Semi-Sleeper"])
    
    # Slider for price
    min_price, max_price = st.sidebar.slider("Price", min_value=200, max_value=5000, value=(200, 5000), step=10)
    
    # Slider for star rating with one decimal
    min_rating, max_rating = st.sidebar.slider("Star Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1)
    
    # Slider for seats available
    min_seat, max_seat = st.sidebar.slider("Seats Available", min_value=1, max_value=76, value=(1, 76), step=1)

    # Define filter conditions for each bus type category
    if col2 == "A/C Sleeper and Seater":
        bustype_filter = "(bustype LIKE '%A/C%' AND (bustype LIKE '%Sleeper%' OR bustype LIKE '%Seater%'))"
    elif col2 == "Non A/C Sleeper and Seater":
        bustype_filter = "(bustype LIKE '%NON A/C%' AND (bustype LIKE '%Sleeper%' OR bustype LIKE '%Seater%'))"
    elif col2 == "A/C Semi-Sleeper":
        bustype_filter = "(bustype LIKE '%A/C%' AND bustype LIKE '%Semi Sleeper%')"
    else:
        bustype_filter = "1=1"  # No filter if none selected

    # SQL query with filtering
    query = f"""
        SELECT * FROM busdata 
        WHERE route_name = %s
        AND {bustype_filter}
        AND price BETWEEN %s AND %s 
        AND star_rating BETWEEN %s AND %s 
        AND seats_available BETWEEN %s AND %s
        ORDER BY route_name ASC
    """
    
    # Execute the query with parameters
    mycursor.execute(query, (col1, min_price, max_price, min_rating, max_rating, min_seat, max_seat))
    
    # Fetching data
    data = mycursor.fetchall()
    
    # Creating DataFrame if data is found
    if data:
        data_df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
        
        # Format the star ratings to one decimal place
        if 'star_rating' in data_df.columns:
            data_df['star_rating'] = data_df['star_rating'].apply(lambda x: f"{x:.1f}")
        
        # Round the price values
        if 'price' in data_df.columns:
            data_df['price'] = data_df['price'].round()

        st.dataframe(data_df, use_container_width=True)
    else:
        st.write("No data found matching the criteria.")
    
# Close the MySQL connection
mycursor.close()
myconnection.close()
