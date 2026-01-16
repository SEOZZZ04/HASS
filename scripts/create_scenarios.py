"""
시연용 시나리오 데이터 생성
사용자가 클릭하여 AI의 사고 과정을 볼 수 있는 상황들
"""
import json
import os

# 시연용 시나리오 (Vision AI → Graph → LLM → Action 전체 프로세스 시연)
DEMO_SCENARIOS = [
    {
        "scenario_id": "scenario_001",
        "title": "안개 속 어선 긴급 회피",
        "thumbnail_desc": "안개가 낀 상황에서 전방에 소형 어선 갑자기 출현",
        "difficulty": "high",
        "risk_level": 9,
        "situation": {
            "visibility": "50미터 (농무)",
            "sea_state": "잔잔함",
            "time": "03:20",
            "weather": "안개",
            "own_ship": {
                "type": "컨테이너선",
                "speed": "12노트",
                "heading": "045°",
                "position": "인천항 서방 5마일"
            },
            "target_vessels": [
                {
                    "id": "target_001",
                    "type": "어선 (소형)",
                    "bearing": "045°",
                    "distance": "0.5마일",
                    "speed": "2노트",
                    "cpa": "0.1마일",
                    "tcpa": "3분",
                    "detected_by": "YOLO (카메라)",
                    "radar_visibility": "Poor (레이더 반사판 없음)",
                    "vessel_status": "어로 작업 중 (표류)"
                }
            ]
        },
        "yolo_detection": {
            "timestamp": "03:20:15",
            "detections": [
                {
                    "class": "Fishing Boat",
                    "confidence": 0.87,
                    "bbox": [245, 180, 315, 240],
                    "bearing": 45.2,
                    "distance": 0.48,
                    "size": "small"
                }
            ]
        },
        "expected_reasoning_flow": {
            "step1_perception": "YOLO가 흐릿한 영상 속에서 Fishing Boat 패턴 즉시 감지",
            "step2_graph_context": "Neo4j에 (TargetShip)-[:IS_APPROACHING {risk: 0.9}]->(OwnShip) 관계 생성. 상황: CROSSING_FROM_STARBOARD + FOG_CONDITION",
            "step3_rule_retrieval": "그래프에서 '시계 제한 + 어선' 상황 → COLREGs 제19조, 제18조, 판례 KMST-2023-001 인출",
            "step4_legal_analysis": "제19조: 안개 중 안전 속력 + 조기 회피. 제18조: 동력선은 어선 피항 의무. 판례: 유사 사고에서 즉시 감속 권고",
            "step5_simulation": "우현 30도 변침 + 감속 5노트 → CPA 1.2마일 확보",
            "step6_recommendation": "즉시 감속 5노트 + 우현 30도 변침 + 안개 신호 발사"
        },
        "correct_actions": [
            {
                "action": "즉시 감속",
                "target_speed": "5노트",
                "priority": 1,
                "colregs": "rule_19"
            },
            {
                "action": "우현 변침",
                "target_heading": "075°",
                "degree_change": 30,
                "priority": 2,
                "colregs": "rule_08"
            },
            {
                "action": "안개 신호 발사",
                "signal_type": "장음 1회",
                "priority": 3,
                "colregs": "rule_19"
            },
            {
                "action": "VHF 교신",
                "channel": "16",
                "priority": 4,
                "colregs": "rule_08"
            }
        ],
        "related_cases": ["KMST-2023-001", "KMST-2024-003"],
        "related_rules": ["rule_05", "rule_06", "rule_07", "rule_18", "rule_19"]
    },
    {
        "scenario_id": "scenario_002",
        "title": "우현 횡단 상황 - 컨테이너선 접근",
        "thumbnail_desc": "우현에서 대형 컨테이너선이 교차 항로로 접근",
        "difficulty": "medium",
        "risk_level": 7,
        "situation": {
            "visibility": "10마일 (맑음)",
            "sea_state": "파고 1미터",
            "time": "14:30",
            "weather": "맑음",
            "own_ship": {
                "type": "화물선",
                "speed": "14노트",
                "heading": "180°",
                "position": "부산 남동방 12마일"
            },
            "target_vessels": [
                {
                    "id": "target_002",
                    "type": "컨테이너선",
                    "bearing": "110°",
                    "distance": "3.5마일",
                    "speed": "18노트",
                    "cpa": "0.4마일",
                    "tcpa": "8분",
                    "detected_by": "레이더 + AIS",
                    "vessel_status": "일반 항행",
                    "relative_position": "우현 (Starboard)"
                }
            ]
        },
        "yolo_detection": {
            "timestamp": "14:30:00",
            "detections": [
                {
                    "class": "Container Ship",
                    "confidence": 0.95,
                    "bbox": [520, 200, 680, 350],
                    "bearing": 110.5,
                    "distance": 3.48,
                    "size": "large"
                }
            ]
        },
        "expected_reasoning_flow": {
            "step1_perception": "YOLO + 레이더로 대형 컨테이너선 탐지. 명확한 우현 접근 확인",
            "step2_graph_context": "(OwnShip)-[:HAS_TARGET_AT_STARBOARD]->(TargetShip). 상황: CROSSING_SITUATION, 본선이 피항선(Give-way)",
            "step3_rule_retrieval": "그래프 쿼리: '우현 교차' → COLREGs 제15조, 제16조, 판례 KMST-2022-045 인출",
            "step4_legal_analysis": "제15조: 타선을 우현에 둔 선박이 피항선. 제16조: 조기 대폭 동작. 판례: 소폭 변침은 오히려 위험, 최소 30도 이상 권고",
            "step5_simulation": "우현 35도 변침 → 상대 선미 통과, CPA 1.8마일 확보. 좌현 변침 시뮬레이션: 상대 선수 횡단 = 위험",
            "step6_recommendation": "조기 우현 35도 변침 (상대 선미 통과). 좌현 변침 금지."
        },
        "correct_actions": [
            {
                "action": "우현 대폭 변침",
                "target_heading": "215°",
                "degree_change": 35,
                "priority": 1,
                "colregs": "rule_15"
            },
            {
                "action": "속력 유지 또는 감속",
                "target_speed": "12노트",
                "priority": 2,
                "colregs": "rule_16"
            },
            {
                "action": "기적 신호",
                "signal_type": "단음 1회 (우현 변침)",
                "priority": 3,
                "colregs": "rule_34"
            }
        ],
        "wrong_actions": [
            {
                "action": "좌현 변침",
                "reason": "상대 선박 앞을 가로지르게 되어 충돌 위험 증가",
                "danger_level": "high"
            },
            {
                "action": "소폭 변침 (10도 이하)",
                "reason": "상대가 인지하지 못해 효과 없음",
                "danger_level": "medium"
            }
        ],
        "related_cases": ["KMST-2022-045", "KMST-2023-134"],
        "related_rules": ["rule_07", "rule_08", "rule_15", "rule_16"]
    },
    {
        "scenario_id": "scenario_003",
        "title": "마주치는 상황 - 여객선 정면 접근",
        "thumbnail_desc": "정면에서 여객선이 마주 보며 접근 중",
        "difficulty": "medium",
        "risk_level": 8,
        "situation": {
            "visibility": "8마일 (맑음)",
            "sea_state": "파고 0.5미터",
            "time": "22:15 (야간)",
            "weather": "맑음",
            "own_ship": {
                "type": "화물선",
                "speed": "13노트",
                "heading": "270°",
                "position": "제주 북방 8마일"
            },
            "target_vessels": [
                {
                    "id": "target_003",
                    "type": "여객선",
                    "bearing": "270°",
                    "distance": "2.0마일",
                    "speed": "20노트",
                    "cpa": "0.0마일",
                    "tcpa": "4분",
                    "detected_by": "육안 (양쪽 현등 보임) + 레이더",
                    "vessel_status": "일반 항행",
                    "lights_visible": "마스트등 + 홍등 + 녹등 (정면)"
                }
            ]
        },
        "yolo_detection": {
            "timestamp": "22:15:00",
            "detections": [
                {
                    "class": "Passenger Ship",
                    "confidence": 0.92,
                    "bbox": [380, 220, 460, 320],
                    "bearing": 270.1,
                    "distance": 1.98,
                    "size": "large",
                    "lights": "red_green_both_visible"
                }
            ]
        },
        "expected_reasoning_flow": {
            "step1_perception": "야간 영상에서 마스트등 + 홍등 + 녹등 모두 탐지 → 정면 마주침 확인",
            "step2_graph_context": "(OwnShip)-[:HEAD_ON]->(TargetShip). 상황: HEAD_ON_SITUATION, 양 선박 모두 피항선",
            "step3_rule_retrieval": "그래프: '정면 마주침' → COLREGs 제14조, 판례 KMST-2024-012 인출",
            "step4_legal_analysis": "제14조: 양 선박 모두 우현 변침. 좌현 변침 절대 금지. 판례: 좌현 변침으로 인한 충돌 사고 다수",
            "step5_simulation": "우현 30도 변침 → 좌현끼리 안전 통과. 좌현 변침 시뮬레이션: 상대도 좌현 변침 시 충돌",
            "step6_recommendation": "즉시 우현 30도 변침. 절대 좌현 변침 금지. 기적 신호 발사."
        },
        "correct_actions": [
            {
                "action": "우현 변침",
                "target_heading": "300°",
                "degree_change": 30,
                "priority": 1,
                "colregs": "rule_14"
            },
            {
                "action": "기적 신호",
                "signal_type": "단음 1회 (우현 변침)",
                "priority": 2,
                "colregs": "rule_34"
            },
            {
                "action": "속력 유지",
                "target_speed": "13노트",
                "priority": 3,
                "colregs": "rule_14"
            }
        ],
        "critical_warnings": [
            {
                "warning": "좌현 변침 절대 금지",
                "reason": "제14조 명시적 금지 사항. 양 선박 모두 좌현 변침 시 충돌 가능성 극대화",
                "severity": "CRITICAL"
            }
        ],
        "related_cases": ["KMST-2024-012"],
        "related_rules": ["rule_08", "rule_14"]
    },
    {
        "scenario_id": "scenario_004",
        "title": "협수로 내 어선 조우",
        "thumbnail_desc": "좁은 수로에서 전방 어선과 조우",
        "difficulty": "medium",
        "risk_level": 6,
        "situation": {
            "visibility": "5마일",
            "sea_state": "잔잔함",
            "time": "10:45",
            "weather": "맑음",
            "own_ship": {
                "type": "화물선",
                "speed": "8노트",
                "heading": "090°",
                "position": "진해만 협수로 (폭 200m)"
            },
            "target_vessels": [
                {
                    "id": "target_004",
                    "type": "어선 (트롤)",
                    "bearing": "085°",
                    "distance": "0.8마일",
                    "speed": "3노트",
                    "vessel_status": "어로 작업 중",
                    "position_in_channel": "중앙 부근"
                }
            ]
        },
        "yolo_detection": {
            "timestamp": "10:45:00",
            "detections": [
                {
                    "class": "Fishing Boat",
                    "confidence": 0.89,
                    "bbox": [310, 190, 370, 250],
                    "bearing": 85.3,
                    "distance": 0.82,
                    "size": "small",
                    "shapes": "red_white_balls_2"
                }
            ]
        },
        "expected_reasoning_flow": {
            "step1_perception": "YOLO로 어선 탐지 + 형상물(빨강-흰색 구 2개) 인식 → 어로 작업 확인",
            "step2_graph_context": "(TargetShip:FishingVessel)-[:IN_NARROW_CHANNEL]->(Channel). (OwnShip:PowerVessel)-[:MUST_AVOID]->(FishingVessel)",
            "step3_rule_retrieval": "그래프: '협수로 + 어선' → COLREGs 제9조, 제18조, 판례 KMST-2023-089 인출",
            "step4_legal_analysis": "제18조: 동력선은 어선 피항. 제9조: 협수로에서도 원칙 적용. 판례: 어선은 조종 제한 상태, 충분한 거리 확보 필요",
            "step5_simulation": "감속 4노트 + 최대한 우측 항행 + VHF 교신 → 안전 통과",
            "step6_recommendation": "감속 + 우측 항행 + VHF 교신으로 어선 동작 파악"
        },
        "correct_actions": [
            {
                "action": "감속",
                "target_speed": "4노트",
                "priority": 1,
                "colregs": "rule_06"
            },
            {
                "action": "우측 항행 유지",
                "priority": 2,
                "colregs": "rule_09"
            },
            {
                "action": "VHF 교신",
                "channel": "16",
                "message": "어선 작업 방향 확인",
                "priority": 3,
                "colregs": "rule_08"
            },
            {
                "action": "안전거리 확보",
                "minimum_distance": "0.3마일",
                "priority": 4,
                "colregs": "rule_18"
            }
        ],
        "related_cases": ["KMST-2023-089"],
        "related_rules": ["rule_06", "rule_09", "rule_18"]
    },
    {
        "scenario_id": "scenario_005",
        "title": "TSS 횡단 - 통항로 직각 통과",
        "thumbnail_desc": "분리통항대(TSS)를 횡단해야 하는 상황",
        "difficulty": "high",
        "risk_level": 7,
        "situation": {
            "visibility": "10마일",
            "sea_state": "파고 1미터",
            "time": "16:00",
            "weather": "맑음",
            "own_ship": {
                "type": "화물선",
                "speed": "12노트",
                "heading": "045°",
                "position": "부산 TSS 진입 지점"
            },
            "tss_info": {
                "traffic_flow_direction": "090°",
                "crossing_required": True,
                "traffic_density": "중간"
            },
            "target_vessels": [
                {
                    "id": "target_005a",
                    "type": "컨테이너선",
                    "bearing": "090°",
                    "distance": "2.5마일",
                    "speed": "18노트",
                    "in_traffic_lane": True
                },
                {
                    "id": "target_005b",
                    "type": "탱커",
                    "bearing": "095°",
                    "distance": "4.0마일",
                    "speed": "15노트",
                    "in_traffic_lane": True
                }
            ]
        },
        "yolo_detection": {
            "timestamp": "16:00:00",
            "detections": [
                {
                    "class": "Container Ship",
                    "confidence": 0.93,
                    "bbox": [280, 210, 390, 310],
                    "bearing": 90.2,
                    "distance": 2.48
                },
                {
                    "class": "Tanker",
                    "confidence": 0.91,
                    "bbox": [420, 230, 510, 315],
                    "bearing": 95.1,
                    "distance": 3.95
                }
            ]
        },
        "expected_reasoning_flow": {
            "step1_perception": "통항로 내 2척의 선박 탐지. 교통 밀도 중간, 횡단 가능 간격 확인",
            "step2_graph_context": "(OwnShip)-[:NEEDS_CROSS]->(TSS_Lane). (Lane)-[:HAS_TRAFFIC_FLOW {direction: 090}]",
            "step3_rule_retrieval": "그래프: 'TSS 횡단' → COLREGs 제10조, 판례 KMST-2024-021 인출",
            "step4_legal_analysis": "제10조: 횡단 시 교통 흐름에 직각(90도). 신속히 통과. 통항선 방해 금지. 판례: 역방향 또는 평행 횡단은 극히 위험",
            "step5_simulation": "침로 180도로 변경 → 교통 흐름(090)에 직각. 2척 선박 간격 통과. 속력 증가로 신속 통과",
            "step6_recommendation": "침로 180도 변경 (직각 횡단) + 속력 증대 15노트 + 지속 경계"
        },
        "correct_actions": [
            {
                "action": "직각 침로 변경",
                "target_heading": "180°",
                "reason": "교통 흐름(090°)에 대하여 직각",
                "priority": 1,
                "colregs": "rule_10"
            },
            {
                "action": "속력 증가",
                "target_speed": "15노트",
                "reason": "신속히 통항로 통과",
                "priority": 2,
                "colregs": "rule_10"
            },
            {
                "action": "지속적 경계",
                "tools": "레이더 + AIS + 육안",
                "priority": 3,
                "colregs": "rule_05"
            }
        ],
        "critical_warnings": [
            {
                "warning": "통항로 내 장시간 체류 금지",
                "reason": "다른 선박의 통행 방해",
                "severity": "HIGH"
            },
            {
                "warning": "역방향 또는 평행 횡단 절대 금지",
                "reason": "고속도로 역주행과 동일한 위험",
                "severity": "CRITICAL"
            }
        ],
        "related_cases": ["KMST-2024-021"],
        "related_rules": ["rule_10"]
    },
    {
        "scenario_id": "scenario_006",
        "title": "유지선 상황 - 피항선 회피 미흡",
        "thumbnail_desc": "본선이 유지선이나 피항선이 제대로 피하지 않는 상황",
        "difficulty": "high",
        "risk_level": 8,
        "situation": {
            "visibility": "10마일",
            "sea_state": "파고 1.5미터",
            "time": "08:30",
            "weather": "맑음",
            "own_ship": {
                "type": "화물선",
                "speed": "14노트",
                "heading": "135°",
                "position": "포항 동방 6마일",
                "role": "유지선 (Stand-on)"
            },
            "target_vessels": [
                {
                    "id": "target_006",
                    "type": "화물선",
                    "bearing": "160°",
                    "distance": "2.0마일",
                    "speed": "15노트",
                    "cpa": "0.3마일",
                    "tcpa": "5분",
                    "role": "피항선 (Give-way)",
                    "action_status": "소폭 변침 (10도) - 불충분"
                }
            ]
        },
        "yolo_detection": {
            "timestamp": "08:30:00",
            "detections": [
                {
                    "class": "Cargo Ship",
                    "confidence": 0.94,
                    "bbox": [340, 240, 450, 340],
                    "bearing": 160.3,
                    "distance": 1.97
                }
            ]
        },
        "expected_reasoning_flow": {
            "step1_perception": "타선이 좌현에서 접근 중 → 본선이 유지선 확인",
            "step2_graph_context": "(OwnShip)-[:IS_STAND_ON]->(Situation). (TargetShip)-[:INSUFFICIENT_ACTION]->(CPA: 0.3mi)",
            "step3_rule_retrieval": "그래프: '유지선 + 피항선 미흡' → COLREGs 제17조, 판례 KMST-2023-134 인출",
            "step4_legal_analysis": "제17조(a): 피항선이 안 피하면 협력 가능. (b): 근접 시 독자 회피 필수. 판례: 유지선도 충돌 책임",
            "step5_simulation": "현재 침로 유지 시: CPA 0.3마일 (위험). 우현 변침 시: CPA 1.0마일 (안전)",
            "step6_recommendation": "즉시 우현 협력 변침 + 기적 5단음 경고"
        },
        "correct_actions": [
            {
                "action": "기적 5단음 이상",
                "reason": "위험 경고 신호",
                "priority": 1,
                "colregs": "rule_34"
            },
            {
                "action": "우현 협력 변침",
                "target_heading": "165°",
                "degree_change": 30,
                "reason": "제17조 협력 회피 의무",
                "priority": 2,
                "colregs": "rule_17"
            },
            {
                "action": "감속",
                "target_speed": "10노트",
                "priority": 3,
                "colregs": "rule_17"
            }
        ],
        "key_lessons": [
            "유지선 ≠ 충돌 권한",
            "피항선이 안 피하면 즉시 협력",
            "CPA 0.5마일 이내는 독자 회피 필수",
            "기적 5단음은 긴급 위험 신호"
        ],
        "related_cases": ["KMST-2023-134"],
        "related_rules": ["rule_15", "rule_17"]
    }
]

def save_scenarios():
    """시연용 시나리오 데이터를 JSON 파일로 저장"""
    output_dir = "/home/user/HASS/data/raw"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "demo_scenarios.json")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(DEMO_SCENARIOS, f, ensure_ascii=False, indent=2)

    print(f"✅ 시연용 시나리오 {len(DEMO_SCENARIOS)}개 저장 완료: {output_file}")

    # 통계 출력
    print(f"\n📊 시나리오 난이도별 통계:")
    difficulties = {}
    for scenario in DEMO_SCENARIOS:
        diff = scenario['difficulty']
        difficulties[diff] = difficulties.get(diff, 0) + 1

    for diff, count in difficulties.items():
        print(f"  - {diff}: {count}개")

    print(f"\n🎯 시나리오 목록:")
    for scenario in DEMO_SCENARIOS:
        print(f"  - {scenario['scenario_id']}: {scenario['title']} (위험도: {scenario['risk_level']}/10)")

    return output_file

if __name__ == "__main__":
    save_scenarios()
