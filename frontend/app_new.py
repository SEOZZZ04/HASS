"""
Maritime Safety Platform - LEGIS-XAI Style
Main Entry Point with Multi-Page Navigation
"""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Maritime Safety Platform",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / "styles" / "custom.css"
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Main landing page
def main():
    # Hero header
    st.markdown("""
    <div class="main-header">
        ⚓ Maritime Safety Platform
    </div>
    <div class="sub-header">
        LEGIS-XAI 스타일 온톨로지 플랫폼 - 해양 안전 규정 지능형 분석 시스템
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Introduction
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🌊 플랫폼 소개</h3>
            <p>
            이 플랫폼은 국제해상충돌예방규칙(COLREGs), 해양 사고 판례, 안전 현안을
            <strong>시맨틱 온톨로지</strong>로 체계화하여 AI 기반 의사결정을 지원합니다.
            </p>
            <ul>
                <li>📚 <strong>13개 COLREGs 규정</strong> RDF/OWL 온톨로지</li>
                <li>⚖️ <strong>8개 해양 사고 판례</strong> 법적 근거 데이터</li>
                <li>🔍 <strong>Graph-Guided RAG</strong> 지식 검색 엔진</li>
                <li>🗺️ <strong>Interactive Ontology Map</strong> 시각화</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="recommendation-box">
            <h4>✨ 주요 기능</h4>
            <ul>
                <li>🎛️ <strong>Control Center</strong>: 시스템 현황 대시보드</li>
                <li>🔍 <strong>Knowledge Search</strong>: AI 기반 규정 검색</li>
                <li>🗺️ <strong>Ontology Map</strong>: 그래프 시각화</li>
                <li>📚 <strong>Ontology Browser</strong>: 온톨로지 탐색</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # System architecture
    st.markdown("""
    <div class="section-header">
        🏗️ 시스템 아키텍처
    </div>
    """, unsafe_allow_html=True)

    arch_cols = st.columns(4)

    with arch_cols[0]:
        st.markdown("""
        <div class="status-card">
            <div class="status-badge status-live">LIVE</div>
            <div class="metric-label">Frontend</div>
            <div class="metric-value">Streamlit</div>
            <div class="metric-description">Multi-page 인터랙티브 UI</div>
        </div>
        """, unsafe_allow_html=True)

    with arch_cols[1]:
        st.markdown("""
        <div class="status-card">
            <div class="status-badge status-optimal">OPTIMAL</div>
            <div class="metric-label">Backend</div>
            <div class="metric-value">FastAPI</div>
            <div class="metric-description">RESTful API 서버</div>
        </div>
        """, unsafe_allow_html=True)

    with arch_cols[2]:
        st.markdown("""
        <div class="status-card">
            <div class="status-badge status-syncing">SYNCING</div>
            <div class="metric-label">Ontology</div>
            <div class="metric-value">RDF/OWL</div>
            <div class="metric-description">시맨틱 지식 그래프</div>
        </div>
        """, unsafe_allow_html=True)

    with arch_cols[3]:
        st.markdown("""
        <div class="status-card">
            <div class="status-badge status-active">ACTIVE</div>
            <div class="metric-label">AI Engine</div>
            <div class="metric-value">Gemini</div>
            <div class="metric-description">Graph-Guided RAG</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick start guide
    st.markdown("""
    <div class="section-header">
        🚀 Quick Start Guide
    </div>
    """, unsafe_allow_html=True)

    guide_col1, guide_col2 = st.columns(2)

    with guide_col1:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">1</div>
            <div class="step-title">📊 Control Center 방문</div>
            <div class="step-content">
                사이드바에서 "Control Center"를 선택하여 시스템 전체 현황과
                실시간 메트릭을 확인하세요.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="step-box">
            <div class="step-number">3</div>
            <div class="step-title">🗺️ Ontology Map 탐색</div>
            <div class="step-content">
                인터랙티브 그래프로 규정, 사례, 안전 현안 간의 관계를
                시각적으로 탐색하세요.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with guide_col2:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">2</div>
            <div class="step-title">🔍 Knowledge Search 사용</div>
            <div class="step-content">
                AI 기반 검색으로 상황에 맞는 규정, 판례, 권고 조치를
                즉시 찾아보세요.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="step-box">
            <div class="step-number">4</div>
            <div class="step-title">📚 Ontology Browser로 상세 조회</div>
            <div class="step-content">
                온톨로지의 모든 엔티티와 속성을 카테고리별로
                자세히 탐색하세요.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style="text-align: center; color: var(--text-muted); padding: 2rem 0;">
        <p>Maritime Safety Platform v2.0 - Powered by RDF/OWL Ontology & Graph-Guided RAG</p>
        <p>© 2026 WeOffice AI Team | 국제해상충돌예방규칙(COLREGs) 1972/2022</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
