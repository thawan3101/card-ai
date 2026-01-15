import streamlit as st
from collections import Counter
from PIL import Image
import random

st.set_page_config(page_title="เค้าไพ่จากภาพ (อัตโนมัติ)", layout="centered")
st.title("🃏 วิเคราะห์เค้าไพ่จากภาพ (ตาต่อตา)")

# ---------- ฟังก์ชันย่อรูป ----------
def resize_image(img, max_width=720):
    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        img = img.resize((max_width, int(h * ratio)))
    return img

# ---------- ฟังก์ชันทำนาย ----------
def predict_next(results, game, n=10):
    preds = []

    if game == "บาคาร่า":
        choices = ["P", "B", "T"]
    elif game == "แดงดำ":
        choices = ["R", "B"]
    else:
        choices = ["T", "D"]

    if not results:
        return [random.choice(choices) for _ in range(n)]

    cnt = Counter(results)
    total = len(results)

    probs = {k: cnt.get(k, 0)/total for k in choices}

    last = results[-1]
    run = 1
    for i in range(total-1, 0, -1):
        if results[i] == results[i-1]:
            run += 1
        else:
            break

    if run >= 3:
        probs[last] = probs.get(last, 0) + 0.15

    s = sum(probs.values())
    weights = [probs.get(c, 0)/s for c in choices]

    for _ in range(n):
        preds.append(random.choices(choices, weights)[0])

    return preds

# ---------- session ----------
if "results" not in st.session_state:
    st.session_state.results = []

# ---------- เลือกเกม ----------
game = st.selectbox("🎮 เลือกเกม", ["บาคาร่า", "แดงดำ", "เสือมังกร"])

# ---------- อัปโหลดรูป ----------
uploaded = st.file_uploader("📸 อัปโหลดภาพผลล่าสุด (แคปหน้าจอได้)", type=["png","jpg","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    img = resize_image(img)

    st.markdown("### 📷 ภาพที่อัปโหลด")
    st.image(img, width=350)

# ---------- เลือกผล (ตาต่อตา) ----------
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

else:
    c = st.columns(2)
    if c[0].button("เสือ"):
        st.session_state.results.append("T")
    if c[1].button("มังกร"):
        st.session_state.results.append("D")

# ---------- วิเคราะห์ ----------
results = st.session_state.results
total = len(results)

if total > 0:
    st.divider()
    st.subheader(f"📊 วิเคราะห์ {total} ตา")

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

    # ---------- ทำนายอัตโนมัติ ----------
    preds = predict_next(results, game, 10)

    st.divider()
    st.subheader("🔮 คาดการณ์ล่วงหน้า 10 ตา")
    st.write(" → ".join(preds))

# ---------- รีเซ็ต ----------
if st.button("🔄 รีเซ็ตทั้งหมด"):
    st.session_state.results = []
