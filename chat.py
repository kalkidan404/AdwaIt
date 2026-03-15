import streamlit as st
import requests
import wikipedia

st.set_page_config(
    page_title="Adwa AI Assistant",
    page_icon="🇪🇹",
    layout="wide"
)

# -------------------------
# PROFESSIONAL UI STYLE
# -------------------------
st.markdown("""
<style>
/* Full background */
.stApp {
    background: url("https://i.ytimg.com/vi/Ukk1S_yFvT8/maxresdefault.jpg") no-repeat center center fixed;
    background-size: cover;
}

/* Headline - Clear background */
h1 {
    color: gold !important;
    font-weight: 900 !important;
    font-size: 50px !important;
    text-align: center;
    text-shadow: 2px 2px 10px black;
    background: none !important;
}

/* Subheaders - Clear background */
h2, h3, h4 {
    color: gold !important;
    text-shadow: 1px 1px 4px black;
}

/* WHITE BACKGROUND: Applied ONLY to Chat Messages and Informational Markdown */
/* We exclude the top-level app headers by targeting specific data-testids */
[data-testid="stChatMessage"], 
.stMarkdown p, 
.stMarkdown li {
    background-color: white !important;
    color: black !important;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 5px;
    font-weight: 500;
}

/* Ensure the Title and Subheaders don't get the white background from the rule above */
[data-testid="stHeader"], h1, h2, h3, h4 {
    background-color: transparent !important;
}

/* Chat input box */
.stTextInput>div>div>input {
    color: gold !important;
    background-color: rgba(0,0,0,0.6) !important;
    border-radius: 8px;
}

/* Navigation Buttons - Clear gold style */
button {
    background: rgba(255,215,0,0.1) !important;
    color: gold !important;
    border: 1px solid gold !important;
    border-radius: 10px !important;
}

button:hover {
    background: rgba(255,215,0,0.25) !important;
    box-shadow: 0 0 8px gold !important;
}
</style>

""", unsafe_allow_html=True)

# -------------------------
# CHAT STATE
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "view" not in st.session_state:
    st.session_state.view = "chat"  # chat, music, history, map, leaders

# -------------------------
# BUTTON DASHBOARD
# -------------------------
def render_buttons():
    cols = st.columns([1,1,1,1])
    with cols[0]:
        if st.button("🎵 Music", key="music_btn", help="Explore Adwa songs"):
            st.session_state.view = "music"
    with cols[1]:
        if st.button("📜 History", key="history_btn", help="View historical timeline"):
            st.session_state.view = "history"
    with cols[2]:
        if st.button("🗺️ Map", key="map_btn", help="View the battlefield map"):
            st.session_state.view = "map"
    with cols[3]:
        if st.button("👑 Leaders", key="leaders_btn", help="Learn about leaders"):
            st.session_state.view = "leaders"

# -------------------------
# MAIN CHAT DASHBOARD
# -------------------------
if st.session_state.view == "chat":
    st.markdown("<h1>🇪🇹 Adwa AI Chat</h1>", unsafe_allow_html=True)
    st.subheader("Ask anything about the Battle of Adwa")

    render_buttons()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input("Type your question here...")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = requests.post("http://127.0.0.1:8000/ask", json={"question": prompt})
            answer = response.json()["answer"]
        except:
            answer = "The historian is currently offline."

        st.session_state.messages.append({"role":"assistant","content":answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

# -------------------------
# MUSIC DASHBOARD
# -------------------------
elif st.session_state.view == "music":
    st.header("🎵 Adwa Songs")
    if st.button("🏠 Home", key="home_music", help="Return to chat"):
        st.session_state.view = "chat"

    songs = {
        "Victory Song 1-by GG": "https://youtu.be/fBTFdgs-hAk?si=W1ESA7wcntPvCY_F",
        "Victory Song 2-by tedi Afro": "https://youtu.be/xKrw9LIkAeU?si=fLVoJEFgbots6YsU",
        "Victory Song 3": "https://youtu.be/FiOc3ZfFRIg?si=PY7Z0KQyt5GqPenQ",
        "victory song 4-Taytu": "https://youtu.be/8avCvatwY7Q?si=h_QNGuN6sN6Q70f4",
        "Victory Song 5-by dagne walle": "https://youtu.be/RLSMEhoQfOk?si=0nm8nwylRrAv1QkH",
        "Victory Song 6": "https://youtu.be/9n2s8l7mXoE?si=0nm8nwylRrAv1QkH",
        "Victory Song 7-animation": "https://youtu.be/PuY12hDM224?si=sJQBeJmQ494s9B3V",
        "Victory Song 8-tewnet": "https://youtu.be/GklIa3IQm-E?si=AHbuVMiHe4QbpMxk",
        "Victory Song 9-by marsha taye": "https://youtu.be/riqNj-SEwsM?si=Gb0QWnVpIr-IN61J",
        "Victory Song 10-by abush zeleke": "https://youtu.be/eYq0YIVACII?si=kePduezefFaXHSD8",
        "Victory poem 11-by abebaw melaku": "https://youtu.be/TdNcAiHKClw?si=j7hpzplCAckNwTCf",
        "Victory poem 12-by loriet tsegaye": "https://youtu.be/9n2s8l7mXoE?si=0nm8nwylRrAv1QkH",
        "Victory poem 14-ye adwa feresoch": "https://youtu.be/Ac2FV7DKJEM?si=Cv_AX24o0f8Bum5k"

    }
    for name, link in songs.items():
        st.markdown(f"[{name}]({link})")

# -------------------------
# HISTORY DASHBOARD
# -------------------------
elif st.session_state.view == "history":
    st.header("📜 Adwa Historical Timeline")
    if st.button("🏠 Home", key="home_history"):
        st.session_state.view = "chat"

    period = st.selectbox("Select Time Period", [
        "1887–1889 Rising Tensions",
        "1889 Treaty of Wuchale",
        "1895–1896 First Italo-Ethiopian War",
        "1896 Battle of Adwa"
    ])

    try:
        if period == "1887–1889 Rising Tensions":
            text = wikipedia.summary("Battle of Dogali", sentences=10)
        elif period == "1889 Treaty of Wuchale":
            text = wikipedia.summary("Treaty of Wuchale", sentences=10)
        elif period == "1895–1896 First Italo-Ethiopian War":
            text = wikipedia.summary("First Italo-Ethiopian War", sentences=10)
        elif period == "1896 Battle of Adwa":
            text = wikipedia.summary("Battle of Adowa", sentences=10)
    except:
        text = "Could not retrieve history from the web."

    st.markdown(text)

# -------------------------
# MAP DASHBOARD
# -------------------------
# -------------------------
# MAP DASHBOARD
# -------------------------
elif st.session_state.view == "map":
    st.header("🗺️ Adwa Battlefield Map")
    if st.button("🏠 Home", key="home_map"):
        st.session_state.view = "chat"

    # Main map showing troop positions
    st.image(
        "https://tse3.mm.bing.net/th/id/OIP.U8UApRmcuXxpAb4Aj7fLvwHaEn?rs=1&pid=ImgDetMain&o=7&rm=3",
        caption="Strategic troop movements around the Battle of Adwa (1896)",
        width=700
    )

    # Second map showing Menelik II's troop progression
    st.image(
        "https://c8.alamy.com/comp/J2X51X/adwa-map-menelik-progression-before-battle-of-adwa-J2X51X.jpg",
        caption="Ethiopian troop movements before the Battle of Adwa (1896)",
        width=700
    )
     #third image  the battle of adwa  historical atlas
    st.image(
        "https://thebattlecastcom.files.wordpress.com/2023/01/route-of-menneliks-adwa-campaign.png",
        caption="Route of Menelik's Adwa Campaign (1896)",
        width=700
    )

    # White info box for key terrain points
    st.markdown("""
    <div style="background-color:white; color:black; padding:12px; border-radius:10px; margin-top:10px;">
             Key Terrain & Strategic Notes:<br>
        - Adwa is surrounded by rugged mountains and volcanic plugs (Soloda, Abba Garima) <br>
        - Ethiopian forces used high ground to their advantage <br>
        - Italian forces were forced into constrained valleys, making them vulnerable <br>
        - Rivers and rough terrain limited mobility, shaping the battle outcome
    </div>
    """, unsafe_allow_html=True)
# -------------------------
# LEADERS DASHBOARD
# -------------------------
# -------------------------
# LEADERS DASHBOARD
# -------------------------
# -------------------------
# LEADERS DASHBOARD
# -------------------------
elif st.session_state.view == "leaders":

    st.header("👑 Prominent Figures")

    if st.button("🏠 Home", key="home_leaders"):
        st.session_state.view = "chat"

    leaders = {
        "Emperor Menelik II": "https://www.armedconflicts.com/files/ethiopia-menelikii.jpg",
        "Empress Taytu Betul": "https://c8.alamy.com/comp/M4XG2A/portrait-of-abyssinian-or-ethiopian-queen-taytu-betul-1851-1918-empress-M4XG2A.jpg",
        "Ras Alula Engida": "https://tse3.mm.bing.net/th/id/OIP.knSaaH4GxYDM7stWAkA_OQHaKx?rs=1&pid=ImgDetMain&o=7&rm=3",
        "Ras Mikael of Wollo": "https://tse2.mm.bing.net/th/id/OIP.ys9ysBx3xiVl3Ue9qQ399QHaJQ?rs=1&pid=ImgDetMain&o=7&rm=3",
        "Ras Gobana Dacche": "https://tse2.mm.bing.net/th/id/OIP.-x82DUoE6MEjLtgLMcfjuQAAAA?rs=1&pid=ImgDetMain&o=7&rm=3",
        "Ras Mengesha Yohannes": "https://tse4.mm.bing.net/th/id/OIP.FDkrREmktLEo6d5mPBL2fAHaI2?rs=1&pid=ImgDetMain&o=7&rm=3",
        "Fitawrari Habte Giyorgis": "https://th.bing.com/th/id/R.ae82e2f0b2c303e34bd81c9199eb0eda?rik=DatnVvRVtkHeTg&pid=ImgRaw&r=0",
        "Dejazmach Balcha Safo": "https://tse4.mm.bing.net/th/id/OIP.rlwFoAsrcM6wcLo3217TYwHaGe?rs=1&pid=ImgDetMain&o=7&rm=3",
        "Ras Wolde Giyorgis": "https://c8.alamy.com/comp/M77FKN/woldegiorgis-woldeyohannes-waldagiyorgis-waldayohanesright-personal-M77FKN.jpg",
        "Ras Kassa Haile Darge": "https://c8.alamy.com/comp/RAM32R/ras-kasa-ethiopian-generalissimo-ethiopian-army-commander-kassa-haile-darge-1881-1956-middle-east-israel-and-reimagined-RAM32R.jpg"
    
    }

    cols = st.columns(4)

    for i, (name, img) in enumerate(leaders.items()):
        with cols[i % 4]:
            st.image(img, width="stretch")

            if st.button(name, key=name):
                st.session_state.selected_leader = name
                st.session_state.view = "leader_profile"

# -------------------------
# LEADER PROFILE PAGE
# -------------------------
elif st.session_state.view == "leader_profile":

    name = st.session_state.selected_leader

    st.header(name)

    if st.button("⬅ Back to Leaders"):
        st.session_state.view = "leaders"

    try:
        story = wikipedia.summary(name, sentences=15)
    except:
        story = "Could not retrieve story from the web."

    st.markdown(
        f"""
        <div style="background:white; color:black; padding:20px; border-radius:10px;">
        {story}
        </div>
        """,
        unsafe_allow_html=True
    )