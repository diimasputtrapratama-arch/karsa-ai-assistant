import os, json, base64
from pathlib import Path
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="KARSA AI Assistant", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

UPLOAD_DIR = Path("uploads"); UPLOAD_DIR.mkdir(exist_ok=True)
GEN_DIR = Path("generated"); GEN_DIR.mkdir(exist_ok=True)

# ---------- STYLE ----------
st.markdown("""
<style>
:root { --bg:#0b1020; --panel:#11182b; --muted:#94a3b8; --text:#eef2ff; --accent:#8b5cf6; }
.stApp { background: radial-gradient(circle at 20% 0%, #18224a 0%, #0b1020 38%, #080c18 100%); color:var(--text); }
.block-container { max-width: 1180px; padding-top: 2rem; }
[data-testid="stSidebar"] { background: rgba(10,15,30,.94); border-right:1px solid rgba(255,255,255,.08); }
.hero { padding:28px 30px; border:1px solid rgba(255,255,255,.08); border-radius:26px;
        background:linear-gradient(135deg,rgba(139,92,246,.18),rgba(59,130,246,.08));
        box-shadow:0 20px 70px rgba(0,0,0,.22); margin-bottom:20px; }
.hero h1 { margin:0; font-size:38px; letter-spacing:-1px; }
.hero p { color:#aeb9d2; margin:.45rem 0 0; }
.card { padding:18px; border-radius:20px; background:rgba(17,24,43,.72); border:1px solid rgba(255,255,255,.07); }
.small { color:#94a3b8; font-size:13px; }
[data-testid="stChatMessage"] { border-radius:18px; }
.stButton>button { border-radius:14px; }
</style>
""", unsafe_allow_html=True)

# ---------- CLIENT ----------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.markdown('<div class="hero"><h1>✦ KARSA AI Assistant</h1><p>Asisten digital untuk berpikir, membuat, menganalisis, dan membantu pekerjaan KARSA.</p></div>', unsafe_allow_html=True)
    st.error("OPENAI_API_KEY belum diset. Jalankan aplikasi dengan API key OpenAI.")
    st.stop()

client = OpenAI(api_key=api_key)
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

# ---------- STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = []

SYSTEM = """Anda adalah KARSA AI Assistant, asisten AI internal KARSA.
Kepribadian: cerdas, tenang, membantu, ringkas tetapi mampu mendalam jika diperlukan.
Anda dapat membantu membuat dokumen, proposal, riset, analisis, ide, pemecahan masalah, dan pekerjaan organisasi.
Jangan mengarang fakta internal KARSA. Jika pengetahuan internal belum tersedia, katakan dengan jelas.
Jika pengguna memberikan informasi yang memang dimaksudkan sebagai pengetahuan untuk KARSA, Anda boleh merangkum dan mempertahankannya dalam sesi ini.
Untuk permintaan berisiko atau membutuhkan verifikasi manusia, jelaskan batasannya.
"""

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## ✦ KARSA")
    st.caption("AI Assistant")
    st.divider()
    mode = st.radio("Mode", ["Chat", "Dokumen", "Proposal", "Analisis"], index=0)
    thinking = st.toggle("🧠 Berpikir lebih keras", value=False)
    st.divider()
    st.markdown("**Kemampuan**")
    st.markdown("• Chat & reasoning\n• Dokumen & proposal\n• Foto & file\n• Analisis\n• Memory sesi")
    if st.button("＋ Percakapan baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
<h1>✦ KARSA AI Assistant</h1>
<p>Satu ruang untuk berpikir, membuat dokumen, menganalisis media, dan membantu pekerjaan KARSA.</p>
</div>
""", unsafe_allow_html=True)

# ---------- QUICK ACTIONS ----------
if not st.session_state.messages:
    cols = st.columns(4)
    prompts = [
        ("✍️", "Buat dokumen", "Buatkan dokumen profesional untuk KARSA tentang "),
        ("📋", "Buat proposal", "Buatkan proposal kegiatan KARSA tentang "),
        ("💡", "Cari solusi", "Bantu saya memecahkan masalah berikut: "),
        ("🔎", "Analisis", "Analisis informasi berikut secara mendalam: ")
    ]
    for c, (icon, title, prompt) in zip(cols, prompts):
        with c:
            st.markdown(f'<div class="card"><div style="font-size:26px">{icon}</div><b>{title}</b><div class="small">Mulai dari sini</div></div>', unsafe_allow_html=True)

# ---------- FILE UPLOAD ----------
uploaded = st.file_uploader(
    "Lampirkan foto, video, PDF, DOCX, TXT, atau file lain",
    type=["png","jpg","jpeg","webp","mp4","mov","pdf","docx","txt","md"],
    accept_multiple_files=True
)
if uploaded:
    for f in uploaded:
        p = UPLOAD_DIR / f.name
        p.write_bytes(f.getbuffer())
    st.success(f"{len(uploaded)} file siap digunakan.")

# ---------- DISPLAY CHAT ----------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

question = st.chat_input("Tulis pesan untuk KARSA AI...")

if question:
    # lightweight session memory
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"):
        st.markdown(question)

    context = ""
    if st.session_state.memory:
        context = "\n\nPengetahuan sesi yang diberikan pengguna:\n" + "\n".join(st.session_state.memory[-20:])

    instruction = SYSTEM + context
    if mode == "Dokumen":
        instruction += "\nMode Dokumen: hasilkan dokumen siap diedit dengan struktur, judul, bagian, dan bahasa profesional."
    elif mode == "Proposal":
        instruction += "\nMode Proposal: hasilkan proposal lengkap dan formal, termasuk latar belakang, tujuan, sasaran, konsep, jadwal, anggaran bila datanya tersedia, dan penutup."
    elif mode == "Analisis":
        instruction += "\nMode Analisis: bedakan fakta, asumsi, risiko, temuan, dan rekomendasi."
    if thinking:
        instruction += "\nPengguna meminta penalaran lebih mendalam. Prioritaskan pemeriksaan asumsi, alternatif, risiko, dan langkah solusi. Jangan tampilkan chain-of-thought rahasia; berikan ringkasan alasan yang relevan."

    # Include recent conversation.
    msgs = [{"role":"system","content":instruction}]
    msgs += st.session_state.messages[-12:]

    with st.chat_message("assistant"):
        with st.spinner("KARSA sedang berpikir..."):
            response = client.responses.create(model=model, input=msgs)
            answer = response.output_text
            st.markdown(answer)

            # optional generated markdown document
            if mode in ("Dokumen","Proposal"):
                safe = "".join(ch if ch.isalnum() or ch in " _-" else "" for ch in question[:50]).strip() or "dokumen"
                out = GEN_DIR / f"{safe}.md"
                out.write_text(answer, encoding="utf-8")
                st.download_button("⬇️ Simpan hasil sebagai Markdown", answer, file_name=out.name, mime="text/markdown")

    st.session_state.messages.append({"role":"assistant","content":answer})

# ---------- MEMORY LEARNING ----------
with st.expander("🧠 Ajarkan sesuatu kepada KARSA"):
    st.caption("Informasi yang dimasukkan di sini disimpan hanya selama sesi aplikasi ini. Untuk memory permanen, gunakan database/memory backend pada tahap produksi.")
    teach = st.text_area("Pengetahuan yang ingin KARSA pelajari", placeholder="Contoh: Struktur divisi KARSA terdiri dari ...")
    if st.button("Simpan ke memory sesi") and teach.strip():
        st.session_state.memory.append(teach.strip())
        st.success("Pengetahuan ditambahkan ke memory sesi KARSA.")
