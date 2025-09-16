# AI-Powered Concept Mindmap 🧠

AI를 활용한 개념 비교 시각화 도구입니다. 두 개념을 입력하면 AI가 분석하여 공통점과 차이점을 인터랙티브 그래프로 보여줍니다.

## 🌟 주요 기능

- **AI 개념 분석**: OpenAI API를 사용한 지능형 개념 관계 분석
- **인터랙티브 시각화**: Cytoscape.js를 활용한 동적 네트워크 그래프
- **다양한 레이아웃**: Force, Circle, Concentric, Hierarchical 레이아웃 지원
- **LangSmith 연동**: 프롬프트 실험 및 추적 기능
- **데이터 내보내기**: Mermaid, PNG, JSON 형태로 결과 내보내기

## 🏗️ 시스템 구조

```
MS-AI-edu/
├── main.py                  # FastAPI 메인 서버
├── config.py                # 환경설정 관리
├── models.py                # Pydantic 데이터 모델
├── services/                # 비즈니스 로직
│   └── concept_analyzer.py  # AI 개념 분석 서비스
├── requirements.txt         # Python 의존성
├── .env.example             # 환경변수 예제
└── static/                  # 프론트엔드 (HTML + JavaScript)
    └── ICE.html             # Interactive Concept Explorer : ICE 랜딩페이지 
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 백엔드 의존성 설치
cd backend
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 편집하여 API 키들을 설정하세요
```

### 2. 환경변수 설정 (.env)

```bash
# OpenAI API 설정
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1

# LangSmith 설정 (선택사항)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=concept-mindmap

# 서버 설정(local test)
HOST=localhost
PORT=8000
DEBUG=true
```

### 3. 서버 실행

```bash
# 백엔드 서버 시작
uvicorn main:app --reload
```

서버가 실행되면 `http://localhost:8000`에서 API가 제공됩니다.

### 4. 프론트엔드 접근

`docs/index.html` 파일을 브라우저에서 열어서 사용할 수 있습니다.

## 📡 API 엔드포인트

### POST `/analyze`

두 개념을 분석하여 관계를 반환합니다.

**요청:**
```json
{
  "concept1": "머신러닝",
  "concept2": "딥러닝"
}
```

**응답:**
```json
{
  "concept1": {
    "name": "머신러닝",
    "shared": ["데이터", "알고리즘", "예측", "모델", "훈련", "평가", "AI"],
    "unique": ["회귀분석", "분류", "클러스터링", "의사결정트리", "SVM", "랜덤포레스트", "앙상블", "피처엔지니어링"]
  },
  "concept2": {
    "name": "딥러닝",
    "shared": ["데이터", "알고리즘", "예측", "모델", "훈련", "평가", "AI"],
    "unique": ["신경망", "역전파", "CNN", "RNN", "LSTM", "Transformer", "GPU", "텐서플로우"]
  },
  "analysis_id": "uuid-for-langsmith-tracing"
}
```

### GET `/health`

시스템 상태를 확인합니다.

## 🔧 기술 스택

### 백엔드
- **FastAPI**: 고성능 Python 웹 프레임워크
- **OpenAI API**: GPT 모델을 사용한 개념 분석
- **LangSmith**: 프롬프트 실험 및 추적
- **Pydantic**: 데이터 검증 및 직렬화

### 프론트엔드
- **Cytoscape.js**: 네트워크 시각화
- **Vanilla JavaScript**: 경량화된 클라이언트
- **CSS3**: 모던 UI 디자인

## 🔍 LangSmith 연동

LangSmith를 활용하여 프롬프트 실험과 성능 추적이 가능합니다:

1. LangSmith 계정에서 API 키 발급
2. `.env` 파일에 LangSmith 설정 추가
3. 각 API 호출마다 trace ID가 생성되어 LangSmith에서 확인 가능

### LangSmith에서 확인할 수 있는 정보:
- 입력 개념들과 생성된 프롬프트
- OpenAI API 응답 시간 및 토큰 사용량
- 파싱 오류 및 예외사항
- 프롬프트 최적화를 위한 A/B 테스트

## 🎨 사용 방법

1. 브라우저에서 `docs/index.html` 열기
2. 두 개념을 입력 필드에 입력
3. "🤖 AI로 개념 분석하기" 버튼 클릭
4. AI가 분석한 결과를 인터랙티브 그래프로 확인
5. 레이아웃 변경, 데이터 내보내기 등 추가 기능 활용

## 📊 시각화 요소

- **빨간색 노드**: 첫 번째 개념
- **파란색 노드**: 두 번째 개념
- **녹색 노드**: 공통 개념
- **노란색 노드**: 첫 번째 개념의 고유 요소
- **핑크색 노드**: 두 번째 개념의 고유 요소

## 🚨 문제 해결

### 백엔드 연결 오류
- 백엔드 서버가 실행 중인지 확인 (`python main.py`)
- 포트 8000이 사용 가능한지 확인
- CORS 설정 확인

### API 키 오류
- OpenAI API 키가 올바른지 확인
- 계정에 충분한 크레딧이 있는지 확인
- API 키 권한 설정 확인

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🔗 관련 링크

- [OpenAI API 문서](https://platform.openai.com/docs)
- [LangSmith 문서](https://docs.smith.langchain.com)
- [Cytoscape.js 문서](https://js.cytoscape.org)
- [FastAPI 문서](https://fastapi.tiangolo.com)