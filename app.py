import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.graph_objects as go

# -------------- Sheets Connection ----------------
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(worksheet='dashboard')



# --------------- FUNCTIONS --------------------

def days_achieved(item):
    succrt = item +'SuccRt'
    succ = item + 'Succ'
    goal = item + 'Goal'
    avg = item + 'Avg'
    chg = item + 'AvgChg'
    chg_cell = selected_row[chg]
    progress = selected_row[succrt]
    
    color = '#7ABD7E' if progress == 100 else \
            '#F8D66D' if progress < 85.71428571428571 and progress > 71.42857142857143 else \
            '#FFB54C' if progress < 57.14285714285714 and progress > 42.857142857142855 else \
            '#FF6961'
    
    arrow = '🔼' if chg_cell > 0 else '' if chg_cell == 0 else '🔽'        
    # subtext = 'Days' if 'Sleep' not in item else 'Nights'
            
    fig = go.Figure(go.Pie(
        values=[progress, 100 - progress],
        hole=0.85,
        marker={'colors': [color, 'lightgray']},
        sort=False,
        showlegend=False,
        textinfo='none'
    ))
    
    # Add text on the graph
    fig.add_annotation(
        text=f'{selected_row[succ]}/{selected_row[goal]}',
        x=0.5,
        y=0.58,
        font={'size': 28, 'color': 'black'},
        showarrow=False
    )
    
    fig.add_annotation(
        text=f'Avg mins: {selected_row[avg]} {arrow}',
        x=0.5,
        y=0.3,
        font={'size': 14, 'color': 'gray'},
        showarrow=False
    )
    
    fig.update_layout(
        height=180,
        width=180,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    return fig




def lift_chg(lift_name):
    weight = lift_name + '1RM'
    chg = lift_name +'Chg'
    lbs = str(selected_row[weight])
    progress = selected_row[chg]
    
    color = '#7ABD7E' if progress >= 0 else '#FF6961'
    
    # Add up arrow or down arrow to subtext
    arrow = '⏫' if progress >= 10 else '⏬' if progress <= -10 else '🔼' if progress > 0 else '🔽' if progress < 0 else ''
    subtext_with_arrow = arrow + ' ' + str(progress) + '%'
    
    fig = go.Figure(go.Pie(
        values=[100, 0],
        hole=0.85,
        marker={'colors': [color, 'lightgray']},
        sort=False,
        showlegend=False,
        textinfo='none'
    ))
    
    # Add text on the graph
    fig.add_annotation(
        text=lbs + ' lbs',
        x=0.5,
        y=0.58,
        font={'size': 28, 'color': 'black'},
        showarrow=False
    )
    
    fig.add_annotation(
        text=subtext_with_arrow,
        x=0.5,
        y=0.3,
        font={'size': 14, 'color': 'gray'},
        showarrow=False
    )
    
    fig.update_layout(
        height=180,
        width=180,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    return fig




def hrv(item):
    avg = item + 'Avg'
    chg = item + 'Chg'
    chg_cell = selected_row[chg]
    avg_cell = selected_row[avg]
    color = '#7ABD7E' if chg_cell >= -50 else '#FF6961'
    
    # Add up arrow or down arrow to subtext
    arrow = '⏫' if chg_cell >= 10 else '⏬' if chg_cell <= -10 else '🔼' if chg_cell > 0 else '🔽' if chg_cell < 0 else ''
    subtext_with_arrow = arrow + ' ' + str(chg_cell) + '%'
    
    fig = go.Figure(go.Pie(
        values=[100, 0],
        hole=0.85,
        marker={'colors': [color, 'lightgray']},
        sort=False,
        showlegend=False,
        textinfo='none'
    ))
    
    # Add text on the graph
    fig.add_annotation(
        text=f'{avg_cell}',
        x=0.5,
        y=0.58,
        font={'size': 28, 'color': 'black'},
        showarrow=False
    )
    
    fig.add_annotation(
        text=subtext_with_arrow,
        x=0.5,
        y=0.3,
        font={'size': 14, 'color': 'gray'},
        showarrow=False
    )
    
    fig.update_layout(
        height=180,
        width=180,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    return fig



# --------------- APP --------------------

title_col, dropdown_col = st.columns(spec=[.65,.35])
with title_col:
    st.header("Week's Review")
    
    st.subheader('1RMs') 

with dropdown_col:
    st.write('')
    st.write('')
    selected_date = st.selectbox('Select a week', df['Dates'])
    selected_row = df[df['Dates'] == selected_date].squeeze()


"---"
col1, col2, col3 = st.columns(3)
# Add content to the three columns
with col1:
    fig1 = lift_chg('BenchPress') 
    st.write("Bench Press")
    st.plotly_chart(fig1)

with col2:
    fig2 = lift_chg('Deadlift') 
    st.write("Deadlift")
    st.plotly_chart(fig2)
    
with col3:
    fig3 = lift_chg('Squat') 
    st.write("Squat")
    st.plotly_chart(fig3)

st.write('')
st.subheader('Inputs')
"---"

col4, col5 = st.columns(2)

with col4:
    st.write('Protein')
    fig4 = days_achieved('Protein') 
    st.plotly_chart(fig4)


with col5:
    st.write('Steps')
    fig5 = days_achieved('Steps') 
    st.plotly_chart(fig5)
    
st.write('')  
st.subheader('Rest')
"---"
col6, col7, col8 = st.columns(3)

with col6:
    st.write('HRV')
    fig6 = hrv('HRV')
    st.plotly_chart(fig6)

with col7:
    st.write('Deep Sleep')
    fig7 = days_achieved('DeepSleep') 
    st.plotly_chart(fig7)
    
with col8:
    st.write('REM Sleep')
    fig8 = days_achieved('REMSleep') 
    st.plotly_chart(fig8)
