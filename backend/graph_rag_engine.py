"""
Graph-Guided RAG 엔진 (쿼리 수정 버전)
"""
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
import google.generativeai as genai
from dataclasses import dataclass
import json

@dataclass
class ReasoningStep:
    step_name: str
    step_number: int
    description: str
    query: Optional[str] = None
    results: Optional[List[Dict]] = None
    reasoning: Optional[str] = None


class GraphGuidedRAG:
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
        self.reset_reasoning_history()
        perception = self._step1_perception(situation_data)
        graph_context = self._step2_graph_context(perception)
        relevant_rules = self._step3_rule_retrieval(graph_context)
        relevant_cases = self._step4_case_retrieval(graph_context, relevant_rules)
        analysis = self._step5_llm_analysis(situation_data, relevant_rules, relevant_cases)
        recommendations = self._step6_action_recommendation(
            situation_data, relevant_rules, relevant_cases, analysis
        )

        return {
            "situation": situation_data,
            "perception": perception,
            "graph_context": graph_context,
            "relevant_rules": relevant_rules,
            "relevant_cases": relevant_cases,
            "analysis": analysis,
            "recommendations": recommendations,
            "reasoning_history": [
                {
                    "step_name": step.step_name,
                    "step_number": step.step_number,
                    "description": step.description,
                    "reasoning": step.reasoning,
                    "results_count": len(step.results) if step.results else 0
                }
                for step in self.reasoning_history
            ]
        }

    def _step1_perception(self, situation_data: Dict[str, Any]) -> Dict[str, Any]:
        situation = situation_data.get('situation', {})
        own_ship = situation.get('own_ship', {})
        targets = situation.get('target_vessels', [])

        perception = {
            "visibility": situation.get('visibility'),
            "own_ship_type": own_ship.get('type'),
            "target_count": len(targets),
            "targets": targets
        }

        self.add_reasoning_step(ReasoningStep(
            step_name="Perception",
            step_number=1,
            description="상황 데이터 인식",
            results=[perception],
            reasoning=f"시계: {perception['visibility']}, 타선: {len(targets)}척"
        ))
        return perception

    def _step2_graph_context(self, perception: Dict[str, Any]) -> Dict[str, Any]:
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
            results = session.run(query, situation_types=situation_types)
            graph_data = [dict(record) for record in results]

        self.add_reasoning_step(ReasoningStep(
            step_name="Graph Context",
            step_number=2,
            description="상황 맥락 추출",
            query=query,
            results=graph_data,
            reasoning=f"식별된 상황: {', '.join(situation_types)}"
        ))
        return {"identified_situations": situation_types, "graph_nodes": graph_data}

    def _determine_situation_types(self, perception: Dict[str, Any]) -> List[str]:
        types = []
        vis = perception.get("visibility", "")
        if "안개" in vis or "농무" in vis: types.append("시계 제한")
        for t in perception.get("targets", []):
            if "우현" in str(t.get("relative_position", "")): types.append("횡단 상황")
            if "마주" in str(t.get("bearing", "")): types.append("마주치는 상황")
        return list(set(types)) if types else ["일반 항행"]

    def _step3_rule_retrieval(self, graph_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Step 3: 규정 검색 (쿼리 수정됨)"""
        situation_types = graph_context.get("identified_situations", [])

        with self.driver.session() as session:
            # [수정] ORDER BY에서 별칭(legal_weight) 사용
            query = """
            MATCH (r:Rule)-[:APPLIES_TO]->(st:SituationType)
            WHERE st.name IN $situation_types
            RETURN DISTINCT r.id as rule_id,
                   r.title as title,
                   r.summary as summary,
                   r.full_text as full_text,
                   r.legal_weight as legal_weight,
                   collect(DISTINCT st.name) as situations
            ORDER BY legal_weight DESC
            LIMIT 5
            """
            results = session.run(query, situation_types=situation_types)
            rules = [dict(record) for record in results]

        self.add_reasoning_step(ReasoningStep(
            step_name="Rule Retrieval",
            step_number=3,
            description="관련 규정 검색",
            query=query,
            results=rules
        ))
        return rules

    def _step4_case_retrieval(self, graph_context: Dict[str, Any], rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Step 4: 사례 검색 (쿼리 수정됨 - 에러 원인 해결)"""
        rule_ids = [r['rule_id'] for r in rules]

        with self.driver.session() as session:
            # [수정] 
            # 1. RETURN 절에 c.legal_weight as legal_weight 추가
            # 2. ORDER BY 절을 c.legal_weight -> legal_weight (별칭)로 변경
            query = """
            MATCH (c:Case)-[:VIOLATED]->(r:Rule)
            WHERE r.id IN $rule_ids
            OPTIONAL MATCH (c)-[:TEACHES]->(l:Lesson)
            RETURN DISTINCT c.case_id as case_id,
                   c.title as title,
                   c.situation_type as situation_type,
                   c.analysis as analysis,
                   c.judgment as judgment,
                   c.legal_weight as legal_weight,
                   collect(DISTINCT l.text) as lessons
            ORDER BY legal_weight DESC
            LIMIT 3
            """
            results = session.run(query, rule_ids=rule_ids)
            cases = [dict(record) for record in results]

        self.add_reasoning_step(ReasoningStep(
            step_name="Case Retrieval",
            step_number=4,
            description="유사 판례 검색",
            query=query,
            results=cases
        ))
        return cases

    def _step5_llm_analysis(self, situation, rules, cases) -> str:
        prompt = f"""
        상황: {json.dumps(situation.get('situation', {}), ensure_ascii=False)}
        규정: {[r['title'] for r in rules]}
        사례: {[c['title'] for c in cases]}
        
        위 상황에 대해 COLREGs 기반으로 분석하고 조치를 권고해줘.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "LLM 분석 실패"

    def _step6_action_recommendation(self, situation, rules, cases, analysis) -> Dict[str, Any]:
        return {
            "priority_actions": [
                {"action": "안전 속력 유지", "priority": 1, "colregs": "Rule 6"},
                {"action": "경계 강화", "priority": 2, "colregs": "Rule 5"}
            ],
            "warnings": []
        }
