# 🔑 API 키 설정 가이드

이 프로젝트는 Neo4j와 OpenAI API를 사용합니다. 아래 단계를 따라 필요한 API 키를 발급받으세요.

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

## 2️⃣ OpenAI API 키 설정

### API 키 발급

1. **OpenAI 계정 생성**
   - URL: https://platform.openai.com/
   - "Sign up" 또는 기존 계정 로그인

2. **API 키 생성**
   - Dashboard → "API keys" 메뉴
   - "Create new secret key" 클릭
   - Key name: `maritime-nav` (원하는 이름)
   - "Create secret key" 클릭

3. **API 키 복사** ⚠️ 중요!

   ```
   sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

   **창을 닫으면 다시 볼 수 없습니다.** 안전하게 저장하세요.

4. **.env 파일에 추가**

   ```bash
   OPENAI_API_KEY=sk-proj-xxxxxxxxxx
   ```

### 사용량 제한 설정 (권장)

1. **Billing 설정**
   - Dashboard → "Settings" → "Billing"
   - "Add payment method" (크레딧 카드 등록)

2. **사용량 한도 설정**
   - "Usage limits" → "Set a monthly budget"
   - 권장: $5 - $10/월 (시연용으로 충분)
   - 한도 도달 시 알림 설정: 80%, 100%

3. **비용 예상**
   - GPT-4: 시나리오 분석 1회당 약 $0.10 - $0.20
   - GPT-3.5-turbo: 시나리오 분석 1회당 약 $0.01 - $0.02
   - 시연 10회 기준: GPT-4 $2, GPT-3.5-turbo $0.20

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

# OpenAI API 키
OPENAI_API_KEY=sk-proj-abcdefghijklmnopqrstuvwxyz1234567890

# LLM 모델 선택 (비용 고려)
# GPT-4: 느리지만 정확, 비쌈 ($0.10/분석)
# GPT-3.5-turbo: 빠르고 저렴 ($0.01/분석)
LLM_MODEL=gpt-4

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
| `OPENAI_API_KEY` | OpenAI API 키 | `sk-proj-xxxxx` |
| `LLM_MODEL` | 사용할 모델 | `gpt-4` 또는 `gpt-3.5-turbo` |
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
# OpenAI API 테스트
python -c "
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
response = openai.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello'}],
    max_tokens=5
)
print('✅ OpenAI API 연결 성공!')
print('응답:', response.choices[0].message.content)
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

### OpenAI API 오류

```
❌ AuthenticationError: Incorrect API key
```

**해결책:**
1. API 키가 `sk-proj-` 또는 `sk-`로 시작하는지 확인
2. 키 복사 시 공백이 없는지 확인
3. OpenAI 계정 상태 확인 (https://platform.openai.com/)
4. 크레딧 잔액 확인

```
❌ RateLimitError: You exceeded your quota
```

**해결책:**
1. Billing 설정 확인
2. 사용량 한도 증가
3. 또는 `LLM_MODEL=gpt-3.5-turbo`로 변경 (저렴)

---

## 💰 비용 최적화

### 개발/테스트 시

```bash
# .env 파일에서
LLM_MODEL=gpt-3.5-turbo  # GPT-4 대신 사용
```

### 프로덕션

```bash
LLM_MODEL=gpt-4  # 정확도 우선
```

### 월 예상 비용

| 사용 패턴 | GPT-4 | GPT-3.5-turbo |
|----------|-------|---------------|
| 시연 (10회) | $2 | $0.20 |
| 개발 (100회) | $20 | $2 |
| 실제 운영 (1000회) | $200 | $20 |

---

## ✅ 최종 체크리스트

배포 전 확인:

- [ ] Neo4j AuraDB 인스턴스 생성 완료
- [ ] Neo4j 연결 정보 안전하게 저장
- [ ] OpenAI API 키 발급 완료
- [ ] 사용량 한도 설정 완료 (권장)
- [ ] `.env` 파일 생성 및 설정 완료
- [ ] 로컬 연결 테스트 통과
- [ ] Render 환경 변수 설정 완료
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인

---

**🎉 설정 완료!**

이제 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)를 참고하여 데이터를 로딩하고 배포하세요.
