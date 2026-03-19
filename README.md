# Onye Clinical Data Reconciliation Engine

A production-ready AI-powered healthcare application for reconciling conflicting medication records and validating clinical data quality using advanced language models and rule-based algorithms.

## 🚀 Features

- **Medication Reconciliation**: AI-driven reconciliation of conflicting medication sources with clinical safety checks
- **Data Quality Validation**: Comprehensive assessment of patient records (completeness, accuracy, timeliness, plausibility)
- **Rate Limiting & Caching**: Built-in rate limit handling with exponential backoff and in-memory caching for cost optimization
- **RESTful API**: FastAPI-based backend with automatic OpenAPI documentation
- **Modern Frontend**: React 19 + TypeScript + Tailwind CSS with sample data loading
- **Docker Ready**: Multi-stage containerization for easy deployment
- **Clinical Rules Engine**: Domain-specific validation for medical data (eGFR adjustments, BP plausibility, etc.)

## 🛠 Tech Stack

### Backend
- **Python 3.12** - Core language
- **FastAPI** - Async web framework
- **Pydantic v2** - Data validation and serialization
- **OpenRouter API** - Unified LLM provider access
- **CacheTools** - In-memory caching with TTL

### Frontend
- **React 19** - UI framework
- **Vite 8** - Build tool and dev server
- **TypeScript** - Type safety
- **Tailwind CSS v3** - Styling
- **Lucide React** - Icons

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **pytest** - Testing framework
- **Git** - Version control

## 📋 Prerequisites

- **Python 3.12+**
- **Node.js 18+** and **npm**
- **Docker & Docker Compose** (for containerized deployment)
- **Git**

## 🏗 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/clinicrecon.git
cd clinicrecon
```
### 2. Full Stack with Docker Compose
```bash
# Build and run both services
docker-compose up --build

# Access the application at http://localhost:5173/
```

## ⚙️ Configuration

Create a `.env` file in the root of the directory:

```env
# LLM Provider API Keys (at least one required)
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### API Key Sources
- **OpenRouter**: Unified access to multiple LLM providers ([openrouter.ai](https://openrouter.ai))

## 🧪 Testing

### Backend Tests
```bash
cd backend
python3 -m pytest tests/ -v --tb=short
```

### Frontend Tests (if implemented)
```bash
cd frontend
npm test
```

## 📖 Usage

### API Endpoints

#### Medication Reconciliation
```bash
curl -X POST "http://localhost:8000/api/reconcile/medication" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "patient_context": {
      "age": 65,
      "conditions": ["diabetes", "hypertension"],
      "recent_labs": {"eGFR": 45.0}
    },
    "sources": [
      {
        "system": "Hospital EMR",
        "medication": "metformin 500mg BID",
        "last_updated": "2024-01-15T10:00:00Z",
        "source_reliability": "high"
      }
    ]
  }'
```

**Response:**
```json
{
  "reconciled_medication": "metformin 500mg twice daily",
  "confidence_score": 0.85,
  "reasoning": "eGFR of 45 indicates renal impairment, so reduced metformin dose is appropriate...",
  "recommended_actions": ["Monitor renal function", "Check for lactic acidosis risk"],
  "clinical_safety_check": "PASSED"
}
```

#### Data Quality Validation
```bash
curl -X POST "http://localhost:8000/api/validate/data-quality" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "demographics": {"age": 68, "gender": "female"},
    "medications": ["metformin 500mg BID", "lisinopril 10mg daily"],
    "allergies": ["penicillin"],
    "conditions": ["type 2 diabetes", "hypertension"],
    "vital_signs": {"systolic_bp": 140, "diastolic_bp": 85},
    "last_updated": "2024-01-15T10:00:00Z"
  }'
```

**Response:**
```json
{
  "overall_score": 85,
  "breakdown": {
    "completeness": 90,
    "accuracy": 80,
    "timeliness": 85,
    "clinical_plausibility": 90
  },
  "issues_detected": [
    {
      "field": "medications",
      "issue": "Missing dosage frequency for lisinopril",
      "severity": "medium"
    }
  ]
}
```

### Frontend Usage
1. Open http://localhost:5173 (Vite dev server)
2. Use the tabs to switch between Medication Reconciliation and Data Quality
3. Click "Load Sample" to populate test data
4. Click "Reconcile with AI" or "Validate Quality" to process
5. View results in the unified response display

## 🏛 Architecture & Design Decisions

### Backend Architecture
```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, router includes
│   ├── core/config.py       # Settings management (Pydantic)
│   ├── models/patient.py    # Request/Response schemas
│   ├── api/v1/handler.py    # API endpoints with auth
│   ├── services/            # Business logic layer
│   │   ├── reconciliation.py # Medication reconciliation
│   │   └── data_quality.py   # Quality validation
│   ├── llm/                 # AI integration
│   │   ├── client.py        # Multi-provider LLM client
│   │   └── prompts.py       # System/user prompts
│   └── utils/clinical_rules.py # Domain-specific rules
├── fixtures/                # Test data
└── tests/                   # Unit tests
```

### Key Design Decisions

#### 1. **Hybrid AI + Rules Approach**
- **Why**: Pure LLM can hallucinate medical data; rules provide safety guardrails
- **Implementation**: Rule-based pre-processing + LLM reasoning + clinical validation

#### 2. **Async-First Architecture**
- **Why**: I/O-bound LLM calls benefit from concurrency
- **Implementation**: FastAPI async endpoints, asyncio locks for thread safety

#### 3. **In-Memory Caching**
- **Why**: Reduce API costs for identical prompts
- **Implementation**: SHA256 hash keys, 24-hour TTL, async-safe

#### 4. **Pydantic v2 for Validation**
- **Why**: Strict type checking prevents runtime errors
- **Implementation**: Request/response models with field validation

## 🔮 Future Improvements

### High Priority
- **Confidence Score Calibration**: Multi-factor weighting (LLM confidence × source agreement × recency × clinical plausibility)
- **Duplicate Record Detection**: Levenshtein distance algorithm for identifying similar medication entries
- **Prompt Improvement**: Prompts especially System one can be improved with few shots example, edge cases and more detail instructions
- **Webhook Support**: Real-time notifications for reconciliation results
- **Database Integration**: PostgreSQL for audit trails and result caching
- **Batch Processing**: Handle multiple patients in single API call

### Medium Priority
- **Advanced Clinical Rules**: Drug interaction checking, allergy cross-referencing
- **Audit Logging**: Comprehensive request/response logging for compliance
- **Rate Limiting**: Per-client limits with Redis
- **Metrics & Monitoring**: Prometheus metrics, health checks
- **API Versioning**: v2 endpoints with breaking changes

### Low Priority
- **GraphQL API**: Flexible querying for complex reconciliation scenarios
- **Real-time WebSocket**: Live updates during long-running reconciliations
- **Multi-language Support**: Internationalization for global healthcare
- **Mobile App**: React Native companion app
- **Integration APIs**: HL7 FHIR, Epic, Cerner connectors

### Technical Debt
- **Integration Tests**: End-to-end testing with LLM mocking
- **Performance Optimization**: Async batch processing, connection pooling
- **Security Audit**: Penetration testing, dependency vulnerability scanning
- **Documentation**: API reference, video tutorials

## ⚠️ Disclaimer

**This software is for research and development purposes only. It is not intended for clinical use without proper validation, regulatory approval, and medical supervision.**

### Important Warnings
- **Not FDA Approved**: This is not a medical device and has not been evaluated by the FDA
- **No Medical Advice**: Outputs should not be used as substitute for professional medical judgment
- **Data Privacy**: Ensure compliance with HIPAA, GDPR, and local privacy regulations
- **Accuracy Limitations**: AI models can hallucinate; always verify critical medical decisions
- **No Warranty**: Provided "as-is" without warranty of any kind

### Clinical Validation Required
Before clinical deployment:
- Conduct thorough validation studies
- Compare against gold-standard reconciliation methods
- Implement human oversight workflows
- Obtain necessary regulatory approvals
- Perform risk assessments for patient safety

### Liability
The authors and contributors are not liable for any damages, injuries, or adverse outcomes resulting from the use of this software in clinical settings.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript strict mode
- Write tests for new features
- Update documentation
- Ensure clinical accuracy of medical logic

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenRouter for unified LLM API access
- FastAPI community for excellent documentation
- Healthcare providers for domain expertise validation

---

**Built with ❤️ and AI for safer healthcare through AI**