# HR Resource Query Chatbot

## Overview
An AI-powered HR assistant that helps find the right employees for specific projects and requirements. Built with a RAG (Retrieval-Augmented Generation) system that combines semantic search with natural language generation to provide intelligent, context-aware recommendations.

## Features
✅ **Natural Language Queries**: Ask questions like "Find Python developers with ML experience"  
✅ **RAG System**: Combines retrieval, augmentation, and generation for intelligent responses  
✅ **Semantic Search**: Uses sentence transformers for meaning-based employee matching  
✅ **RESTful API**: FastAPI backend with automatic documentation  
✅ **Interactive Frontend**: Streamlit-powered chat interface with multiple views  
✅ **Comprehensive Employee Database**: 16 employees with realistic profiles  
✅ **Multiple Search Methods**: Both AI-powered and traditional filtering  
✅ **Real-time Responses**: Fast query processing and result generation  
✅ **Fallback System**: Works even without OpenAI API key

## Architecture

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │◄──►│   FastAPI       │◄──►│   RAG System    │
│   Frontend      │    │   Backend       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                               ┌─────────────────┐
                                               │  OpenAI GPT     │
                                               │  +              │
                                               │  Embeddings     │
                                               └─────────────────┘
```

### RAG Pipeline
1. **Retrieval**: Convert queries to embeddings, find similar employee profiles
2. **Augmentation**: Combine retrieved employee data with query context  
3. **Generation**: Use OpenAI GPT to create natural language recommendations

## Setup & Installation

### Prerequisites
- Python 3.8+ (tested on Python 3.9+)
- OpenAI API key (optional, system has fallback)

### Installation Steps

1. **Clone/Download the project**
```bash
# If using git
git clone <your-repo-url>
cd hr-chatbot

# Or create directory manually and copy files
mkdir hr-chatbot
cd hr-chatbot
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables (optional)**
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# To get an API key:
# 1. Visit https://platform.openai.com/api-keys
# 2. Sign up/Login
# 3. Create new API key
# 4. Replace 'your_openai_api_key_here' with your actual key
```

5. **Run the application**

**Terminal 1 - Start FastAPI backend:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Streamlit frontend:**
```bash
streamlit run frontend/streamlit_app.py --server.port 8501
```

6. **Access the application**
- **Frontend**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## API Documentation

### Core Endpoints

#### POST /chat
Process natural language queries using RAG system.

**Request:**
```json
{
  "query": "Find Python developers with 3+ years experience"
}
```

**Response:**
```json
{
  "response": "Based on your requirements, I found 3 excellent Python developers...",
  "relevant_employees": [...],
  "confidence_score": 0.85
}
```

#### GET /employees
Get all employees in the database.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "skills": ["Python", "React", "AWS"],
    "experience_years": 5,
    "projects": ["E-commerce Platform"],
    "availability": "available",
    "department": "Engineering"
  }
]
```

#### GET /employees/search
Search with basic filters.

**Parameters:**
- `skills`: Comma-separated skills (e.g., "Python,React")
- `min_experience`: Minimum years of experience
- `availability`: "available" or "busy"
- `department`: Department name

**Example:**
```
GET /employees/search?skills=Python,ML&min_experience=3&availability=available
```

#### GET /health
Health check endpoint showing system status.

**Response:**
```json
{
  "status": "healthy",
  "employees_loaded": 16
}
```

## AI Development Process

### AI Tools Used in Development

**Primary AI Assistants:**
- **Claude (Anthropic)**: 85% - Architecture design, code generation, documentation
- **VS Code IntelliCode**: 10% - Code completion and suggestions
- **Manual Development**: 5% - Custom business logic and fine-tuning

### Development Phases & AI Assistance

#### 1. Architecture Planning (90% AI-assisted)
- **AI Help**: System design, technology stack selection, RAG pipeline design
- **AI Generated**: Component structure, data flow diagrams
- **Manual Work**: Final architecture decisions, specific implementation choices

#### 2. Backend Development (80% AI-assisted)
- **AI Generated**: FastAPI boilerplate, Pydantic models, CRUD operations
- **AI Optimized**: RAG system implementation, embeddings integration
- **Manual Refinement**: Error handling, performance optimization, custom business logic

#### 3. RAG System Implementation (75% AI-assisted)
- **AI Help**: Sentence transformers integration, similarity search logic
- **AI Generated**: OpenAI integration, prompt engineering, fallback mechanisms
- **Manual Work**: Fine-tuning similarity thresholds, performance optimization

#### 4. Frontend Development (85% AI-assisted)
- **AI Generated**: Streamlit interface, component structure, CSS styling
- **AI Help**: User experience flow, interactive elements, responsive design
- **Manual Refinement**: UI polish, error handling, user feedback

#### 5. Data Creation (60% AI-assisted)
- **AI Generated**: Employee profiles, realistic project names, skill combinations
- **Manual Curation**: Data validation, ensuring diversity, realistic constraints

### Code Distribution
- **AI-Generated**: ~75% (with human review and modification)
- **AI-Assisted**: ~15% (human-written with AI suggestions)
- **Hand-Written**: ~10% (specific business logic, custom integrations)

### Interesting AI-Generated Solutions
1. **Smart Employee Text Representation**: AI suggested combining all employee attributes into searchable text blocks for better semantic matching
2. **Confidence Score Calculation**: Using cosine similarity scores as confidence metrics for recommendations
3. **Fallback Response System**: Template-based responses when OpenAI API fails or is unavailable
4. **Dynamic Prompt Engineering**: Context-aware prompt construction for better LLM responses
5. **Multi-tab Interface Design**: AI suggested tabbed interface for better user experience

### Challenges Where AI Couldn't Help
1. **API Rate Limiting**: Had to manually implement proper error handling for OpenAI API limits
2. **Streamlit State Management**: Required manual debugging of session state issues and rerun logic
3. **Performance Optimization**: Manual tuning of embedding model parameters and similarity thresholds
4. **Cross-platform Compatibility**: Manual testing and fixes for Windows/Mac/Linux compatibility
5. **Production Deployment**: Manual configuration for different environments and security considerations

## Technical Decisions

### AI/ML Stack Choices

**Embedding Model: SentenceTransformers ('all-MiniLM-L6-v2')**
- ✅ **Pros**: Fast, lightweight, good balance of quality and speed
- ✅ No GPU required, works well on CPU
- ✅ Small model size (90MB), quick loading
- ❌ **Cons**: Less sophisticated than larger models like OpenAI embeddings
- **Alternative Considered**: OpenAI text-embedding-ada-002 (more accurate but requires API calls)

**LLM: OpenAI GPT-3.5-turbo vs Local Models**
- **Chosen**: OpenAI GPT-3.5-turbo with fallback system
- ✅ **Pros**: High-quality responses, reliable, fast, excellent at following complex prompts
- ✅ Good at maintaining context and providing actionable recommendations
- ❌ **Cons**: Requires API key, costs money (~$0.002 per query), external dependency
- **Alternative Considered**: Local LLM (Ollama + Llama 2)
  - **Would provide**: Privacy, no API costs, offline capability
  - **Rejected because**: Setup complexity, slower responses, lower quality outputs

**Vector Search: Scikit-learn vs FAISS vs Pinecone**
- **Chosen**: Scikit-learn cosine_similarity
- ✅ **Pros**: Simple, reliable, no additional dependencies, perfect for small datasets
- ✅ Excellent performance for <1000 employees
- **Future Consideration**: FAISS for larger datasets (1000+ employees)
- **Enterprise Option**: Pinecone for production scale with real-time updates

### Framework Choices

**Backend: FastAPI vs Flask**
- **Chosen**: FastAPI
- ✅ Automatic API documentation (Swagger/OpenAPI)
- ✅ Built-in async support for better performance
- ✅ Type hints and validation with Pydantic
- ✅ Modern, developer-friendly, great for ML APIs
- **Alternative**: Flask (simpler but less features)

**Frontend: Streamlit vs React vs Gradio**
- **Chosen**: Streamlit
- ✅ **Pros**: Rapid prototyping, perfect for AI/ML applications, built-in chat components
- ✅ No JavaScript knowledge required, great for data scientists
- ❌ **Cons**: Less customizable than React, limited styling options
- **Production Alternative**: React + Next.js for more control and customization

### Performance vs Cost vs Privacy Trade-offs

**Current Setup (Development/Demo)**:
- **Performance**: Good (sub-second responses, <500ms for most queries)
- **Cost**: Low ($0.002 per query with GPT-3.5-turbo, ~$5/month for moderate use)
- **Privacy**: Medium (employee data sent to OpenAI for response generation)

**Production Considerations**:
```
High Performance + Low Cost + High Privacy = Local LLM (Ollama + Mistral)
High Performance + Low Privacy + Medium Cost = OpenAI GPT-4
Medium Performance + High Privacy + Low Cost = Open Source Stack (Transformers + Local)
```

**Scalability Recommendations**:
- **<100 employees**: Current setup is perfect
- **100-1000 employees**: Add FAISS vector database, implement caching
- **1000+ employees**: Consider Pinecone + dedicated embedding service
- **Enterprise**: Local LLM deployment for privacy compliance

## Future Improvements

### Short Term (1-2 weeks)
- 🔐 **Authentication & Authorization**: User management, role-based access control
- 📊 **Analytics Dashboard**: Query patterns, popular searches, usage metrics
- 🔍 **Advanced Filters**: Salary range, remote/onsite preferences, certifications
- 💾 **Database Integration**: PostgreSQL/MongoDB instead of JSON files
- 📱 **Mobile Responsive**: Better mobile UI/UX optimization
- 🚀 **Performance**: Response caching, query optimization

### Medium Term (1-2 months)
- 🤖 **Conversation Memory**: Multi-turn conversations with context preservation
- 🎯 **Personalized Recommendations**: Learning from user preferences and feedback
- 📅 **Calendar Integration**: Real-time availability checking and meeting scheduling
- 🔄 **HR System Integration**: Connect with BambooHR, Workday, ADP
- 🔍 **Advanced Search**: Boolean queries, fuzzy matching, synonym handling
- 📈 **Reporting**: Generate team composition reports, skills gap analysis

### Long Term (3-6 months)
- 🧠 **Advanced AI Features**: 
  - Team composition optimization
  - Skills gap analysis and recommendations
  - Succession planning suggestions
  - Performance prediction models
- 🌐 **Multi-language Support**: Internationalization for global teams
- 🔐 **Enterprise Security**: SSO integration, audit logs, compliance features
- 📊 **Predictive Analytics**: Employee retention analysis, promotion readiness
- 🤝 **Platform Integrations**: Slack bot, Microsoft Teams app, email notifications
- 🎓 **Learning Recommendations**: Suggest training based on skill gaps

## Sample Queries & Expected Responses

### Query Examples

**Simple Skill Search:**
```
Query: "Find Python developers"
Expected: List of developers with Python skills, ranked by experience
```

**Complex Requirements:**
```
Query: "I need someone experienced with machine learning for a healthcare project"
AI Response: "Based on your requirements for ML expertise in healthcare, I found 2 excellent candidates:

**Dr. Sarah Chen** would be perfect for this role. She has 6 years of ML experience and specifically worked on the 'Medical Diagnosis Platform' project where she implemented computer vision for X-ray analysis. Her skills include TensorFlow, PyTorch, and healthcare AI specialization. She's currently available.

**Michael Rodriguez** is another strong candidate with 4 years of ML experience. He built the 'Patient Risk Prediction System' and has experience with HIPAA compliance for healthcare data..."
```

**Availability Focused:**
```
Query: "Who is available for a React Native project next week?"
Expected: Available developers with React Native skills, with availability status highlighted
```

## Deployment Options

### Local Development
```bash
# Standard setup as described in installation
python -m uvicorn app.main:app --reload --port 8000
streamlit run frontend/streamlit_app.py
```

### Streamlit Cloud (Recommended for Demo)
1. Push code to GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repo and deploy
4. Add OpenAI API key