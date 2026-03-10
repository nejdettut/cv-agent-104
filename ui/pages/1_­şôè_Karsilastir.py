"""İki CV'yi karşılaştır ve hangisi daha güçlü analizi."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.pdf_reader import read_uploaded_file
from core.llm import get_llm
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="CV Karşılaştır", page_icon="📊", layout="wide")
st.markdown("# 📊 İki CV'yi Karşılaştır")
st.markdown("İki farklı CV versiyonunu yükle — hangisinin daha güçlü olduğunu analiz et.")
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📄 CV #1 (Mevcut)")
    file1 = st.file_uploader("CV 1 Yükle", type=["pdf","txt"], key="cv1")

with col2:
    st.markdown("### 📄 CV #2 (Rakip / Yeni Versiyon)")
    file2 = st.file_uploader("CV 2 Yükle", type=["pdf","txt"], key="cv2")

if st.button("⚡ Karşılaştır", use_container_width=True) and file1 and file2:
    with st.spinner("Analiz yapılıyor..."):
        text1 = read_uploaded_file(file1)
        text2 = read_uploaded_file(file2)
        llm = get_llm()
        prompt = f"""
İki CV'yi karşılaştır ve hangisinin daha güçlü olduğunu analiz et.
CV 1: {text1[:1500]}
CV 2: {text2[:1500]}
YANIT: Her CV için 3 güçlü yön, 3 zayıf yön ve kazanan CV gerekçesiyle belirt. Türkçe yaz.
"""
        response = llm.invoke([HumanMessage(content=prompt)])
    st.markdown("### 🏆 Karşılaştırma Sonucu")
    st.markdown(response.content)
