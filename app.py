import streamlit as st
import DbConnection as db
import random

# ✅ 상태 초기화
if "entered" not in st.session_state:
    st.session_state.entered = False
if "show_price_select" not in st.session_state:
    st.session_state.show_price_select = False
if "show_intro_page" not in st.session_state:
    st.session_state.show_intro_page = False

# ✅ Step 1: 입장 페이지
if not st.session_state.entered and not st.session_state.show_intro_page:
    st.title("🔥 이상형 월드컵 🔥")
    st.markdown("## 원하시는 메뉴를 선택해주세요")
    btn_cols = st.columns(3)

    with btn_cols[0]:
        if st.button("👑 이상형 월드컵 시작"):
            st.session_state.entered = True
            st.session_state.show_price_select = True
            st.rerun()

    with btn_cols[1]:
        if st.button("📊 통계 보기"):
            st.session_state.show_intro_page = True
            st.rerun()

    with btn_cols[2]:
        st.button("⚙️ 설정")

    st.stop()

# ✅ Step 2: 자기소개 페이지
if st.session_state.show_intro_page:
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

    if st.button("🏠 홈으로 돌아가기"):
        for key in ["entered", "show_price_select", "show_intro_page"]:
            st.session_state[key] = False
        st.rerun()

    st.stop()

# ✅ Step 3: 가격 선택 페이지
if st.session_state.get("show_price_select", False) and "selected_price" not in st.session_state:
    st.title("💰 가격대를 선택해주세요!")
    st.markdown("### 원하는 가격 범위를 골라주세요")

    selected = st.selectbox(
        "가격 범위 선택",
        ["500만원~2000만원", "2000만원~3000만원", "3000만원~5000만원", "5000만원~8000만원", "8000만원 이상"]
    )

    if st.button("선택 완료"):
        st.session_state.selected_price = selected
        st.session_state.show_price_select = False
        st.rerun()

    st.stop()

# ✅ Step 4: 월드컵 시작 전 초기화
if "round" not in st.session_state:
    st.session_state.round = 1
    connnn = db.DbConnection() 
    res = connnn.select_all_data(st.session_state.selected_price)
    st.session_state.car = random.sample(res, 16)  # 리스트 내 Car 객체들
    st.session_state.winners = []
    st.session_state.index = 0

# ✅ 종료 조건
if len(st.session_state.car) == 1:
    st.title("🏆 이상형 월드컵 결과")
    final_car = st.session_state.car[0]
    st.success(f"🎉 당신의 이상형은: {final_car.model} ({final_car.price}만원)")
    st.image(final_car.img_url, width=400)
    if st.button("다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.stop()

# ✅ 인덱스 초과 시 다음 라운드로
if st.session_state.index + 1 >= len(st.session_state.car):
    st.session_state.car = st.session_state.winners
    st.session_state.winners = []
    st.session_state.index = 0
    st.session_state.round += 1
    st.rerun()

# ✅ 현재 대결 차량 객체
left_car = st.session_state.car[st.session_state.index]
right_car = st.session_state.car[st.session_state.index + 1]

cols = st.columns([5, 1, 5])

with cols[0]:
    st.image(left_car.img_url, use_container_width=True)
    st.markdown(f"""
        <div style='text-align: center; max-width: 300px; margin: 0 auto;'>
            <h4 style="margin-bottom: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                {left_car.model}
            </h4>
            <h3>💰 <b>가격:</b> {left_car.price}만원</h3>
            <p>🚗 <b>등급:</b> {left_car.car_level}</p>
            <p>⛽ <b>연료:</b> {left_car.fuel_type}</p>
            <p>⚙️ <b>엔진:</b> {left_car.engine_type}</p>
            <p>💨 <b>마력:</b> {left_car.horse_power}hp</p>
            <p>📏 <b>배기량:</b> {left_car.car_displ}cc</p>
            <p>🛣️ <b>연비:</b> {left_car.fuel_effic}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("💖 선택!", key="left"):
        st.session_state.winners.append(left_car)
        st.session_state.index += 2
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with cols[1]:
    st.markdown(
        """
        <div style='height: 100%; display: flex; justify-content: center; margin-top: 220px;'>
            <span style='font-size: 48px; font-weight: bold; color: red;'>VS</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with cols[2]:
    st.image(right_car.img_url, use_container_width=True)
    st.markdown(f"""
        <div style='text-align: center; max-width: 300px; margin: 0 auto;'>
            <h4 style="margin-bottom: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                {right_car.model}
            </h4>
            <h3>💰 <b>가격:</b> {right_car.price}만원</h3>
            <p>🚗 <b>등급:</b> {right_car.car_level}</p>
            <p>⛽ <b>연료:</b> {right_car.fuel_type}</p>
            <p>⚙️ <b>엔진:</b> {right_car.engine_type}</p>
            <p>💨 <b>마력:</b> {right_car.horse_power}hp</p>
            <p>📏 <b>배기량:</b> {right_car.car_displ}cc</p>
            <p>🛣️ <b>연비:</b> {right_car.fuel_effic}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("💖 선택!", key="right"):
        st.session_state.winners.append(right_car)
        st.session_state.index += 2
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


