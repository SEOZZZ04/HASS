# 🚀 Render 배포 가이드 (GitHub → Render)

> GitHub 리포지토리에서 직접 Render로 배포하는 상세 가이드

---

## 📋 사전 준비 (필수!)

### 1️⃣ Neo4j AuraDB 계정 및 데이터베이스 생성

#### Neo4j 인스턴스 생성

1. **Neo4j Aura 접속**
   - URL: https://neo4j.com/cloud/aura/
   - "Start Free" 클릭

2. **계정 생성**
   - Google 또는 GitHub 계정으로 간편 가입

3. **새 데이터베이스 생성**
   - Dashboard → "New Instance"
   - **Type**: AuraDB Free (무료)
   - **Name**: `maritime-navigation`
   - **Region**: `asia-northeast1` (가장 가까운 지역)
   - "Create" 클릭

4. **⚠️ 연결 정보 저장** (매우 중요!)

   생성 즉시 다음 정보가 **단 한 번만** 표시됩니다:
   ```
   Connection URI: neo4j+s://xxxxx.databases.neo4j.io
   Username: neo4j
   Password: xxxxxxxxxxxxxxxx (자동 생성)
   ```

   **반드시 메모장에 복사해두세요!** 다시 볼 수 없습니다.

#### 데이터 로딩 (로컬에서)

```bash
# 1. 리포지토리 클론 (로컬 컴퓨터에서)
git clone https://github.com/SEOZZZ04/HASS.git
cd HASS

# 2. .env 파일 생성
cp .env.example .env

# 3. .env 파일 편집
nano .env

# 다음 내용 입력:
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=여기에_비밀번호
GEMINI_API_KEY=나중에_발급받을_키  # 일단 빈칸으로 둬도 됨

# 4. Python 의존성 설치
pip install -r requirements.txt

# 5. Neo4j 데이터 로딩
cd backend
python neo4j_loader.py
```

**출력 예시:**
```
✅ COLREGs 규정 13개 로딩 완료!
✅ 해양안전심판원 재결서 8개 로딩 완료!
✅ 시나리오 6개 로딩 완료!

📊 노드 통계:
  - Rule: 13개
  - Case: 8개
  - Scenario: 6개
```

---

### 2️⃣ Google Gemini API 키 발급

1. **Google AI Studio 접속**
   - URL: https://aistudio.google.com/app/apikey
   - Google 계정으로 로그인

2. **API 키 생성**
   - "Create API Key" 버튼 클릭
   - 프로젝트 선택 (또는 "Create API key in new project")
   - 키가 즉시 생성됩니다

3. **키 복사**
   ```
   AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
   ```

   안전한 곳에 저장하세요.

---

## 🚀 Render 배포 단계

### Step 1: Render 계정 생성 및 GitHub 연결

1. **Render 접속**
   - URL: https://render.com/
   - "Get Started for Free" 클릭

2. **GitHub 계정으로 가입**
   - "Sign Up with GitHub" 선택
   - GitHub 인증 승인

3. **Render에 GitHub 접근 권한 부여**
   - "Authorize Render" 클릭
   - 리포지토리 접근 허용

---

### Step 2: Web Service 생성

1. **Render Dashboard로 이동**
   - 로그인 후 Dashboard 화면

2. **New Web Service 클릭**
   - 상단 "New +" 버튼 → "Web Service" 선택

3. **GitHub 리포지토리 연결**
   - "Connect a repository" 섹션에서
   - `SEOZZZ04/HASS` 리포지토리 찾기
   - "Connect" 클릭

   만약 리포지토리가 안 보이면:
   - "Configure account" 클릭
   - GitHub에서 Render 앱 설정 → "SEOZZZ04/HASS" 체크
   - 저장 후 돌아오기

---

### Step 3: 서비스 설정

#### 기본 정보

| 항목 | 값 |
|-----|-----|
| **Name** | `maritime-navigation-system` (원하는 이름) |
| **Region** | Singapore (Asia) 또는 Oregon (US West) |
| **Branch** | `claude/maritime-navigation-system-0tSw0` |
| **Root Directory** | 비워두기 (루트) |

#### Build & Deploy 설정

| 항목 | 값 |
|-----|-----|
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0` |

**Start Command 상세:**
```bash
streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0
```

#### Instance Type

| 항목 | 값 |
|-----|-----|
| **Instance Type** | `Free` |

---

### Step 4: Environment Variables 설정 (핵심!)

**⚠️ 매우 중요한 단계입니다!**

스크롤을 내려서 "Environment Variables" 섹션을 찾으세요.

#### "Add Environment Variable" 클릭하여 다음 변수들을 **하나씩** 추가:

1. **NEO4J_URI**
   ```
   Key: NEO4J_URI
   Value: neo4j+s://xxxxx.databases.neo4j.io
   ```
   (Neo4j Aura에서 받은 URI)

2. **NEO4J_USER**
   ```
   Key: NEO4J_USER
   Value: neo4j
   ```

3. **NEO4J_PASSWORD**
   ```
   Key: NEO4J_PASSWORD
   Value: 여기에_Neo4j_비밀번호
   ```
   (Neo4j Aura에서 받은 비밀번호)

4. **GEMINI_API_KEY**
   ```
   Key: GEMINI_API_KEY
   Value: AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
   ```
   (Google AI Studio에서 발급받은 키)

5. **LLM_MODEL**
   ```
   Key: LLM_MODEL
   Value: gemini-2.0-flash-exp
   ```

6. **PORT** (자동 설정되지만 명시적으로 추가 권장)
   ```
   Key: PORT
   Value: 8501
   ```

#### 최종 확인

Environment Variables가 다음과 같이 6개 설정되어 있는지 확인:

| Key | Value 예시 | 비고 |
|-----|-----------|------|
| NEO4J_URI | neo4j+s://abc123.databases.neo4j.io | ✅ |
| NEO4J_USER | neo4j | ✅ |
| NEO4J_PASSWORD | MyPassword123 | ✅ |
| GEMINI_API_KEY | AIzaSy... | ✅ |
| LLM_MODEL | gemini-2.0-flash-exp | ✅ |
| PORT | 8501 | ✅ |

---

### Step 5: 배포 시작!

1. **"Create Web Service" 버튼 클릭**
   - 하단의 큰 버튼

2. **빌드 프로세스 시작**
   - Render가 자동으로:
     - GitHub에서 코드 가져오기
     - `pip install -r requirements.txt` 실행
     - Streamlit 앱 시작

3. **로그 확인**
   - 화면에 실시간 로그 표시됨
   - 다음과 같은 메시지들이 보입니다:
   ```
   ==> Cloning from https://github.com/SEOZZZ04/HASS...
   ==> Running build command: pip install -r requirements.txt
   ==> Installing dependencies...
   ==> Build successful!
   ==> Starting service...
   ==> Streamlit app is running on port 8501
   ```

4. **배포 완료 대기**
   - 첫 배포는 약 **5-10분** 소요
   - 상태가 "Live"로 바뀌면 완료!

---

## 🎉 배포 완료 후 확인

### 1. 앱 URL 확인

배포가 완료되면 Render가 자동으로 URL을 할당합니다:
```
https://maritime-navigation-system.onrender.com
```

**Dashboard에서 확인:**
- 서비스 이름 클릭
- 상단에 URL 표시됨

### 2. 앱 접속 테스트

1. **브라우저에서 URL 열기**
   ```
   https://your-service-name.onrender.com
   ```

2. **정상 작동 확인**
   - Streamlit 앱이 로드되는지 확인
   - 사이드바에서 시나리오 목록이 보이는지 확인
   - 시나리오 하나 선택 → "AI 사고 과정 시작" 클릭
   - 추론 단계가 표시되는지 확인

### 3. 로그 확인

문제가 있다면 Render Dashboard에서:
- 서비스 선택 → "Logs" 탭
- 에러 메시지 확인

---

## 🔍 문제 해결

### ❌ 빌드 실패: "Could not find requirements.txt"

**원인:** Root Directory 설정 오류

**해결:**
1. Render Dashboard → 서비스 선택 → "Settings"
2. "Root Directory" 필드가 **비어있는지** 확인
3. 비어있지 않으면 삭제 후 저장

---

### ❌ "ServiceUnavailable: Neo4j connection failed"

**원인:** Neo4j 환경 변수 오류

**해결:**
1. Environment Variables 확인:
   - `NEO4J_URI`가 `neo4j+s://`로 시작하는지 확인
   - 비밀번호에 오타가 없는지 확인
2. Neo4j Aura에서 인스턴스가 "Running" 상태인지 확인
3. 변수 수정 후 "Manual Deploy" 클릭하여 재배포

---

### ❌ "InvalidArgument: Gemini API key not valid"

**원인:** Gemini API 키 오류

**해결:**
1. Google AI Studio에서 키 재확인
2. Environment Variables에서 `GEMINI_API_KEY` 값 확인
3. 키 앞뒤 공백 제거
4. 저장 후 재배포

---

### ❌ 앱이 로드되지 않음 (무한 로딩)

**원인:** Free tier는 비활성 15분 후 sleep

**해결:**
- 첫 접속 시 **1-2분** 대기 (Cold Start)
- 앱이 깨어나면서 시작됨
- 이후부터는 정상 속도

---

### ❌ "시나리오를 불러올 수 없습니다"

**원인:** Backend API가 실행되지 않음

**해결:**

**Option 1: Backend를 별도 서비스로 배포** (권장)

1. 새 Web Service 생성:
   - Name: `maritime-backend`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables: 동일하게 설정

2. Frontend 서비스에 환경 변수 추가:
   ```
   Key: API_BASE_URL
   Value: https://maritime-backend.onrender.com
   ```

3. `frontend/app.py` 수정:
   ```python
   import os
   API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
   ```

**Option 2: 단일 서비스로 실행** (현재 설정)

Start Command를 다음으로 변경:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port=$PORT --server.address=0.0.0.0
```

---

## 📊 배포 후 관리

### 자동 재배포 설정

Render는 **GitHub Push 시 자동 재배포**를 지원합니다.

**설정:**
1. Dashboard → 서비스 선택 → "Settings"
2. "Build & Deploy" 섹션
3. "Auto-Deploy" → **Yes** (기본값)

**사용:**
```bash
# 코드 수정 후
git add .
git commit -m "Update feature"
git push

# Render가 자동으로 재배포!
```

---

### 로그 모니터링

**실시간 로그 확인:**
1. Dashboard → 서비스 선택 → "Logs"
2. 에러, 경고, 정보 메시지 실시간 표시

**로그 검색:**
- Logs 화면에서 Ctrl+F로 검색

---

### 환경 변수 업데이트

**키 변경 시:**
1. Dashboard → 서비스 선택 → "Environment"
2. 변수 값 수정
3. "Save Changes" 클릭
4. 자동으로 재배포됨

---

## 💰 비용 안내

### Render Free Tier

| 항목 | 무료 제공 |
|------|----------|
| 실행 시간 | 750시간/월 |
| 메모리 | 512MB |
| CPU | Shared |
| 대역폭 | 100GB/월 |
| **제한** | 비활성 15분 후 Sleep |

**시연용으로 충분합니다!**

### Neo4j AuraDB Free

| 항목 | 무료 제공 |
|------|----------|
| 노드 | 200,000개 |
| 관계 | 400,000개 |
| **현재 사용** | 노드 ~50개, 관계 ~100개 |

**여유롭게 충분합니다!**

### Google Gemini API

| 항목 | 무료 제공 |
|------|----------|
| gemini-2.0-flash-exp | 제한적 무료 |
| gemini-1.5-flash | 15 RPM, 1M TPM |

**시연용으로 완전 무료!**

---

## ✅ 최종 체크리스트

배포 전 확인:

- [ ] Neo4j AuraDB 인스턴스 생성 완료
- [ ] Neo4j 연결 정보 메모 완료 (URI, Password)
- [ ] 로컬에서 Neo4j 데이터 로딩 완료 (`python backend/neo4j_loader.py`)
- [ ] Google Gemini API 키 발급 완료
- [ ] Render 계정 생성 및 GitHub 연결 완료
- [ ] Web Service 생성 완료
- [ ] Environment Variables 6개 모두 설정 완료
- [ ] 배포 성공 (Live 상태)
- [ ] URL 접속 테스트 통과
- [ ] 시나리오 분석 테스트 통과

---

## 🎯 배포 완료 후

### 발표 준비

1. **URL 공유**
   ```
   https://your-service-name.onrender.com
   ```

2. **시연 시나리오 선택**
   - "안개 속 어선 긴급 회피" (가장 드라마틱)
   - "우현 횡단 상황" (규정 명확)

3. **AI 사고 과정 강조**
   - 6단계 추론이 실시간으로 표시됨
   - 법적 근거가 명확히 제시됨

### 성능 최적화 팁

**Cold Start 방지:**
- 발표 5분 전에 URL 미리 열어두기
- 앱이 깨어나서 준비되도록

**빠른 응답:**
- Gemini API는 GPT-4보다 빠름
- 일반적으로 2-3초 내 응답

---

## 📞 도움이 필요하면

**Render 공식 문서:**
- https://render.com/docs

**Render 커뮤니티:**
- https://community.render.com/

**GitHub Issues:**
- https://github.com/SEOZZZ04/HASS/issues

---

**🎉 배포 완료를 축하합니다!**

이제 전 세계 어디서나 접속 가능한 Maritime Navigation System이 준비되었습니다! 🚢⚓
