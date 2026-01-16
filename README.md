# 🚢 Maritime Cognitive Navigation System

**팔란티어식 Vision-to-Action 해상 관제 시스템**

> AI가 YOLO Vision으로 선박을 탐지하고, Neo4j 지식 그래프에서 COLREGs 규정과 사고 판례를 검색하여, 법적 근거 기반 회피 조치를 실시간으로 권고하는 인지하는 선박(Cognitive Ship) 시스템

---

## 🎯 핵심 개념

### Vision-to-Action Pipeline

```
Camera Frame (YOLO)
    ↓
[Perception Layer] 선박 객체 탐지 (Fishing Boat, Container Ship...)
    ↓
[Semantic Layer] Neo4j 그래프: (TargetShip)-[:IS_APPROACHING {risk: 0.8}]->(OwnShip)
    ↓
[Knowledge Layer] COLREGs 규정 + 해양안전심판원 재결서 검색
    ↓
[LLM Reasoning] "제15조 적용: 본선이 피항선. 우현 30도 변침 권고"
    ↓
[Action] 대시보드 경고 + 구체적 조치 (법적 근거 포함)
```

---

## 🏗️ 아키텍처

### 3계층 온톨로지

| Layer | Technology | 역할 |
|-------|-----------|------|
| **Perception** | YOLOv8, OpenCV | 픽셀 → 의미 (객체 탐지) |
| **Semantic** | Neo4j Graph DB | 맥락 이해 (관계망) |
| **Knowledge** | Vector Store | 법규/판례 검색 |

### Graph-Guided RAG

**기존 RAG의 문제점:**
- 질문 → 전체 Vector 검색 → 느리고 부정확

**Graph-Guided RAG (팔란티어 방식):**
1. **Graph Search** (1차): 상황 → 관련 규정 (그래프 위상으로 필터링)
2. **Vector Search** (2차): 좁혀진 규정에서만 상세 검색
3. **LLM Synthesis**: 종합 판단 및 조치 권고

---

## 🚀 빠른 시작

### 로컬 실행

```bash
# 1. 리포지토리 클론
git clone https://github.com/your-username/HASS.git
cd HASS

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일에서 NEO4J_URI, OPENAI_API_KEY 설정

# 3. 의존성 설치
pip install -r requirements.txt

# 4. Neo4j 데이터 로딩
cd backend
python neo4j_loader.py

# 5. 백엔드 실행 (터미널 1)
python main.py

# 6. 프론트엔드 실행 (터미널 2)
cd ..
streamlit run frontend/app.py
```

브라우저: `http://localhost:8501`

### Render 배포

자세한 가이드: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📚 프로젝트 구조

```
HASS/
├── backend/
│   ├── main.py                  # FastAPI 서버
│   ├── graph_rag_engine.py      # Graph-Guided RAG 엔진
│   └── neo4j_loader.py          # 데이터 로딩 스크립트
├── frontend/
│   └── app.py                   # Streamlit UI
├── scripts/
│   ├── fetch_colregs.py         # COLREGs 규정 데이터
│   ├── fetch_kmst_cases.py      # 해양안전심판원 재결서
│   └── create_scenarios.py      # 시연 시나리오
├── data/
│   └── raw/                     # 생성된 데이터 (JSON)
├── requirements.txt             # 의존성
├── .env.example                 # 환경 변수 템플릿
├── DEPLOYMENT_GUIDE.md          # 배포 가이드
└── README.md                    # 이 파일
```

---

## 📊 데이터베이스

### Neo4j 그래프 구조

**노드:**
- `Rule`: COLREGs 규정 (13개)
- `Case`: 해양안전심판원 재결서 (8개)
- `Scenario`: 시연 시나리오 (6개)
- `SituationType`: 상황 유형 (횡단, 마주침, 안개 등)
- `Action`: 권고 조치

**관계:**
- `(Rule)-[:APPLIES_TO]->(SituationType)`
- `(Case)-[:VIOLATED]->(Rule)`
- `(Scenario)-[:REQUIRES]->(Rule)`
- `(Case)-[:TEACHES]->(Lesson)`

---

## 🎓 필요한 API 키

### 1. Neo4j AuraDB
- 무료 계정: [Neo4j Aura](https://neo4j.com/cloud/aura/)
- 필요 정보: URI, Username, Password

### 2. Google Gemini API
- 발급: [Google AI Studio](https://aistudio.google.com/app/apikey)
- API 키 형식: `AIzaSy...`
- 권장 모델: gemini-2.0-flash-exp (무료!)
- **장점**: 무료 할당량 풍부, OpenAI보다 저렴

---

## 📄 라이선스

MIT License

---

## 📞 문의

GitHub Issues를 통해 문의해주세요.

---

**⚓ Made with passion for maritime safety**