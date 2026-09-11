# KARSA AI Assistant — Pro v1

MVP UI/UX untuk asisten AI internal KARSA.

## Fitur
- UI minimal, modern, dark/glass.
- Chat AI.
- Mode Dokumen.
- Mode Proposal.
- Mode Analisis.
- Toggle "Berpikir lebih keras" untuk meminta analisis yang lebih mendalam.
- Upload file/foto/video sebagai fondasi workflow media.
- Memory sesi: pengguna dapat mengajarkan pengetahuan ke KARSA.
- Export hasil dokumen/proposal ke Markdown.

## Catatan penting
Versi ini adalah fondasi aplikasi. Upload media sudah tersedia di UI, tetapi pipeline vision/video editing produksi membutuhkan pemrosesan media tambahan. PDF/DOCX parsing, OCR, RAG knowledge base, database, autentikasi, dan editing/generasi media sebaiknya ditambahkan pada fase berikutnya.

## Menjalankan
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Set API key:
```bash
# macOS/Linux
export OPENAI_API_KEY="YOUR_KEY"

# Windows PowerShell
$env:OPENAI_API_KEY="YOUR_KEY"
```

Jalankan:
```bash
streamlit run app.py
```

## Roadmap produksi
1. Vision: analisis gambar + OCR.
2. File ingestion: PDF/DOCX/XLSX.
3. RAG: knowledge base KARSA dengan citation.
4. Auth + role-based access.
5. Persistent memory dengan persetujuan pengguna.
6. Document engine: DOCX/PDF/PPTX.
7. Video understanding & media pipeline.
8. Image editing/generation.
9. Tool calling + workflow automation.
10. Audit log, rate limit, security, monitoring.
