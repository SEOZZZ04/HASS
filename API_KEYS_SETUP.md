# 🔑 API 키 설정 가이드

이 프로젝트는 Neo4j와 Google Gemini API를 사용합니다. 아래 단계를 따라 필요한 API 키를 발급받으세요.

---

## 1️⃣ Neo4j AuraDB 설정

### 계정 생성 및 인스턴스 생성

1. **Neo4j Aura 접속**
   - URL: https://neo4j.com/cloud/aura/
   - "Start Free" 버튼 클릭

2. **계정 생성**
   - Google, GitHub 또는 이메일로 가입
   - 무료 계정 선택

3. **새 인스턴스 생성**
   - Dashboard → "New Instance" 클릭
   - **Instance Type**: AuraDB Free
   - **Instance Name**: `maritime-navigation` (원하는 이름)
   - **Region**: 가장 가까운 지역 선택 (예: `asia-northeast1`)
   - "Create" 클릭

4. **연결 정보 저장** ⚠️ 매우 중요!

   인스턴스 생성 후 다음 정보가 **단 한 번만** 표시됩니다:

   ```
   Connection URI: neo4j+s://xxxxx.databases.neo4j.io
   Username: neo4j
   Password: xxxxxxxxxx (랜덤 생성)
   ```

   **반드시 안전한 곳에 저장하세요!** 나중에 다시 볼 수 없습니다.

5. **.env 파일에 추가**

   ```bash
   NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password_here
   ```

### 데이터베이스 접속 확인

Neo4j Browser에서 확인:
1. Aura Dashboard → 인스턴스 "Open" 클릭
2. Cypher Shell에서 테스트:
   ```cypher
   MATCH (n) RETURN count(n)
   ```
   (처음에는 0 반환됨 - 정상)

---

## 2️⃣ Google Gemini API 키 설정

### API 키 발급

1. **Google AI Studio 접속**
   - URL: https://aistudio.google.com/app/apikey
   - Google 계정으로 로그인

2. **API 키 생성**
   - "Create API Key" 버튼 클릭
   - 프로젝트 선택 (또는 새 프로젝트 생성)
   - API 키가 즉시 생성됩니다

3. **API 키 복사** ⚠️ 중요!

   ```
   AIzaSy... (40자 정도)
   ```

   **안전하게 저장하세요.**

4. **.env 파일에 추가**

   ```bash
   GEMINI_API_KEY=AIzaSy...
   ```

### Gemini 모델 정보

현재 사용 가능한 Gemini 모델:

| 모델 | 특징 | 비용 (2024년 기준) |
|-----|------|-------------------|
| **gemini-2.0-flash-exp** | 최신 실험 모델, 빠르고 강력 | 무료 (제한적) |
| **gemini-1.5-flash** | 빠른 응답, 가벼운 작업 | 무료 할당량 풍부 |
| **gemini-1.5-pro** | 고품질 분석, 복잡한 작업 | 무료 할당량 제한적 |

**권장**: `gemini-2.0-flash-exp` (최신 모델)

### 무료 할당량

Google Gemini API는 **무료 할당량**이 있습니다:

- **gemini-1.5-flash**: 15 RPM (분당 요청 수), 1,000,000 TPM (분당 토큰 수)
- **gemini-1.5-pro**: 2 RPM, 32,000 TPM
- **gemini-2.0-flash-exp**: 실험 모델로 제한적 무료 제공

시연용으로는 **충분히 무료**로 사용 가능합니다!

### API 키 사용량 확인

1. Google Cloud Console: https://console.cloud.google.com/
2. "APIs & Services" → "Enabled APIs"
3. "Generative Language API" 선택
4. "Quotas" 탭에서 사용량 확인

---

## 3️⃣ .env 파일 최종 설정

### .env 파일 생성

```bash
cd /home/user/HASS
cp .env.example .env
nano .env  # 또는 선호하는 에디터
```

### 완성된 .env 파일 예시

```bash
# Neo4j AuraDB 설정
NEO4J_URI=neo4j+s://abc123xyz.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=MySecretPassword123

# Google Gemini API 키
GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ1234567

# LLM 모델 선택
# gemini-2.0-flash-exp: 최신 실험 모델 (권장)
# gemini-1.5-flash: 빠르고 가벼움
# gemini-1.5-pro: 고품질 분석
LLM_MODEL=gemini-2.0-flash-exp

# 서버 포트
PORT=8000
STREAMLIT_PORT=8501
```

### 보안 주의사항

⚠️ **.env 파일은 절대 Git에 커밋하지 마세요!**

이미 `.gitignore`에 추가되어 있지만, 확인:
```bash
cat .gitignore | grep .env
```

출력: `.env`

---

## 4️⃣ Render 배포 시 환경 변수 설정

### Render Dashboard에서 설정

1. Render → 프로젝트 선택 → "Environment"
2. "Add Environment Variable" 클릭
3. 다음 변수들을 하나씩 추가:

| Key | Value | 예시 |
|-----|-------|------|
| `NEO4J_URI` | Neo4j 연결 URI | `neo4j+s://abc.databases.neo4j.io` |
| `NEO4J_USER` | Neo4j 사용자명 | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j 비밀번호 | `MySecretPass123` |
| `GEMINI_API_KEY` | Google Gemini API 키 | `AIzaSy...` |
| `LLM_MODEL` | 사용할 모델 | `gemini-2.0-flash-exp` |
| `PORT` | 포트 (자동 설정) | `8501` |

4. "Save Changes" 클릭
5. 자동으로 재배포됨

---

## 5️⃣ 설정 검증

### 로컬 환경 테스트

```bash
# Neo4j 연결 테스트
cd backend
python -c "
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()
driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
)
driver.verify_connectivity()
print('✅ Neo4j 연결 성공!')
driver.close()
"
```

```bash
# Gemini API 테스트
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')
response = model.generate_content('Hello')
print('✅ Gemini API 연결 성공!')
print('응답:', response.text)
"
```

### Render 배포 후 테스트

```bash
# 헬스 체크
curl https://your-app.onrender.com/

# 시나리오 목록 조회
curl https://your-app.onrender.com/scenarios
```

---

## 🚨 문제 해결

### Neo4j 연결 오류

```
❌ ServiceUnavailable: Unable to connect to Neo4j
```

**해결책:**
1. URI가 `neo4j+s://`로 시작하는지 확인 (SSL 필수)
2. Aura 인스턴스가 "Running" 상태인지 확인
3. 비밀번호에 특수문자가 있으면 URL 인코딩 필요
4. 방화벽/VPN이 7687 포트를 차단하는지 확인

### Gemini API 오류

```
❌ InvalidArgument: API key not valid
```

**해결책:**
1. API 키가 올바르게 복사되었는지 확인
2. 키 복사 시 공백이 없는지 확인
3. Google AI Studio에서 키가 활성화되어 있는지 확인
4. API 사용량 할당량 확인

```
❌ ResourceExhausted: Quota exceeded
```

**해결책:**
1. Google Cloud Console에서 할당량 확인
2. 잠시 후 다시 시도 (분당 요청 수 제한)
3. 또는 다른 모델로 변경 (`gemini-1.5-flash` 등)

---

## 💰 비용 비교

### Gemini vs OpenAI

| 항목 | Gemini | OpenAI |
|------|--------|--------|
| **무료 할당량** | ✅ 풍부 (1.5-flash) | ❌ 제한적 |
| **시연용 비용** | 무료 | $1-2 |
| **개발용 비용** | 거의 무료 | $10-20 |
| **품질** | 매우 우수 | 매우 우수 |
| **속도** | 빠름 | 빠름 |

**결론**: Gemini는 시연 및 개발용으로 **완전 무료** 또는 매우 저렴합니다!

---

## 🎯 모델 선택 가이드

### 용도별 권장 모델

**시연/데모:**
```bash
LLM_MODEL=gemini-2.0-flash-exp
```
- 최신 모델
- 빠른 응답
- 무료

**개발/테스트:**
```bash
LLM_MODEL=gemini-1.5-flash
```
- 안정적
- 빠른 응답
- 무료 할당량 풍부

**프로덕션:**
```bash
LLM_MODEL=gemini-1.5-pro
```
- 최고 품질
- 복잡한 분석
- 할당량 제한적 (필요 시 유료)

---

## ✅ 최종 체크리스트

배포 전 확인:

- [ ] Neo4j AuraDB 인스턴스 생성 완료
- [ ] Neo4j 연결 정보 안전하게 저장
- [ ] Google Gemini API 키 발급 완료
- [ ] `.env` 파일 생성 및 설정 완료
- [ ] 로컬 연결 테스트 통과 (Neo4j + Gemini)
- [ ] Render 환경 변수 설정 완료
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인

---

**🎉 설정 완료!**

이제 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)를 참고하여 데이터를 로딩하고 배포하세요.

**Gemini API의 장점:**
- ✅ 무료 할당량 풍부
- ✅ 빠른 응답 속도
- ✅ 최신 AI 기술
- ✅ Google의 안정적인 인프라
