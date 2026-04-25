# 12cut 프로젝트 컨텍스트

> 최종 업데이트: 2026-04-22
> 목적: 인수인계, 외주 커뮤니케이션, 클라이언트 보고용 통합 문서

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로젝트 | 12cut 제품 랜딩 페이지 |
| 위치 | `/Users/jinwonchoi/Desktop/project/12cut` |
| 스택 | HTML + Vanilla CSS + Vanilla JS |
| 호스팅 | Cloudflare Pages (GitHub 연동 자동 배포) |
| Production URL | https://12cut.pages.dev |
| GitHub 저장소 | https://github.com/dobuddyinc-lab/12cut |
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

---

## 11. 배포 & 버전관리 (2026-04-22 세션 추가)

### 11.1 인프라 구성도

```
로컬 (MacBook Pro)
  └─ /Users/jinwonchoi/Desktop/project/12cut (Git main)
       │ git push
       ▼
GitHub 저장소
  └─ github.com/dobuddyinc-lab/12cut (Public)
       │ webhook
       ▼
Cloudflare Pages
  └─ 12cut.pages.dev (Global CDN, 300+ POP)
```

### 11.2 GitHub 저장소

| 항목 | 값 |
|---|---|
| 소유 계정 | `dobuddyinc-lab` (개인 계정, 조직 아님) |
| 가시성 | Public |
| 기본 브랜치 | `main` |
| 초기 커밋 | `05fb9a6` chore: initial commit — 12cut brand site |
| 용량 | 약 38MB (영상·3D 모델·이미지 포함) |

### 11.3 Cloudflare Pages 설정

| 항목 | 값 |
|---|---|
| Cloudflare 계정 | Dobuddy.inc@gmail.com |
| Project name | `12cut` |
| Production branch | `main` |
| Framework preset | None (정적 사이트) |
| Build command | (없음) |
| Build output directory | `/` |
| 배포 영역 | Region: Earth (글로벌) |
| 초기 응답 속도 | 약 68ms (CDN 캐시 히트) |

### 11.4 인증·권한 구성

**Git push 인증 (로컬 → GitHub)**
- 방식: HTTPS + Personal Access Token (PAT)
- 이유: Mac SSH 공개키가 `jay11111762` 계정에 종속되어 `dobuddyinc-lab` 계정 SSH 접근 불가
- 자격 저장 위치: macOS Keychain (`git credential-osxkeychain`)
- PAT 발급 계정: `dobuddyinc-lab`
- PAT 만료: 90일 (재발급 필요 시점 캘린더 등록 권장)

**Cloudflare ↔ GitHub 연동**
- 설치 앱: Cloudflare Workers and Pages (GitHub App)
- Repository access: Only select repositories → `dobuddyinc-lab/12cut`
- 권한 관리 URL: `github.com/settings/installations`

### 11.5 운영 플로우 (확정 CI/CD)

```bash
# 코드 수정 → 자동 배포까지 한 줄
cd /Users/jinwonchoi/Desktop/project/12cut
git add -A && git commit -m "feat: 설명" && git push
# → 약 30~60초 내 https://12cut.pages.dev 반영
```

- Pull Request 생성 시 → 고유 Preview URL 자동 생성 (스테이징 용도)
- Cloudflare Dashboard → Pages → `12cut` → Deployments 탭에서 이력·롤백 가능
- 과거 배포로 1-click rollback 지원

### 11.6 세션 중 발생한 이슈 & 해결 (재발 방지 기록)

| # | 증상 | 원인 | 해결 |
|---|---|---|---|
| 1 | `brew install gh` 실패 | Cursor 권한 다이얼로그 렌더링 오류 | gh CLI 없이 웹 UI로 레포 생성 방식 채택 |
| 2 | SSH push 시 `Permission to dobuddyinc-lab/12cut.git denied to jay11111762` | Mac SSH 키가 jay11111762에만 등록됨, GitHub는 동일 키 복수 계정 등록 불가 | HTTPS + PAT 방식으로 전환 |
| 3 | HTTPS push 시 `Password authentication is not supported` | GitHub가 2021년부터 비밀번호 인증 폐지 | PAT(classic, `repo` scope)를 Password 자리에 입력 |
| 4 | Push 중 `RPC failed; HTTP 400 / send-pack: unexpected disconnect` | Git 기본 `http.postBuffer` 1MB가 17MiB 압축본보다 작아 전송 중단 | `git config http.postBuffer 524288000` (500MB)로 증가 |
| 5 | Cloudflare Pages `Connect GitHub` 반복 클릭 시 같은 화면 복귀 | 이전 설치 상태에서 OAuth 재링크 과정 불완전 | Chrome 정상 창에서 재시도 → 성공 |

### 11.7 향후 고도화 로드맵 (배포 인프라 관점)

| 우선순위 | 작업 | 예상 소요 | 기대 효과 |
|---|---|---|---|
| High | 커스텀 도메인 연결 (예: `12cut.dobuddy.com`) | 5분 | BX 일관성, `pages.dev` 노출 제거 |
| High | `.glb` MIME type 확인 및 필요 시 `_headers` 추가 | 2분 | 3D 모델 로드 안정성 |
| Med | Cloudflare Web Analytics 활성화 | 1분 | 방문자·성능 무료 모니터링 |
| Med | OpenGraph 이미지·메타태그 점검 | 5분 | SNS 공유 시 썸네일 정상화 |
| Low | Branch 전략 정립 (`main` + `dev` 분리) | 10분 | 스테이징/프로덕션 분리, PR 기반 리뷰 체계 |
| Low | GitHub Actions → Lighthouse CI 연동 | 30분 | 성능·접근성 점수 자동 모니터링 |

### 11.8 반드시 기억해야 할 것

- **절대 하지 말 것**:
  - PAT를 코드·채팅·공개 저장소에 노출 (유출 시 `github.com/settings/tokens` 에서 즉시 Revoke)
  - `main` 브랜치에 검증되지 않은 코드 직접 푸시 (자동 프로덕션 반영)
  - `.vercel/` 폴더를 저장소에 커밋 (이미 `.gitignore` 등록됨)

- **정기 점검**:
  - PAT 만료 1주 전 재발급 (90일 주기)
  - Cloudflare Web Analytics로 월 1회 트래픽·성능 리뷰
  - 의존 외부 자원(3D 모델 CDN 등) 가용성 점검

### 11.9 백업·복구

- GitHub 저장소 자체가 1차 백업
- Cloudflare Pages는 과거 배포본 무제한 보관 → 1-click rollback
- 로컬 손실 시 복구: `git clone https://github.com/dobuddyinc-lab/12cut.git` 후 Pages 재연결 불필요 (이미 Git 연동 상태)
