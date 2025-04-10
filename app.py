import streamlit as st
import random
import DbConnection as db

# ✅ 전체 페이지 레이아웃 설정
st.set_page_config(page_title="이상형 월드컵", layout="wide")

# ✅ 스타일 설정 (완전 다크 모드 + 버튼 및 선택 UI + selectbox 크기 조정)
st.markdown("""
    <style>
    html, body, .stApp, .block-container {
        background-color: #000000 !important;
        color: white !important;
    }
    header, .css-1lcbmhc.e1fqkh3o2, .css-18ni7ap.e8zbici2 {
        background-color: #000000 !important;
    }
    .main {
        background-color: #000000 !important;
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
    }
    .card {
        border: 2px solid #fff;
        border-radius: 16px;
        padding: 12px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 2px 2px 12px rgba(255,255,255,0.05);
        background-color: #ffffff;
        font-size: 13px;
        color: #000;
    }
    .card img {
        width: 100%;
        border-radius: 10px;
        height: 240px;
        object-fit: cover;
    }
    .card h2 {
        font-size: 18px;
        margin: 8px 0;
    }
    .stRadio > div, .stSelectbox label {
        color: white !important;
    }
    .stButton > button {
        color: black !important;
        background-color: white !important;
        width: auto !important;
        padding: 0.5rem 1.5rem;
        border-radius: 6px;
        display: inline-block;
        margin-top: 1rem;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    /* ✅ selectbox 높이와 너비 조정 */
    div[data-baseweb="select"] {
        max-width: 300px !important;
        margin-left: 0 !important;
    }
    div[data-baseweb="select"] > div {
        min-height: 36px !important;
        padding-top: 2px !important;
        padding-bottom: 2px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 사이드바 메뉴
menu = st.sidebar.radio("메뉴", ["🏆 월드컵", "📊 통계자료", "👨‍💻 Developer"])

# ✅ 상태 초기화
for key in ["entered", "show_price_select", "selected_price", "round", "car", "winners", "index", "show_intro_page"]:
    if key not in st.session_state:
        st.session_state[key] = False if key in ["entered", "show_price_select", "show_intro_page"] else None if key == "selected_price" else [] if key in ["car", "winners"] else 0 if key == "index" else 1

# ✅ 메인 콘텐츠 시작
st.markdown("<div class='main'>", unsafe_allow_html=True)

# ✅ 월드컵 탭
if menu == "🏆 월드컵":
    if not st.session_state.entered:
        st.markdown("""
            <h1>🔥 이상형 월드컵 🔥</h1>
            <h3>아래 버튼을 눌러 시작하세요</h3>
        """, unsafe_allow_html=True)

        if st.button("👑 이상형 월드컵 시작"):
            st.session_state.entered = True
            st.session_state.show_price_select = True
            st.rerun()
        st.stop()

    if st.session_state.show_price_select and not st.session_state.selected_price:
        st.markdown("""
            <h1>💰 가격대를 선택해주세요</h1>
            <h3>아래 옵션에서 가격대를 선택하고 시작하세요</h3>
        """, unsafe_allow_html=True)

        selected = st.selectbox("가격 범위 선택",
            ["500만원~2000만원", "2000만원~3000만원", "3000만원~5000만원", "5000만원~8000만원", "8000만원 이상"])

        if st.button("선택 완료"):
            st.session_state.selected_price = selected
            st.session_state.show_price_select = False
            conn = db.DbConnection()
            result = conn.select_all_data(selected)
            st.session_state.car = random.sample(result, 16)
            st.rerun()
        st.stop()

    if len(st.session_state.car) == 1:
        final = st.session_state.car[0]
        st.title("🏆 우승 차량")
        st.image(final.img_url, use_container_width=True)
        st.markdown(f"### 🎉 {final.model} ({final.price}만원)")
        if st.button("다시 시작하기"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.stop()

    if st.session_state.index + 1 >= len(st.session_state.car):
        st.session_state.car = st.session_state.winners
        st.session_state.winners = []
        st.session_state.index = 0
        st.session_state.round += 1
        st.rerun()

    left_car = st.session_state.car[st.session_state.index]
    right_car = st.session_state.car[st.session_state.index + 1]

    total = len(st.session_state.car)
    current = st.session_state.index // 2
    st.markdown(f"### 🏁 Round {st.session_state.round} - {total}강 (대결 {current + 1} / {total // 2})")
    st.progress(current / (total // 2))

    def render_card(car, key):
        st.markdown(f"""
            <div class="card">
                <img src="{car.img_url}" />
                <h2>{car.model}</h2>
                <p>🚗 <b>등급:</b> {car.car_level}</p>
                <p>⛽️ <b>연료:</b> {car.fuel_type}</p>
                <p>⚙️ <b>엔진:</b> {car.engine_type}</p>
                <p>💨 <b>마력:</b> {car.horse_power}hp</p>
                <p>📏 <b>배기량:</b> {car.car_displ}cc</p>
                <p>🛣️ <b>연비:</b> {car.fuel_effic}km/l</p>
                <p>💰 <b>가격:</b> {car.price}만원</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("✅ 이 차를 선택", key=f"btn_{key}"):
            st.session_state.winners.append(car)
            st.session_state.index += 2
            st.rerun()

    cols = st.columns([5, 1, 5])
    with cols[0]:
        render_card(left_car, "left")
    with cols[1]:
        st.markdown("<div style='text-align:center; font-size:32px; margin-top:120px; color:white;'>VS</div>", unsafe_allow_html=True)
    with cols[2]:
        render_card(right_car, "right")

# ✅ 통계 탭
elif menu == "📊 통계자료":
    st.title("📊 통계 페이지")
    st.markdown("- 여기에 통계 내용을 표시할 수 있습니다.")

# ✅ 개발자 탭
elif menu == "👨‍💻 Developer":
    st.title("👋 팀원소개")
    profiles = [
        {"name": "지원", "img": "imgs/1.png", "desc": "맛있는 걸 좋아하는 활발한 성격!"},
        {"name": "민수", "img": "imgs/2.png", "desc": "조용하지만 배려심 넘치는 친구"},
        {"name": "하늘", "img": "imgs/3.png", "desc": "유쾌하고 장난기 많은 스타일"},
        {"name": "지우", "img": "imgs/4.png", "desc": "책과 커피를 좋아하는 감성파"},
        {"name": "태호", "img": "imgs/5.png", "desc": "운동과 여행을 사랑하는 열정남"},
    ]

    for profile in profiles:
        st.image(profile["img"], width=200, caption=profile["name"])
        st.markdown(f"**{profile['desc']}**")
        st.markdown("---")

# ✅ 메인 영역 닫기
st.markdown("</div>", unsafe_allow_html=True)
