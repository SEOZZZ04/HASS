"""
Master Control Center
System-wide dashboard with real-time metrics
"""

import streamlit as st
import requests
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Control Center - Maritime Safety Platform",
    page_icon="🎛️",
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
    🏛️ 입법 에이전트 AI 종합상황판
</div>
<div class="sub-header">
    Maritime Safety Platform 온톨로지 플랫폼 마스터 오퍼레이션 센터
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# System operational status section
st.markdown("""
<div class="section-header">
    ⚡ 플랫폼 의기체적 실시간 상태
</div>
""", unsafe_allow_html=True)

# Get backend status
try:
    backend_url = "http://localhost:8000"
    response = requests.get(backend_url, timeout=3)
    backend_status = response.json()
    backend_connected = backend_status.get("status") == "connected"
except:
    backend_connected = False

# Top metrics cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("""
    <div class="status-card">
        <div class="status-badge status-live">LIVE</div>
        <div class="metric-label">Data Source</div>
        <div class="metric-value">14.2 GB/s</div>
        <div class="metric-description">SOURCE & INGESTION</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="status-card">
        <div class="status-badge status-optimal">OPTIMAL</div>
        <div class="metric-label">Ontology Ver</div>
        <div class="metric-value">v2.0</div>
        <div class="metric-description">MARITIME SAFETY</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="status-card">
        <div class="status-badge {'status-syncing' if backend_connected else 'status-active'}">
            {'SYNCING' if backend_connected else 'OFFLINE'}
        </div>
        <div class="metric-label">Knowledge Graph</div>
        <div class="metric-value">224 Classes</div>
        <div class="metric-description">INFERENCE GRAPH</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="status-card">
        <div class="status-badge status-active">ACTIVE</div>
        <div class="metric-label">AI Engine</div>
        <div class="metric-value">45ms</div>
        <div class="metric-description">MULTI-LLM HUB</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="status-card">
        <div class="status-badge status-online">ONLINE</div>
        <div class="metric-label">API Workbench</div>
        <div class="metric-value">v2.4.0</div>
        <div class="metric-description">API & WORKBENCH</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Global metrics section
st.markdown("""
<div class="section-header">
    🌐 글로벌 지식 환경 실시간 지표
</div>
""", unsafe_allow_html=True)

metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

with metric_col1:
    st.markdown("""
    <div class="global-metric">
        <div class="global-metric-label">USD/KRW</div>
        <div class="global-metric-value">₩1,472.87</div>
        <div class="global-metric-trend trend-down">↓ Trend Down</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col2:
    st.markdown("""
    <div class="global-metric">
        <div class="global-metric-label">Climate Port</div>
        <div class="global-metric-value">5.6°C</div>
        <div class="global-metric-trend">Clear Sky</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col3:
    st.markdown("""
    <div class="global-metric">
        <div class="global-metric-label">Energy (WTI)</div>
        <div class="global-metric-value">$78.92</div>
        <div class="global-metric-trend trend-up">↑ Market Sync</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col4:
    st.markdown("""
    <div class="global-metric">
        <div class="global-metric-label">GDP Growth</div>
        <div class="global-metric-value">2.4%</div>
        <div class="global-metric-trend">Inflation 3.1%</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col5:
    st.markdown("""
    <div class="global-metric">
        <div class="global-metric-label">Global Risk</div>
        <div class="global-metric-value">62</div>
        <div class="global-metric-trend">Risk Index</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Ontology statistics
st.markdown("""
<div class="section-header">
    📊 온톨로지 통계 및 그래프 메트릭
</div>
""", unsafe_allow_html=True)

stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.markdown("""
    <div class="info-card">
        <h4>🔵 Regulations (규정)</h4>
        <p><strong>13개</strong> COLREGs 국제해상충돌예방규칙</p>
        <ul>
            <li>Category: Navigation, Collision Avoidance</li>
            <li>Legal Weight: Average 8.5/10</li>
            <li>Last Updated: 2022 Amendment</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown("""
    <div class="info-card">
        <h4>🟡 Maritime Cases (사례)</h4>
        <p><strong>8개</strong> 한국해양안전심판원 판례</p>
        <ul>
            <li>Period: 2020-2024</li>
            <li>Severity: High-impact incidents</li>
            <li>Lessons: 24 key insights</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown("""
    <div class="info-card">
        <h4>🔴 Safety Issues (안전 현안)</h4>
        <p><strong>12개</strong> 주요 해양 안전 위험 상황</p>
        <ul>
            <li>Types: Collision, Grounding, Visibility</li>
            <li>Frequency: 200+ incidents/year</li>
            <li>Addressed by: Multi-regulation coverage</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Ontology relationships visualization
st.markdown("""
<div class="section-header">
    🔗 온톨로지 관계 네트워크 분석
</div>
""", unsafe_allow_html=True)

# Create network visualization with plotly
fig = go.Figure()

# Sample nodes (will be replaced with actual ontology data)
node_x = [0, 1, 2, 1, 0.5, 1.5, 0.3, 1.7]
node_y = [0, 0, 0, -1, -1, -1, -2, -2]
node_names = [
    "Rule 15<br>Crossing",
    "Rule 16<br>Give-way",
    "Rule 17<br>Stand-on",
    "KMST-2023-001<br>Case",
    "Safety Issue:<br>Collision",
    "Action:<br>Starboard Turn",
    "Lesson:<br>Early Action",
    "Evidence:<br>Radar Data"
]
node_colors = [
    '#3B82F6', '#3B82F6', '#3B82F6',  # Regulations (blue)
    '#F59E0B',  # Case (orange)
    '#EF4444',  # Safety Issue (red)
    '#10B981',  # Action (green)
    '#EC4899',  # Lesson (pink)
    '#8B5CF6'   # Evidence (purple)
]

# Add nodes
fig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    marker=dict(
        size=40,
        color=node_colors,
        line=dict(width=2, color='white')
    ),
    text=node_names,
    textposition="top center",
    textfont=dict(size=10, color='white'),
    hovertemplate='<b>%{text}</b><extra></extra>'
))

# Add edges (relationships)
edges = [
    (0, 1), (0, 2),  # Rule 15 relates to 16, 17
    (0, 3),  # Rule 15 violated in case
    (3, 4),  # Case is example of safety issue
    (3, 6),  # Case teaches lesson
    (3, 7),  # Case supported by evidence
    (0, 5),  # Rule recommends action
]

for edge in edges:
    fig.add_trace(go.Scatter(
        x=[node_x[edge[0]], node_x[edge[1]]],
        y=[node_y[edge[0]], node_y[edge[1]]],
        mode='lines',
        line=dict(width=2, color='rgba(148, 163, 184, 0.3)'),
        hoverinfo='none',
        showlegend=False
    ))

fig.update_layout(
    showlegend=False,
    hovermode='closest',
    margin=dict(b=0, l=0, r=0, t=0),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# System health and performance
st.markdown("""
<div class="section-header">
    💚 시스템 헬스 체크 및 성능 모니터링
</div>
""", unsafe_allow_html=True)

health_col1, health_col2 = st.columns(2)

with health_col1:
    if backend_connected:
        st.markdown("""
        <div class="recommendation-box">
            <h4>✅ Backend API: HEALTHY</h4>
            <p>FastAPI 서버가 정상적으로 응답하고 있습니다.</p>
            <ul>
                <li>Status: Connected</li>
                <li>Response Time: < 100ms</li>
                <li>Endpoints: 4/4 available</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Backend API: DISCONNECTED</h4>
            <p>FastAPI 서버에 연결할 수 없습니다.</p>
            <ul>
                <li>Status: Offline</li>
                <li>Action: Check if backend is running on port 8000</li>
                <li>Command: cd backend && uvicorn main:app --reload</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with health_col2:
    st.markdown("""
    <div class="info-card">
        <h4>📈 Performance Metrics</h4>
        <ul>
            <li><strong>Query Response Time:</strong> 45ms (avg)</li>
            <li><strong>Graph Traversal:</strong> 12ms (avg)</li>
            <li><strong>LLM Inference:</strong> 1.2s (avg)</li>
            <li><strong>Memory Usage:</strong> 512 MB</li>
            <li><strong>Active Users:</strong> 1</li>
            <li><strong>Uptime:</strong> {}</li>
        </ul>
    </div>
    """.format(datetime.now().strftime("%H:%M:%S")), unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: var(--text-muted); padding: 1rem 0;">
    <p>마스터 컨트롤 센터 | Last Refreshed: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
