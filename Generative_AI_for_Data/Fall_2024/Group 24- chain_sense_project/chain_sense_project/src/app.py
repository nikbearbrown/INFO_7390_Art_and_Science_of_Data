import streamlit as st
from rag_pipeline import answer_query_with_weather
from utils.fetch_weather import fetch_weather

# Streamlit App Title
st.title("ChainSense: Supply Chain Intelligence with Weather Insights")

# Section 1: Supply Chain Query
st.subheader("Ask Supply Chain Questions")
user_query = st.text_input("Ask about supply chain disruptions, logistics, etc.")
if st.button("Get Supply Chain Answer"):
    if user_query.strip():
        with st.spinner("Generating answer..."):
            try:
                # Query the RAG pipeline
                answer = answer_query_with_weather(user_query)
                st.write("**Answer:**")
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query to get an answer.")

# Section 2: Real-time Weather Insights
st.subheader("Real-time Weather Insights")
location = st.text_input("Enter a location to fetch weather data:")
if st.button("Get Weather Insights"):
    if location.strip():
        with st.spinner(f"Fetching weather data for {location}..."):
            try:
                # Fetch real-time weather data
                weather = fetch_weather(location)
                if "error" in weather:
                    st.error(weather["error"])
                else:
                    # Display weather information
                    st.write(f"**Weather for {weather['location']}**")
                    st.write(f"**Latitude:** {weather['latitude']}")
                    st.write(f"**Longitude:** {weather['longitude']}")
                    st.write(f"**Temperature:** {weather['temperature']}°C")
                    st.write(f"**Wind Speed:** {weather['wind_speed']} km/h")
                    st.write(f"**Description Code:** {weather['description']}")
            except Exception as e:
                st.error(f"Error fetching weather data: {e}")
    else:
        st.warning("Please enter a location to fetch weather data.")

# Section 3: Combined Insights
st.subheader("Supply Chain & Weather Impact Analysis")
sc_query = st.text_input("Ask a question combining supply chain and weather insights:")
if st.button("Analyze Combined Impact"):
    if sc_query.strip() and location.strip():
        with st.spinner(f"Analyzing combined impact for {location}..."):
            try:
                # Fetch weather data
                weather = fetch_weather(location)
                if "error" in weather:
                    st.error(weather["error"])
                else:
                    # Generate a combined insight
                    combined_context = f"""
                    **Weather Context:**
                    - Location: {weather['location']}
                    - Latitude: {weather['latitude']}
                    - Longitude: {weather['longitude']}
                    - Temperature: {weather['temperature']}°C
                    - Wind Speed: {weather['wind_speed']} km/h
                    - Description: {weather['description']}
                    
                    **Supply Chain Context:**
                    {answer_query_with_weather(sc_query, location)}
                    """
                    st.write("**Combined Insight:**")
                    st.write(combined_context)
            except Exception as e:
                st.error(f"Error during combined analysis: {e}")
    else:
        st.warning("Please enter a query and location for combined analysis.")


# - above code is the most updated and running 

# import streamlit as st
# from rag_pipeline import answer_query_with_weather

# st.title("Supply Chain and Weather Query Tool")

# query = st.text_input("Enter your supply chain query:")
# location = st.text_input("Enter a location for weather insights (optional):")

# if query:
#     answer = answer_query_with_weather(query, location)
#     st.write(answer)






#correct -below code

# import streamlit as st
# from rag_pipeline import answer_query
# from utils.fetch_weather import fetch_weather

# st.title("ChainSense: Supply Chain Intelligence with Weather Insights")

# # Supply Chain Query Section
# st.subheader("Ask Supply Chain Questions")
# user_query = st.text_input("Ask about supply chain disruptions, logistics, etc.")
# if st.button("Get Answer"):
#     if user_query.strip():
#         with st.spinner("Generating answer..."):
#             answer = answer_query(user_query)
#             st.write("**Answer:**")
#             st.write(answer)

# # Weather Section
# st.subheader("Real-time Weather Insights")
# location = st.text_input("Enter a location to fetch weather data:")
# if st.button("Get Weather"):
#     if location.strip():
#         with st.spinner(f"Fetching weather data for {location}..."):
#             weather = fetch_weather(location)
#             if "error" in weather:
#                 st.error(weather["error"])
#             else:
#                 st.write(f"**Weather for {weather['location']}**")
#                 st.write(f"Latitude: {weather['latitude']}")
#                 st.write(f"Longitude: {weather['longitude']}")
#                 st.write(f"Temperature: {weather['temperature']}°C")
#                 st.write(f"Wind Speed: {weather['wind_speed']} km/h")
#                 st.write(f"Description Code: {weather['description']}")



# import streamlit as st
# from rag_pipeline import answer_query

# st.title("ChainSense: RAG-Powered Supply Chain Intelligence")

# user_query = st.text_input("Ask about supply chain disruptions, logistics, etc.:")
# if st.button("Get Answer"):
#     if user_query.strip():
#         with st.spinner("Generating answer..."):
#             answer = answer_query(user_query)
#         st.write("**Answer:**")
#         st.write(answer)
