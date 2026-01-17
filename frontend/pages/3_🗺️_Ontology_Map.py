"""
Legis-XAI Ontology Map
RDF/OWL Semantic Knowledge Store with Interactive Graph Visualization
"""

import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Ontology Map - Maritime Safety Platform",
    page_icon="🗺️",
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
    Legis-XAI Ontology Map
</div>
<div class="sub-header">
    RDF/OWL Semantic Knowledge Store - Maritime Safety Ontology v2.0
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Ontology info
info_col1, info_col2 = st.columns([3, 1])

with info_col1:
    st.markdown("""
    <div class="section-header">
        🗺️ 해양 안전 온톨로지 지식 그래프
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div style="text-align: right;">
        <div class="status-badge status-syncing" style="display: inline-block; margin-bottom: 0.5rem;">
            🔄 SYNC LIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

# Legend
st.markdown("""
<div class="info-card">
    <h4>📌 SEMANTIC LEGENDS</h4>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
        <div>
            <span style="color: #3B82F6; font-weight: bold;">🔵 법안 (Bill)</span> - COLREGs Regulations
        </div>
        <div>
            <span style="color: #10B981; font-weight: bold;">🟢 Policy Issue (정안)</span> - Safety Issues
        </div>
        <div>
            <span style="color: #F59E0B; font-weight: bold;">🟡 Stakeholder (이해관계자)</span> - Vessels
        </div>
        <div>
            <span style="color: #8B5CF6; font-weight: bold;">🟣 Evidence (근거)</span> - Data Sources
        </div>
        <div>
            <span style="color: #EC4899; font-weight: bold;">💗 Clause (조항)</span> - Articles
        </div>
        <div>
            <span style="color: #14B8A6; font-weight: bold;">🟦 PolicyActor (정책행위자)</span> - Actors
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Create interactive graph
st.markdown("""
<div class="section-header">
    🌐 Force-Directed Graph Visualization
</div>
""", unsafe_allow_html=True)

# Build graph with networkx
G = nx.Graph()

# Add nodes with types
nodes = {
    # Regulations (Blue)
    "Rule-05": {"type": "Regulation", "label": "Rule 5\n경계", "color": "#3B82F6"},
    "Rule-06": {"type": "Regulation", "label": "Rule 6\n안전 속력", "color": "#3B82F6"},
    "Rule-15": {"type": "Regulation", "label": "Rule 15\n횡단 상황", "color": "#3B82F6"},
    "Rule-19": {"type": "Regulation", "label": "Rule 19\n시계 제한", "color": "#3B82F6"},

    # Safety Issues (Green)
    "SI-Collision": {"type": "SafetyIssue", "label": "충돌 위험", "color": "#10B981"},
    "SI-Visibility": {"type": "SafetyIssue", "label": "시계 제한", "color": "#10B981"},
    "SI-Crossing": {"type": "SafetyIssue", "label": "횡단 상황", "color": "#10B981"},

    # Cases (Orange)
    "KMST-001": {"type": "Case", "label": "KMST-2023-001\n안개 충돌", "color": "#F59E0B"},
    "KMST-002": {"type": "Case", "label": "KMST-2023-002\n횡단 충돌", "color": "#F59E0B"},

    # Evidence (Purple)
    "EVD-Radar": {"type": "Evidence", "label": "Radar\nData", "color": "#8B5CF6"},
    "EVD-AIS": {"type": "Evidence", "label": "AIS\nData", "color": "#8B5CF6"},

    # Vessels (Teal)
    "Vessel-Cargo": {"type": "Vessel", "label": "화물선", "color": "#14B8A6"},
    "Vessel-Fishing": {"type": "Vessel", "label": "어선", "color": "#14B8A6"},

    # Lessons (Pink)
    "Lesson-01": {"type": "Lesson", "label": "조기 대폭 변침", "color": "#EC4899"},
    "Lesson-02": {"type": "Lesson", "label": "속력 감속 필수", "color": "#EC4899"},

    # Actions (Light Green)
    "Action-Turn": {"type": "Action", "label": "우현 변침", "color": "#10B981"},
    "Action-Slow": {"type": "Action", "label": "감속", "color": "#10B981"},
}

for node_id, attrs in nodes.items():
    G.add_node(node_id, **attrs)

# Add edges (relationships)
edges = [
    # Regulations address Safety Issues
    ("Rule-05", "SI-Collision"),
    ("Rule-06", "SI-Collision"),
    ("Rule-15", "SI-Crossing"),
    ("Rule-19", "SI-Visibility"),

    # Cases violate Regulations
    ("KMST-001", "Rule-19"),
    ("KMST-001", "Rule-05"),
    ("KMST-002", "Rule-15"),

    # Cases are examples of Safety Issues
    ("KMST-001", "SI-Visibility"),
    ("KMST-002", "SI-Crossing"),

    # Cases supported by Evidence
    ("KMST-001", "EVD-Radar"),
    ("KMST-001", "EVD-AIS"),
    ("KMST-002", "EVD-Radar"),

    # Cases involve Vessels
    ("KMST-001", "Vessel-Cargo"),
    ("KMST-001", "Vessel-Fishing"),
    ("KMST-002", "Vessel-Cargo"),

    # Cases teach Lessons
    ("KMST-001", "Lesson-02"),
    ("KMST-002", "Lesson-01"),

    # Regulations recommend Actions
    ("Rule-15", "Action-Turn"),
    ("Rule-19", "Action-Slow"),

    # Actions prevent Safety Issues
    ("Action-Turn", "SI-Crossing"),
    ("Action-Slow", "SI-Visibility"),

    # Related regulations
    ("Rule-05", "Rule-06"),
    ("Rule-15", "Rule-19"),
]

G.add_edges_from(edges)

# Use spring layout for positioning
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# Create Plotly figure
edge_trace = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace.append(
        go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=2, color='rgba(148, 163, 184, 0.3)'),
            hoverinfo='none',
            showlegend=False
        )
    )

# Node traces by type
node_traces = {}
for node_id, node_data in G.nodes(data=True):
    node_type = node_data['type']
    if node_type not in node_traces:
        node_traces[node_type] = {
            'x': [], 'y': [], 'text': [], 'color': node_data['color'], 'labels': []
        }

    x, y = pos[node_id]
    node_traces[node_type]['x'].append(x)
    node_traces[node_type]['y'].append(y)
    node_traces[node_type]['text'].append(node_id)
    node_traces[node_type]['labels'].append(node_data['label'])

# Create figure
fig = go.Figure()

# Add edges
for trace in edge_trace:
    fig.add_trace(trace)

# Add nodes
for node_type, data in node_traces.items():
    # Determine size based on type
    size_map = {
        'SafetyIssue': 50,
        'Regulation': 40,
        'Case': 35,
        'Vessel': 30,
        'Evidence': 25,
        'Lesson': 25,
        'Action': 25,
    }
    node_size = size_map.get(node_type, 30)

    fig.add_trace(go.Scatter(
        x=data['x'],
        y=data['y'],
        mode='markers+text',
        marker=dict(
            size=node_size,
            color=data['color'],
            line=dict(width=2, color='white')
        ),
        text=data['labels'],
        textposition="top center",
        textfont=dict(size=9, color='white', family='Inter'),
        hovertemplate='<b>%{text}</b><br>Type: ' + node_type + '<extra></extra>',
        name=node_type,
        showlegend=True
    ))

fig.update_layout(
    showlegend=True,
    hovermode='closest',
    margin=dict(b=0, l=0, r=0, t=0),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='rgba(15, 23, 42, 1)',
    paper_bgcolor='rgba(15, 23, 42, 1)',
    height=700,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor="rgba(30, 41, 59, 0.8)",
        bordercolor="rgba(148, 163, 184, 0.3)",
        borderwidth=1,
        font=dict(color='white')
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Graph statistics
st.markdown("""
<div class="section-header">
    📊 그래프 통계
</div>
""", unsafe_allow_html=True)

stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)

with stat_col1:
    st.metric("Total Nodes", len(G.nodes()), "Entities")

with stat_col2:
    st.metric("Total Edges", len(G.edges()), "Relationships")

with stat_col3:
    st.metric("Regulation Nodes", len([n for n, d in G.nodes(data=True) if d['type'] == 'Regulation']), "Rules")

with stat_col4:
    st.metric("Case Nodes", len([n for n, d in G.nodes(data=True) if d['type'] == 'Case']), "Precedents")

with stat_col5:
    avg_degree = sum(dict(G.degree()).values()) / len(G.nodes()) if len(G.nodes()) > 0 else 0
    st.metric("Avg Connections", f"{avg_degree:.1f}", "per node")

st.markdown("<br>", unsafe_allow_html=True)

# Interactive exploration
st.markdown("""
<div class="section-header">
    🔎 인터랙티브 탐색
</div>
""", unsafe_allow_html=True)

explore_col1, explore_col2 = st.columns(2)

with explore_col1:
    selected_node = st.selectbox(
        "노드 선택",
        options=list(G.nodes()),
        format_func=lambda x: f"{nodes[x]['label']} ({nodes[x]['type']})"
    )

with explore_col2:
    if selected_node:
        neighbors = list(G.neighbors(selected_node))
        st.info(f"**{selected_node}** has {len(neighbors)} connections")

if selected_node:
    st.markdown(f"""
    <div class="info-card">
        <h4>🎯 Selected Node: {nodes[selected_node]['label']}</h4>
        <p><strong>Type:</strong> {nodes[selected_node]['type']}</p>
        <p><strong>ID:</strong> {selected_node}</p>
        <p><strong>Connections:</strong> {len(neighbors)}</p>
        <p><strong>Connected to:</strong></p>
        <ul>
    """, unsafe_allow_html=True)

    for neighbor in neighbors:
        st.markdown(f"<li>{nodes[neighbor]['label']} ({nodes[neighbor]['type']})</li>", unsafe_allow_html=True)

    st.markdown("</ul></div>", unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown(f"""
<div style="text-align: center; color: var(--text-muted); padding: 1rem 0;">
    <p>Ontology Map | Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</div>
""", unsafe_allow_html=True)
