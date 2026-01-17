"""
National Legislative Ontology (NLO)
Semantic Core Framework - Detailed Ontology Browser
"""

import streamlit as st
from pathlib import Path
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Ontology Browser - Maritime Safety Platform",
    page_icon="📚",
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
    National Legislative Ontology (NLO)
</div>
<div class="sub-header">
    Semantic Core Framework • Last Updated: 2025-03-24 • v1.1.0
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Top controls
control_col1, control_col2, control_col3 = st.columns([2, 1, 1])

with control_col1:
    st.markdown("""
    <div class="status-badge status-syncing" style="display: inline-block; font-size: 1rem; padding: 0.5rem 1.5rem;">
        🔄 SYNC LIVE
    </div>
    """, unsafe_allow_html=True)

with control_col2:
    st.button("📊 Share", use_container_width=True)

with control_col3:
    st.button("🖨️ Print Definition", use_container_width=True, type="primary")

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📦 OBJECT TYPES", "🔗 RELATIONS", "💻 CODE"])

# Ontology data
entity_types = {
    "법안 (Bill)": {
        "uri": "URI: BILL",
        "count": 13,
        "definition": "국회에 발의된 법률안의 최상위 엔티티",
        "color": "#EF4444",
        "properties": [
            {"name": "addresses (해결함)", "description": "법안이 특정 정책 현안을 해결함을 명시"},
            {"name": "cites (인용함)", "description": "A 법안 B 법안이나 기존 법률을 인용함을 표시"}
        ]
    },
    "조항 (Clauses)": {
        "uri": "URI: CLAUSE",
        "count": 45,
        "definition": "규정의 세부 조항 및 하위 항목",
        "color": "#EC4899",
        "properties": [
            {"name": "part_of (소속)", "description": "조항이 특정 규정에 속함"},
            {"name": "requires (요구)", "description": "조항이 특정 조치를 요구함"}
        ]
    },
    "정책 현안 (Policy Issue)": {
        "uri": "URI: POLICY_ISSUE",
        "count": 12,
        "definition": "해양에서 발생 가능한 안전 위험 상황",
        "color": "#3B82F6",
        "properties": [
            {"name": "addressed_by (해결됨)", "description": "어떤 규정이 이 현안을 해결하는가"},
            {"name": "evidenced_by (증거)", "description": "어떤 증거로 확인되는가"}
        ]
    },
    "이해관계자 (Stakeholder)": {
        "uri": "URI: STAKEHOLDER",
        "count": 24,
        "definition": "선박, 선원, 관계 기관 등 해양 안전 이해관계자",
        "color": "#10B981",
        "properties": [
            {"name": "operates (운영)", "description": "선박을 운영함"},
            {"name": "affected_by (영향받음)", "description": "안전 현안의 영향을 받음"}
        ]
    },
    "입법 근거 (Evidence)": {
        "uri": "URI: EVIDENCE",
        "count": 16,
        "definition": "레이더, AIS, VDR 등 사건을 뒷받침하는 데이터 및 증거",
        "color": "#8B5CF6",
        "properties": [
            {"name": "supports (뒷받침)", "description": "사례를 뒷받침함"},
            {"name": "indicates (나타냄)", "description": "안전 현안을 나타냄"}
        ]
    }
}

with tab1:
    # Sidebar for entity type selection
    sidebar_col, content_col = st.columns([1, 3])

    with sidebar_col:
        st.markdown("""
        <div class="section-header" style="font-size: 1.2rem;">
            OBJECT TYPES
        </div>
        """, unsafe_allow_html=True)

        selected_entity = st.radio(
            "Select entity type",
            options=list(entity_types.keys()),
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Entity type cards
        for entity_name, entity_data in entity_types.items():
            is_selected = entity_name == selected_entity
            card_class = "entity-type-card active" if is_selected else "entity-type-card"

            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>{entity_name}</span>
                    <span class="entity-count">{entity_data['count']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with content_col:
        if selected_entity:
            entity_data = entity_types[selected_entity]

            # Entity header
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {entity_data['color']}20 0%, {entity_data['color']}10 100%);
                        border: 2px solid {entity_data['color']};
                        border-radius: 1rem;
                        padding: 2rem;
                        margin-bottom: 2rem;">
                <h2 style="margin: 0; color: {entity_data['color']};">{selected_entity}</h2>
                <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">{entity_data['uri']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Definition
            st.markdown(f"""
            <div class="info-card">
                <h4>📝 DEFINITION (RDFS:COMMENT)</h4>
                <p style="font-size: 1.1rem; line-height: 1.8;"
>"{entity_data['definition']}"</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Properties & Attributes
            st.markdown("""
            <div class="section-header">
                📊 ASSOCIATED PROPERTIES & ATTRIBUTES
            </div>
            """, unsafe_allow_html=True)

            # Property cards grid
            prop_cols = st.columns(2)
            for idx, prop in enumerate(entity_data['properties']):
                with prop_cols[idx % 2]:
                    st.markdown(f"""
                    <div class="property-card">
                        <div style="background: rgba(59, 130, 246, 0.2);
                                    padding: 0.5rem;
                                    border-radius: 0.5rem;
                                    margin-bottom: 0.75rem;">
                            <strong style="color: var(--primary-blue);">OBJECTPROPERTY</strong>
                        </div>
                        <h4 style="margin-bottom: 0.5rem;">{prop['name']}</h4>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">
                            {prop['description']}
                        </p>
                        <div style="margin-top: 1rem; padding: 0.75rem;
                                    background: rgba(148, 163, 184, 0.1);
                                    border-radius: 0.375rem;">
                            <small><strong>RANGE:</strong> POLICY_ISSUE</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Example instances
            st.markdown("""
            <div class="section-header">
                🔍 Example Instances
            </div>
            """, unsafe_allow_html=True)

            if selected_entity == "법안 (Bill)":
                examples = [
                    {"id": "COLREG-Rule-15", "title": "횡단하는 상태 (Crossing Situation)", "weight": 9},
                    {"id": "COLREG-Rule-19", "title": "시계 제한 상황 (Restricted Visibility)", "weight": 10},
                    {"id": "COLREG-Rule-05", "title": "경계 (Look-out)", "weight": 10},
                ]
            elif selected_entity == "정책 현안 (Policy Issue)":
                examples = [
                    {"id": "SI-Collision-Risk", "title": "충돌 위험 (Collision Risk)", "weight": 9},
                    {"id": "SI-Restricted-Visibility", "title": "시계 제한 (Restricted Visibility)", "weight": 10},
                    {"id": "SI-Crossing-Situation", "title": "횡단 상황 (Crossing Situation)", "weight": 8},
                ]
            else:
                examples = [
                    {"id": "Example-001", "title": f"{selected_entity} Instance 1", "weight": 8},
                    {"id": "Example-002", "title": f"{selected_entity} Instance 2", "weight": 7},
                ]

            for example in examples:
                st.markdown(f"""
                <div class="search-result">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0;">{example['title']}</h4>
                        <div class="priority-badge priority-1">Weight: {example['weight']}</div>
                    </div>
                    <p style="color: var(--text-muted); margin-top: 0.5rem;">
                        <strong>URI:</strong> {example['id']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="section-header">
        🔗 Ontology Relationships (Object Properties)
    </div>
    """, unsafe_allow_html=True)

    relationships = [
        {
            "name": "addresses (해결함)",
            "domain": "Regulation",
            "range": "SafetyIssue",
            "description": "A regulation addresses a specific safety issue",
            "inverse": "addressed_by"
        },
        {
            "name": "violated (위반함)",
            "domain": "MaritimeCase",
            "range": "Regulation",
            "description": "A case involved violation of a regulation",
            "inverse": None
        },
        {
            "name": "supports (뒷받침함)",
            "domain": "Evidence",
            "range": "MaritimeCase",
            "description": "Evidence supports a maritime case",
            "inverse": "supported_by"
        },
        {
            "name": "teaches (교훈을 줌)",
            "domain": "MaritimeCase",
            "range": "Lesson",
            "description": "A case teaches specific lessons",
            "inverse": "learned_from"
        },
    ]

    for rel in relationships:
        st.markdown(f"""
        <div class="property-card">
            <h3 style="color: var(--primary-blue); margin-bottom: 1rem;">{rel['name']}</h3>
            <div class="property-grid" style="grid-template-columns: 1fr 1fr;">
                <div>
                    <div class="property-label">DOMAIN</div>
                    <div class="property-value">{rel['domain']}</div>
                </div>
                <div>
                    <div class="property-label">RANGE</div>
                    <div class="property-value">{rel['range']}</div>
                </div>
            </div>
            <div style="margin-top: 1rem;">
                <div class="property-label">DESCRIPTION</div>
                <div class="property-value">{rel['description']}</div>
            </div>
            {f'<div style="margin-top: 0.75rem;"><span class="status-badge status-optimal">Inverse: {rel["inverse"]}</span></div>' if rel['inverse'] else ''}
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="section-header">
        💻 RDF/Turtle Code
    </div>
    """, unsafe_allow_html=True)

    st.code("""
@prefix mso: <http://weoffice.ai/ontology/maritime-safety#> .
@prefix colreg: <http://weoffice.ai/ontology/colregs#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Example Instance
colreg:rule-15 a mso:Regulation ;
    mso:titleKr "횡단하는 상태"@ko ;
    mso:titleEn "Crossing Situation"@en ;
    mso:legalWeight 9 ;
    mso:addresses mso:SI-Crossing ;
    mso:contains colreg:rule-15-a, colreg:rule-15-b .

mso:SI-Crossing a mso:SafetyIssue ;
    mso:nameKr "횡단 충돌 위험"@ko ;
    mso:severity 9 ;
    mso:addressed_by colreg:rule-15 .

mso:KMST-2023-002 a mso:MaritimeCase ;
    mso:titleKr "횡단 상황에서의 화물선 충돌"@ko ;
    mso:date "2023-05-20"^^xsd:date ;
    mso:violated colreg:rule-15 ;
    mso:exampleOf mso:SI-Crossing ;
    mso:teaches mso:lesson-early-action .
    """, language="turtle")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h4>📥 Download Options</h4>
        <p>You can export the ontology in multiple formats:</p>
        <ul>
            <li><strong>Turtle (.ttl)</strong> - Human-readable RDF format</li>
            <li><strong>RDF/XML (.rdf)</strong> - XML-based RDF format</li>
            <li><strong>JSON-LD (.jsonld)</strong> - JSON format for Linked Data</li>
            <li><strong>N-Triples (.nt)</strong> - Line-based triple format</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Statistics footer
st.markdown("""
<div class="section-header">
    📊 Ontology Statistics
</div>
""", unsafe_allow_html=True)

stats_col1, stats_col2, stats_col3, stats_col4, stats_col5 = st.columns(5)

with stats_col1:
    st.metric("Total Classes", "11", "Entity Types")

with stats_col2:
    st.metric("Object Properties", "28", "Relationships")

with stats_col3:
    st.metric("Data Properties", "45", "Attributes")

with stats_col4:
    st.metric("Total Instances", "110", "Entities")

with stats_col5:
    st.metric("Total Triples", "1,247", "RDF Statements")

st.markdown("---")

# Footer
st.markdown(f"""
<div style="text-align: center; color: var(--text-muted); padding: 1rem 0;">
    <p>National Legislative Intelligence Engine | Security Level: Public</p>
    <p>Maritime Safety Ontology v2.0 | Last Synced: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
</div>
""", unsafe_allow_html=True)
