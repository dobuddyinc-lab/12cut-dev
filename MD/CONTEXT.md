# 12cut 프로젝트 컨텍스트

> 최종 업데이트: 2026-05-03 (Shopify Storefront API 연동 완료)
> 목적: 인수인계, 외주 커뮤니케이션, 클라이언트 보고용 통합 문서

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로젝트 | 12cut 제품 랜딩 페이지 |
| 위치 | `/Users/jinwonchoi/Desktop/project/12cut` |
| 스택 | HTML + Vanilla CSS + Vanilla JS |
| 호스팅 | Cloudflare Pages (GitHub 연동 자동 배포) — **Vercel 사용하지 않음** |
| Production URL | https://12cut.pages.dev |
| GitHub 저장소 | https://github.com/dobuddyinc-lab/12cut |
| 다국어 | 한국어, 영어, 일본어, 중국어 |

### 1.1 도메인·URL 전략 메모 (2026-05)

WHOIS 확인분과 **실제 공개 사이트**를 맞춘 기록이다. 레지스트 실무·카피 작성 시 단일 레퍼런스로 쓸 것.

#### 공개 브랜드·법인 디지털 자산

| 채널 | URL |
|------|-----|
| 한국 회사 사이트 | https://www.dobuddy.co.kr/ |
| 일본 DOBUDDY.INC | https://www.dobuddyjp.com/home |

#### 제품 존 후보 · WHOIS 요약 (키워드 12cut)

| 도메인 | 메모 |
|--------|------|
| `12cut.com` | 선점(예: Metaregistrar BV, NL). 응답 404 미사용 추정. 만료 ~2026-10 전후 — 매입·만료 감시 선택지 |
| `12cut.co` | 등록 가능 권장 1순위(글로벌 짧은 URL) |
| `12cut.jp` | 등록 가능(일본 우편 등록 의무 검토) |
| `12cut.photo`, `12cut.studio` | 등록 가능 보조·전시용 |
| `dobuddy.com` | 존 등록됨 다만 레지 공개 정보상 NS 파킹(SedoParking) 형태로 관측 — **실제 DNS 통제 주체가 사업본부와 동일한지 반드시 확인** 후에만 `12cut.dobuddy.com` 채택 |
| `dobuddy.net` | WHOIS 미등록으로 관측됨 — **존 레벨 선등록 필요** 후 `12cut.dobuddy.net` 가능 |

#### 서브도메인 후보 — 운영 존와 정렬

실제 Apex를 통제하는 경우에 한한다.

| 후보 | 용도 |
|------|------|
| `12cut.dobuddy.co.kr` | 국내 B2B·내부·제조 신뢰 노출(APX: dobuddy.co.kr) |
| `12cut.dobuddyjp.com`(또는 `dobuddyjp.com/[...]` 경로 분리) | 일본 바이어·전시 신뢰(APX: dobuddyjp.com) |

#### 전략 옵션 분기(Option A/B)

| Option | 근거 |
|--------|------|
| **A. 회사 존 우선** | Acquisition 신뢰·법인 책임 전달 최소 노력.BX: 제품 헤더·푸터에 회사 링크를 고정해 “12CUT 제품성”과 “DOBUDDY 디자인/제조” 충돌 완충 |
| **B. 제품 독립 존 우선** | 브랜드 검색·직판 채널에 `12cut.co` 등 독립 canonical.Retention/Referral 장기에는 자산 단순함 |

#### 미결 정책(역질문 보류)

검색·광고·명함 등 **표준 진입 Canonical**가 “제품 전용 존”인지 “항상 `*.dobuddy*` 계열만”인지 **합의 전**이며, 미정 시 SEO 및 퍼널 UTM 재작업이 중복된다.

#### 내부 정적 리포트

저장소 `domain-report.html` — Pages 배포 시 `/domain-report.html`, `robots`/헤더 `noindex` 유지.

---

## 2. 작업 내역

### 2026-05-01 세션

#### A. 필름 뷰어 렌즈 구현

릴 상단 12시 방향에 원형 뷰파인더 렌즈를 고정 배치. 스텝 회전 시 해당 위치의 슬라이드 이미지를 렌즈 안에 확대 표시.

| 구성요소 | 파일 | 내용 |
|---|---|---|
| HTML | `index.html` | `.film-reel__lens` 블록 (img + grain + vignette) |
| CSS | `style.css` | 원형 30%, `top: -15%`, 메탈릭 테두리, 비네팅, 그레인 오버레이 |
| JS | `script.js` | `setInterval(2000)` — CSS steps(12) 24s와 동기화, 페이드 전환 |
| 반응형 | `style.css` | 768px 이하: 렌즈를 릴 위 별도 블록으로 이동 (width: 60%) |

- `.examples` overflow `hidden` → `visible`, `.film-reel` margin-top 80px 추가
- 렌즈-릴 매칭 수정: 시계방향 회전 시 12시 방향 슬롯 순서가 역순(0→11→10...)이므로 `stepIndex - 1`로 변경

#### B. 테마 태그 삭제

- 대상: `.examples__themes` (여행/커플/육아/졸업/반려동물/생일)
- 삭제 근거: 필터링 기능 없는 장식용 UI → 클릭 후 결과 없어 유저 기대 위반 (Nielsen 휴리스틱)
- 제거 범위: HTML 요소, CSS 스타일, JS 이벤트 핸들러

#### C. 톤앤매너 검토 + 디자인 시스템 정비

**Option B (Figma 원안 유지) 채택** — 이탈 색상을 디자인 시스템에 공식 등록.

| 변수명 | 값 | 용도 |
|---|---|---|
| `--accent-red` | `#F63237` | How It Works step 라벨 |
| `--cta-blue` | `#0092FB` | Product 구매 버튼 |
| `--cta-blue-dark` | `#007AD9` | Product 구매 버튼 hover |
| `--gray-mid` | `#484848` | Product 카드 배경 |
| `--font-rounded` | SF Pro Rounded fallback chain | Product/How It Works 서체 |

- 하드코딩 9건 → CSS 변수로 교체 완료
- Footer `© 2025` → `© 2026` 수정

#### D. 섹션 순서 재배치

설득 흐름 최적화 (욕구 → 제품 → 과정 → 신뢰 → 전환).

| # | AS-IS | TO-BE |
|---|---|---|
| 1 | Hero | Hero |
| 2 | How It Works | **Gallery** |
| 3 | Gallery | **Product** |
| 4 | Product | **How It Works** |
| 5 | Testimonials | Testimonials |
| 6 | Pricing | Pricing |

- Nav 링크 순서도 섹션 순서에 맞춰 변경 (갤러리→제품→이용방법→가격)

#### E. 가격 체계 통일

| AS-IS | TO-BE |
|---|---|
| Product: 35,000원 / Pricing: Basic 39,000원, Gift 52,000원 | Product: 70,000원 |
| Basic/Gift 2종 티어 | **수량 기반 3종** |

| 구분 | 가격 | 개당 |
|---|---|---|
| 1개 | 70,000원 | 70,000원 |
| 2개 (추천) | 100,000원 | 50,000원 |
| 3개 | 150,000원 | 50,000원 |

- CSS pricing grid `2fr` → `3fr` 변경

#### F. Vercel 배포

| 항목 | 값 |
|---|---|
| Vercel 계정 | jay11111762 |
| Project | 12cut |
| Production URL | https://12cut.vercel.app |
| 배포 방식 | `npx vercel --yes --prod` (수동) |

#### G. 히어로 섹션 영상 프롬프트 검토 & 재설계

Higgsfield(Seedance 2.0) 기반 히어로 영상 v5 프롬프트 검토. 사용자 지적 2건 + 추가 결함 3건 진단 후 v6 Option A/B 산출.

**진단 (5건)**

| # | 결함 | 등급 |
|---|---|---|
| A | 뷰파인더 창 비율: `rounded-square`(1:1) 12회 명시 → 실물은 4:3 라운드 직사각형 (BACK면 권위 이미지 기준) | Critical |
| B | 셔터 누름 손: `right hand index` 명시 → 양손 그립 + 좌측 검지 인체공학 위반 | Critical |
| C | 사진 콘텐츠 비율: 1:1 전제 → 4:3 landscape STILL로 재정의 필요 | High |
| D | 정면(FRONT)/후면(BACK) 면 정의 혼선 → 엔드카드 임의 합성 위험 | High |
| E | Shot 1 → 2 인과 역전: 누르기 전에 휠 자동 회전 | Med |

**FRONT/BACK 권위 이미지 락**

| 면 | 출처 | 구성 |
|---|---|---|
| FRONT | `assets/KakaoTalk_Photo_2024-09-15-15-30-02_001-051d647f-80bc-4a97-bcf7-b4a309e37da0.png` | 매트 화이트 라운드 사각형 / 상단 우측 코너 빨간 돔 셔터 / 좌측면 빨간 하트 스트랩 루프 / 중앙 작은 원형 렌즈 홀(바디 폭 1/4) / 하단 중앙 `12cut` 음각 |
| BACK | `assets/IMG_1464-d1a7f7be-8b83-4500-9a81-39938f122dcd.png` | 4:3 landscape 라운드 직사각형 뷰파인더 창 + 검정 베젤 + `12cut` 음각 |

**산출물 v6 — 두 옵션 발행**

| 옵션 | episode | Shot 수 | 컨셉 | 1차 KPI |
|---|---|---|---|---|
| A (안정 보정) | `12CUT_Hero_EP1_v6_OptionA` | 6 | 기존 구조 유지 + 4:3·좌손·FRONT면 패치 | Activation |
| B (후크 재설계) | `12CUT_Hero_EP1_v6_OptionB` | 5 | 첫 1.5s 매크로 후크(누름 → 정지화) → 페이오프 → 페르소나 → 몽타주 → 엔드카드 | Acquisition |

**공통 적용 규칙**
/ 뷰파인더 창: 4:3 LANDSCAPE rounded-rectangle (정사각·원형 금지)
/ 셔터 압력: LEFT INDEX FINGER 단독 (RIGHT 금지)
/ 사진 콘텐츠: 4:3 STILL (폴라로이드·필름 슬라이드·움직임 금지)
/ 엔드카드: FRONT 면 정면, 25–30% 프레임 점유, ZERO 모션, 텍스트 없음

**의사결정 대기 항목**

| Q | 내용 | 비고 |
|---|---|---|
| Q1 | A vs B 채택 결정 | KPI(Acquisition vs Activation)에 따라 분기 |
| Q2 | 추억 페르소나 풀: 2종(엄마·10대) vs 다세대 확장(연인·가족·노부부) | 1차 타겟 명확화 필요 |
| Q3 | Seedance `image_reference` 슬롯에 BACK면 권위 이미지 동시 주입 가능 여부 | 4:3 정확 렌더링 보강 |

---

### 2026-04-22 세션 (이전)

#### 2.1 텍스트 콘텐츠 수정
- "12컷을 만드는 과정(How It Works)" 3단계 설명 문구 한·영·일·중 4개 언어 업데이트
- 수정 파일: `script.js` (i18n 객체)

#### 2.2 제품 3D 뷰어 신규 구현 (핵심)

**진행 경로**:
1. 분해 영상 비디오 스크러빙 시도 → 회전용 영상이 아니라 부적합
2. AI 이미지→3D 변환 (Meshy.ai) → 무료 다운로드 제한
3. 사용자 자체 AI 변환 GLB 적용 → 품질 한계
4. **STP(기구설계 파일) → GLB 변환 + Blender 정렬** ← 현재 적용

#### 2.3 Blender 자동화 스크립트
- `scripts/fix-glb.py` 신규 생성
- 기능: GLB 축/원점 정렬, 스케일 정규화, 회전 베이크
- 실행 명령: `blender --background --python scripts/fix-glb.py -- 180 -90 -90`
- 회전 파라미터: `X Y Z` 순서 (도 단위)

#### 2.4 컬러 변경 기능
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
├── style.css               # 스타일 (디자인 시스템 변수 포함)
├── script.js               # 인터랙션 + 필름 뷰어 렌즈 동기화
├── AGENTS.md               # Vercel 베스트 프랙티스
├── .vercel/                # Vercel 프로젝트 설정 (.gitignore 등록)
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
    │   ├── nav-logo.svg         # 헤더 로고
    │   ├── how-step1~3.png      # How It Works 폰 목업
    │   ├── product-logo.svg     # Product 섹션 로고
    │   ├── product-viewer.png   # poster 이미지
    │   ├── product-colors.svg   # 컬러 선택 에셋
    │   ├── film-reel-center.png # 필름 릴 중앙 (고정)
    │   └── slides/
    │       └── slide-01~12.jpg  # 필름 릴 슬라이드 이미지 12장
    └── videos/
        └── hero-bg.webm/mp4    # 히어로 배경 영상
```

---

## 7. 현재 버전 명칭

**v1.2 — Shopify 커머스 연동**

> Shopify Headless 커머스 연동 완료. Storefront API 기반 Cart → Checkout 파이프라인 구현. 에디터-체크아웃 리다이렉트 동선 확립.

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
| 히어로 영상 v6 | Option A (안정 보정 6 Shot) | Option B (후크 재설계 5 Shot) |

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

---

## 12. 히어로 배경 영상 교체 (2026-04-25 세션)

### 12.1 작업 요약

| 항목 | 내용 |
|---|---|
| 목적 | 히어로 섹션 배경 영상을 신규 자산으로 교체 |
| 커밋 | `b50b490` feat(hero): 히어로 배경 영상 신규 자산으로 교체 |
| 변경 규모 | 4 files, +113 / -5 |
| 배포 경로 | 로컬 `main` → GitHub push → Cloudflare Pages 자동 빌드 |

### 12.2 변경 사항 (AS-IS → TO-BE)

| 구분 | AS-IS | TO-BE |
|---|---|---|
| 영상 파일 | `hero-bg.webm` + `hero-bg.mp4` 듀얼 소스 | `hero-bg.mp4` 단일 소스 (2.6MB 신규) |
| `<video>` 태그 | webm 우선 + mp4 fallback | mp4 단일 + `preload="auto"` 추가 |
| 리스크 | 일부 브라우저가 webm(구영상) 우선 재생 | 단일 자산으로 잔존 리스크 차단 |

### 12.3 수정 파일

```
index.html                       # <video> 태그 정리 (60~67행)
assets/videos/hero-bg.mp4        # 신규 영상으로 덮어쓰기
assets/videos/hero-bg.webm       # 삭제
```

### 12.4 변경 후 `<video>` 마크업

```html
<video autoplay loop muted playsinline preload="auto" class="hero__video">
    <source src="assets/videos/hero-bg.mp4" type="video/mp4">
</video>
```

### 12.5 로컬 검증 환경

- 명령: `python3 -m http.server 5500`
- 접속: `http://localhost:5500`
- 캐시 우회: 강력 새로고침 (`⌘+Shift+R`) 권장

### 12.6 잔여 검증 / 후속 검토 항목

| 우선순위 | 항목 | 비고 |
|---|---|---|
| High | 신규 영상이 BX 톤("정제된 빈티지 필름 슬라이드")과 정합되는지 시각 검토 | 톤 충돌 시 `hero__overlay` 강도 / `mix-blend-mode` 조정 |
| Med | 모바일 LCP 영향 측정 (Cloudflare Web Analytics) | 2.6MB → 첫 화면 로드 영향 모니터링 |
| Low | webm 추가 인코딩으로 30~40% 용량 절감 검토 | 성능 우선 시 재도입 (단, 듀얼 소스 잔존 리스크 재확인 필요) |

### 12.7 부수 발견 사항 (조치 대기)

- `git config user.name/email` 미설정 상태로 호스트 자동 추론값(`jinwonchoi@jinwonui-MacBookPro-2.local`) 커밋 중
- 영향: 협업 합류 시 작성자 식별 불가, GitHub contribution 그래프 미반영
- 권장 조치: `git config --global user.name/user.email` 명시 설정 (GitHub 계정 일치)

---

## 13. 커머스 연동 & 개발 환경 분리 (2026-05-02~03 세션)

> 최종 업데이트: 2026-05-03

### 13.1 전략 의사결정 요약

| 항목 | 결정 |
|---|---|
| 커머스 백엔드 | Shopify (Headless) 채택 — 글로벌 확장 + 결제 인프라 |
| 1차 타겟 시장 | 일본 |
| 결제 방식 | Shopify 기본 체크아웃 (1차) |
| 소셜 로그인 | Google + Apple (양쪽 모두 완성 후 오픈) |
| 로그인/회원가입/체크아웃 UI | Headless 자체 구현 (Shopify 기본 UI 미사용) |
| 사용자 동선 | Landing → Editor → Save → (Login) → Cart → Checkout |

### 13.2 에디터 연동

| 항목 | 내용 |
|---|---|
| 에디터 URL | `https://www.donutframe.com/12cut_editor/index.html` |
| 스택 | HTML + Vanilla JS + Fabric.js (Vue.js 일부) |
| 연동 방식 | URL 파라미터로 plan/lang/login_url/join_url/cart_url/flow_mode/return_url 전달 |

**수정 파일**:
- `index.html` — CTA 링크를 에디터 URL로 변경, `js-editor-link` / `js-checkout-link` 클래스 및 `data-plan` 속성 추가
- `script.js` — `buildEditorLink(plan)` 함수 추가, `syncCommerceLinks()` 함수로 모든 CTA를 에디터 우선 동선으로 통일

### 13.3 상품 구조 (Shopify 등록 예정)

| Plan | 설명 | 가격 |
|---|---|---|
| single | 1개 | 70,000원 |
| same2 | 같은 사진 2개 | 100,000원 |
| mix2 | 다른 사진 2개 | 100,000원 |

### 13.4 인프라 — 개발 환경 분리

#### 배포 환경

| 환경 | URL | 용도 | GitHub 리포 |
|---|---|---|---|
| Production | `https://12cut.pages.dev` | 외부 공유용 (외부 개발자 전달 등) | `dobuddyinc-lab/12cut` (main) |
| Development | `https://12cut-dev.pages.dev` | 내부 개발/테스트용 | `dobuddyinc-lab/12cut-dev` (dev) |

#### Git 리모트 구성

| 리모트명 | URL | 브랜치 | 용도 |
|---|---|---|---|
| `public` | `github.com/dobuddyinc-lab/12cut` | main | Production 배포 |
| `devrepo` | `github.com/dobuddyinc-lab/12cut-dev` | dev | Development 배포 |

#### Cloudflare Pages 프로젝트

| 프로젝트 | 유형 | 배포 방식 |
|---|---|---|
| `12cut` | GitHub 연동 (자동) | `main` push → 자동 배포 |
| `12cut-dev` | Direct Upload | `wrangler pages deploy` 수동 배포 |

### 13.5 개발 환경 배포 명령

```bash
cd /Users/jinwonchoi/Desktop/project/12cut
CLOUDFLARE_API_TOKEN='<REDACTED>' \
npx wrangler@latest pages deploy . --project-name 12cut-dev --branch dev --commit-dirty=true
```

### 13.6 세션 중 발생한 이슈 & 해결

| # | 증상 | 원인 | 해결 |
|---|---|---|---|
| 1 | GitHub PAT로 push 시 `workflow scope` 에러 | `.github/workflows/` 파일 포함 push에는 `workflow` scope 필요 | workflow 파일 제거 후 push |
| 2 | Cloudflare Pages 대시보드에서 Git 연동 실패 (HTTP 500) | 방금 삭제한 프로젝트명 재사용 시 내부 충돌 | 다른 이름으로 생성 |
| 3 | `Clone a public repository via Git URL` 실패 | `12cut-dev` 리포가 private | API로 public 전환 |
| 4 | Cloudflare Pages 빌드 실패 | `main` 브랜치 빌드 시도했으나 코드는 `dev` 브랜치에만 존재 | `dev` → `main` 으로도 push |
| 5 | 대시보드에서 프로젝트 삭제 불가 | UI 제한 | Cloudflare API로 삭제 |

### 13.7 파일 구조 변경

```
12cut/
├── wrangler.toml              # Cloudflare Pages 설정 (신규)
├── .gitignore                 # .wrangler/ 추가
└── (기존 파일 동일)
```

### 13.8 Shopify Storefront API 연동 (2026-05-03 완료)

#### 스토어 정보

| 항목 | 값 |
|---|---|
| 스토어 도메인 | `12cut-2.myshopify.com` |
| 계정 | `smiletube9@gmail.com` (choijw) |
| 플랜 | 유료 |
| Headless 채널 | 설치 완료 |
| 공개 Storefront API 토큰 | `1fbcf067bf726bfac94a51637c195326` |
| 비공개 Storefront API 토큰 | `<REDACTED>` |

#### 등록 상품 3종

| Plan | 상품명 | 가격 | Variant ID |
|---|---|---|---|
| single | 12컷 1개 | 70,000원 | `44139069407268` |
| same2 | 12컷 2개 (같은 사진) | 100,000원 | `44139071471652` |
| mix2 | 12컷 2개 (다른 사진) | 140,000원 | `44139073765412` |

#### 연동 구현 내역

| 구성요소 | 파일 | 내용 |
|---|---|---|
| Shopify 설정 | `script.js` | `SHOPIFY_STORE`, `SHOPIFY_STOREFRONT_TOKEN`, `SHOPIFY_VARIANTS` 상수 |
| API 호출 | `script.js` | `shopifyFetch()` — Storefront GraphQL 호출 래퍼 |
| 카트 생성 | `script.js` | `createShopifyCheckout(plan)` — CartCreate mutation → checkoutUrl 반환 |
| 체크아웃 핸들러 | `script.js` | `handleCheckoutRedirect()` — `?action=checkout&plan=single` URL 감지 시 Shopify 체크아웃으로 리다이렉트 |
| CTA 링크 | `script.js` | `buildEditorLink()` — 에디터 URL에 `cart_url`로 체크아웃 리턴 URL 주입 |

#### 사용자 동선

```
Landing CTA 클릭
  → 에디터 (donutframe.com) — plan/lang/cart_url 파라미터 포함
    → 에디터 완료 → cart_url로 리다이렉트
      → Landing (?action=checkout&plan=single)
        → Shopify Cart API → checkoutUrl 생성
          → Shopify 체크아웃 페이지로 리다이렉트
```

### 13.9 향후 작업 (커머스)

| 우선순위 | 항목 | 상태 |
|---|---|---|
| ~~High~~ | ~~Shopify 가입 및 스토어 생성~~ | ✅ 완료 |
| ~~High~~ | ~~Shopify에 상품 3종 등록~~ | ✅ 완료 |
| ~~High~~ | ~~Storefront API 연동 (Cart → Checkout)~~ | ✅ 완료 |
| High | 로그인/회원가입 페이지 자체 구현 (Google/Apple 소셜 로그인) | 미완 |
| High | 체크아웃 페이지 자체 구현 (Shopify Storefront API 연동) | 미완 |
| Med | 에디터 자체 호스팅 (현재 donutframe.com) | 미완 |
| Low | 개발 환경 자동배포 (GitHub Actions 또는 Cloudflare Git 연동) | 보류 |

---

## 14. 미진행 / 향후 과제 (2026-05-03 기준)

> 코드베이스 전수 조사 결과 기반. 아래 4건은 모두 코드 미구현 상태.

### 14.1 커스텀 도메인 연결 + SNS OAuth 활성화

| 항목 | 현재 상태 | 비고 |
|---|---|---|
| 커스텀 도메인 | 미연결 | Production: `12cut.pages.dev` / Dev: `12cut-dev.pages.dev` |
| Google OAuth | 미구현 | Google Cloud Console → OAuth 2.0 클라이언트 생성 필요 |
| Apple OAuth | 미구현 | Apple Developer → Services ID 생성 필요 |
| Shopify Customer Account API | 미전환 | 현재 Storefront API의 Cart→Checkout만 구현 |

**선행 의존관계**:
1. 커스텀 도메인 연결 (OAuth redirect URI 등록 시 `pages.dev` 도메인은 심사 통과 어려움)
2. Shopify Customer Account API 전환 (`customerAccessTokenCreate`, `customerCreate` mutation 추가)
3. OAuth 프로바이더 연동 (Social Login → Shopify Multipass 또는 Customer Account API 신규 흐름)

**전환 경로**: 기존 `shopifyFetch()` 래퍼 위에 Customer Access Token 레이어 추가 필요
- `customerCreate` — 회원가입
- `customerAccessTokenCreate` — 이메일/비밀번호 로그인
- Social Login → accessToken 교환

### 14.2 마이페이지 구현

| 항목 | 현재 상태 | 비고 |
|---|---|---|
| getCustomer query | ✅ 구현 완료 | `12cut-app/src/lib/shopify.ts` |
| 프로필 UI | ✅ 구현 완료 | `12cut-app/src/app/mypage/page.tsx` |
| 주문내역 조회 | ✅ 구현 완료 | `customer.orders` (최근 10건, 날짜 역순) |
| BottomNav 연결 | ✅ 구현 완료 | 로그인 시 my → `/mypage`, 비로그인 시 → `/login` |

### 14.3 비밀번호 찾기 기능

| 항목 | 현재 상태 | 비고 |
|---|---|---|
| `customerRecover` mutation | ✅ 구현 완료 | `12cut-app/src/lib/shopify.ts` |
| 비밀번호 재설정 UI | ✅ 구현 완료 | `12cut-app/src/app/forgot-password/page.tsx` |
| 로그인 페이지 연결 | ✅ 구현 완료 | "비밀번호 찾기" → `/forgot-password` 링크 |
| 흐름 | — | 이메일 입력 → Shopify 재설정 메일 발송 → 성공 확인 화면

### 14.4 최신 배포 반영

| 항목 | 현재 상태 | 비고 |
|---|---|---|
| Production (`public/main`) | ✅ 배포 완료 (`f85d3ea`) | Cloudflare Pages 자동 배포 |
| Development (`devrepo/dev`) | ✅ 배포 완료 (`60ecd28`) | `dev`가 `main`보다 2커밋 ahead (wrangler 설정 + 에디터 동선 — 개발 환경 전용) |
| stash | 1건 (`stash@{0}`: 에디터 동선 파라미터) | 반영 여부 확인 필요 |

### 14.5 실행 우선순위 (2026-05-03 확정)

| 순서 | 항목 | 소요 예상 | 선행 조건 |
|---|---|---|---|
| ~~1~~ | ~~14.4 최신 배포 반영~~ | — | ✅ 이미 배포 완료 |
| ~~1~~ | ~~14.2 마이페이지~~ | — | ✅ 구현 완료 (`12cut-app/src/app/mypage/`) |
| ~~2~~ | ~~14.3 비밀번호 찾기~~ | — | ✅ 구현 완료 (`12cut-app/src/app/forgot-password/`) |
| 후순위 | 14.1-① 커스텀 도메인 연결 | 5~10분 | 외부 URL 공유 시점에 연결 (현재 기능상 불필요) |
| 후순위 | 14.1-② SNS OAuth (Google/Apple) | 1~2일 | 커스텀 도메인 완료 후, 사업 우선순위 재검토 시 착수 |
| **대기** | **14.9 주문-썸네일 연결** | 미정 | 에디터 개발자 확인 후 착수 (아래 참조) |

### 14.9 주문-썸네일 연결 (에디터 확인 대기)

> 고객이 에디터에서 편집한 12컷 사진을 Shopify 주문에 첨부하여, 관리자가 Admin에서 다운로드할 수 있도록 하는 기능.

**에디터 개발자에게 확인할 질문**:

| # | 질문 |
|---|---|
| Q1 | 편집 완료 시 결과물(썸네일 이미지 또는 개별 사진 12장)을 URL이나 파일로 내보내는 API/콜백이 있는지? |
| Q2 | `cart_url` 리다이렉트 시 이미지 데이터를 파라미터(URL 등)로 넘겨줄 수 있는지? |
| Q3 | 편집 결과물이 에디터 서버에 저장되는지, 클라이언트(브라우저)에만 존재하는지? |

**답변 수령 후 구현 방향**:
- 에디터가 썸네일 URL을 넘겨줄 수 있으면 → Shopify 카트 `customAttributes`에 URL 첨부 → Admin 주문에서 확인/다운로드
- URL 전달 불가 시 → Cloudflare R2 등 저장소에 직접 업로드하는 중간 레이어 필요

### 14.7 12cut-app 프로젝트 현황 (Next.js 앱)

> 별도 프로젝트: `~/Desktop/project/12cut-app/`
> 배포: Cloudflare Pages (정적 export)

| 항목 | 값 |
|---|---|
| 스택 | Next.js 16 (App Router) + TailwindCSS + TypeScript |
| 빌드 모드 | `output: "export"` (정적 생성) |
| 인증 | Shopify Storefront API Customer 관련 mutation/query |
| 세션 | localStorage 기반 (`lib/auth.ts`) |
| Shopify API | `lib/shopify.ts` (공개/비공개 토큰 분리) |

#### 페이지 라우트

| 경로 | 기능 | 상태 |
|---|---|---|
| `/` | 랜딩으로 리다이렉트 | ✅ |
| `/login` | 이메일/비밀번호 로그인 + SNS 버튼 (토스트) | ✅ |
| `/signup` | 가입 방법 선택 (카카오/네이버/12cut ID) | ✅ |
| `/signup/terms` | 약관 동의 | ✅ |
| `/signup/form` | 회원가입 폼 (이메일/비밀번호/이름/전화번호) | ✅ |
| `/forgot-password` | 비밀번호 찾기 (이메일 → 재설정 메일 발송) | ✅ |
| `/mypage` | 프로필 + 주문내역 (최근 10건) + 로그아웃 | ✅ |
| `/cart` | 장바구니 (plan별 상품 선택 → Shopify 체크아웃) | ✅ |
| `/checkout` | 주문/결제 UI (배송지/결제수단) | ✅ |

#### 파일 구조

```
12cut-app/
├── src/
│   ├── app/
│   │   ├── page.tsx              # 랜딩 리다이렉트
│   │   ├── layout.tsx            # RootLayout (Nunito 폰트)
│   │   ├── globals.css           # TailwindCSS
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   ├── signup/terms/page.tsx
│   │   ├── signup/form/page.tsx
│   │   ├── forgot-password/page.tsx
│   │   ├── mypage/page.tsx
│   │   ├── cart/page.tsx
│   │   └── checkout/page.tsx
│   ├── components/
│   │   ├── Header.tsx            # 뒤로가기 + 타이틀
│   │   └── BottomNav.tsx         # category / home / my (로그인 상태별 분기)
│   └── lib/
│       ├── shopify.ts            # Shopify Storefront API 유틸리티
│       └── auth.ts               # localStorage 기반 인증 상태 관리
├── .env.local                    # Shopify 토큰 + Variant ID
├── next.config.ts                # output: "export"
└── package.json
```

### 14.8 보안 주의사항

- `devrepo` 원격 URL에 **PAT가 하드코딩**되어 있음 → 토큰 로테이션 및 credential helper 전환 권장
- Shopify Storefront 토큰이 `script.js`에 하드코딩 (공개 전제 토큰이나, 권한 범위 점검 필요)
- 12cut-app 인증은 현재 **localStorage 기반** — 프로덕션 전환 시 httpOnly cookie 또는 서버 세션으로 고도화 권장
- **Vercel 사용하지 않음** — 모든 배포는 Cloudflare Pages 전용

### 13.10 Cloudflare API 토큰

| 용도 | 토큰 | 비고 |
|---|---|---|
| Pages 배포 | `<REDACTED>` | Account ID: `<REDACTED>` |

### 13.11 GitHub PAT

| 용도 | 토큰 | Scope | 비고 |
|---|---|---|---|
| API + Git push | `<REDACTED>` | repo | workflow scope 없음 |
