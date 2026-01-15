import streamlit as st
from collections import Counter

st.set_page_config(page_title="เค้าไพ่ตาต่อตา", layout="centered")
st.title("🃏 วิเคราะห์เค้าไพ่ จากภาพ (ตาต่อตา)")

if "results" not in st.session_state:
    st.session_state.results = []

game = st.selectbox("เลือกเกม", ["บาคาร่า", "แดงดำ", "เสือมังกร"])

img = st.file_uploader("📸 อัปโหลดภาพผลล่าสุด", type=["png","jpg","jpeg"])
if img:
    st.image(img, use_column_width=True)

st.subheader("เลือกผลจากภาพ")
if game == "บาคาร่า":
    c = st.columns(3)
    if c[0].button("ผู้เล่น"):
        st.session_state.results.append("P")
    if c[1].button("เจ้ามือ"):
        st.session_state.results.append("B")
    if c[2].button("เสมอ"):
        st.session_state.results.append("T")

elif game == "แดงดำ":
    c = st.columns(2)
    if c[0].button("แดง"):
        st.session_state.results.append("R")
    if c[1].button("ดำ"):
        st.session_state.results.append("B")

elif game == "เสือมังกร":
    c = st.columns(2)
    if c[0].button("เสือ"):
        st.session_state.results.append("T")
    if c[1].button("มังกร"):
        st.session_state.results.append("D")

results = st.session_state.results
total = len(results)

if total > 0:
    st.divider()
    st.subheader(f"📊 ตาที่ {total}")

    cnt = Counter(results)
    for k, v in cnt.items():
        st.write(k, "=", v, f"({v/total*100:.1f}%)")

    run = 1
    for i in range(total-1, 0, -1):
        if results[i] == results[i-1]:
            run += 1
        else:
            break
    st.write("🔥 เค้าปัจจุบันติด:", run, "ตา")

if st.button("🔄 รีเซ็ต"):
    st.session_state.results = []
