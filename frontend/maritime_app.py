"""
Maritime Safety Platform - Clean & Precise UI
Real-time reasoning with visible regulations and cases
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import networkx as nx
from typing import Dict, Any, List
import time

# Page config
st.set_page_config(
    page_title="Maritime Safety Platform",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean LEGIS-XAI inspired design
st.markdown("""
<style>
    /* Main layout */
    .main {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F1F5F9;
    }

    /* Headers */
    .platform-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .platform-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #94A3B8;
        margin-bottom: 2rem;
    }

    /* Status cards */
    .status-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-critical {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }

    .badge-high {
        background: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .badge-optimal {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    /* Reasoning steps */
    .reasoning-step {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-left: 4px solid #3B82F6;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .step-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .step-number {
        width: 3rem;
        height: 3rem;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.4);
    }

    .step-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #F1F5F9;
    }

    /* Rule cards */
    .rule-card {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }

    .rule-title {
        color: #3B82F6;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .rule-text {
        color: #CBD5E1;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* Case cards */
    .case-card {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }

    .case-title {
        color: #F59E0B;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .case-text {
        color: #CBD5E1;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* Action cards */
    .action-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 2px solid rgba(16, 185, 129, 0.5);
        border-radius: 0.75rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .action-priority {
        display: inline-block;
        background: #10B981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
    }

    .action-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #F1F5F9;
        margin-bottom: 0.5rem;
    }

    .action-detail {
        color: #CBD5E1;
        line-height: 1.6;
    }

    /* Warning cards */
    .warning-card {
        background: rgba(239, 68, 68, 0.1);
        border: 2px solid rgba(239, 68, 68, 0.5);
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }

    .warning-title {
        color: #EF4444;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    /* Info boxes */
    .info-box {
        background: rgba(51, 65, 85, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #3B82F6;
    }

    .metric-label {
        font-size: 0.875rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Arrows */
    .arrow-down {
        text-align: center;
        font-size: 2rem;
        color: #3B82F6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000"

@st.cache_data
def get_scenarios():
    """Get available scenarios"""
    try:
        response = requests.get(f"{API_BASE_URL}/scenarios", timeout=5)
        if response.status_code == 200:
            return response.json()["scenarios"]
    except:
        pass
    return []

def analyze_scenario(scenario_id: str):
    """Analyze scenario and get reasoning steps"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"scenario_id": scenario_id},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
    return None

def render_situation_overview(situation: Dict[str, Any]):
    """Render current situation overview"""
    st.markdown('<div class="platform-subtitle">⚓ 현재 상황</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="info-box">
            <div class="metric-label">시계</div>
            <div class="metric-value">{situation.get('visibility', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="info-box">
            <div class="metric-label">시간</div>
            <div class="metric-value">{situation.get('time', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="info-box">
            <div class="metric-label">기상</div>
            <div class="metric-value">{situation.get('weather', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        target_count = len(situation.get('target_vessels', []))
        st.markdown(f"""
        <div class="info-box">
            <div class="metric-label">타선 수</div>
            <div class="metric-value">{target_count}</div>
        </div>
        """, unsafe_allow_html=True)

    # Vessel details
    own_ship = situation.get('own_ship', {})
    targets = situation.get('target_vessels', [])

    st.markdown("<br>", unsafe_allow_html=True)

    vessel_col1, vessel_col2 = st.columns(2)

    with vessel_col1:
        st.markdown(f"""
        <div class="status-card">
            <h4 style="color: #3B82F6; margin-bottom: 0.75rem;">🚢 본선</h4>
            <p style="margin: 0.25rem 0;"><strong>종류:</strong> {own_ship.get('type', 'N/A')}</p>
            <p style="margin: 0.25rem 0;"><strong>속력:</strong> {own_ship.get('speed', 'N/A')}</p>
            <p style="margin: 0.25rem 0;"><strong>침로:</strong> {own_ship.get('heading', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

    with vessel_col2:
        if targets:
            target = targets[0]
            cpa = target.get('cpa', 'N/A')
            tcpa = target.get('tcpa', 'N/A')

            # Determine risk level
            risk_badge = "badge-critical"
            if "0." in str(cpa) or "< 1" in str(cpa):
                risk_badge = "badge-critical"
            elif "1" in str(cpa) or "2" in str(cpa):
                risk_badge = "badge-high"

            st.markdown(f"""
            <div class="status-card">
                <h4 style="color: #F59E0B; margin-bottom: 0.75rem;">🎯 타선</h4>
                <p style="margin: 0.25rem 0;"><strong>종류:</strong> {target.get('type', 'N/A')}</p>
                <p style="margin: 0.25rem 0;"><strong>방위:</strong> {target.get('bearing', 'N/A')}</p>
                <p style="margin: 0.25rem 0;"><strong>거리:</strong> {target.get('distance', 'N/A')}</p>
                <p style="margin: 0.25rem 0;">
                    <strong>CPA:</strong> <span class="status-badge {risk_badge}">{cpa}</span>
                    <strong>TCPA:</strong> {tcpa}
                </p>
            </div>
            """, unsafe_allow_html=True)

def render_reasoning_step(step_num: int, title: str, content: str, data: List[Dict] = None):
    """Render a reasoning step with actual data"""
    st.markdown(f"""
    <div class="reasoning-step">
        <div class="step-header">
            <div class="step-number">{step_num}</div>
            <div class="step-title">{title}</div>
        </div>
        <p style="color: #CBD5E1; margin-bottom: 1rem;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

    if data:
        # Show actual data in expander
        with st.expander(f"📊 {title} 상세 데이터 ({len(data)}건)", expanded=True):
            for item in data[:5]:  # Show top 5
                st.json(item)

    st.markdown('<div class="arrow-down">↓</div>', unsafe_allow_html=True)
    time.sleep(0.2)  # Animation effect

def render_rules(rules: List[Dict]):
    """Render COLREGs rules with actual content"""
    st.markdown("### 🔵 적용된 COLREGs 규정")

    for rule in rules:
        rule_num = rule.get('id', rule.get('rule_id', 'Unknown'))
        title = rule.get('title', '규정')
        summary = rule.get('summary', rule.get('full_text', ''))[:200]
        weight = rule.get('legal_weight', 0)

        st.markdown(f"""
        <div class="rule-card">
            <div class="rule-title">{rule_num}: {title}</div>
            <div class="rule-text">{summary}...</div>
            <div style="margin-top: 0.5rem;">
                <span class="status-badge badge-optimal">Legal Weight: {weight}/10</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_cases(cases: List[Dict]):
    """Render maritime cases with actual content"""
    st.markdown("### 🟡 유사 사고 판례")

    for case in cases:
        case_id = case.get('case_id', 'Unknown')
        title = case.get('title', '사례')
        judgment = case.get('judgment', case.get('analysis', ''))[:200]
        weight = case.get('legal_weight', 0)

        st.markdown(f"""
        <div class="case-card">
            <div class="case-title">{case_id}: {title}</div>
            <div class="case-text">{judgment}...</div>
            <div style="margin-top: 0.5rem;">
                <span class="status-badge badge-high">Precedent Weight: {weight}/10</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_ontology_graph(rules: List[Dict], cases: List[Dict], situation_types: List[str]):
    """Render ontology connection graph"""
    st.markdown("### 🗺️ 온톨로지 연결 그래프")

    # Create graph
    G = nx.Graph()

    # Add situation nodes (center)
    for sit_type in situation_types:
        G.add_node(sit_type, node_type='situation', color='#EF4444')

    # Add rule nodes
    for rule in rules[:5]:
        rule_id = rule.get('id', rule.get('rule_id', 'rule'))
        title = rule.get('title', '')[:20]
        node_label = f"{rule_id}\n{title}"
        G.add_node(node_label, node_type='rule', color='#3B82F6')

        # Connect to situation
        for sit_type in situation_types:
            G.add_edge(sit_type, node_label)

    # Add case nodes
    for case in cases[:3]:
        case_id = case.get('case_id', 'case')
        title = case.get('title', '')[:15]
        node_label = f"{case_id}\n{title}"
        G.add_node(node_label, node_type='case', color='#F59E0B')

        # Connect to situation
        for sit_type in situation_types:
            G.add_edge(sit_type, node_label)

    # Layout
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Create Plotly figure
    edge_trace = go.Scatter(
        x=[],
        y=[],
        mode='lines',
        line=dict(width=2, color='rgba(148, 163, 184, 0.3)'),
        hoverinfo='none'
    )

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    # Node traces by type
    node_traces = []
    for node_type, color in [('situation', '#EF4444'), ('rule', '#3B82F6'), ('case', '#F59E0B')]:
        nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == node_type]
        if nodes:
            x = [pos[n][0] for n in nodes]
            y = [pos[n][1] for n in nodes]

            trace = go.Scatter(
                x=x,
                y=y,
                mode='markers+text',
                marker=dict(size=40, color=color, line=dict(width=2, color='white')),
                text=nodes,
                textposition="top center",
                textfont=dict(size=9, color='white'),
                name=node_type.capitalize(),
                hoverinfo='text'
            )
            node_traces.append(trace)

    fig = go.Figure(data=[edge_trace] + node_traces)
    fig.update_layout(
        showlegend=True,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(15, 23, 42, 1)',
        paper_bgcolor='rgba(15, 23, 42, 1)',
        height=500,
        legend=dict(font=dict(color='white'))
    )

    st.plotly_chart(fig, use_container_width=True)

def main():
    # Header
    st.markdown('<div class="platform-header">⚓ Maritime Safety Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="platform-subtitle">AI 기반 선박 충돌 회피 지원 시스템 - Real-time Ontology Reasoning</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 시나리오 선택")

        scenarios = get_scenarios()

        if not scenarios:
            st.error("⚠️ Backend가 연결되지 않았습니다")
            st.code("cd backend && uvicorn main:app --reload")
            return

        scenario_dict = {f"{s['scenario_id']}: {s['title']}": s['scenario_id'] for s in scenarios}

        selected = st.selectbox(
            "시나리오",
            options=list(scenario_dict.keys()),
            label_visibility="collapsed"
        )

        scenario_id = scenario_dict[selected]

        # Scenario info
        scenario_detail = next((s for s in scenarios if s['scenario_id'] == scenario_id), {})

        if scenario_detail:
            st.markdown("---")
            st.markdown(f"**난이도**: {scenario_detail.get('difficulty', 'N/A')}")
            st.markdown(f"**위험도**: {scenario_detail.get('risk_level', 0)}/10")
            st.markdown(f"**설명**: {scenario_detail.get('thumbnail_desc', '')}")

        st.markdown("---")
        analyze_btn = st.button("🧠 AI 분석 시작", type="primary", use_container_width=True)

    # Main area
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None

    if analyze_btn:
        with st.spinner("🤖 AI가 상황을 분석하고 있습니다..."):
            st.session_state.analysis = analyze_scenario(scenario_id)

    if st.session_state.analysis:
        result = st.session_state.analysis
        analysis = result.get('analysis', {})

        # 1. Situation Overview
        situation = analysis.get('situation', {}).get('situation', {})
        render_situation_overview(situation)

        st.markdown("---")

        # 2. AI Reasoning Process
        st.markdown('<div class="platform-subtitle">🧠 AI 추론 과정</div>', unsafe_allow_html=True)

        # Get actual data
        relevant_rules = analysis.get('relevant_rules', [])
        relevant_cases = analysis.get('relevant_cases', [])
        graph_context = analysis.get('graph_context', {})
        situation_types = graph_context.get('situation_types', [])

        # Step 1: Perception
        render_reasoning_step(
            1,
            "Perception - 상황 인식",
            f"시계: {situation.get('visibility')}, 타선: {len(situation.get('target_vessels', []))}척",
            [analysis.get('perception', {})]
        )

        # Step 2: Graph Context
        render_reasoning_step(
            2,
            "Graph Context - 상황 맥락 추출",
            f"판단된 상황: {', '.join(situation_types)}",
            [graph_context]
        )

        # Step 3: Rule Retrieval - WITH ACTUAL RULES
        st.markdown(f"""
        <div class="reasoning-step">
            <div class="step-header">
                <div class="step-number">3</div>
                <div class="step-title">Rule Retrieval - 관련 규정 검색</div>
            </div>
            <p style="color: #CBD5E1; margin-bottom: 1rem;">
                상황에 적용 가능한 COLREGs 규정 {len(relevant_rules)}개를 검색했습니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        render_rules(relevant_rules)
        st.markdown('<div class="arrow-down">↓</div>', unsafe_allow_html=True)

        # Step 4: Case Retrieval - WITH ACTUAL CASES
        st.markdown(f"""
        <div class="reasoning-step">
            <div class="step-header">
                <div class="step-number">4</div>
                <div class="step-title">Case Retrieval - 유사 사례 검색</div>
            </div>
            <p style="color: #CBD5E1; margin-bottom: 1rem;">
                유사한 해양 사고 판례 {len(relevant_cases)}개를 검색했습니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

        render_cases(relevant_cases)
        st.markdown('<div class="arrow-down">↓</div>', unsafe_allow_html=True)

        # Step 5: Ontology Graph
        if relevant_rules or relevant_cases:
            render_ontology_graph(relevant_rules, relevant_cases, situation_types)
            st.markdown('<div class="arrow-down">↓</div>', unsafe_allow_html=True)

        # Step 6: LLM Analysis
        llm_analysis = analysis.get('analysis', '')
        if llm_analysis:
            render_reasoning_step(
                5,
                "LLM Analysis - AI 종합 분석",
                llm_analysis[:300] + "..."
            )

        # 3. Final Recommendations
        st.markdown("---")
        st.markdown('<div class="platform-subtitle">✅ 최종 권고 조치</div>', unsafe_allow_html=True)

        recommendations = analysis.get('recommendations', {})
        actions = recommendations.get('priority_actions', [])

        for i, action in enumerate(actions, 1):
            action_name = action.get('action', '조치')
            colregs = action.get('colregs', 'N/A')

            # Build details
            details = []
            if 'target_heading' in action:
                details.append(f"목표 침로: {action['target_heading']}")
            if 'target_speed' in action:
                details.append(f"목표 속력: {action['target_speed']}")
            if 'degree_change' in action:
                details.append(f"변침각: {action['degree_change']}")

            detail_text = " | ".join(details) if details else ""

            st.markdown(f"""
            <div class="action-card">
                <div class="action-priority">우선순위 {i}</div>
                <div class="action-title">{action_name}</div>
                <div class="action-detail">
                    <strong>법적 근거:</strong> COLREGs {colregs}<br>
                    {detail_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Warnings
        warnings = recommendations.get('warnings', [])
        if warnings:
            st.markdown("### ⚠️ 중요 경고")
            for warning in warnings:
                warning_text = warning.get('warning', warning) if isinstance(warning, dict) else warning
                reason = warning.get('reason', '') if isinstance(warning, dict) else ''

                st.markdown(f"""
                <div class="warning-card">
                    <div class="warning-title">{warning_text}</div>
                    <p style="margin: 0; color: #CBD5E1;">{reason}</p>
                </div>
                """, unsafe_allow_html=True)

        # Legal basis
        legal_basis = recommendations.get('legal_basis', [])
        if legal_basis:
            st.markdown(f"""
            <div class="info-box">
                <strong>📚 적용된 법규:</strong> {', '.join(legal_basis)}
            </div>
            """, unsafe_allow_html=True)

        # Lessons
        lessons = recommendations.get('key_lessons', [])
        if lessons:
            st.markdown("### 💡 핵심 교훈")
            for lesson in lessons[:5]:
                st.markdown(f"- {lesson}")

    else:
        # Welcome screen
        st.info("👈 왼쪽 사이드바에서 시나리오를 선택하고 'AI 분석 시작' 버튼을 눌러주세요.")

        st.markdown("---")
        st.markdown("### 🎯 시스템 특징")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="status-card">
                <h4 style="color: #3B82F6;">🔍 Graph-Guided RAG</h4>
                <p>Neo4j 지식 그래프를 통해 상황에 맞는 규정과 판례를 정밀하게 검색합니다.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="status-card">
                <h4 style="color: #F59E0B;">📊 실시간 추론 과정</h4>
                <p>AI가 어떻게 판단을 내렸는지 단계별로 명확하게 보여줍니다.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="status-card">
                <h4 style="color: #10B981;">⚖️ 법적 근거 기반</h4>
                <p>모든 권고는 COLREGs 규정과 실제 판례에 근거합니다.</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
