"""
Neo4j 데이터베이스 스키마 설계 및 데이터 로딩
Graph-Guided RAG를 위한 온톨로지 구축
"""
import json
import os
from typing import List, Dict, Any
from neo4j import GraphDatabase
import openai

class Neo4jMaritimeKnowledgeGraph:
    """해상 항법 지식 그래프 구축 및 관리"""

    def __init__(self, uri: str, user: str, password: str, openai_api_key: str = None):
        """
        Args:
            uri: Neo4j 데이터베이스 URI
            user: Neo4j 사용자명
            password: Neo4j 비밀번호
            openai_api_key: OpenAI API 키 (임베딩용)
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        if openai_api_key:
            openai.api_key = openai_api_key

    def close(self):
        """데이터베이스 연결 종료"""
        self.driver.close()

    def clear_database(self):
        """데이터베이스 초기화 (개발용)"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("✅ 데이터베이스 초기화 완료")

    def create_schema(self):
        """그래프 스키마 생성 (제약 조건 및 인덱스)"""
        with self.driver.session() as session:
            # Unique constraints
            constraints = [
                "CREATE CONSTRAINT rule_id_unique IF NOT EXISTS FOR (r:Rule) REQUIRE r.id IS UNIQUE",
                "CREATE CONSTRAINT case_id_unique IF NOT EXISTS FOR (c:Case) REQUIRE c.case_id IS UNIQUE",
                "CREATE CONSTRAINT scenario_id_unique IF NOT EXISTS FOR (s:Scenario) REQUIRE s.scenario_id IS UNIQUE",
                "CREATE CONSTRAINT situation_type_unique IF NOT EXISTS FOR (st:SituationType) REQUIRE st.name IS UNIQUE",
                "CREATE CONSTRAINT vessel_type_unique IF NOT EXISTS FOR (vt:VesselType) REQUIRE vt.name IS UNIQUE",
            ]

            for constraint in constraints:
                try:
                    session.run(constraint)
                    print(f"✅ 제약 조건 생성: {constraint.split('FOR')[1].split('REQUIRE')[0].strip()}")
                except Exception as e:
                    print(f"⚠️  제약 조건 생성 스킵 (이미 존재 또는 오류): {e}")

            # Indexes for full-text search
            indexes = [
                "CREATE INDEX rule_title_index IF NOT EXISTS FOR (r:Rule) ON (r.title)",
                "CREATE INDEX case_title_index IF NOT EXISTS FOR (c:Case) ON (c.title)",
            ]

            for index in indexes:
                try:
                    session.run(index)
                    print(f"✅ 인덱스 생성: {index.split('FOR')[1].split('ON')[0].strip()}")
                except Exception as e:
                    print(f"⚠️  인덱스 생성 스킵: {e}")

    def get_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        """
        텍스트 임베딩 생성

        Args:
            text: 임베딩할 텍스트
            model: OpenAI 임베딩 모델

        Returns:
            임베딩 벡터 (리스트)
        """
        try:
            response = openai.embeddings.create(
                input=text,
                model=model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"⚠️  임베딩 생성 실패: {e}")
            # 실패 시 더미 벡터 반환 (개발용)
            return [0.0] * 1536

    def load_colregs_rules(self, file_path: str):
        """COLREGs 규정 데이터를 그래프에 로딩"""
        with open(file_path, 'r', encoding='utf-8') as f:
            rules = json.load(f)

        with self.driver.session() as session:
            for rule in rules:
                # 임베딩 생성 (제목 + 요약 + 전문)
                embedding_text = f"{rule['title']}\n{rule['summary']}\n{rule['full_text']}"
                # embedding = self.get_embedding(embedding_text)  # 실제 운영 시 활성화

                # Rule 노드 생성
                cypher = """
                MERGE (r:Rule {id: $id})
                SET r.title = $title,
                    r.category = $category,
                    r.summary = $summary,
                    r.full_text = $full_text,
                    r.legal_weight = $legal_weight,
                    r.updated_at = timestamp()
                RETURN r.id as rule_id
                """

                result = session.run(cypher, **rule)
                rule_id = result.single()['rule_id']

                # SituationType 노드 생성 및 관계 설정
                for situation in rule['trigger_situations']:
                    session.run("""
                        MERGE (st:SituationType {name: $situation})
                        WITH st
                        MATCH (r:Rule {id: $rule_id})
                        MERGE (r)-[:APPLIES_TO]->(st)
                    """, situation=situation, rule_id=rule_id)

                # VesselType 노드 생성 및 관계 설정
                for vessel_type in rule['vessel_types']:
                    session.run("""
                        MERGE (vt:VesselType {name: $vessel_type})
                        WITH vt
                        MATCH (r:Rule {id: $rule_id})
                        MERGE (r)-[:GOVERNS]->(vt)
                    """, vessel_type=vessel_type, rule_id=rule_id)

                # Action 노드 생성 및 관계 설정
                for action in rule['actions']:
                    session.run("""
                        MERGE (a:Action {name: $action})
                        WITH a
                        MATCH (r:Rule {id: $rule_id})
                        MERGE (r)-[:RECOMMENDS]->(a)
                    """, action=action, rule_id=rule_id)

                print(f"✅ Rule 로딩 완료: {rule_id} - {rule['title']}")

        print(f"\n🎉 총 {len(rules)}개 COLREGs 규정 로딩 완료!")

    def load_kmst_cases(self, file_path: str):
        """해양안전심판원 재결서 데이터를 그래프에 로딩"""
        with open(file_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)

        with self.driver.session() as session:
            for case in cases:
                # Case 노드 생성
                cypher = """
                MERGE (c:Case {case_id: $case_id})
                SET c.title = $title,
                    c.date = $date,
                    c.location = $location,
                    c.situation_type = $situation_type,
                    c.incident_description = $incident_description,
                    c.analysis = $analysis,
                    c.judgment = $judgment,
                    c.penalty = $penalty,
                    c.legal_weight = $legal_weight,
                    c.updated_at = timestamp()
                RETURN c.case_id as case_id
                """

                result = session.run(cypher, **{
                    'case_id': case['case_id'],
                    'title': case['title'],
                    'date': case['date'],
                    'location': case['location'],
                    'situation_type': case['situation_type'],
                    'incident_description': case['incident_description'],
                    'analysis': case['analysis'],
                    'judgment': case['judgment'],
                    'penalty': case['penalty'],
                    'legal_weight': case['legal_weight']
                })

                case_id = result.single()['case_id']

                # Case와 Rule 관계 설정
                for rule_id in case['colregs_violated']:
                    session.run("""
                        MATCH (c:Case {case_id: $case_id})
                        MATCH (r:Rule {id: $rule_id})
                        MERGE (c)-[:VIOLATED]->(r)
                    """, case_id=case_id, rule_id=rule_id)

                # SituationType과 관계 설정
                session.run("""
                    MERGE (st:SituationType {name: $situation_type})
                    WITH st
                    MATCH (c:Case {case_id: $case_id})
                    MERGE (c)-[:OCCURRED_IN]->(st)
                """, situation_type=case['situation_type'], case_id=case_id)

                # Lessons learned 저장
                if 'lessons_learned' in case:
                    for lesson in case['lessons_learned']:
                        session.run("""
                            MERGE (l:Lesson {text: $lesson})
                            WITH l
                            MATCH (c:Case {case_id: $case_id})
                            MERGE (c)-[:TEACHES]->(l)
                        """, lesson=lesson, case_id=case_id)

                print(f"✅ Case 로딩 완료: {case_id} - {case['title']}")

        print(f"\n🎉 총 {len(cases)}개 재결서 로딩 완료!")

    def load_scenarios(self, file_path: str):
        """시연용 시나리오 데이터를 그래프에 로딩"""
        with open(file_path, 'r', encoding='utf-8') as f:
            scenarios = json.load(f)

        with self.driver.session() as session:
            for scenario in scenarios:
                # Scenario 노드 생성
                cypher = """
                MERGE (s:Scenario {scenario_id: $scenario_id})
                SET s.title = $title,
                    s.thumbnail_desc = $thumbnail_desc,
                    s.difficulty = $difficulty,
                    s.risk_level = $risk_level,
                    s.situation = $situation,
                    s.updated_at = timestamp()
                RETURN s.scenario_id as scenario_id
                """

                result = session.run(cypher, **{
                    'scenario_id': scenario['scenario_id'],
                    'title': scenario['title'],
                    'thumbnail_desc': scenario['thumbnail_desc'],
                    'difficulty': scenario['difficulty'],
                    'risk_level': scenario['risk_level'],
                    'situation': json.dumps(scenario['situation'], ensure_ascii=False)
                })

                scenario_id = result.single()['scenario_id']

                # Scenario와 Rule 관계 설정
                if 'related_rules' in scenario:
                    for rule_id in scenario['related_rules']:
                        session.run("""
                            MATCH (s:Scenario {scenario_id: $scenario_id})
                            MATCH (r:Rule {id: $rule_id})
                            MERGE (s)-[:REQUIRES]->(r)
                        """, scenario_id=scenario_id, rule_id=rule_id)

                # Scenario와 Case 관계 설정
                if 'related_cases' in scenario:
                    for case_id in scenario['related_cases']:
                        session.run("""
                            MATCH (s:Scenario {scenario_id: $scenario_id})
                            MATCH (c:Case {case_id: $case_id})
                            MERGE (s)-[:SIMILAR_TO]->(c)
                        """, scenario_id=scenario_id, case_id=case_id)

                print(f"✅ Scenario 로딩 완료: {scenario_id} - {scenario['title']}")

        print(f"\n🎉 총 {len(scenarios)}개 시나리오 로딩 완료!")

    def create_additional_relationships(self):
        """추가 관계 생성 (추론을 위한 메타 관계)"""
        with self.driver.session() as session:
            # 동일한 SituationType을 공유하는 Rule과 Case 연결
            session.run("""
                MATCH (r:Rule)-[:APPLIES_TO]->(st:SituationType)<-[:OCCURRED_IN]-(c:Case)
                MERGE (c)-[:EXAMPLE_OF]->(r)
            """)
            print("✅ Case-Rule 추가 관계 생성 완료")

            # 동일한 Rule을 위반한 Case들 간 관계
            session.run("""
                MATCH (c1:Case)-[:VIOLATED]->(r:Rule)<-[:VIOLATED]-(c2:Case)
                WHERE c1.case_id < c2.case_id
                MERGE (c1)-[:RELATED_CASE]->(c2)
            """)
            print("✅ Case-Case 관계 생성 완료")

    def verify_data(self):
        """데이터 로딩 검증"""
        with self.driver.session() as session:
            # 노드 카운트
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)

            print("\n📊 노드 통계:")
            for record in result:
                print(f"  - {record['label']}: {record['count']}개")

            # 관계 카운트
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)

            print("\n🔗 관계 통계:")
            for record in result:
                print(f"  - {record['rel_type']}: {record['count']}개")

    def create_sample_query_patterns(self):
        """샘플 쿼리 패턴 생성 (테스트용)"""
        print("\n🔍 샘플 Cypher 쿼리:")

        print("\n1️⃣ 특정 상황에 적용되는 규정 찾기:")
        print("""
        MATCH (r:Rule)-[:APPLIES_TO]->(st:SituationType {name: '횡단 상황'})
        RETURN r.id, r.title, r.summary
        """)

        print("\n2️⃣ 특정 규정을 위반한 사고 사례 찾기:")
        print("""
        MATCH (c:Case)-[:VIOLATED]->(r:Rule {id: 'rule_15'})
        RETURN c.case_id, c.title, c.judgment
        """)

        print("\n3️⃣ 시나리오에 필요한 규정과 참고 사례 찾기:")
        print("""
        MATCH (s:Scenario {scenario_id: 'scenario_002'})
        OPTIONAL MATCH (s)-[:REQUIRES]->(r:Rule)
        OPTIONAL MATCH (s)-[:SIMILAR_TO]->(c:Case)
        RETURN s.title, collect(DISTINCT r.title) as rules, collect(DISTINCT c.title) as cases
        """)

        print("\n4️⃣ 특정 상황에 대한 규정 → 사례 → 교훈 경로:")
        print("""
        MATCH path = (st:SituationType {name: '안개'})<-[:APPLIES_TO]-(r:Rule)<-[:VIOLATED]-(c:Case)-[:TEACHES]->(l:Lesson)
        RETURN r.title as rule, c.title as case_example, l.text as lesson
        LIMIT 5
        """)


def main():
    """메인 실행 함수"""
    # 환경 변수에서 설정 읽기 (실제 운영 시)
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

    # 데이터 파일 경로
    DATA_DIR = "/home/user/HASS/data/raw"
    COLREGS_FILE = os.path.join(DATA_DIR, "colregs_rules.json")
    KMST_FILE = os.path.join(DATA_DIR, "kmst_cases.json")
    SCENARIOS_FILE = os.path.join(DATA_DIR, "demo_scenarios.json")

    print("🚢 해상 항법 지식 그래프 구축 시작...\n")

    kg = Neo4jMaritimeKnowledgeGraph(
        uri=NEO4J_URI,
        user=NEO4J_USER,
        password=NEO4J_PASSWORD,
        openai_api_key=OPENAI_API_KEY
    )

    try:
        # 1. 데이터베이스 초기화 (주의: 기존 데이터 삭제)
        # kg.clear_database()

        # 2. 스키마 생성
        print("📐 스키마 생성 중...")
        kg.create_schema()

        # 3. 데이터 로딩
        print("\n📚 COLREGs 규정 로딩 중...")
        kg.load_colregs_rules(COLREGS_FILE)

        print("\n⚖️  해양안전심판원 재결서 로딩 중...")
        kg.load_kmst_cases(KMST_FILE)

        print("\n🎬 시연용 시나리오 로딩 중...")
        kg.load_scenarios(SCENARIOS_FILE)

        # 4. 추가 관계 생성
        print("\n🔗 추가 관계 생성 중...")
        kg.create_additional_relationships()

        # 5. 검증
        kg.verify_data()

        # 6. 샘플 쿼리 출력
        kg.create_sample_query_patterns()

        print("\n✅ 모든 데이터 로딩 완료!")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

    finally:
        kg.close()


if __name__ == "__main__":
    main()
