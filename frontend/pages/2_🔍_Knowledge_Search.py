"""
Legis-Indexer Pro
HWP/PDF Semantic Indexing and Hybrid RAG Search
"""

import streamlit as st
import requests
from pathlib import Path
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Knowledge Search - Maritime Safety Platform",
    page_icon="🔍",
    layout="wide"
)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent.parent / "styles" / "custom.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Header
st.markdown("""
<div class="main-header">
    Legis-Indexer Pro
</div>
<div class="sub-header">
    HWP/PDF 의미론적 인덱싱 및 하이브리드 RAG 검색 엔진
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Knowledge search active indicator
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <div class="status-badge status-live" style="display: inline-block; font-size: 1rem; padding: 0.5rem 1.5rem;">
        ⚡ KNOWLEDGE SEARCH ACTIVE
    </div>
</div>
""", unsafe_allow_html=True)

# Search interface
st.markdown("""
<div class="search-container">
    <div class="section-header">
        🔍 지능형 검색
    </div>
</div>
""", unsafe_allow_html=True)

# Search input
search_query = st.text_input(
    "검색어를 입력하세요",
    placeholder="예: ai 법에 처벌 수위, 안개 중 충돌 회피 방법, Rule 15 적용 사례",
    label_visibility="collapsed"
)

search_col1, search_col2 = st.columns([3, 1])

with search_col1:
    search_button = st.button("🧠 검색 실행", type="primary", use_container_width=True)

with search_col2:
    advanced_mode = st.checkbox("고급 검색 모드", value=False)

st.markdown("<br>", unsafe_allow_html=True)

# Perform search
if search_button and search_query:
    with st.spinner("검색 중..."):
        st.markdown("""
        <div class="step-box">
            <div class="step-number">1</div>
            <div class="step-title">입법 의도 분석 및 법률 도메인 매핑...</div>
            <div class="step-content">
                사용자 질의를 분석하여 관련 법규 도메인(COLREGs, 해양안전법)과
                의도(규정 조회, 사례 검색, 권고 조치)를 파악합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sample search - will be replaced with actual backend API call
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            📊 검색 결과
        </div>
        """, unsafe_allow_html=True)

        # RAG Integrated Intelligence Response
        st.markdown("""
        <div class="info-card">
            <h3>🧠 RAG 통합 인텔리전스 응답</h3>
            <p style="line-height: 1.8;">
            현재 대한민국에서는 논의 중인 인공지능 기본법(인공지능 산업 육성 및 신뢰 기반 조성 등에 관한 법률안)이 따라,
            주요 처벌 수위는 3년 이하의 징역 또는 3천만 원 이하의 벌금이 예상됩니다. 제26조 제2항에 따르면 신뢰성 확보를 위한 의무를
            해태하거나 보호조치를 하지 않아 인권침해가 발생한 경우 3% 이하의 과태료가 부과됩니다. 다만, 인공지능을 수단으로 활용하여 저지른
            개인정보보호법 위반이나 스토이커범죄의 처벌 등에 관한 법률 위반 등은 이미 해당 법령에서 3년 이상의 징역이 가능합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Semantic chunks (Regulation results)
        st.markdown("""
        <div class="section-header">
            🗂️ 온톨로지 검색 결과 (SEMANTIC CHUNKS)
        </div>
        """, unsafe_allow_html=True)

        # Result 1 - Regulation
        st.markdown("""
        <div class="search-result">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0;">인공지능 산업 육성 및 신뢰 기반 조성 등에 관한 법률안(대안)</h4>
                <div class="relevance-score">95% RELEVANCE</div>
            </div>
            <p style="color: var(--primary-blue); font-size: 0.9rem; margin-bottom: 0.75rem;">
                <strong>CLASS: HTTPS://LIKMS.ASSEMBLY.GO.KR/BILL/MAIN.DO</strong>
            </p>
            <p style="line-height: 1.8;">
                "...제40조(과태료) ① 다음 각 호의 어느 하나에 해당하는 자에게는 3천만원 이하의 과태료를 부과한다.
                1. 제26조제2항을 위반하여 고지하지 아니한 자. 2. 제26조제3항을 위반하여 허위로 표시를 하거나 허위로 공표한 자.
                3. 제26조제2항에 따른 신뢰도록 요구조치를 이행하거나 요구조치를 순수하지 아니한 자..."
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Result 2 - Case law
        st.markdown("""
        <div class="search-result">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0;">개인정보보호 법정관 개정안 매뉴얼</h4>
                <div class="relevance-score">88% RELEVANCE</div>
            </div>
            <p style="color: var(--primary-blue); font-size: 0.9rem; margin-bottom: 0.75rem;">
                <strong>CLASS: HTTPS://WWW.PIPC.GO.KR</strong>
            </p>
            <p style="line-height: 1.8;">
                "...인공지능 더유 한국 산업을 의의미어서. 가. 인증자치나 스스이커의 가능성이 승이는 AI시스템의 존재합니다.
                그로서 위반한 고위험 AI시스템에 관리 기준를 명확히 치정한다면, 지인 집합법률 이용 서비스자 AI. 개인자치
                인즈법의 이용이나에 대응 개발의 가은 세치. 개인 지정법실적 연구개연 경과 위반할 이발한, 계온 새치로 이의
                부위로각 기 AI원자 의무의 지향을 명확히..."
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Result 3 - Maritime specific
        st.markdown("""
        <div class="search-result">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0;">Rule 19 - Conduct in Restricted Visibility</h4>
                <div class="relevance-score">92% RELEVANCE</div>
            </div>
            <p style="color: var(--primary-blue); font-size: 0.9rem; margin-bottom: 0.75rem;">
                <strong>CLASS: COLREGS/RULE-19</strong>
            </p>
            <p style="line-height: 1.8;">
                "This Rule applies to vessels not in sight of one another when navigating in or near an area of restricted visibility.
                (a) Every vessel shall proceed at a safe speed adapted to the prevailing circumstances and conditions of restricted visibility.
                A power-driven vessel shall have her engines ready for immediate manoeuvre.
                (b) Every vessel shall have due regard to the prevailing circumstances and conditions of restricted visibility when complying
                with the Rules of Section I of this Part.
                (c) A vessel which detects by radar alone the presence of another vessel shall determine if a close-quarters situation is
                developing and/or risk of collision exists. If so, she shall take avoiding action in ample time..."
            </p>
            <div style="margin-top: 1rem; padding: 1rem; background: rgba(59, 130, 246, 0.1); border-radius: 0.5rem;">
                <strong>관련 사례:</strong> KMST-2023-001 (안개 중 어선과 화물선 충돌)
            </div>
        </div>
        """, unsafe_allow_html=True)

elif search_button and not search_query:
    st.warning("검색어를 입력해주세요.")

# Example queries
st.markdown("---")

st.markdown("""
<div class="section-header">
    💡 예시 검색 쿼리
</div>
""", unsafe_allow_html=True)

example_col1, example_col2, example_col3 = st.columns(3)

with example_col1:
    st.markdown("""
    <div class="info-card">
        <h4>⚓ COLREGs 규정 검색</h4>
        <ul>
            <li>"횡단 상황에서 피항선의 의무는?"</li>
            <li>"안개 시 안전 속력은 얼마인가?"</li>
            <li>"좁은 수로에서의 항해 규칙"</li>
            <li>"Rule 15 적용 조건"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with example_col2:
    st.markdown("""
    <div class="info-card">
        <h4>⚖️ 판례 및 사례 검색</h4>
        <ul>
            <li>"시계 제한 중 충돌 사례"</li>
            <li>"레이더 의존 항해 위험성"</li>
            <li>"어선 충돌 판결 사례"</li>
            <li>"대폭 변침 실패 사례"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with example_col3:
    st.markdown("""
    <div class="info-card">
        <h4>🎯 권고 조치 검색</h4>
        <ul>
            <li>"안개에서 권고되는 조치는?"</li>
            <li>"마주치는 상황 회피 방법"</li>
            <li>"경계 강화 시기와 방법"</li>
            <li>"음향 신호 사용 규칙"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Search statistics
st.markdown("""
<div class="section-header">
    📈 검색 통계
</div>
""", unsafe_allow_html=True)

stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.metric("총 인덱싱 문서", "224개", "+13 this month")

with stats_col2:
    st.metric("검색 가능 규정", "13개", "COLREGs")

with stats_col3:
    st.metric("평균 검색 시간", "0.45초", "-0.1s")

with stats_col4:
    st.metric("검색 정확도", "95%", "+2%")

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: var(--text-muted); padding: 1rem 0;">
    <p>Legis-Indexer Pro | Powered by Graph-Guided RAG & Semantic Search</p>
</div>
""", unsafe_allow_html=True)
