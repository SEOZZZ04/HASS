"""
Streamlit 프론트엔드 - Maritime Cognitive Navigation System
AI의 사고 과정을 실시간으로 시각화
"""
import streamlit as st
import requests
import json
import time
from typing import Dict, Any, List

# 페이지 설정
st.set_page_config(
    page_title="Maritime Navigation System",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .step-number {
        font-size: 1.5rem;
        font-weight: 700;
        display: inline-block;
        width: 40px;
        height: 40px;
        background: white;
        color: #667eea;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        margin-right: 1rem;
    }
    .arrow-down {
        text-align: center;
        font-size: 2rem;
        color: #667eea;
        margin: 1rem 0;
    }
    .recommendation-box {
        background: #10B981;
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background: #EF4444;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .info-card {
        background: #F1F5F9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API 엔드포인트
API_BASE_URL = "http://localhost:8000"


def get_scenarios() -> List[Dict[str, Any]]:
    """시나리오 목록 가져오기"""
    try:
        response = requests.get(f"{API_BASE_URL}/scenarios")
        if response.status_code == 200:
            return response.json()["scenarios"]
        return []
    except:
        return []


def get_scenario_detail(scenario_id: str) -> Dict[str, Any]:
    """시나리오 상세 정보 가져오기"""
    try:
        response = requests.get(f"{API_BASE_URL}/scenarios/{scenario_id}")
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}


def analyze_scenario(scenario_id: str) -> Dict[str, Any]:
    """시나리오 분석 요청"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"scenario_id": scenario_id}
        )
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        st.error(f"분석 실패: {e}")
        return {}


def render_reasoning_step(step: Dict[str, Any], delay: float = 0.3):
    """추론 단계 렌더링 (애니메이션 효과)"""
    step_number = step.get("step_number", 0)
    step_name = step.get("step_name", "")
    description = step.get("description", "")
    reasoning = step.get("reasoning", "")
    results_count = step.get("results_count", 0)

    # 단계별 박스
    st.markdown(f"""
    <div class="step-box">
        <span class="step-number">{step_number}</span>
        <strong>{step_name}</strong>
        <p style="margin: 0.5rem 0 0 3.5rem; font-size: 0.9rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

    # 추론 내용
    if reasoning:
        with st.expander(f"💭 {step_name} 상세 내용", expanded=True):
            st.write(reasoning)
            if results_count > 0:
                st.info(f"📊 검색 결과: {results_count}건")

    # 화살표
    st.markdown('<div class="arrow-down">↓</div>', unsafe_allow_html=True)

    # 애니메이션 효과
    time.sleep(delay)


def main():
    """메인 앱"""
    # 헤더
    st.markdown('<div class="main-header">🚢 Maritime Cognitive Navigation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">팔란티어식 Vision-to-Action 해상 관제 시스템</div>', unsafe_allow_html=True)

    # 사이드바 - 시나리오 선택
    with st.sidebar:
        st.header("📋 시나리오 선택")

        scenarios = get_scenarios()

        if not scenarios:
            st.warning("시나리오를 불러올 수 없습니다. 백엔드 서버를 확인하세요.")
            st.info("백엔드 실행: `cd backend && python main.py`")
            return

        scenario_options = {
            f"{s['scenario_id']}: {s['title']}": s['scenario_id']
            for s in scenarios
        }

        selected_name = st.selectbox(
            "시나리오 선택",
            options=list(scenario_options.keys()),
            index=0
        )

        selected_scenario_id = scenario_options[selected_name]

        # 시나리오 상세 정보
        scenario_detail = get_scenario_detail(selected_scenario_id)

        if scenario_detail:
            st.markdown("---")
            st.subheader("📊 시나리오 정보")
            st.write(f"**난이도**: {scenario_detail.get('difficulty', 'N/A')}")
            st.write(f"**위험도**: {scenario_detail.get('risk_level', 0)}/10")
            st.write(f"**설명**: {scenario_detail.get('thumbnail_desc', '')}")

        # 분석 시작 버튼
        st.markdown("---")
        analyze_button = st.button("🧠 AI 사고 과정 시작", type="primary", use_container_width=True)

    # 메인 영역
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None

    if analyze_button:
        st.session_state.analysis_result = None

        # 분석 진행 표시
        with st.spinner("🤖 AI가 상황을 분석하고 있습니다..."):
            result = analyze_scenario(selected_scenario_id)
            if result:
                st.session_state.analysis_result = result

    # 결과 표시
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        analysis = result.get("analysis", {})

        # 상황 정보
        st.header("🌊 현재 상황")
        situation = analysis.get("situation", {}).get("situation", {})

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("시계", situation.get("visibility", "N/A"))
        with col2:
            st.metric("시간", situation.get("time", "N/A"))
        with col3:
            st.metric("기상", situation.get("weather", "N/A"))

        # 본선 정보
        own_ship = situation.get("own_ship", {})
        st.markdown(f"""
        <div class="info-card">
            <strong>본선 정보</strong><br>
            종류: {own_ship.get('type', 'N/A')} | 속력: {own_ship.get('speed', 'N/A')} | 침로: {own_ship.get('heading', 'N/A')}
        </div>
        """, unsafe_allow_html=True)

        # 타선 정보
        targets = situation.get("target_vessels", [])
        if targets:
            st.subheader("🎯 타선 정보")
            for i, target in enumerate(targets, 1):
                st.markdown(f"""
                <div class="info-card">
                    <strong>타선 {i}</strong><br>
                    종류: {target.get('type', 'N/A')} |
                    방위: {target.get('bearing', 'N/A')} |
                    거리: {target.get('distance', 'N/A')} |
                    CPA: {target.get('cpa', 'N/A')} |
                    TCPA: {target.get('tcpa', 'N/A')}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # AI 사고 과정 시각화
        st.header("🧠 AI 사고 과정 (실시간 추론)")

        reasoning_steps = result.get("reasoning_steps", [])

        if reasoning_steps:
            # 각 단계별 렌더링
            for step in reasoning_steps:
                render_reasoning_step(step, delay=0.1)

            # 최종 권고
            st.markdown("---")
            st.header("✅ 최종 권고 조치")

            recommendations = analysis.get("recommendations", {})
            priority_actions = recommendations.get("priority_actions", [])

            if priority_actions:
                for i, action in enumerate(priority_actions, 1):
                    action_name = action.get("action", "조치")
                    priority = action.get("priority", i)
                    colregs = action.get("colregs", "N/A")

                    # 추가 정보
                    extra_info = ""
                    if "target_heading" in action:
                        extra_info += f" → 목표 침로: {action['target_heading']}"
                    if "target_speed" in action:
                        extra_info += f" → 목표 속력: {action['target_speed']}"
                    if "degree_change" in action:
                        extra_info += f" (변침 {action['degree_change']}도)"

                    st.markdown(f"""
                    <div class="recommendation-box">
                        <h3 style="margin: 0;">우선순위 {priority}: {action_name}</h3>
                        <p style="margin: 0.5rem 0 0 0;">
                            법적 근거: COLREGs {colregs}{extra_info}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            # 경고사항
            warnings = recommendations.get("warnings", [])
            if warnings:
                st.subheader("⚠️ 중요 경고")
                for warning in warnings:
                    warning_text = warning.get("warning", "경고") if isinstance(warning, dict) else warning
                    reason = warning.get("reason", "") if isinstance(warning, dict) else ""

                    st.markdown(f"""
                    <div class="warning-box">
                        <strong>{warning_text}</strong><br>
                        {reason}
                    </div>
                    """, unsafe_allow_html=True)

            # 법적 근거
            st.subheader("📚 적용된 규정")
            legal_basis = recommendations.get("legal_basis", [])
            if legal_basis:
                st.write(", ".join(legal_basis))

            # 교훈
            key_lessons = recommendations.get("key_lessons", [])
            if key_lessons:
                st.subheader("💡 핵심 교훈")
                for lesson in key_lessons[:5]:
                    st.markdown(f"- {lesson}")

    else:
        # 초기 화면
        st.info("👈 왼쪽 사이드바에서 시나리오를 선택하고 '**AI 사고 과정 시작**' 버튼을 눌러주세요.")

        # 시스템 소개
        st.markdown("---")
        st.header("🎯 시스템 특징")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("👁️ Perception Layer")
            st.write("""
            - YOLO Vision AI로 선박 탐지
            - 레이더/AIS 데이터 융합
            - 실시간 위치/속도 추적
            """)

        with col2:
            st.subheader("🧠 Semantic Layer")
            st.write("""
            - Neo4j 지식 그래프
            - COLREGs 규정 연결
            - 사고 판례 데이터베이스
            """)

        with col3:
            st.subheader("⚡ Action Layer")
            st.write("""
            - Graph-Guided RAG
            - LLM 기반 분석
            - 법적 근거 기반 권고
            """)

        st.markdown("---")
        st.header("🚀 작동 원리")
        st.write("""
        1. **Vision AI** → 카메라 영상에서 선박 객체 탐지 (YOLO)
        2. **Graph Context** → Neo4j에서 상황 맥락 추출 (횡단/마주침/추월 등)
        3. **Rule Retrieval** → 그래프 기반으로 관련 COLREGs 규정 검색
        4. **Case Retrieval** → 유사 사고 판례 검색
        5. **LLM Analysis** → 종합 분석 및 판단
        6. **Action** → 구체적 조치 권고 (법적 근거 포함)
        """)


if __name__ == "__main__":
    main()
