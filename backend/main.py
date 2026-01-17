"""
FastAPI 백엔드 - Maritime Navigation System API
(프론트엔드 크래시 방지 패치 적용)
"""
import os
import sys
import json
import traceback
from typing import List, Dict, Any, Optional

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# RAG 엔진 임포트
try:
    from graph_rag_engine import GraphGuidedRAG
except ImportError as e:
    print(f"⚠️ 모듈 임포트 실패: {e}")
    GraphGuidedRAG = None

app = FastAPI(title="Maritime API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 경로 설정
BASE_DIR = os.path.dirname(current_dir)
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
SCENARIOS_PATH = os.path.join(DATA_DIR, "demo_scenarios.json")

# RAG 엔진 관리
rag_engine = None
connection_error = None

def get_rag_engine():
    global rag_engine, connection_error
    
    if rag_engine is not None:
        return rag_engine

    NEO4J_URI = os.getenv("NEO4J_URI", "")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    print(f"🔌 Neo4j 연결 시도: URI={NEO4J_URI}, User={NEO4J_USER}")

    if not NEO4J_URI or not NEO4J_PASSWORD:
        connection_error = "Render 환경변수(NEO4J_URI 또는 NEO4J_PASSWORD)가 설정되지 않았습니다."
        print(f"❌ {connection_error}")
        return None

    try:
        rag_engine = GraphGuidedRAG(
            neo4j_uri=NEO4J_URI,
            neo4j_user=NEO4J_USER,
            neo4j_password=NEO4J_PASSWORD,
            gemini_api_key=GEMINI_API_KEY,
            llm_model=os.getenv("LLM_MODEL", "gemini-2.5-flash")
        )
        rag_engine.driver.verify_connectivity()
        print("✅ Neo4j 연결 성공!")
        connection_error = None
        return rag_engine

    except Exception as e:
        rag_engine = None
        connection_error = f"Neo4j 연결 실패: {str(e)}"
        print(f"❌ {connection_error}")
        traceback.print_exc()
        return None

# Pydantic 모델
class AnalyzeRequest(BaseModel):
    scenario_id: Optional[str] = None
    situation_data: Optional[Dict[str, Any]] = None

class AnalyzeResponse(BaseModel):
    scenario_id: Optional[str]
    analysis: Dict[str, Any]
    reasoning_steps: List[Dict[str, Any]]

def load_json_file(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

@app.get("/")
async def root():
    rag = get_rag_engine()
    status = "connected" if rag else "disconnected"
    return {
        "status": status,
        "last_error": connection_error
    }

@app.get("/scenarios")
async def list_scenarios():
    scenarios = load_json_file(SCENARIOS_PATH)
    return {"scenarios": scenarios, "count": len(scenarios)}

@app.get("/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    scenarios = load_json_file(SCENARIOS_PATH)
    scenario = next((s for s in scenarios if s.get("scenario_id") == scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_situation(request: AnalyzeRequest):
    # 1. 시나리오 데이터 로드
    if request.scenario_id:
        scenarios = load_json_file(SCENARIOS_PATH)
        situation_data = next((s for s in scenarios if s.get("scenario_id") == request.scenario_id), None)
    else:
        situation_data = request.situation_data

    # 2. RAG 엔진 로드
    rag = get_rag_engine()
    
    # 3. 연결 실패 시 에러 반환
    if not rag:
        error_msg = connection_error if connection_error else "알 수 없는 연결 오류"
        return AnalyzeResponse(
            scenario_id=request.scenario_id,
            analysis={
                "error": "DB Connection Failed",
                "recommendations": { # 여기는 딕셔너리라 안전함
                    "priority_actions": [],
                    "warnings": [f"DB 연결 실패: {error_msg}"]
                }
            },
            reasoning_steps=[
                {
                    "step_name": "Connection Error",
                    "description": "Neo4j 데이터베이스 연결 실패",
                    "reasoning": f"상세 에러: {error_msg}"
                }
            ]
        )

    # 4. 분석 실행
    try:
        result = rag.analyze_situation(situation_data)
        return AnalyzeResponse(
            scenario_id=request.scenario_id,
            analysis=result,
            reasoning_steps=result.get("reasoning_history", [])
        )
    except Exception as e:
        # [핵심 수정] 에러 발생 시 recommendations를 빈 딕셔너리({})로 반환
        print(f"Runtime Error: {e}")
        traceback.print_exc()
        return AnalyzeResponse(
            scenario_id=request.scenario_id,
            analysis={
                "error": str(e), 
                "recommendations": {} # <-- 여기가 [] 였던 게 문제였습니다! {}로 수정됨.
            },
            reasoning_steps=[{"step_name": "Runtime Error", "reasoning": str(e)}]
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
