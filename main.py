from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import logging
from config import config
from models import ConceptAnalysisRequest, ConceptAnalysisResponse, ErrorResponse
from services.concept_analyzer import concept_analyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Concept Mindmap API",
    description="AI-powered concept analysis and mindmap generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        config.validate_config()
        logger.info("✅ Configuration validated successfully")
        logger.info(f"🚀 Server starting on {config.HOST}:{config.PORT}")
        if config.LANGCHAIN_TRACING_V2:
            logger.info(f"📊 LangSmith tracing enabled - Project: {config.LANGCHAIN_PROJECT}")
    except Exception as e:
        logger.error(f"❌ Configuration error: {e}")
        raise e

@app.get("/")
async def root():
    return FileResponse("ICE.html")

@app.get("/default")
async def root():
    """Health check endpoint"""
    return {
        "message": "Concept Mindmap API is running!",
        "version": "1.0.0",
        "langsmith_enabled": config.LANGCHAIN_TRACING_V2
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "openai_configured": bool(config.OPENAI_API_KEY),
        "langsmith_enabled": config.LANGCHAIN_TRACING_V2,
        "model": config.OPENAI_MODEL
    }

@app.post("/analyze", response_model=ConceptAnalysisResponse)
async def analyze_concepts(request: ConceptAnalysisRequest):
    """
    Analyze 2-5 concepts and return their relationships.

    This endpoint uses OpenAI to analyze the conceptual relationships between
    multiple given concepts, returning shared concepts and unique concepts for each.
    """
    try:
        concepts_str = ", ".join(f"'{c}'" for c in request.concepts)
        logger.info(f"🔍 Analyzing {len(request.concepts)} concepts: {concepts_str}")

        # Perform analysis
        result = await concept_analyzer.analyze_concepts(request.concepts)

        logger.info(f"✅ Analysis completed for {len(request.concepts)} concepts")
        if result.analysis_id:
            logger.info(f"📊 LangSmith trace ID: {result.analysis_id}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=f"Request path: {request.url.path}"
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"❌ Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if config.DEBUG else "An unexpected error occurred"
        ).model_dump()
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )