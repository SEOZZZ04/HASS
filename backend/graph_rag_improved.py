"""
Improved Graph-Guided RAG Engine
Returns actual rule and case content for UI display
"""
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
import google.generativeai as genai
from dataclasses import dataclass, asdict
import json

@dataclass
class ReasoningStep:
    step_name: str
    step_number: int
    description: str
    query: Optional[str] = None
    results: Optional[List[Dict]] = None
    reasoning: Optional[str] = None


class ImprovedGraphGuidedRAG:
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 gemini_api_key: str, llm_model: str = "gemini-2.0-flash-exp"):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(llm_model)
        self.reasoning_history: List[ReasoningStep] = []

    def close(self):
        self.driver.close()

    def reset_reasoning_history(self):
        self.reasoning_history = []

    def add_reasoning_step(self, step: ReasoningStep):
        self.reasoning_history.append(step)

    def analyze_situation(self, situation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main analysis pipeline"""
        self.reset_reasoning_history()

        # Step 1: Perception
        perception = self._step1_perception(situation_data)

        # Step 2: Graph Context
        graph_context = self._step2_graph_context(perception)

        # Step 3: Rule Retrieval - RETURNS ACTUAL RULES
        relevant_rules = self._step3_rule_retrieval(graph_context)

        # Step 4: Case Retrieval - RETURNS ACTUAL CASES
        relevant_cases = self._step4_case_retrieval(graph_context, relevant_rules)

        # Step 5: LLM Analysis
        analysis = self._step5_llm_analysis(situation_data, relevant_rules, relevant_cases)

        # Step 6: Action Recommendation
        recommendations = self._step6_action_recommendation(
            situation_data, relevant_rules, relevant_cases, analysis
        )

        return {
            "situation": situation_data,
            "perception": perception,
            "graph_context": graph_context,
            "relevant_rules": relevant_rules,  # FULL RULE DATA
            "relevant_cases": relevant_cases,  # FULL CASE DATA
            "analysis": analysis,
            "recommendations": recommendations,
            "reasoning_history": [
                {
                    "step_name": step.step_name,
                    "step_number": step.step_number,
                    "description": step.description,
                    "reasoning": step.reasoning,
                    "results_count": len(step.results) if step.results else 0,
                    "results": step.results  # Include actual results
                }
                for step in self.reasoning_history
            ]
        }

    def _step1_perception(self, situation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key features from situation"""
        situation = situation_data.get('situation', {})
        own_ship = situation.get('own_ship', {})
        targets = situation.get('target_vessels', [])

        perception = {
            "visibility": situation.get('visibility'),
            "own_ship_type": own_ship.get('type'),
            "target_count": len(targets),
            "targets": targets,
            "weather": situation.get('weather'),
            "time": situation.get('time')
        }

        self.add_reasoning_step(ReasoningStep(
            step_name="Perception",
            step_number=1,
            description="상황 데이터 인식 및 파싱",
            results=[perception],
            reasoning=f"시계: {perception['visibility']}, 타선: {len(targets)}척, 기상: {perception.get('weather')}"
        ))

        return perception

    def _determine_situation_types(self, perception: Dict[str, Any]) -> List[str]:
        """Determine applicable situation types"""
        situation_types = []

        visibility = str(perception.get('visibility', '')).lower()
        targets = perception.get('targets', [])

        # Check for restricted visibility
        if any(keyword in visibility for keyword in ['안개', 'fog', '50미터', '시정', '제한']):
            situation_types.append('시계 제한')

        # Check target bearings for crossing/head-on/overtaking
        for target in targets:
            bearing = str(target.get('bearing', '')).lower()

            if any(keyword in bearing for keyword in ['우현', 'starboard', '우측']):
                situation_types.append('횡단 상황')
            elif any(keyword in bearing for keyword in ['정선수', 'ahead', '전방', 'head']):
                situation_types.append('마주치는 상황')
            elif any(keyword in bearing for keyword in ['후방', 'stern', 'astern']):
                situation_types.append('추월')

        # Default if none detected
        if not situation_types:
            situation_types.append('일반 항해')

        return situation_types

    def _step2_graph_context(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Extract graph context based on situation types"""
        situation_types = self._determine_situation_types(perception)

        with self.driver.session() as session:
            query = """
            MATCH (st:SituationType)
            WHERE st.name IN $situation_types
            OPTIONAL MATCH (st)<-[:APPLIES_TO]-(r:Rule)
            OPTIONAL MATCH (st)<-[:OCCURRED_IN]-(c:Case)
            RETURN st.name as situation_type,
                   count(DISTINCT r) as rule_count,
                   count(DISTINCT c) as case_count
            """

            result = session.run(query, situation_types=situation_types)
            context_data = [dict(record) for record in result]

        graph_context = {
            "situation_types": situation_types,
            "context_data": context_data
        }

        self.add_reasoning_step(ReasoningStep(
            step_name="Graph Context",
            step_number=2,
            description="상황 맥락 추출",
            query=query,
            results=context_data,
            reasoning=f"판단된 상황: {', '.join(situation_types)}"
        ))

        return graph_context

    def _step3_rule_retrieval(self, graph_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieve applicable COLREGs rules - RETURNS FULL RULE DATA"""
        situation_types = graph_context.get('situation_types', [])

        with self.driver.session() as session:
            query = """
            MATCH (r:Rule)-[:APPLIES_TO]->(st:SituationType)
            WHERE st.name IN $situation_types
            RETURN DISTINCT r.id as id,
                   r.title as title,
                   r.summary as summary,
                   r.full_text as full_text,
                   r.legal_weight as legal_weight,
                   collect(DISTINCT st.name) as situations
            ORDER BY r.legal_weight DESC
            LIMIT 5
            """

            result = session.run(query, situation_types=situation_types)
            rules = [dict(record) for record in result]

        self.add_reasoning_step(ReasoningStep(
            step_name="Rule Retrieval",
            step_number=3,
            description=f"관련 COLREGs 규정 검색 ({len(rules)}건)",
            query=query,
            results=rules,
            reasoning=f"검색된 규정: {', '.join([r['id'] for r in rules])}"
        ))

        return rules

    def _step4_case_retrieval(self, graph_context: Dict[str, Any],
                              relevant_rules: List[Dict]) -> List[Dict[str, Any]]:
        """Retrieve similar maritime cases - RETURNS FULL CASE DATA"""
        situation_types = graph_context.get('situation_types', [])
        rule_ids = [r['id'] for r in relevant_rules]

        with self.driver.session() as session:
            query = """
            MATCH (c:Case)-[:VIOLATED]->(r:Rule)
            WHERE r.id IN $rule_ids
            OPTIONAL MATCH (c)-[:TEACHES]->(l:Lesson)
            RETURN DISTINCT c.case_id as case_id,
                   c.title as title,
                   c.situation_type as situation_type,
                   c.incident_description as incident_description,
                   c.analysis as analysis,
                   c.judgment as judgment,
                   c.penalty as penalty,
                   c.legal_weight as legal_weight,
                   collect(DISTINCT l.text) as lessons
            ORDER BY c.legal_weight DESC
            LIMIT 3
            """

            result = session.run(query, rule_ids=rule_ids)
            cases = [dict(record) for record in result]

        self.add_reasoning_step(ReasoningStep(
            step_name="Case Retrieval",
            step_number=4,
            description=f"유사 사고 판례 검색 ({len(cases)}건)",
            query=query,
            results=cases,
            reasoning=f"검색된 사례: {', '.join([c['case_id'] for c in cases])}"
        ))

        return cases

    def _step5_llm_analysis(self, situation_data: Dict[str, Any],
                           relevant_rules: List[Dict],
                           relevant_cases: List[Dict]) -> str:
        """LLM-based comprehensive analysis"""
        # Build context for LLM
        situation = situation_data.get('situation', {})

        rules_text = "\n".join([
            f"- {r['id']}: {r['title']} (가중치: {r['legal_weight']})"
            for r in relevant_rules
        ])

        cases_text = "\n".join([
            f"- {c['case_id']}: {c['title']}\n  판결: {c['judgment'][:100]}..."
            for c in relevant_cases
        ])

        prompt = f"""
당신은 해양 안전 전문가입니다. 다음 상황을 분석하고 종합 의견을 제시하세요.

**현재 상황:**
- 시계: {situation.get('visibility')}
- 본선: {situation.get('own_ship', {}).get('type')}
- 타선: {len(situation.get('target_vessels', []))}척

**적용 가능한 규정:**
{rules_text}

**유사 판례:**
{cases_text}

이 상황에서 주요 위험 요인과 법적 의무를 종합 분석하세요. (200자 이내)
"""

        try:
            response = self.model.generate_content(prompt)
            analysis = response.text
        except:
            analysis = "LLM 분석 실패. 기본 분석: 상황에 적합한 규정과 판례를 참조하세요."

        self.add_reasoning_step(ReasoningStep(
            step_name="LLM Analysis",
            step_number=5,
            description="AI 종합 분석",
            results=[{"analysis": analysis}],
            reasoning=analysis[:200]
        ))

        return analysis

    def _step6_action_recommendation(self, situation_data: Dict[str, Any],
                                    relevant_rules: List[Dict],
                                    relevant_cases: List[Dict],
                                    analysis: str) -> Dict[str, Any]:
        """Generate action recommendations"""
        situation = situation_data.get('situation', {})
        targets = situation.get('target_vessels', [])

        recommendations = {
            "priority_actions": [],
            "warnings": [],
            "legal_basis": [],
            "key_lessons": []
        }

        # Extract actions from rules
        for rule in relevant_rules:
            rule_id = rule['id']
            recommendations["legal_basis"].append(f"{rule_id}: {rule['title']}")

            # Rule-specific actions
            if 'rule_19' in rule_id.lower():
                recommendations["priority_actions"].append({
                    "action": "안전한 속력으로 감속",
                    "priority": 1,
                    "colregs": rule_id,
                    "target_speed": "5노트"
                })
            elif 'rule_15' in rule_id.lower() or 'rule_16' in rule_id.lower():
                recommendations["priority_actions"].append({
                    "action": "우현으로 대폭 변침",
                    "priority": 2,
                    "colregs": rule_id,
                    "degree_change": "30도 이상"
                })

        # Extract lessons from cases
        for case in relevant_cases:
            lessons = case.get('lessons', [])
            for lesson in lessons:
                if lesson and lesson not in recommendations["key_lessons"]:
                    recommendations["key_lessons"].append(lesson)

        # Generate warnings
        if targets:
            target = targets[0]
            cpa = str(target.get('cpa', '')).lower()

            if '0.' in cpa or '< 1' in cpa:
                recommendations["warnings"].append({
                    "warning": "충돌 위험 매우 높음!",
                    "reason": f"CPA가 {target.get('cpa')}로 매우 가까움",
                    "severity": "CRITICAL"
                })

        # Sort actions by priority
        recommendations["priority_actions"].sort(key=lambda x: x.get("priority", 999))

        self.add_reasoning_step(ReasoningStep(
            step_name="Action Recommendation",
            step_number=6,
            description=f"권고 조치 생성 ({len(recommendations['priority_actions'])}개)",
            results=[recommendations],
            reasoning="규정과 판례를 기반으로 구체적 조치 생성"
        ))

        return recommendations


# For backward compatibility
GraphGuidedRAG = ImprovedGraphGuidedRAG
