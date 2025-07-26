import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

if "loaded" not in st.session_state:
    st.session_state.loaded = False

if not st.session_state.loaded:
    splash = st.empty()

    image_urls = [
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-k1AoNwPz3uxZaY74Lwbuxi0s2YAuyE.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-OFwUiXE5rQRHFHmyeQ3A174tB4u8Bi.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-XD0GNDAjf6X8YzYPC0aue1AIDkSkAE.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-0aLqwSnKzPm4EvWb5O4VOKRI5UzEAe.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-NBPjBaumLic9HVjpwW1VDllE8BT5kS.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-lCvW4p3khtoganHdqFzwxmQszzsKjS.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-iw8rjXa0BkX4F5beyqkOA3ekkaEBIe.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-bAouzi32HRwdlSwaIBBO3LDSkehEiT.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-qHD0Vvr8KcM7QcTI2yKSWNpgEfqQ1h.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-kILVA3oqftLkuC8xOSdmnIqJnMcs9A.png&w=320&q=75",
        "https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-vWNtze4PKzNocMU83mA7XPHKksu5En.png&w=320&q=75"
    ]

    for img_url in image_urls:
        with splash.container():
            st.markdown(
                f"""
                <div style='display: flex; flex-direction: column; align-items: center;'>
                    <img src="{img_url}" width="200" />
                    <p style='margin-top: 20px; font-size: 20px;'>Airbnb Price Estimator Loading...</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        time.sleep(0.1) 

    splash.empty()
    st.session_state.loaded = True


city_neighbourhood_df = pd.read_csv('F-city_neighbourhood_map.csv')
airbnb_raw = pd.read_csv('G-featured_airbnb.csv')

st.markdown("<h1 style='color:#FF4B4B;'>California Airbnb Price Estimator</h1>", unsafe_allow_html=True)
st.write("""
> This app predicts the **California Airbnb** prices!

> Data obtained from the [Inside Airbnb](http://insideairbnb.com/get-the-data.html) website.
""")

st.sidebar.image("assets/airbnb_logo.svg.png", use_container_width=True)
st.sidebar.header('Input Features')

def user_input_features():
    city = st.sidebar.selectbox('🔸 City', 
    ['Los Angeles', 'Oakland', 'Pacific Grove', 'San Diego', 'San Francisco', 
    'San Mateo County', 'Santa Clara County', 'Santa Cruz County'], help="Select the city where the Airbnb is located.")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        availability_365 = st.slider('🔸 Availability (days/year)', 1, 365, 313, help="Number of days the property is available in a year.")
        listings_per_host = st.slider('🔸 Listings per Host', 1, 1088, 939, help="Total listings by the host.")

    with col2:
        avg_reviews_per_host = st.slider('🔸 Avg. Reviews/Host', 0, 448, 391, help="Average number of reviews per host.")
        neighbourhood_density = st.slider('🔸 Airbnb Density', 20, 1800, 1575, help="No. of listings in the neighbourhood.")
    
    room_type = st.sidebar.selectbox('🔸 Room Type', 
        ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'], help="Type of room offered in the Airbnb listing.")
    
    min_nights_group = st.sidebar.selectbox('🔸 Minimum Nights', 
        ['Up to 3 days', 'Up to 10 days', 'Up to 3 months', 'Long term rental'], help="Minimum number of nights required for booking.")
    
    city_neighbourhoods = city_neighbourhood_df[city_neighbourhood_df['city'] == city.lower()]['neighbourhood'].unique().tolist()
    selected_neighbourhoods = st.sidebar.multiselect(
    '🔸 Select Neighbourhood', 
    city_neighbourhoods,
    default=[city_neighbourhoods[0]], help="Select one or more neighbourhoods in the chosen city."
    )

    landmarks = ['Silicon_Valley(PaloAlto)', 'Stanford_University', 'LAX(Los Angeles International)', 
                 'SFO(San Francisco International)', 'SAN(San Diego International)', 'Golden_Gate_Bridge', 
                 'Santa_Monica_Pier', 'Venice_Beach', 'Disneyland', 'Hollywood_WalkOfFame', 
                 'Universal_Studios', 'Griffith_Observatory', 'Big_Sur', 'Yosemite_Valley', 'Lake_Tahoe']
    
    selected_landmark = st.sidebar.selectbox('🔸 Distance to:', landmarks, 
    index=landmarks.index('SFO(San Francisco International)'), help="Select a landmark to calculate distance from the Airbnb location.")


    distance_col = f'dist_to_{selected_landmark}(in kms)'
    min_distance = float(airbnb_raw[distance_col].min())
    max_distance = float(airbnb_raw[distance_col].max())
    default_distance = float(airbnb_raw[distance_col].max())

    distance_to_landmark = st.sidebar.slider(
    f'dist_to_{selected_landmark}(in kms)', 
    min_distance, 
    max_distance, 
    default_distance,
    0.1
    )

    all_neighbourhoods = city_neighbourhood_df['neighbourhood'].unique().tolist()
    
    feature_names = ['availability_365', 'listings_per_host', 'avg_reviews_per_host', 'neighbourhood_freq',
        'dist_to_Silicon_Valley(PaloAlto)(in kms)', 'dist_to_Stanford_University(in kms)', 
        'dist_to_LAX(Los Angeles International)(in kms)', 'dist_to_SFO(San Francisco International)(in kms)', 
        'dist_to_SAN(San Diego International)(in kms)', 'dist_to_Golden_Gate_Bridge(in kms)', 
        'dist_to_Santa_Monica_Pier(in kms)', 'dist_to_Venice_Beach(in kms)', 'dist_to_Disneyland(in kms)', 
        'dist_to_Hollywood_WalkOfFame(in kms)', 'dist_to_Universal_Studios(in kms)', 
        'dist_to_Griffith_Observatory(in kms)', 'dist_to_Big_Sur(in kms)', 'dist_to_Yosemite_Valley(in kms)', 
        'dist_to_Lake_Tahoe(in kms)', 'room_type_Entire home/apt', 'room_type_Hotel room', 
        'room_type_Private room', 'room_type_Shared room', 'min_nights_group_long_term_rental', 
        'min_nights_group_upto_10_days', 'min_nights_group_upto_3_days', 'min_nights_group_upto_3_months', 
        'review_density', 'city_los angeles', 'city_oakland', 'city_pacific grove', 'city_san diego', 
        'city_san francisco', 'city_san mateo county', 'city_santa clara county', 
        'city_santa cruz county'] + [f'neighbourhood_{n}' for n in all_neighbourhoods]

    data = {name: 0 for name in feature_names}
    
    data['availability_365'] = availability_365
    data['listings_per_host'] = listings_per_host
    data['avg_reviews_per_host'] = avg_reviews_per_host
    data['neighbourhood_freq'] = neighbourhood_density
    data[f'dist_to_{selected_landmark}(in kms)'] = distance_to_landmark
    data[f'room_type_{room_type}'] = 1
    
    min_nights_map = {
        'Up to 3 days': 'min_nights_group_upto_3_days',
        'Up to 10 days': 'min_nights_group_upto_10_days', 
        'Up to 3 months': 'min_nights_group_upto_3_months',
        'Long term rental': 'min_nights_group_long_term_rental'
    }
    data[min_nights_map[min_nights_group]] = 1
    
    city_map = {
        'Los Angeles': 'city_los angeles',
        'Oakland': 'city_oakland',
        'Pacific Grove': 'city_pacific grove', 
        'San Diego': 'city_san diego',
        'San Francisco': 'city_san francisco',
        'San Mateo County': 'city_san mateo county',
        'Santa Clara County': 'city_santa clara county',
        'Santa Cruz County': 'city_santa cruz county'
    }
    data[city_map[city]] = 1
    
    for neighbourhood in selected_neighbourhoods:
        data[f'neighbourhood_{neighbourhood}'] = 1

    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 15px; justify-content: flex-start;">
        <img src="https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-e0904rWYQ29GCwVnLKDYLOjvAXcSXy.png&w=3840&q=75" 
             width="40" 
             style="vertical-align: middle;">
        <h3 style="color:#FFFFFF; margin: 0; line-height: 1; vertical-align: middle; white-space: nowrap;">User Input Summary</h3>
    </div>
    """,
    unsafe_allow_html=True
)
st.dataframe(input_df)

selected_neighbourhoods = []
for col in input_df.columns:
    if col.startswith('neighbourhood_') and input_df[col].iloc[0] == 1:
        neighbourhood_name = col.replace('neighbourhood_', '')
        selected_neighbourhoods.append(neighbourhood_name)

if selected_neighbourhoods:
    st.markdown(
         """
    <div style="display: flex; align-items: center; gap: 15px; justify-content: flex-start;">
        <img src="https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-igeoKPShP33E35sBtTGol79NGhHQlK.png&w=320&q=75" 
             width="40" 
             style="vertical-align: middle;">
        <h3 style="color:#FFFFFF; margin: 0; line-height: 1; vertical-align: middle; white-space: nowrap;">Selected Neighbourhood(s)</h3>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.write(", ".join(selected_neighbourhoods))
    
    all_coords = []
    for neighbourhood in selected_neighbourhoods:
        neighbourhood_col = f'neighbourhood_{neighbourhood}'
        if neighbourhood_col in airbnb_raw.columns:
            matching_rows = airbnb_raw[airbnb_raw[neighbourhood_col] == 1]
            if not matching_rows.empty and 'latitude' in matching_rows.columns and 'longitude' in matching_rows.columns:
                coords = matching_rows[['latitude', 'longitude']].drop_duplicates()
                all_coords.append(coords)
    
    if all_coords:
        coords_df = pd.concat(all_coords, ignore_index=True)
        st.markdown(
         """
    <div style="display: flex; align-items: center; gap: 15px; justify-content: flex-start;">
        <img src="https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-JgVvskF7j2zQ9LmIWmnCHHInmpJcTJ.png&w=3840&q=75" 
             width="40" 
             style="vertical-align: middle;">
        <h3 style="color:#FFFFFF; margin: 0; line-height: 1; vertical-align: middle; white-space: nowrap;">Selected Neighbourhood(s) on Map</h3>
    </div>
    """,
    unsafe_allow_html=True
    )
        st.map(coords_df)
        st.caption("__Note: Map shows all Airbnb locations in selected neighbourhood(s), not filtered by other criteria.__")
    else:
        st.write("No coordinates available for selected neighbourhoods")

try:
    load_model = pickle.load(open('I-airbnb_price_estimator_model.pkl', 'rb'))
    
    exclude_columns = ['price', 'latitude', 'longitude']
    model_features = [col for col in airbnb_raw.columns if col not in exclude_columns]
    
    for col in model_features:
        if col not in input_df.columns:
            input_df[col] = 0
    
    input_df = input_df[model_features]
    
    prediction = load_model.predict(input_df)
    
    st.markdown(
         """
    <div style="display: flex; align-items: center; gap: 15px; justify-content: flex-start;">
        <img src="https://www.thiings.co/_next/image?url=https%3A%2F%2Flftz25oez4aqbxpq.public.blob.vercel-storage.com%2Fimage-wnzXfGqb6aI838iS9TCufJSh2ToJP8.png&w=320&q=75" 
             width="40" 
             style="vertical-align: middle;">
        <h3 style="color:#FFFFFF; margin: 0; line-height: 1; vertical-align: middle; white-space: nowrap;">Price Prediction</h3>
    </div>
    """,
    unsafe_allow_html=True
    )

    predicted_price = np.expm1(prediction[0])
    st.write(f'**Estimated Price: ${predicted_price:.2f} per night**')
    
    if predicted_price < 250:
        st.write("**Budget-friendly option**")
    elif predicted_price < 500:
        st.write("**Mid-range pricing**")
    elif predicted_price < 1000:
        st.write("**Premium pricing**")
    else:
        st.write("**Luxury pricing**")

except Exception as e:
    st.error(f"Error loading model or making prediction: {str(e)}")
    st.write("Please ensure the model file 'I-airbnb_price_estimator_model.pkl' exists and the feature engineering matches the training data.")


st.markdown("""
<hr>
<p style='text-align: center; color: gray;'>
Built using Streamlit | By Niharika
</p>
""", unsafe_allow_html=True)

