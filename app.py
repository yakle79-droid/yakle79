import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="모임 회비 관리 계산기", layout="centered")

# 제목과 설명
st.title("모임 회비 관리 계산기")
st.write("총 금액, 인원 수, 팁/서비스 비율을 입력하여 1인당 부담할 금액을 계산합니다.")

# 기본값 설정
if "total_amount" not in st.session_state:
    st.session_state.total_amount = 100000
if "people_count" not in st.session_state:
    st.session_state.people_count = 4
if "tip_percent" not in st.session_state:
    st.session_state.tip_percent = 10
if "per_person" not in st.session_state:
    st.session_state.per_person = 0
if "final_total" not in st.session_state:
    st.session_state.final_total = 0


# 계산 함수
def calculate_bill(total_amount, people_count, tip_percent):
    # 팁이 포함된 총 금액 계산
    final_total = total_amount + (total_amount * tip_percent / 100)

    # 1인당 부담 금액 계산
    per_person = final_total / people_count

    return round(per_person), round(final_total)


# 입력 영역과 결과 영역을 2열로 배치
col1, col2 = st.columns(2)

with col1:
    # 총 금액 입력
    total_amount = st.number_input(
        "총 금액 (원)",
        min_value=0,
        step=1000,
        value=st.session_state.total_amount
    )

    # 인원 수 입력
    people_count = st.number_input(
        "인원 수 (명)",
        min_value=1,
        step=1,
        value=st.session_state.people_count
    )

    # 팁/서비스 비율 입력
    tip_percent = st.slider(
        "팁/서비스 비율 (%)",
        min_value=0,
        max_value=20,
        value=st.session_state.tip_percent
    )

with col2:
    # 계산 결과 표시용 입력창 형태
    per_person_display = st.text_input(
        "1인당 금액 (원)",
        value=str(st.session_state.per_person),
        disabled=True
    )

    final_total_display = st.text_input(
        "팁 포함 총 금액 (원)",
        value=str(st.session_state.final_total),
        disabled=True
    )

# 버튼 영역
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("Clear", use_container_width=True):
        # 입력값과 결과값 초기화
        st.session_state.total_amount = 0
        st.session_state.people_count = 1
        st.session_state.tip_percent = 0
        st.session_state.per_person = 0
        st.session_state.final_total = 0
        st.rerun()

with btn_col2:
    if st.button("Submit", use_container_width=True):
        # 계산 실행
        per_person, final_total = calculate_bill(total_amount, people_count, tip_percent)

        # 세션 상태에 결과 저장
        st.session_state.total_amount = total_amount
        st.session_state.people_count = people_count
        st.session_state.tip_percent = tip_percent
        st.session_state.per_person = per_person
        st.session_state.final_total = final_total

        st.success("계산이 완료되었습니다.")
        st.rerun()