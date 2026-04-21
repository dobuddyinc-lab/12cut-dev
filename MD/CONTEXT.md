# 12cut 프로젝트 컨텍스트

> 최종 업데이트: 2026-04-18
> 목적: 인수인계, 외주 커뮤니케이션, 클라이언트 보고용 통합 문서

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로젝트 | 12cut 제품 랜딩 페이지 |
| 위치 | `/Users/jinwonchoi/Desktop/project/12cut` |
| 스택 | HTML + Vanilla CSS + Vanilla JS |
| 호스팅 | Vercel |
| Production URL | https://12cut.vercel.app |
| 다국어 | 한국어, 영어, 일본어, 중국어 |

---

## 2. 작업 내역 (최근 세션)

### 2.1 텍스트 콘텐츠 수정
- "12컷을 만드는 과정(How It Works)" 3단계 설명 문구 한·영·일·중 4개 언어 업데이트
- 수정 파일: `script.js` (i18n 객체)

### 2.2 제품 3D 뷰어 신규 구현 (핵심)

**진행 경로**:
1. 분해 영상 비디오 스크러빙 시도 → 회전용 영상이 아니라 부적합
2. AI 이미지→3D 변환 (Meshy.ai) → 무료 다운로드 제한
3. 사용자 자체 AI 변환 GLB 적용 → 품질 한계
4. **STP(기구설계 파일) → GLB 변환 + Blender 정렬** ← 현재 적용

### 2.3 Blender 자동화 스크립트
- `scripts/fix-glb.py` 신규 생성
- 기능: GLB 축/원점 정렬, 스케일 정규화, 회전 베이크
- 실행 명령: `blender --background --python scripts/fix-glb.py -- 180 -90 -90`
- 회전 파라미터: `X Y Z` 순서 (도 단위)

### 2.4 컬러 변경 기능
- 컬러 6종 (화이트/크림/라이트블루/그린/레드/다크그레이)
- 구현: `model-viewer`의 `pbrMetallicRoughness.setBaseColorFactor` API
- 한계: 단색 덮기 방식 (파츠별 분리 불가)

---

## 3. 현재 배포 상태

### 3.1 적용 기능

| 기능 | 상태 |
|---|---|
| 3D 모델 표시 | ✅ |
| 360도 드래그 회전 | ✅ |
| 컬러 6종 전환 | ✅ |
| 반응형 레이아웃 | ✅ |
| 접근성 (ARIA, 키보드) | ✅ |
| 스크롤 줌/팬 비활성화 | ✅ |

### 3.2 model-viewer 설정

```html
<model-viewer
  src="assets/models/product-fixed.glb?v=r2"
  poster="assets/images/product-viewer.png"
  camera-controls
  disable-zoom
  disable-pan
  shadow-intensity="1.5"
  shadow-softness="0.9"
  exposure="1.15"
  environment-image="neutral"
  camera-orbit="-15deg 75deg auto"
  interaction-prompt="none">
</model-viewer>
```

---

## 4. 알려진 한계

### 4.1 재질감 부재
- **원인**: STP(CAD) 파일은 색상·재질 정보 미포함
- **증상**: 단색 회색 플라스틱 느낌, 매트 질감 표현 불가
- **영향도**: 중간

### 4.2 컬러 변경 방식의 한계
- **원인**: 단일 Material에 단색 덮기
- **증상**: 본체·스트랩·버튼 모두 동일 색으로 변경됨 (실제 제품은 파츠별 다른 색)
- **영향도**: 높음

### 4.3 12cut 로고 음각 미흡
- **원인**: Normal Map 미적용
- **증상**: 음각 깊이감 부족
- **영향도**: 낮음

---

## 5. 향후 작업 (Phase 2)

### 5.1 외주 업체 요청 사항

**우선순위 1**: 컬러별 GLB 파일 6종
- product-white.glb / cream / lightblue / green / red / darkgray

**우선순위 2 (1순위 불가 시)**: 원본 3D 렌더링 파일
- FBX 또는 OBJ + 텍스처 맵
- 컬러별 Material 정의 포함

### 5.2 기술 스펙

| 항목 | 사양 |
|---|---|
| 폴리곤 수 | 10만 이하 |
| 파일 용량 | 5MB 이하 |
| 텍스처 해상도 | 2048x2048 또는 1024x1024 |
| 좌표계 | Y-up |
| Material | PBR (Albedo/Roughness/Metallic/Normal) |

### 5.3 PBR Material 설정 가이드

| 파츠 | Albedo | Roughness | Metallic |
|---|---|---|---|
| 본체 (실리콘) | 컬러별 | 0.75 (매트) | 0 |
| 스트랩 | 컬러별 | 0.8 (매트) | 0 |
| 버튼/다이얼 | 컬러별 | 0.5 (세미매트) | 0 |
| 12cut 로고 | 본체와 동일 | 0.8 + Normal Map (음각) | 0 |

### 5.4 외주 핵심 질문
> "과거 제품 렌더링 이미지를 제작한 적이 있는지, 있다면 그 원본 파일(.blend/.max/.c4d 등)을 공유받을 수 있는지?"

---

## 6. 파일 구조

```
12cut/
├── index.html              # 메인 페이지
├── style.css               # 스타일
├── script.js               # 인터랙션 + i18n
├── AGENTS.md               # Vercel 베스트 프랙티스
├── MD/
│   ├── CONTEXT.md          # 본 문서
│   └── prd-12cut.md        # 제품 요구사항 정의서
├── scripts/
│   └── fix-glb.py          # Blender GLB 정렬 스크립트
└── assets/
    ├── models/
    │   ├── product-viewer.glb   # 원본 (CAD 변환본)
    │   └── product-fixed.glb    # Blender 정렬 버전 (현재 사용)
    ├── images/
    │   └── product-viewer.png   # poster 이미지
    └── videos/
        └── product-3d.mp4       # 미사용 (분해 영상)
```

---

## 7. 현재 버전 명칭

**Beta 3D Preview (v1.0)**

> 정밀 CAD 설계 기반의 1차 인터랙티브 3D 뷰어. 형상·치수·회전·컬러 전환 기능 완성. PBR 재질 레이어는 Phase 2에서 외주 협업 후 적용 예정.

---

## 8. 클라이언트 설명 프레이밍

### DON'T
- ❌ "아직 완성이 아니라서..."
- ❌ "재질이 제대로 안 나왔는데..."

### DO
- ✅ "정밀 설계 기반으로 먼저 구현했습니다. 실제 제품과 치수·비율이 1:1 일치합니다."
- ✅ "Phase 1은 형상과 인터랙션을 우선 완성하고, Phase 2에서 PBR 재질 레이어를 추가하는 점진적 고도화 방식입니다."

---

## 9. 외주 전달 메시지 템플릿

```markdown
안녕하세요, 12컷 제품 웹사이트 3D 뷰어 제작을 위해 추가 파일 요청드립니다.

■ 용도
- 제품 상세 페이지 내 인터랙티브 3D 뷰어 (360도 회전, 컬러 변경)
- 기존 전달받은 STP(기구설계) 파일은 색상/재질 정보가 없어 웹용 3D 뷰어로 부적합

■ 요청 파일 (우선순위 순)
1순위: 컬러별 GLB 파일 6종 (화이트/크림/라이트블루/그린/레드/다크그레이)
2순위: FBX 또는 OBJ + 텍스처 맵 (당사에서 GLB 변환 처리)

■ 기술 스펙
- 폴리곤 10만 이하, 파일 5MB 이하
- 좌표계: Y-up
- Material: PBR (Albedo/Roughness/Metallic/Normal)

■ 재질 기준
- 전체 매트(Matte) 실리콘/플라스틱 질감
- Roughness: 0.7 ~ 0.85 (반사 거의 없음)
- Metallic: 0 (비금속)
- 12cut 로고는 Normal Map 음각 표현
- 스트랩/버튼은 실제 제품 컬러 반영

■ 납기
- 1차 샘플(1개 컬러): 1주
- 최종 6종: 검수 후 2주

문의 부탁드립니다. 감사합니다.
```

---

## 10. 의사결정 대기 항목

| 항목 | Option A | Option B |
|---|---|---|
| 외주 비용 발생 시 | 6종 GLB 정식 의뢰 (품질 우선) | FBX만 받고 자체 변환 |
| 외주 파일 미보유 시 | Photogrammetry 별도 외주 | 현재 Beta + AI 텍스처링 |
| Beta 배지 표시 | 3D 뷰어 상단에 배지 추가 | 배지 없이 설명서만 |
