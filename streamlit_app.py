import streamlit as st
from PIL import Image
from collections import Counter
import random

st.set_page_config(page_title="Card AI", layout="centered")

st.title("🃏 Card AI")
st.write("อัปโหลดรูป → ระบบคำนวณให้อัตโนมัติ")

# ---------- session state ----------
if "results" not in st.session_state:
    st.session_state.results = []

# ---------- upload image ----------
uploaded = st.file_uploader(
    "📸 อัปโหลดรูป (แคปหน้าจอได้เลย)",
    type=["png", "jpg", "jpeg"]
)

if uploaded is not None:
    img = Image.open(uploaded)

    # แสดงรูปตามขนาดจริง
    st.image(img, caption="รูปที่อัปโหลด", use_container_width=True)

    # ---------- ตัวอย่าง logic วิเคราะห์ (แทน AI) ----------
    # ตรงนี้คุณจะเอาไปต่อ OCR / AI ทีหลังได้
    possible = ["แดง", "ดำ"]
    result = random.choice(possible)

    st.session_state.results.append(result)

# ---------- แสดงผล ----------
results = st.session_state.results
total = len(results)

if total > 0:
    st.divider()
    st.subheader(f"📊 ทั้งหมด {total} ตา")

    cnt = Counter(results)
    for k, v in cnt.items():
        st.write(f"{k} = {v} ({v/total*100:.1f}%)")

    # นับติด
    run = 1
    for i in range(total - 1, 0, -1):
        if results[i] == results[i - 1]:
            run += 1
        else:
            break

    st.write(f"🔥 ปัจจุบันติด {run} ตา")

# ---------- reset ----------
st.divider()
if st.button("🔄 รีเซ็ต"):
    st.session_state.results = []
    st.experimental_rerun()
