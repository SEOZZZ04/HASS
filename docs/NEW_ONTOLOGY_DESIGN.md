# Maritime Safety Ontology (MSO) v2.0
## LEGIS-XAI 스타일 온톨로지 재설계

Last Updated: 2026-01-17

---

## 1. ONTOLOGY OVERVIEW

### Vision
법률 온톨로지(LEGIS-XAI)의 체계를 해양 안전 도메인에 적용하여,
규정(Regulation), 사례(Case), 선박(Vessel), 안전현안(SafetyIssue) 간의
복잡한 관계를 시맨틱하게 표현하는 지식 그래프 구축.

### Core Philosophy
- **Semantic Richness**: RDF/OWL 기반의 풍부한 의미론적 표현
- **Legal Traceability**: 모든 권고사항은 법적 근거와 연결
- **Evidence-Based**: 레이더, AIS, 시각 데이터로 뒷받침
- **Interactive Visualization**: Force-directed graph로 관계 시각화

---

## 2. ENTITY TYPES (Object Types)

### 2.1 Regulation (규정) 🔵
**정의**: 국제해상충돌예방규칙(COLREGs) 및 해양안전법규

**Properties**:
- `regulation_id`: string (예: "COLREG-Rule-15")
- `title`: string (예: "횡단 상황")
- `title_en`: string (예: "Crossing Situation")
- `category`: enum ["collision_avoidance", "navigation", "lights_shapes", "sound_signals"]
- `version`: string (예: "1972/2022")
- `full_text_kr`: text
- `full_text_en`: text
- `legal_weight`: integer (1-10, 중요도)
- `applicable_waters`: array (예: ["international", "coastal", "port"])
- `effective_date`: date
- `last_amended`: date
- `source_url`: string

**Relationships**:
- `addresses` → SafetyIssue (어떤 안전 현안을 해결하는가)
- `contains` → Article (어떤 조항들을 포함하는가)
- `cites` → Regulation (다른 규정을 인용)
- `supersedes` → Regulation (이전 규정을 대체)
- `applies_to` → VesselType (어떤 선박 유형에 적용되는가)

---

### 2.2 Article (조항) 🟢
**정의**: 규정의 세부 조항 (LEGIS-XAI의 Clause에 해당)

**Properties**:
- `article_id`: string (예: "COLREG-Rule-15-A")
- `regulation_id`: string (부모 규정)
- `article_number`: string (예: "제15조 제1항")
- `content_kr`: text
- `content_en`: text
- `interpretation_notes`: text

**Relationships**:
- `part_of` → Regulation
- `requires` → Action (어떤 조치를 요구하는가)
- `related_to` → Article (관련 조항)

---

### 2.3 SafetyIssue (안전 현안) 🔴
**정의**: 해양에서 발생 가능한 안전 위험 상황 (LEGIS-XAI의 PolicyIssue에 해당)

**Properties**:
- `issue_id`: string (예: "SI-001")
- `name_kr`: string (예: "안개 중 충돌 위험")
- `name_en`: string (예: "Collision Risk in Fog")
- `category`: enum ["collision", "grounding", "fire", "pollution", "man_overboard"]
- `severity`: integer (1-10)
- `frequency`: integer (연간 발생 건수)
- `description`: text

**Relationships**:
- `addressed_by` → Regulation (어떤 규정이 해결하는가)
- `evidenced_by` → Evidence (어떤 증거로 확인되는가)
- `occurred_in` → MaritimeCase (어떤 사례에서 발생했는가)
- `involves` → Vessel (어떤 선박이 관련되는가)
- `affects` → Stakeholder (누구에게 영향을 미치는가)

---

### 2.4 MaritimeCase (해양 사례) 🟡
**정의**: 실제 해양 사고 및 준사고 판례 (LEGIS-XAI의 Case + Evidence)

**Properties**:
- `case_id`: string (예: "KMST-2023-001")
- `title_kr`: string
- `title_en`: string
- `date`: date
- `location`: string (예: "부산항 외해")
- `location_lat`: float
- `location_lon`: float
- `situation_type`: array (예: ["crossing", "restricted_visibility"])
- `incident_description_kr`: text
- `incident_description_en`: text
- `analysis`: text
- `judgment`: text
- `penalty`: string
- `casualties`: integer
- `damage_usd`: integer
- `legal_weight`: integer (1-10, 판례 중요도)
- `tribunal`: string (예: "한국해양안전심판원")

**Relationships**:
- `violated` → Regulation (어떤 규정을 위반했는가)
- `violated_article` → Article (어떤 조항을 위반했는가)
- `example_of` → SafetyIssue (어떤 안전 현안의 사례인가)
- `teaches` → Lesson (어떤 교훈을 주는가)
- `related_case` → MaritimeCase (유사 사례)
- `supported_by` → Evidence (어떤 증거로 뒷받침되는가)
- `involves` → Vessel (어떤 선박이 관련되었는가)
- `caused_by` → Actor (누가 원인을 제공했는가)

---

### 2.5 Vessel (선박) 🚢
**정의**: 사건에 관련된 선박 엔티티

**Properties**:
- `vessel_id`: string (예: "IMO-9234567")
- `name`: string
- `vessel_type`: enum ["cargo", "container", "tanker", "fishing", "passenger", "navy", "sailing"]
- `imo_number`: string
- `mmsi`: string
- `flag`: string (국적)
- `length`: float (미터)
- `beam`: float (미터)
- `draft`: float (미터)
- `gross_tonnage`: integer
- `build_year`: integer

**Relationships**:
- `governed_by` → Regulation (어떤 규정의 적용을 받는가)
- `involved_in` → MaritimeCase (어떤 사례에 관련되었는가)
- `operated_by` → Actor (누가 운항하는가)
- `equipped_with` → Equipment (어떤 장비를 갖추고 있는가)

---

### 2.6 Evidence (증거) 📊
**정의**: 사건을 뒷받침하는 데이터 및 증거 (레이더, AIS, VDR, 목격자 등)

**Properties**:
- `evidence_id`: string (예: "EVD-001")
- `evidence_type`: enum ["radar", "ais", "vdr", "visual", "witness", "photo", "video", "weather_data"]
- `timestamp`: datetime
- `description`: text
- `data_source`: string
- `reliability`: integer (1-10)
- `file_url`: string (증거 파일 경로)

**Relationships**:
- `supports` → MaritimeCase (어떤 사례를 뒷받침하는가)
- `indicates` → SafetyIssue (어떤 안전 현안을 나타내는가)
- `collected_by` → Actor (누가 수집했는가)

---

### 2.7 Action (조치) ✅
**정의**: 권고되는 안전 조치

**Properties**:
- `action_id`: string (예: "ACT-001")
- `name_kr`: string (예: "우현 대폭 변침")
- `name_en`: string (예: "Large Starboard Alteration")
- `action_type`: enum ["course_change", "speed_change", "signal", "communication", "watch"]
- `priority`: integer (1-5, 1이 최우선)
- `description`: text
- `parameters`: json (예: {"heading_change": 30, "new_speed": 5})

**Relationships**:
- `recommended_by` → Regulation (어떤 규정이 권고하는가)
- `required_by` → Article (어떤 조항이 요구하는가)
- `prevented` → SafetyIssue (어떤 위험을 방지하는가)
- `applied_in` → MaritimeCase (어떤 사례에서 적용되었는가)

---

### 2.8 Actor (행위자) 👤
**정의**: 해양 안전과 관련된 인적 주체 (LEGIS-XAI의 Stakeholder + PolicyActor)

**Properties**:
- `actor_id`: string (예: "ACT-CAPTAIN-001")
- `role`: enum ["captain", "officer", "pilot", "vts_operator", "investigator", "regulator"]
- `name`: string (익명화 가능)
- `organization`: string (예: "한국해양안전심판원")
- `license_type`: string
- `experience_years`: integer

**Relationships**:
- `operates` → Vessel
- `responsible_for` → MaritimeCase
- `enforces` → Regulation
- `provides` → Evidence

---

### 2.9 Lesson (교훈) 💡
**정의**: 사례에서 얻은 교훈 및 안전 지침

**Properties**:
- `lesson_id`: string (예: "LSN-001")
- `text_kr`: text (예: "안개 시 속력 대폭 감속 필수")
- `text_en`: text
- `importance`: integer (1-10)

**Relationships**:
- `learned_from` → MaritimeCase
- `reinforces` → Regulation

---

### 2.10 Location (위치) 🗺️
**정의**: 사건 발생 수역 및 항로

**Properties**:
- `location_id`: string (예: "LOC-BUSAN-001")
- `name_kr`: string (예: "부산항 진입 수로")
- `name_en`: string
- `location_type`: enum ["port", "channel", "tss", "anchorage", "coastal", "open_sea"]
- `latitude`: float
- `longitude`: float
- `water_depth`: float
- `traffic_density`: integer (1-10)

**Relationships**:
- `site_of` → MaritimeCase
- `governed_by` → Regulation (특정 수역 규정)

---

### 2.11 Equipment (장비) 🛠️
**정의**: 선박 장비 및 항해 시스템

**Properties**:
- `equipment_id`: string
- `equipment_type`: enum ["radar", "ais", "gps", "ecdis", "vhf", "gyro"]
- `manufacturer`: string
- `model`: string
- `operational_status`: enum ["operational", "degraded", "failed"]

**Relationships**:
- `installed_on` → Vessel
- `malfunction_caused` → MaritimeCase

---

## 3. RELATIONSHIP TYPES (Object Properties)

### 3.1 Regulation → SafetyIssue
- `addresses`: 규정이 특정 안전 현안을 해결함

### 3.2 Regulation → Article
- `contains`: 규정이 조항을 포함함

### 3.3 Article → Action
- `requires`: 조항이 특정 조치를 요구함

### 3.4 MaritimeCase → Regulation
- `violated`: 사례가 규정을 위반함
- `example_of`: 사례가 규정 적용 사례임

### 3.5 MaritimeCase → Evidence
- `supported_by`: 사례가 증거로 뒷받침됨

### 3.6 MaritimeCase → Lesson
- `teaches`: 사례가 교훈을 제공함

### 3.7 Vessel → Actor
- `operated_by`: 선박이 행위자에 의해 운영됨

### 3.8 SafetyIssue → Evidence
- `evidenced_by`: 안전 현안이 증거로 확인됨

---

## 4. VISUALIZATION DESIGN

### Force-Directed Graph Layout
- **중심 노드**: SafetyIssue (안전 현안) - 가장 큰 노드
- **1차 노드**: Regulation, MaritimeCase - 중간 크기
- **2차 노드**: Article, Evidence, Action - 작은 노드
- **3차 노드**: Vessel, Actor, Lesson - 가장 작은 노드

### Color Coding (LEGIS-XAI 스타일)
- 🔵 **Regulation** (규정) - Blue
- 🟢 **Article** (조항) - Green
- 🔴 **SafetyIssue** (안전 현안) - Red
- 🟡 **MaritimeCase** (사례) - Orange
- 🟣 **Evidence** (증거) - Purple
- 🟠 **Vessel** (선박) - Teal
- 👤 **Actor** (행위자) - Gray
- 💡 **Lesson** (교훈) - Pink
- ✅ **Action** (조치) - Light Green
- 🗺️ **Location** (위치) - Brown

---

## 5. EXAMPLE ONTOLOGY INSTANCE

### Scenario: 안개 중 어선과 화물선 충돌

```turtle
# Regulation
:COLREG-Rule-19 a :Regulation ;
    :title_kr "시계 제한 상태에서의 선박의 운항" ;
    :title_en "Conduct of Vessels in Restricted Visibility" ;
    :legal_weight 10 ;
    :addresses :SI-RestrictedVisibility .

# Article
:COLREG-Rule-19-E a :Article ;
    :part_of :COLREG-Rule-19 ;
    :content_kr "시계 제한 수역에서는 안전한 속력으로 항행해야 한다" ;
    :requires :ACT-ReduceSpeed .

# SafetyIssue
:SI-RestrictedVisibility a :SafetyIssue ;
    :name_kr "안개 중 충돌 위험" ;
    :severity 9 ;
    :addressed_by :COLREG-Rule-19 .

# MaritimeCase
:KMST-2023-001 a :MaritimeCase ;
    :title_kr "안개 중 어선과 화물선 충돌" ;
    :date "2023-03-15" ;
    :violated :COLREG-Rule-19 ;
    :violated_article :COLREG-Rule-19-E ;
    :example_of :SI-RestrictedVisibility ;
    :supported_by :EVD-Radar-001 ;
    :teaches :LSN-SlowDownInFog .

# Evidence
:EVD-Radar-001 a :Evidence ;
    :evidence_type "radar" ;
    :description "충돌 5분 전 레이더 스크린샷" ;
    :supports :KMST-2023-001 .

# Vessel
:Vessel-CargoShip-001 a :Vessel ;
    :vessel_type "cargo" ;
    :involved_in :KMST-2023-001 ;
    :operated_by :ACT-CAPTAIN-001 .

# Action
:ACT-ReduceSpeed a :Action ;
    :name_kr "안전 속력으로 감속" ;
    :priority 1 ;
    :recommended_by :COLREG-Rule-19 .

# Lesson
:LSN-SlowDownInFog a :Lesson ;
    :text_kr "안개 시 속력을 대폭 감속하고 경계를 강화해야 함" ;
    :learned_from :KMST-2023-001 .
```

---

## 6. RDF/OWL NAMESPACES

```turtle
@prefix mso: <http://weoffice.ai/ontology/maritime-safety#> .
@prefix colreg: <http://weoffice.ai/ontology/colregs#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

---

## 7. SPARQL QUERY EXAMPLES

### Find all regulations addressing a specific safety issue
```sparql
PREFIX mso: <http://weoffice.ai/ontology/maritime-safety#>

SELECT ?regulation ?title ?article
WHERE {
  ?regulation mso:addresses mso:SI-RestrictedVisibility ;
              mso:title_kr ?title .
  OPTIONAL {
    ?regulation mso:contains ?article .
  }
}
```

### Find cases that violated a specific regulation
```sparql
PREFIX mso: <http://weoffice.ai/ontology/maritime-safety#>

SELECT ?case ?title ?judgment ?lesson
WHERE {
  ?case mso:violated mso:COLREG-Rule-19 ;
        mso:title_kr ?title ;
        mso:judgment ?judgment .
  OPTIONAL {
    ?case mso:teaches ?lesson_node .
    ?lesson_node mso:text_kr ?lesson .
  }
}
ORDER BY DESC(?case)
```

### Find evidence supporting a case
```sparql
PREFIX mso: <http://weoffice.ai/ontology/maritime-safety#>

SELECT ?evidence ?type ?description
WHERE {
  mso:KMST-2023-001 mso:supported_by ?evidence .
  ?evidence mso:evidence_type ?type ;
            mso:description ?description .
}
```

---

## 8. IMPLEMENTATION ROADMAP

### Phase 1: Data Model
- [ ] Create RDF/OWL schema files
- [ ] Define all entity classes and properties
- [ ] Define all relationship types
- [ ] Validate with Protégé or similar tool

### Phase 2: Data Migration
- [ ] Convert existing Neo4j data to RDF format
- [ ] Enrich with new properties
- [ ] Load into triple store (GraphDB or Virtuoso)

### Phase 3: Visualization
- [ ] Build force-directed graph with D3.js
- [ ] Implement interactive exploration
- [ ] Add filtering and search

### Phase 4: Integration
- [ ] Update backend to query triple store
- [ ] Expose SPARQL endpoint
- [ ] Build ontology browser UI

---

**End of Document**
