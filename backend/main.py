"""
FastAPI 백엔드 - Maritime Navigation System API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
from graph_rag_engine import GraphGuidedRAG

app = FastAPI(
    title="Maritime Cognitive Navigation System API",
    description="팔란티어식 해상 항법 의사결정 지원 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAG 엔진 초기화
rag_engine = None


def get_rag_engine():
    """RAG 엔진 싱글톤"""
    global rag_engine
    if rag_engine is None:
        NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
        NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

        rag_engine = GraphGuidedRAG(
            neo4j_uri=NEO4J_URI,
            neo4j_user=NEO4J_USER,
            neo4j_password=NEO4J_PASSWORD,
            openai_api_key=OPENAI_API_KEY,
            llm_model=os.getenv("LLM_MODEL", "gpt-4")
        )
    return rag_engine


# Pydantic 모델
class AnalyzeRequest(BaseModel):
    scenario_id: Optional[str] = None
    situation_data: Optional[Dict[str, Any]] = None


class AnalyzeResponse(BaseModel):
    scenario_id: Optional[str]
    analysis: Dict[str, Any]
    reasoning_steps: List[Dict[str, Any]]


# API 엔드포인트
@app.get("/")
async def root():
    """헬스 체크"""
    return {
        "service": "Maritime Cognitive Navigation System",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/scenarios")
async def list_scenarios():
    """시연용 시나리오 목록 조회"""
    try:
        with open("/home/user/HASS/data/raw/demo_scenarios.json", 'r', encoding='utf-8') as f:
            scenarios = json.load(f)

        # 메타데이터만 반환
        scenario_list = [
            {
                "scenario_id": s["scenario_id"],
                "title": s["title"],
                "thumbnail_desc": s["thumbnail_desc"],
                "difficulty": s["difficulty"],
                "risk_level": s["risk_level"]
            }
            for s in scenarios
        ]

        return {"scenarios": scenario_list, "count": len(scenario_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    """특정 시나리오 상세 조회"""
    try:
        with open("/home/user/HASS/data/raw/demo_scenarios.json", 'r', encoding='utf-8') as f:
            scenarios = json.load(f)

        scenario = next((s for s in scenarios if s["scenario_id"] == scenario_id), None)

        if scenario is None:
            raise HTTPException(status_code=404, detail="Scenario not found")

        return scenario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_situation(request: AnalyzeRequest):
    """
    상황 분석 및 의사결정 지원

    시나리오 ID 또는 직접 상황 데이터를 받아 분석
    """
    try:
        # 시나리오 로드
        if request.scenario_id:
            with open("/home/user/HASS/data/raw/demo_scenarios.json", 'r', encoding='utf-8') as f:
                scenarios = json.load(f)
            situation_data = next(
                (s for s in scenarios if s["scenario_id"] == request.scenario_id),
                None
            )
            if situation_data is None:
                raise HTTPException(status_code=404, detail="Scenario not found")
        elif request.situation_data:
            situation_data = request.situation_data
        else:
            raise HTTPException(status_code=400, detail="Either scenario_id or situation_data required")

        # RAG 엔진으로 분석
        rag = get_rag_engine()
        result = rag.analyze_situation(situation_data)

        return AnalyzeResponse(
            scenario_id=request.scenario_id,
            analysis=result,
            reasoning_steps=result.get("reasoning_history", [])
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/rules")
async def list_rules():
    """COLREGs 규정 목록 조회"""
    try:
        with open("/home/user/HASS/data/raw/colregs_rules.json", 'r', encoding='utf-8') as f:
            rules = json.load(f)

        rule_list = [
            {
                "id": r["id"],
                "title": r["title"],
                "category": r["category"],
                "summary": r["summary"]
            }
            for r in rules
        ]

        return {"rules": rule_list, "count": len(rule_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rules/{rule_id}")
async def get_rule(rule_id: str):
    """특정 규정 상세 조회"""
    try:
        with open("/home/user/HASS/data/raw/colregs_rules.json", 'r', encoding='utf-8') as f:
            rules = json.load(f)

        rule = next((r for r in rules if r["id"] == rule_id), None)

        if rule is None:
            raise HTTPException(status_code=404, detail="Rule not found")

        return rule
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cases")
async def list_cases():
    """해양안전심판원 재결서 목록 조회"""
    try:
        with open("/home/user/HASS/data/raw/kmst_cases.json", 'r', encoding='utf-8') as f:
            cases = json.load(f)

        case_list = [
            {
                "case_id": c["case_id"],
                "title": c["title"],
                "date": c["date"],
                "situation_type": c["situation_type"]
            }
            for c in cases
        ]

        return {"cases": case_list, "count": len(case_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cases/{case_id}")
async def get_case(case_id: str):
    """특정 재결서 상세 조회"""
    try:
        with open("/home/user/HASS/data/raw/kmst_cases.json", 'r', encoding='utf-8') as f:
            cases = json.load(f)

        case = next((c for c in cases if c["case_id"] == case_id), None)

        if case is None:
            raise HTTPException(status_code=404, detail="Case not found")

        return case
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
