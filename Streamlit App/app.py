import pickle
import streamlit as st
import pandas as pd

teams = ['Kolkata Knight Riders',
    'Royal Challengers Bangalore',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Mumbai Indians',
    'Sunrisers Hyderabad',
    'Delhi Capitals',
    'Punjab Kings',
    'Lucknow Super Giants',
    'Gujarat Titans']

venue = ['Pune', 'Chennai', 'Delhi', 'Mumbai', 'Kolkata', 'Mohali',
    "St George's Park", 'Cuttack', 'Kingsmead',
    'Sharjah Cricket Stadium', 'Jaipur', 'Ahmedabad', 'Hyderabad',
    'New Wanderers Stadium', 'Bangalore',
    'Dubai International Cricket Stadium', 'Abu Dhabi',
    'Visakhapatnam', 'SuperSport Park', 'Raipur', 'Dharamshala',
    'Kanpur', 'Ranchi', 'Indore', 'OUTsurance Oval', 'Newlands',
    'Buffalo Park', 'Rajkot', 'Kimberley']

pipe = pickle.load(open('pipe.pkl', 'rb'))


st.title('IPL Win Probabilities')
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
    
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_stadium = st.selectbox('Select the stadium', sorted(venue))

target = st.number_input('Target')

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.number_input('Wickets out')
    
if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - overs*6
    wickets = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left
    
    input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team],
                            'venue': [selected_stadium], 'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wickets],
                            'inning1_runs': [target -1], 'crr': [crr], 'rrr': [rrr]})
    
    # st.table(input_df)
    
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + ': ' + str(round(win*100, 2)) + '%')
    st.header(bowling_team + ': ' + str(round(loss*100, 2)) + '%')
    
