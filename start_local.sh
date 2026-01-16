#!/bin/bash

# 🚢 Maritime Navigation System - 로컬 실행 스크립트

echo "🚢 Maritime Cognitive Navigation System"
echo "========================================="
echo ""

# 환경 변수 체크
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다."
    echo "📝 .env.example을 복사하여 .env 파일을 생성하고 설정을 입력하세요."
    echo ""
    echo "cp .env.example .env"
    echo "nano .env"
    exit 1
fi

echo "✅ 환경 변수 파일 확인 완료"

# Python 가상환경 체크 (선택적)
if [ ! -d "venv" ]; then
    echo "📦 Python 가상환경 생성 중..."
    python3 -m venv venv
fi

echo "🔄 가상환경 활성화..."
source venv/bin/activate

# 의존성 설치
echo "📦 의존성 설치 중..."
pip install -r requirements.txt -q

echo ""
echo "🎯 실행 옵션을 선택하세요:"
echo "1) Neo4j 데이터 로딩만 실행"
echo "2) 백엔드 (FastAPI) 실행"
echo "3) 프론트엔드 (Streamlit) 실행"
echo "4) 백엔드 + 프론트엔드 동시 실행"
echo ""

read -p "선택 (1-4): " choice

case $choice in
    1)
        echo "🗄️  Neo4j 데이터 로딩 시작..."
        cd backend
        python neo4j_loader.py
        ;;
    2)
        echo "🚀 FastAPI 백엔드 실행 중..."
        cd backend
        python main.py
        ;;
    3)
        echo "🎨 Streamlit 프론트엔드 실행 중..."
        streamlit run frontend/app.py
        ;;
    4)
        echo "🚀 백엔드 + 프론트엔드 동시 실행..."
        echo "백엔드: http://localhost:8000"
        echo "프론트엔드: http://localhost:8501"
        echo ""
        cd backend
        python main.py &
        BACKEND_PID=$!
        cd ..
        streamlit run frontend/app.py &
        FRONTEND_PID=$!

        echo ""
        echo "✅ 실행 완료!"
        echo "종료하려면 Ctrl+C를 누르세요."

        # 프로세스 대기
        wait $BACKEND_PID $FRONTEND_PID
        ;;
    *)
        echo "❌ 잘못된 선택입니다."
        exit 1
        ;;
esac
