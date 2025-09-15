import json
import uuid
from typing import Dict, Any, List
from openai import OpenAI
from langsmith import Client as LangSmithClient
from langsmith.schemas import Run
from config import config
from models import ConceptData, ConceptAnalysisResponse

class ConceptAnalyzer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.langsmith_client = LangSmithClient(
            api_key=config.LANGCHAIN_API_KEY
        ) if config.LANGCHAIN_TRACING_V2 else None

    def create_prompt(self, concepts: List[str]) -> str:
        """Create optimized prompt for single or multi-concept analysis"""
        concepts_str = ", ".join(f'"{c}"' for c in concepts)

        if len(concepts) == 1:
            # Single concept analysis
            return f"""다음 개념을 분석하여 JSON 형태로 응답해주세요: "{concepts[0]}"

단일 개념의 특성, 하위 개념, 관련 기술들을 다음 형식으로 응답하세요:

{{
    "concepts": [
        {{"name": "{concepts[0]}", "unique": ["특성1", "특성2", "특성3", "특성4", "특성5", "..."]}}
    ],
    "shared_concepts": []
}}

중요한 조건:
1. unique 배열: 해당 개념의 핵심 특성, 구성 요소, 관련 기술, 응용 분야 등 (5-12개)
2. shared_concepts: 단일 개념이므로 빈 배열로 설정
3. 실제로 의미있고 중요한 특성들만 포함
4. 모든 용어는 간결하고 이해하기 쉽게 작성
5. 모든 용어는 한국어로 응답하되, 불가능한 경우 영어 사용 가능
6. JSON만 응답하고 다른 설명은 불필요

해당 개념의 핵심적이고 대표적인 특성들을 자연스럽게 분석해주세요."""

        else:
            # Multi-concept analysis
            return f"""다음 {len(concepts)}개 개념들을 분석하여 JSON 형태로 응답해주세요: {concepts_str}

각 개념의 고유한 특성과 공통점을 찾아 다음 형식으로 응답하세요:

{{
    "concepts": [
        {{"name": "{concepts[0]}", "unique": ["고유개념1", "고유개념2", "고유개념3", "고유개념4", "고유개념5", "..."]}},
        {{"name": "{concepts[1]}", "unique": ["고유개념1", "고유개념2", "고유개념3", "고유개념4", "고유개념5", "..."]}}{', ...' if len(concepts) > 2 else ''}
    ],
    "shared_concepts": ["공통개념1", "공통개념2", "공통개념3", "..."]
}}

중요한 조건:
1. unique 배열: 각 개념만의 고유한 특성, 기술, 방법론 등 (5-12개, 실제 관련성에 따라 유동적)
2. shared_concepts: 모든 개념이 공유하는 공통점들 (개수는 실제 공통점 정도에 따라 자연스럽게 결정)
3. 억지로 개수를 맞추지 말고, 실제로 의미있는 개념들만 포함
4. 모든 용어는 간결하고 이해하기 쉽게 작성
5. 모든 용어는 한국어로 응답하되, 불가능한 경우 영어 사용 가능
6. JSON만 응답하고 다른 설명은 불필요

개념 간 관련성이 적다면 shared_concepts가 적을 수 있고, 매우 관련성이 높다면 많을 수 있습니다. 자연스럽게 분석해주세요."""

    async def analyze_concepts(self, concepts: List[str]) -> ConceptAnalysisResponse:
        """Analyze multiple concepts and return structured data"""

        run_id = str(uuid.uuid4()) if self.langsmith_client else None

        try:
            prompt = self.create_prompt(concepts)

            # Start LangSmith run if enabled
            if self.langsmith_client:
                analysis_type = "single_concept" if len(concepts) == 1 else "multi_concept"
                self.langsmith_client.create_run(
                    id=run_id,
                    name=f"{analysis_type}_analysis",
                    run_type="llm",
                    inputs={
                        "concepts": concepts,
                        "concept_count": len(concepts),
                        "analysis_type": analysis_type,
                        "prompt": prompt
                    },
                    project_name=config.LANGCHAIN_PROJECT
                )

            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 개념 분석 전문가입니다. 여러 개념들의 관계를 분석하여 JSON 형태로만 응답하세요. 개수는 실제 관련성에 따라 자연스럽게 결정하고, 억지로 맞추지 마세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2500  # Increased for multiple concepts
            )

            raw_content = response.choices[0].message.content
            parsed_data = self._parse_ai_response(raw_content)

            # Create response object
            analysis_type = "single" if len(concepts) == 1 else "comparison"
            result = ConceptAnalysisResponse(
                concepts=[ConceptData(**concept_data) for concept_data in parsed_data["concepts"]],
                shared_concepts=parsed_data["shared_concepts"],
                analysis_type=analysis_type,
                analysis_id=run_id
            )

            # End LangSmith run with success
            if self.langsmith_client and run_id:
                self.langsmith_client.update_run(
                    run_id,
                    outputs={
                        "result": result.model_dump(),
                        "raw_response": raw_content,
                        "tokens_used": response.usage.total_tokens
                    },
                    end_time=None
                )

            return result

        except Exception as e:
            # End LangSmith run with error
            if self.langsmith_client and run_id:
                self.langsmith_client.update_run(
                    run_id,
                    error=str(e),
                    end_time=None
                )
            raise e

    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response and validate structure"""
        try:
            # Clean the response text
            clean_text = response_text.replace('```json\n', '').replace('\n```', '').replace('```', '').strip()
            parsed = json.loads(clean_text)

            # Validate structure
            if not isinstance(parsed, dict):
                raise ValueError("Response is not a JSON object")

            # Check for required keys
            if "concepts" not in parsed:
                raise ValueError("Missing required key: 'concepts'")

            if "shared_concepts" not in parsed:
                raise ValueError("Missing required key: 'shared_concepts'")

            # Validate concepts array
            concepts = parsed["concepts"]
            if not isinstance(concepts, list) or len(concepts) < 1:
                raise ValueError("'concepts' must be a list with at least 1 item")

            # Validate each concept
            for i, concept_data in enumerate(concepts):
                if not isinstance(concept_data, dict):
                    raise ValueError(f"Concept {i+1} is not a valid object")

                if not all(k in concept_data for k in ["name", "unique"]):
                    raise ValueError(f"Concept {i+1} missing required fields: 'name', 'unique'")

                if not isinstance(concept_data["unique"], list):
                    raise ValueError(f"Concept {i+1}: 'unique' must be a list")

                if len(concept_data["unique"]) < 5 or len(concept_data["unique"]) > 12:
                    raise ValueError(f"Concept {i+1}: 'unique' must have 5-12 items, got {len(concept_data['unique'])}")

            # Validate shared_concepts
            if not isinstance(parsed["shared_concepts"], list):
                raise ValueError("'shared_concepts' must be a list")

            return parsed

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Response parsing error: {str(e)}")

# Global instance
concept_analyzer = ConceptAnalyzer()