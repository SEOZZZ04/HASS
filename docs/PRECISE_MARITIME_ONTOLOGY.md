# Maritime Safety Ontology - Precise Design
# For COLREGs, Vessel Collision Avoidance, and Maritime Cases

## Core Entities

### 1. Vessel (선박)
**Purpose**: Represents ships involved in maritime scenarios
**Properties**:
- vessel_id: string
- vessel_type: enum [cargo, container, tanker, fishing, passenger, tugboat, sailing]
- name: string
- imo_number: string (optional)
- mmsi: string (optional)
- length: float (meters)
- draft: float (meters)
- position: geo-coordinates
- heading: float (degrees)
- speed: float (knots)
- status: enum [underway, anchored, moored, restricted_maneuverability]

### 2. COLREGsRule (국제해상충돌예방규칙)
**Purpose**: International regulations for preventing collisions at sea
**Properties**:
- rule_id: string (e.g., "rule_05", "rule_15")
- rule_number: string (e.g., "Rule 5", "Rule 15")
- title_kr: string
- title_en: string
- category: enum [general, steering_sailing, lights_shapes, sound_signals]
- full_text_kr: text
- full_text_en: text
- legal_weight: integer (1-10, importance level)
- applicable_waters: array [international, coastal, port, narrow_channel]
- last_updated: date

### 3. SituationType (상황 유형)
**Purpose**: Classification of maritime encounter situations
**Types**:
- crossing_situation: 횡단 상황 (vessels crossing paths)
- head_on_situation: 마주치는 상황 (vessels meeting head-on)
- overtaking_situation: 추월 상황 (one vessel overtaking another)
- restricted_visibility: 시계 제한 상황 (fog, rain, darkness)
- narrow_channel: 좁은 수로 (confined waters)
- traffic_separation: 통항분리방식 (TSS)
- give_way_situation: 피항 상황 (give-way vessel required)
- stand_on_situation: 유지 상황 (stand-on vessel maintains course)

### 4. MaritimeCase (해양 사고 사례)
**Purpose**: Real accident cases with tribunal judgments
**Properties**:
- case_id: string (e.g., "KMST-2023-001")
- title_kr: string
- title_en: string
- date: date
- location: string
- coordinates: geo-coordinates
- weather_conditions: string
- visibility: string (e.g., "50미터", "1해리")
- situation_types: array of SituationType
- incident_description: text
- root_causes: array of string
- judgment: text
- penalty: string
- casualties: integer
- damage_amount: integer (USD)
- legal_weight: integer (1-10, precedent importance)
- tribunal: string (e.g., "한국해양안전심판원")

### 5. Evidence (증거)
**Purpose**: Supporting data for cases and situations
**Types**:
- radar_data: Radar screen captures
- ais_data: AIS transponder records
- vdr_data: Voyage Data Recorder
- visual_observation: Eyewitness accounts
- weather_data: Meteorological conditions
- gps_track: GPS position history
- photo_video: Visual documentation

**Properties**:
- evidence_id: string
- evidence_type: enum [radar, ais, vdr, visual, weather, gps, photo, video]
- timestamp: datetime
- description: text
- file_path: string (optional)
- reliability_score: integer (1-10)
- collected_by: string (investigator/officer)

### 6. Action (권고 조치)
**Purpose**: Recommended actions for collision avoidance
**Properties**:
- action_id: string
- action_type: enum [course_change, speed_change, sound_signal, light_signal, communication, watch]
- name_kr: string (e.g., "우현 대폭 변침")
- name_en: string (e.g., "Large Starboard Alteration")
- priority: integer (1-5, 1=highest)
- description: text
- parameters: JSON
  - heading_change: float (degrees)
  - new_speed: float (knots)
  - signal_type: string

### 7. Lesson (교훈)
**Purpose**: Lessons learned from cases
**Properties**:
- lesson_id: string
- text_kr: text
- text_en: text
- category: enum [procedure, judgment, equipment, communication, training]
- importance: integer (1-10)
- applicable_situations: array of SituationType

### 8. Actor (행위자)
**Purpose**: People involved (captains, officers, investigators)
**Properties**:
- actor_id: string
- role: enum [captain, chief_officer, pilot, vts_operator, investigator]
- name: string (anonymized if needed)
- organization: string
- license_type: string
- experience_years: integer

### 9. Location (수역)
**Purpose**: Geographical waterways
**Properties**:
- location_id: string
- name_kr: string
- name_en: string
- type: enum [port, channel, anchorage, tss, open_sea, narrow_channel]
- coordinates: geo-coordinates
- water_depth: float (meters)
- traffic_density: integer (1-10)
- special_regulations: array of string

### 10. CollisionRisk (충돌 위험)
**Purpose**: Assessed collision risk between vessels
**Properties**:
- risk_id: string
- primary_vessel: Vessel
- target_vessel: Vessel
- cpa: float (Closest Point of Approach, nautical miles)
- tcpa: float (Time to CPA, minutes)
- bearing: float (degrees)
- relative_bearing: string (e.g., "우현 전방")
- risk_level: enum [critical, high, medium, low]
- situation_type: SituationType
- timestamp: datetime

---

## Relationships

### Vessel Relationships
- **Vessel** -[:INVOLVED_IN]-> **MaritimeCase**
- **Vessel** -[:OPERATED_BY]-> **Actor**
- **Vessel** -[:EQUIPPED_WITH]-> **Equipment**
- **Vessel** -[:IN_COLLISION_RISK_WITH]-> **Vessel**
- **Vessel** -[:GOVERNED_BY]-> **COLREGsRule** (based on vessel type)

### COLREGs Relationships
- **COLREGsRule** -[:APPLIES_TO]-> **SituationType**
- **COLREGsRule** -[:RECOMMENDS]-> **Action**
- **COLREGsRule** -[:CITES]-> **COLREGsRule** (cross-references)
- **COLREGsRule** -[:SUPERSEDES]-> **COLREGsRule** (amendments)

### Case Relationships
- **MaritimeCase** -[:VIOLATED]-> **COLREGsRule**
- **MaritimeCase** -[:EXAMPLE_OF]-> **SituationType**
- **MaritimeCase** -[:SUPPORTED_BY]-> **Evidence**
- **MaritimeCase** -[:TEACHES]-> **Lesson**
- **MaritimeCase** -[:OCCURRED_AT]-> **Location**
- **MaritimeCase** -[:INVOLVED]-> **Vessel**
- **MaritimeCase** -[:INVESTIGATED_BY]-> **Actor**
- **MaritimeCase** -[:RELATED_TO]-> **MaritimeCase** (similar cases)

### Situation & Risk
- **CollisionRisk** -[:TRIGGERS]-> **SituationType**
- **CollisionRisk** -[:REQUIRES_RULE]-> **COLREGsRule**
- **CollisionRisk** -[:MITIGATED_BY]-> **Action**

### Evidence Relationships
- **Evidence** -[:SUPPORTS]-> **MaritimeCase**
- **Evidence** -[:INDICATES]-> **CollisionRisk**
- **Evidence** -[:COLLECTED_BY]-> **Actor**

### Action Relationships
- **Action** -[:RECOMMENDED_BY]-> **COLREGsRule**
- **Action** -[:PREVENTS]-> **CollisionRisk**
- **Action** -[:APPLIED_IN]-> **MaritimeCase** (successfully or not)

---

## Example Data Structure

### Scenario: Crossing Situation in Fog

```
Vessel_A (Cargo Ship):
  - type: cargo
  - speed: 12 knots
  - heading: 090° (East)
  - position: (35.1234, 129.5678)

Vessel_B (Fishing Vessel):
  - type: fishing
  - speed: 8 knots
  - heading: 180° (South)
  - position: (35.1240, 129.5685)
  - relative_bearing to A: Starboard bow (우현 전방)

CollisionRisk:
  - CPA: 0.2 NM
  - TCPA: 5 minutes
  - Situation: crossing_situation + restricted_visibility
  - Risk Level: critical

Applicable Rules:
  - Rule 15: Crossing Situation
  - Rule 19: Restricted Visibility
  - Rule 5: Look-out
  - Rule 6: Safe Speed

Relevant Case:
  - KMST-2023-001: Fog collision between cargo and fishing vessel
  - Violated: Rule 19 (안전한 속력 미준수)
  - Lesson: "시계 제한 시 속력을 대폭 감속하고 경계를 강화해야 함"

Recommended Actions:
  1. Reduce speed to 5 knots (Rule 19)
  2. Sound fog signal (Rule 19)
  3. Alter course to starboard 30° (Rule 15, 16)
  4. Maintain radar watch (Rule 5)

Evidence:
  - Radar screenshot at T-5min
  - AIS track data
  - Weather report: visibility 50m
```

---

## Graph Query Examples

### Find all rules applicable to crossing situation:
```cypher
MATCH (r:COLREGsRule)-[:APPLIES_TO]->(st:SituationType {name: "crossing_situation"})
RETURN r.rule_number, r.title_kr, r.full_text_kr
```

### Find cases that violated Rule 15:
```cypher
MATCH (c:MaritimeCase)-[:VIOLATED]->(r:COLREGsRule {rule_id: "rule_15"})
RETURN c.case_id, c.title_kr, c.judgment
```

### Find actions recommended for restricted visibility:
```cypher
MATCH (st:SituationType {name: "restricted_visibility"})<-[:APPLIES_TO]-(r:COLREGsRule)-[:RECOMMENDS]->(a:Action)
RETURN DISTINCT a.name_kr, a.description, r.rule_number
```

### Find similar cases based on situation type:
```cypher
MATCH (c1:MaritimeCase)-[:EXAMPLE_OF]->(st:SituationType)<-[:EXAMPLE_OF]-(c2:MaritimeCase)
WHERE c1.case_id = "KMST-2023-001" AND c1 <> c2
RETURN c2.case_id, c2.title_kr, c2.judgment
```

---

## Ontology Metrics

- **Total Entity Types**: 10
- **Total Relationship Types**: 25+
- **COLREGs Rules**: ~20 (key rules)
- **Situation Types**: 8 major types
- **Action Types**: 6 categories
- **Evidence Types**: 7 types

This ontology enables:
1. Precise situation classification
2. Rule-based reasoning
3. Case-based reasoning
4. Evidence-supported decisions
5. Multi-hop graph traversal
6. Explainable AI recommendations
