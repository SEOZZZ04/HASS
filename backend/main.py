"""
FastAPI 백엔드 - Maritime Navigation System API
(동적 경로 계산 및 모듈 경로 자동 추가 버전)
"""
import os
import sys
import json
from typing import List, Dict, Any, Optional

# [중요 1] 현재 파일(main.py)이 있는 폴더를 파이썬 검색 경로에 추가
# 이걸 해야 'ModuleNotFoundError: No module named graph_rag_engine' 에러가 사라집니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 이제 sys.path에 경로가 추가되었으므로 import가 정상 작동합니다.
try:
    from graph_rag_engine import GraphGuidedRAG
except ImportError as e:
    print(f"⚠️ 경고: graph_rag_engine을 불러올 수 없습니다. ({e})")
    GraphGuidedRAG = None

app = FastAPI(
    title="Maritime Cognitive Navigation System API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [중요 2] 파일 경로를 '절대 경로'로 동적 계산
# backend/main.py -> 부모(backend) -> 부모(root) -> data/raw
BASE_DIR = os.path.dirname(current_dir)
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

SCENARIOS_PATH = os.path.join(DATA_DIR, "demo_scenarios.json")
RULES_PATH = os.path.join(DATA_DIR, "colregs_rules.json")
CASES_PATH = os.path.join(DATA_DIR, "kmst_cases.json")

# 디버깅용: 서버 로그에 현재 데이터 경로 출력
print(f"📂 데이터 경로 설정됨: {DATA_DIR}")

# RAG 엔진 초기화
rag_engine = None

def get_rag_engine():
    """RAG 엔진 싱글톤"""
    global rag_engine
    if rag_engine is None:
        if GraphGuidedRAG is None:
            return None
            
        NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
        NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

        try:
            rag_engine = GraphGuidedRAG(
                neo4j_uri=NEO4J_URI,
                neo4j_user=NEO4J_USER,
                neo4j_password=NEO4J_PASSWORD,
                gemini_api_key=GEMINI_API_KEY,
                llm_model=os.getenv("LLM_MODEL", "gemini-2.0-flash-exp")
            )
        except Exception as e:
            print(f"❌ RAG 엔진 초기화 실패: {e}")
            return None
    return rag_engine


# Pydantic 모델
class AnalyzeRequest(BaseModel):
    scenario_id: Optional[str] = None
    situation_data: Optional[Dict[str, Any]] = None


class AnalyzeResponse(BaseModel):
    scenario_id: Optional[str]
    analysis: Dict[str, Any]
    reasoning_steps: List[Dict[str, Any]]


# 헬퍼 함수: JSON 파일 안전하게 읽기
def load_json_file(filepath):
    if not os.path.exists(filepath):
        print(f"❌ 파일을 찾을 수 없음: {filepath}")
        # 파일이 없을 경우 빈 리스트 반환하여 서버 다운 방지
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 파일 읽기 에러 ({filepath}): {e}")
        return []


# API 엔드포인트
@app.get("/")
async def root():
    return {
        "service": "Maritime Cognitive Navigation System",
        "status": "operational",
        "data_path_checked": os.path.exists(DATA_DIR)
    }


@app.get("/scenarios")
async def list_scenarios():
    scenarios = load_json_file(SCENARIOS_PATH)
    scenario_list = [
        {
            "scenario_id": s.get("scenario_id"),
            "title": s.get("title"),
            "thumbnail_desc": s.get("thumbnail_desc"),
            "difficulty": s.get("difficulty"),
            "risk_level": s.get("risk_level")
        }
        for s in scenarios
    ]
    return {"scenarios": scenario_list, "count": len(scenario_list)}


@app.get("/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    scenarios = load_json_file(SCENARIOS_PATH)
    scenario = next((s for s in scenarios if s.get("scenario_id") == scenario_id), None)

    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_situation(request: AnalyzeRequest):
    try:
        if request.scenario_id:
            scenarios = load_json_file(SCENARIOS_PATH)
            situation_data = next(
                (s for s in scenarios if s.get("scenario_id") == request.scenario_id),
                None
            )
            if situation_data is None:
                raise HTTPException(status_code=404, detail="Scenario not found")
        elif request.situation_data:
            situation_data = request.situation_data
        else:
            raise HTTPException(status_code=400, detail="Either scenario_id or situation_data required")

        rag = get_rag_engine()
        
        # RAG 엔진 연결 실패 시 안전 장치
        if rag is None:
             return AnalyzeResponse(
                scenario_id=request.scenario_id,
                analysis={
                    "situation": "System Error", 
                    "recommendations": {"priority_actions": [{"action": "백엔드 연결 확인 필요", "priority": 1}]}
                },
                reasoning_steps=[{"step": "Error", "detail": "RAG Engine load failed"}]
            )

        result = rag.analyze_situation(situation_data)

        return AnalyzeResponse(
            scenario_id=request.scenario_id,
            analysis=result,
            reasoning_steps=result.get("reasoning_history", [])
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/rules")
async def list_rules():
    rules = load_json_file(RULES_PATH)
    rule_list = [
        {
            "id": r.get("id"),
            "title": r.get("title"),
            "category": r.get("category"),
            "summary": r.get("summary")
        }
        for r in rules
    ]
    return {"rules": rule_list, "count": len(rule_list)}


@app.get("/cases")
async def list_cases():
    cases = load_json_file(CASES_PATH)
    case_list = [
        {
            "case_id": c.get("case_id"),
            "title": c.get("title"),
            "date": c.get("date"),
            "situation_type": c.get("situation_type")
        }
        for c in cases
    ]
    return {"cases": case_list, "count": len(case_list)}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
