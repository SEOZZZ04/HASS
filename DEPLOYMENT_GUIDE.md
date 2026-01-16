# 🚢 Maritime Navigation System - Render 배포 가이드

## 📋 사전 준비

### 1. Neo4j AuraDB 계정 생성
1. [Neo4j Aura](https://neo4j.com/cloud/aura/) 접속
2. 무료 계정 생성
3. 새 데이터베이스 인스턴스 생성 (Free tier)
4. 연결 정보 저장:
   - URI: `neo4j+s://xxxxx.databases.neo4j.io`
   - Username: `neo4j`
   - Password: (생성 시 제공된 비밀번호)

### 2. OpenAI API 키 발급
1. [OpenAI Platform](https://platform.openai.com/) 접속
2. API Keys 섹션에서 새 키 생성
3. 키 복사 및 안전하게 보관

### 3. Render 계정 생성
1. [Render](https://render.com/) 접속
2. GitHub 계정으로 가입
3. 리포지토리 연결

---

## 🗄️ Neo4j 데이터베이스 초기 설정

### 로컬에서 데이터 로딩

```bash
# 1. 환경 변수 설정
cp .env.example .env

# 2. .env 파일 편집
# NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=your_password
# OPENAI_API_KEY=sk-your_key

# 3. 의존성 설치
pip install -r requirements.txt

# 4. Neo4j 데이터 로딩
cd backend
python neo4j_loader.py
```

출력 예시:
```
✅ COLREGs 규정 13개 로딩 완료!
✅ 해양안전심판원 재결서 8개 로딩 완료!
✅ 시나리오 6개 로딩 완료!

📊 노드 통계:
  - Rule: 13개
  - Case: 8개
  - Scenario: 6개
  - SituationType: 15개
  - Action: 25개
```

---

## 🚀 Render 배포

### Option 1: Streamlit 단일 앱으로 배포 (권장)

Render에서 Streamlit 앱은 자동으로 FastAPI와 통합됩니다.

#### 1. 리포지토리를 GitHub에 푸시

```bash
git add .
git commit -m "Initial commit: Maritime Navigation System"
git push origin claude/maritime-navigation-system-0tSw0
```

#### 2. Render에서 새 Web Service 생성

1. Render 대시보드 → "New" → "Web Service"
2. GitHub 리포지토리 연결
3. 설정:
   - **Name**: `maritime-navigation-system`
   - **Environment**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0 & uvicorn backend.main:app --host 0.0.0.0 --port 8000
     ```
   - **Instance Type**: `Free`

#### 3. 환경 변수 설정

Render 대시보드 → Environment → "Add Environment Variable":

| Key | Value |
|-----|-------|
| `NEO4J_URI` | `neo4j+s://xxxxx.databases.neo4j.io` |
| `NEO4J_USER` | `neo4j` |
| `NEO4J_PASSWORD` | (Neo4j 비밀번호) |
| `OPENAI_API_KEY` | `sk-xxxxx` |
| `LLM_MODEL` | `gpt-4` |
| `PORT` | `8501` (Streamlit 기본 포트) |

#### 4. 배포 시작

"Create Web Service" 버튼 클릭 → 자동 배포 시작

---

### Option 2: FastAPI와 Streamlit 분리 배포

#### 백엔드 (FastAPI) 배포

1. Render → "New" → "Web Service"
2. 설정:
   - **Name**: `maritime-backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - 환경 변수 추가 (위와 동일)

3. 배포 후 백엔드 URL 복사: `https://maritime-backend.onrender.com`

#### 프론트엔드 (Streamlit) 배포

1. Render → "New" → "Web Service"
2. 설정:
   - **Name**: `maritime-frontend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0`
   - 환경 변수:
     - `API_BASE_URL`: `https://maritime-backend.onrender.com`

3. `frontend/app.py` 수정:
   ```python
   API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
   ```

---

## 🧪 로컬 테스트

### 백엔드 실행

```bash
cd backend
python main.py
```

브라우저: `http://localhost:8000/docs` (Swagger UI)

### 프론트엔드 실행

```bash
streamlit run frontend/app.py
```

브라우저: `http://localhost:8501`

---

## 🔍 문제 해결

### 1. Neo4j 연결 실패

```
❌ 오류: Failed to establish connection to Neo4j
```

**해결책:**
- Neo4j Aura 인스턴스가 실행 중인지 확인
- URI가 `neo4j+s://`로 시작하는지 확인 (SSL 필요)
- 비밀번호 정확성 확인

### 2. OpenAI API 오류

```
❌ 오류: Invalid API key
```

**해결책:**
- API 키가 `sk-`로 시작하는지 확인
- OpenAI 계정에 크레딧이 있는지 확인
- 환경 변수가 올바르게 설정되었는지 확인

### 3. Render 빌드 실패

```
❌ Build failed: Requirements could not be installed
```

**해결책:**
- `requirements.txt` 파일이 루트 디렉토리에 있는지 확인
- Python 버전 호환성 확인 (Python 3.10+ 권장)

### 4. Streamlit 앱이 백엔드에 연결 안 됨

```
⚠️  시나리오를 불러올 수 없습니다
```

**해결책:**
- `frontend/app.py`의 `API_BASE_URL` 확인
- 백엔드가 정상 실행 중인지 확인
- CORS 설정 확인 (이미 설정되어 있음)

---

## 📊 배포 후 확인사항

### 1. 헬스 체크

```bash
curl https://your-app.onrender.com/
```

응답:
```json
{
  "service": "Maritime Cognitive Navigation System",
  "status": "operational",
  "version": "1.0.0"
}
```

### 2. 시나리오 목록 조회

```bash
curl https://your-app.onrender.com/scenarios
```

### 3. Streamlit 앱 접속

브라우저에서 Render가 제공한 URL 접속 예시:
- `https://maritime-navigation-system.onrender.com`

---

## 💰 비용 안내

### Render (Free Tier)
- ✅ 무료
- ⚠️ 제한: 750시간/월 실행 시간
- ⚠️ 비활성 15분 후 자동 슬립 (첫 요청 시 재시작)

### Neo4j Aura (Free Tier)
- ✅ 무료
- 제한: 200K nodes, 400K relationships
- 본 프로젝트는 여유롭게 충분

### OpenAI API
- 💳 사용량 기반 과금
- GPT-4 예상 비용: 시연 1회당 약 $0.10~0.20
- 권장: API 키에 사용량 제한 설정

---

## 🎯 최적화 팁

### 1. 응답 속도 개선

- `LLM_MODEL`을 `gpt-3.5-turbo`로 변경 (저렴하고 빠름)
- Neo4j 쿼리 결과 캐싱

### 2. 비용 절감

```python
# frontend/app.py에서
st.cache_data(ttl=3600)  # 1시간 캐싱
def get_scenarios():
    ...
```

### 3. 프로덕션 설정

```python
# backend/main.py에서
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.onrender.com"],  # 특정 도메인만 허용
    ...
)
```

---

## 📞 지원

문제가 발생하면:
1. Render 로그 확인: Dashboard → Logs
2. Neo4j 로그 확인: Aura Console → Logs
3. GitHub Issues에 문의

---

## ✅ 체크리스트

배포 전 확인:

- [ ] Neo4j AuraDB 인스턴스 생성 및 데이터 로딩 완료
- [ ] OpenAI API 키 발급 및 크레딧 확인
- [ ] GitHub 리포지토리에 코드 푸시
- [ ] Render 계정 생성
- [ ] 환경 변수 설정 완료
- [ ] 로컬 테스트 통과
- [ ] 배포 후 헬스 체크 통과
- [ ] Streamlit 앱에서 시나리오 분석 테스트

---

**🎉 배포 완료!**

이제 팀원들과 공유하고 시연을 준비하세요!
