import streamlit as st
from datetime import date
from supabase import create_client

url = "https://hdcjkvhqndnpgzmdlemt.supabase.co"
key = "sb_publishable_T-_FMwKXcLpwAojRq3BJNQ_8cAmdw1P"

supabase = create_client(url, key)

st.set_page_config(page_title="독서 기록장", page_icon=None)

st.title("독서 기록장")
st.write("읽은 책의 정보와 간단한 감상을 기록할 수 있습니다.")

# 입력 폼
title = st.text_input("책 제목")
author = st.text_input("저자")
read_date = st.date_input("완독 날짜", value=date.today())
rating = st.selectbox("별점", [1, 2, 3, 4, 5], index=4)
memo = st.text_area("한 줄 감상 또는 메모")

# 저장 버튼
if st.button("저장"):
    if not title.strip() or not author.strip():
        st.error("책 제목과 저자는 반드시 입력해야 합니다.")
    else:
        try:
            supabase.table("books").insert({
                "title": title.strip(),
                "author": author.strip(),
                "read_date": str(read_date),
                "rating": rating,
                "memo": memo.strip()
            }).execute()

            st.success("독서 기록이 저장되었습니다.")
        except Exception as e:
            st.error(f"저장 중 오류가 발생했습니다: {e}")

st.subheader("최근 독서 기록")

# DB에서 기록 불러오기
try:
    response = supabase.table("books").select("*").order("id", desc=True).execute()
    records = response.data

    if records:
        for record in records:
            st.markdown(f"책 제목: {record['title']}")
            st.markdown(f"저자: {record['author']}")
            st.markdown(f"읽은 날짜: {record['read_date']}")
            st.markdown(f"별점: {record['rating']}점")
            st.markdown(f"메모: {record['memo'] or '-'}")
            st.divider()
    else:
        st.write("저장된 독서 기록이 없습니다.")
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
