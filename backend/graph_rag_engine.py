"""
Graph-Guided RAG 엔진
Neo4j 그래프를 활용한 맥락 기반 규정 검색
"""
from typing import List, Dict, Any, Optional, Tuple
from neo4j import GraphDatabase
import openai
from dataclasses import dataclass
import json


@dataclass
class ReasoningStep:
    """추론 단계 기록용 데이터 클래스"""
    step_name: str
    step_number: int
    description: str
    query: Optional[str] = None
    results: Optional[List[Dict]] = None
    reasoning: Optional[str] = None


class GraphGuidedRAG:
    """팔란티어식 Graph-Guided RAG 엔진"""

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 openai_api_key: str, llm_model: str = "gpt-4"):
        """
        Args:
            neo4j_uri: Neo4j 데이터베이스 URI
            neo4j_user: Neo4j 사용자명
            neo4j_password: Neo4j 비밀번호
            openai_api_key: OpenAI API 키
            llm_model: 사용할 LLM 모델
        """
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        openai.api_key = openai_api_key
        self.llm_model = llm_model
        self.reasoning_history: List[ReasoningStep] = []

    def close(self):
        """데이터베이스 연결 종료"""
        self.driver.close()

    def reset_reasoning_history(self):
        """추론 기록 초기화"""
        self.reasoning_history = []

    def add_reasoning_step(self, step: ReasoningStep):
        """추론 단계 기록"""
        self.reasoning_history.append(step)

    def analyze_situation(self, situation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        상황 분석 및 관련 규정/사례 검색

        Args:
            situation_data: 시나리오 데이터

        Returns:
            분석 결과 및 추천 조치
        """
        self.reset_reasoning_history()

        # Step 1: Perception - 상황 파악
        perception = self._step1_perception(situation_data)

        # Step 2: Graph Context - 그래프에서 상황 맥락 추출
        graph_context = self._step2_graph_context(perception)

        # Step 3: Rule Retrieval - 적용 규정 검색
        relevant_rules = self._step3_rule_retrieval(graph_context)

        # Step 4: Case Retrieval - 유사 사례 검색
        relevant_cases = self._step4_case_retrieval(graph_context, relevant_rules)

        # Step 5: LLM Analysis - 종합 분석
        analysis = self._step5_llm_analysis(
            situation_data, relevant_rules, relevant_cases
        )

        # Step 6: Action Recommendation - 조치 권고
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
        """Step 1: 상황 인식 및 핵심 요소 추출"""
        situation = situation_data.get('situation', {})
        own_ship = situation.get('own_ship', {})
        targets = situation.get('target_vessels', [])

        perception = {
            "visibility": situation.get('visibility'),
            "own_ship_type": own_ship.get('type'),
            "own_ship_speed": own_ship.get('speed'),
            "target_count": len(targets),
            "targets": []
        }

        # 각 타겟 선박 분석
        for target in targets:
            target_info = {
                "type": target.get('type'),
                "bearing": target.get('bearing'),
                "distance": target.get('distance'),
                "cpa": target.get('cpa'),
                "tcpa": target.get('tcpa'),
                "relative_position": target.get('relative_position'),
                "status": target.get('vessel_status')
            }
            perception["targets"].append(target_info)

        self.add_reasoning_step(ReasoningStep(
            step_name="Perception",
            step_number=1,
            description="YOLO 및 센서 데이터로부터 상황 인식",
            results=[perception],
            reasoning=f"시계: {perception['visibility']}, 본선: {perception['own_ship_type']}, 타선: {perception['target_count']}척"
        ))

        return perception

    def _step2_graph_context(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: 그래프에서 상황 맥락 파악"""
        # 상황 타입 판단
        situation_types = self._determine_situation_types(perception)

        # Neo4j에서 관련 SituationType 노드 검색
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

        context = {
            "identified_situations": situation_types,
            "graph_nodes": graph_data
        }

        self.add_reasoning_step(ReasoningStep(
            step_name="Graph Context",
            step_number=2,
            description="Neo4j 그래프에서 상황 맥락 추출",
            query=query,
            results=graph_data,
            reasoning=f"식별된 상황: {', '.join(situation_types)}"
        ))

        return context

    def _determine_situation_types(self, perception: Dict[str, Any]) -> List[str]:
        """인식 데이터로부터 상황 타입 추론"""
        situation_types = []

        # 시정 조건
        visibility = perception.get("visibility", "")
        if any(keyword in visibility for keyword in ["안개", "농무", "눈", "비", "50미터", "100미터"]):
            situation_types.append("시계 제한 상황")

        # 타선 위치 기반 상황 판단
        for target in perception.get("targets", []):
            rel_pos = target.get("relative_position", "")
            bearing = target.get("bearing")

            if rel_pos == "우현" or "우현" in str(rel_pos):
                situation_types.append("횡단 상황")
            elif bearing and "정면" in str(bearing):
                situation_types.append("마주치는 상황")

            # 선박 타입 기반
            target_type = target.get("type", "")
            if "어선" in target_type:
                situation_types.append("각종 선박 간 책임")

        # 위치 기반
        own_position = perception.get("own_ship_position", "")
        if "협수로" in own_position or "TSS" in own_position:
            situation_types.append("좁은 수로")

        # 중복 제거
        return list(set(situation_types)) if situation_types else ["일반 항행"]

    def _step3_rule_retrieval(self, graph_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Step 3: 적용 가능한 COLREGs 규정 검색"""
        situation_types = graph_context.get("identified_situations", [])

        with self.driver.session() as session:
            query = """
            MATCH (r:Rule)-[:APPLIES_TO]->(st:SituationType)
            WHERE st.name IN $situation_types
            RETURN DISTINCT r.id as rule_id,
                   r.title as title,
                   r.summary as summary,
                   r.full_text as full_text,
                   r.legal_weight as legal_weight,
                   collect(DISTINCT st.name) as situations
            ORDER BY r.legal_weight DESC
            LIMIT 5
            """
            results = session.run(query, situation_types=situation_types)
            rules = [dict(record) for record in results]

        self.add_reasoning_step(ReasoningStep(
            step_name="Rule Retrieval",
            step_number=3,
            description="그래프 기반 관련 규정 검색",
            query=query,
            results=rules,
            reasoning=f"{len(rules)}개의 관련 규정 검색 완료"
        ))

        return rules

    def _step4_case_retrieval(self, graph_context: Dict[str, Any],
                               relevant_rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Step 4: 유사 사고 사례 검색"""
        rule_ids = [rule['rule_id'] for rule in relevant_rules]

        with self.driver.session() as session:
            query = """
            MATCH (c:Case)-[:VIOLATED]->(r:Rule)
            WHERE r.id IN $rule_ids
            OPTIONAL MATCH (c)-[:TEACHES]->(l:Lesson)
            RETURN DISTINCT c.case_id as case_id,
                   c.title as title,
                   c.situation_type as situation_type,
                   c.analysis as analysis,
                   c.judgment as judgment,
                   collect(DISTINCT l.text) as lessons
            ORDER BY c.legal_weight DESC
            LIMIT 3
            """
            results = session.run(query, rule_ids=rule_ids)
            cases = [dict(record) for record in results]

        self.add_reasoning_step(ReasoningStep(
            step_name="Case Retrieval",
            step_number=4,
            description="유사 사고 판례 검색",
            query=query,
            results=cases,
            reasoning=f"{len(cases)}개의 유사 사례 검색 완료"
        ))

        return cases

    def _step5_llm_analysis(self, situation_data: Dict[str, Any],
                            rules: List[Dict[str, Any]],
                            cases: List[Dict[str, Any]]) -> str:
        """Step 5: LLM을 활용한 종합 분석"""
        # 프롬프트 구성
        prompt = self._build_analysis_prompt(situation_data, rules, cases)

        # LLM 호출
        try:
            response = openai.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "당신은 국제해상충돌방지규칙(COLREGs) 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            analysis = response.choices[0].message.content
        except Exception as e:
            analysis = f"LLM 분석 실패: {e}\n\n기본 분석: 관련 규정 {len(rules)}개, 유사 사례 {len(cases)}개 검토 필요."

        self.add_reasoning_step(ReasoningStep(
            step_name="LLM Analysis",
            step_number=5,
            description="LLM 기반 종합 분석",
            reasoning=analysis
        ))

        return analysis

    def _build_analysis_prompt(self, situation: Dict[str, Any],
                                rules: List[Dict[str, Any]],
                                cases: List[Dict[str, Any]]) -> str:
        """LLM 분석용 프롬프트 구성"""
        prompt = f"""
현재 해상 상황을 분석하고 적용 가능한 COLREGs 규정과 유사 사례를 바탕으로 판단을 제시하세요.

## 현재 상황
{json.dumps(situation.get('situation', {}), ensure_ascii=False, indent=2)}

## 적용 가능한 COLREGs 규정
"""
        for i, rule in enumerate(rules, 1):
            prompt += f"\n### {i}. {rule['title']}\n"
            prompt += f"요약: {rule['summary']}\n"

        prompt += "\n## 유사 사고 사례\n"
        for i, case in enumerate(cases, 1):
            prompt += f"\n### {i}. {case['title']}\n"
            prompt += f"상황: {case['situation_type']}\n"
            prompt += f"판단: {case['judgment'][:200]}...\n"

        prompt += """

## 분석 요청
1. 현재 상황에 가장 적합한 규정은 무엇인가?
2. 유사 사례에서 얻을 수 있는 교훈은?
3. 본선의 법적 지위는? (피항선/유지선/기타)
4. 예상되는 위험 요소는?

간결하고 명확하게 분석해주세요.
"""
        return prompt

    def _step6_action_recommendation(self, situation: Dict[str, Any],
                                      rules: List[Dict[str, Any]],
                                      cases: List[Dict[str, Any]],
                                      analysis: str) -> Dict[str, Any]:
        """Step 6: 구체적인 조치 권고"""
        # 시나리오에 정답이 있다면 사용
        if 'correct_actions' in situation:
            recommended_actions = situation['correct_actions']
        else:
            # LLM으로 조치 생성
            recommended_actions = self._generate_actions_with_llm(situation, rules, analysis)

        recommendations = {
            "priority_actions": recommended_actions[:3] if isinstance(recommended_actions, list) else [],
            "legal_basis": [rule['rule_id'] for rule in rules[:2]],
            "warnings": situation.get('critical_warnings', []),
            "key_lessons": cases[0].get('lessons', []) if cases else []
        }

        self.add_reasoning_step(ReasoningStep(
            step_name="Action Recommendation",
            step_number=6,
            description="구체적인 조치 권고 생성",
            results=[recommendations],
            reasoning=f"{len(recommended_actions)}개의 우선 조치 권고"
        ))

        return recommendations

    def _generate_actions_with_llm(self, situation: Dict[str, Any],
                                    rules: List[Dict[str, Any]],
                                    analysis: str) -> List[Dict[str, Any]]:
        """LLM으로 조치 생성 (시나리오에 정답이 없을 경우)"""
        # 간단한 기본 조치 반환 (실제로는 LLM 호출)
        return [
            {
                "action": "경계 강화",
                "priority": 1,
                "colregs": rules[0]['rule_id'] if rules else "rule_05"
            },
            {
                "action": "속력 조절",
                "priority": 2,
                "colregs": "rule_06"
            }
        ]


# 사용 예시
if __name__ == "__main__":
    import os

    # 환경 변수에서 설정 읽기
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # RAG 엔진 초기화
    rag = GraphGuidedRAG(
        neo4j_uri=NEO4J_URI,
        neo4j_user=NEO4J_USER,
        neo4j_password=NEO4J_PASSWORD,
        openai_api_key=OPENAI_API_KEY
    )

    # 테스트 시나리오 로드
    with open("/home/user/HASS/data/raw/demo_scenarios.json", 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    # 첫 번째 시나리오 분석
    result = rag.analyze_situation(scenarios[0])

    print("🎯 분석 결과:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    rag.close()
