# Kasparro — Agentic Facebook Performance Analyst

An autonomous multi-agent system that diagnoses Facebook Ads performance issues, identifies drivers behind ROAS fluctuations, and recommends creative improvements using both quantitative signals and creative messaging data.

## Quick Start
```bash
python -V  # should be >= 3.10
python -m venv .venv && source .venv/bin/activate  # win: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
python run.py "Analyze ROAS drop in last 7 days"
```

## Data
- Place the full CSV locally and set path in `config/config.yaml`
- Or use the included sample: `data/sample_fb_ads.csv`
- See `data/README.md` for details

## Config
Edit `config/config.yaml`:
```yaml
python: "3.10"
random_seed: 42
llm:
  model: "gpt-4o"
  temperature: 0.3
  max_tokens: 2500
thresholds:
  confidence_min: 0.6
data:
  use_sample_data: false
```

## Repo Map
- `src/agents/` — planner.py, data_agent.py, insight_agent.py, evaluator.py, creative_generator.py
- `prompts/` — *.md prompt files with variable placeholders
- `reports/` — report.md, insights.json, creatives.json
- `logs/` — json traces
- `tests/` — test_evaluator.py

## Run
```bash
make run  # or: python run.py "Analyze ROAS drop"
```

## Outputs
- `reports/report.md` — Full analysis report
- `reports/insights.json` — Hypotheses and evaluations
- `reports/creatives.json` — Creative recommendations

## 📊 Architecture

### Agent System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     USER QUERY                               │
│            "Analyze ROAS drop in last 7 days"               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   PLANNER AGENT                              │
│  • Decomposes query into subtasks                           │
│  • Identifies required metrics & analysis                   │
│  • Creates execution plan                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA AGENT                                │
│  • Loads Facebook Ads dataset                               │
│  • Performs quantitative analysis                           │
│  • Identifies trends & anomalies                            │
│  • Segments data by campaign/creative/audience              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   INSIGHT AGENT                              │
│  • Generates hypotheses about performance                   │
│  • Explains patterns (fatigue, saturation, etc.)            │
│  • Identifies root causes                                   │
│  • Assigns preliminary confidence scores                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  EVALUATOR AGENT                             │
│  • Validates hypotheses with quantitative evidence          │
│  • Tests statistical significance                           │
│  • Filters low-confidence insights                          │
│  • Produces validated insights                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            CREATIVE GENERATOR AGENT                          │
│  • Identifies low-performing campaigns                      │
│  • Analyzes top-performing creative patterns               │
│  • Generates new creative recommendations                   │
│  • Provides A/B testing strategy                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   FINAL OUTPUTS                              │
│  • reports/report.md                                        │
│  • reports/insights.json                                    │
│  • reports/creatives.json                                   │
│  • logs/execution_*.json                                    │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Separation of Concerns**: Each agent has a single, well-defined responsibility
2. **Structured Prompts**: Prompts use Think→Analyze→Conclude framework
3. **Validation Layer**: Evaluator agent critically tests all hypotheses
4. **Data Grounding**: All insights backed by quantitative evidence
5. **Iterative Refinement**: Low-confidence results trigger reflection

## 📁 Repository Structure

```
kasparro-agentic-fb-analyst-bruuu/
├── README.md                    # This file
├── requirements.txt             # Python dependencies (pinned)
├── run.py                       # Main CLI entry point
├── Makefile                     # Automation commands
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
│
├── config/
│   └── config.yaml             # Configuration (thresholds, paths, seeds)
│
├── src/
│   ├── agents/                 # Agent implementations
│   │   ├── base_agent.py      # Base agent class
│   │   ├── planner.py         # Query decomposition
│   │   ├── data_agent.py      # Data loading & analysis
│   │   ├── insight_agent.py   # Hypothesis generation
│   │   ├── evaluator.py       # Hypothesis validation
│   │   └── creative_generator.py  # Creative recommendations
│   │
│   ├── orchestrator/           # Workflow coordination
│   │   └── orchestrator.py    # Main orchestrator
│   │
│   └── utils/                  # Utility functions
│       ├── logger.py          # Structured logging
│       └── config_loader.py   # Config management
│
├── prompts/                    # Prompt templates (.md)
│   ├── planner_prompt.md
│   ├── data_agent_prompt.md
│   ├── insight_agent_prompt.md
│   ├── evaluator_prompt.md
│   └── creative_generator_prompt.md
│
├── data/
│   ├── README.md              # Data documentation
│   └── synthetic_fb_ads_undergarments.csv  # Full dataset
│
├── reports/                    # Generated outputs
│   ├── report.md              # Final markdown report
│   ├── insights.json          # Structured insights
│   ├── creatives.json         # Creative recommendations
│   └── observability/         # Screenshots/traces
│
├── logs/                       # Execution logs
│   └── execution_*.json       # Structured JSON logs
│
└── tests/                      # Test suite
    └── test_evaluator.py      # Evaluator tests
```

## 🔧 Configuration

Edit `config/config.yaml` to customize:

```yaml
# Python version requirement
python: "3.10"

# Reproducibility
random_seed: 42

# Data source
data:
  full_csv: "data/synthetic_fb_ads_undergarments.csv"
  use_sample_data: false

# Analysis thresholds
thresholds:
  confidence_min: 0.6          # Minimum confidence for validated insights
  low_ctr_threshold: 0.015     # CTR threshold for low performers
  low_roas_threshold: 2.0      # ROAS threshold
  significant_change_pct: 0.15 # 15% change significance

# LLM settings
llm:
  model: "claude-sonnet-4-20250514"
  temperature: 0.7
  max_tokens: 4000
```

## 📈 Data

The system analyzes Facebook Ads data with the following columns:

- **Identifiers**: campaign_name, adset_name, date
- **Performance**: spend, impressions, clicks, ctr, purchases, revenue, roas
- **Creative**: creative_type, creative_message
- **Targeting**: audience_type, platform, country

**Dataset**: ~4,500 rows covering January 2025

See `data/README.md` for more details.

## 🏃 Usage

### Web Interface (Streamlit)

**Launch the interactive web UI:**
```bash
./start_frontend.sh
# Or: streamlit run app.py
```

**Features:**
- 🎯 Interactive query input with example suggestions
- 📊 Real-time data visualizations (ROAS trends, CTR comparison, creative performance)
- 🔍 AI-powered analysis with confidence scores
- 🎨 Creative recommendations with detailed variants
- 📄 Downloadable reports (Markdown, JSON)
- 📈 Data exploration with interactive charts

**Access:** Open http://localhost:8501 in your browser

See [FRONTEND_README.md](FRONTEND_README.md) for detailed frontend documentation.

### Command Line Interface

**Basic Usage:**

```bash
python run.py "Analyze ROAS drop in last 7 days"
```

### Example Queries

```bash
# ROAS analysis
python run.py "Why did ROAS drop in the last week?"

# CTR investigation
python run.py "Which campaigns have low CTR and why?"

# Creative fatigue
python run.py "Identify creative fatigue in our campaigns"

# Platform comparison
python run.py "Compare Facebook vs Instagram performance"

# Comprehensive analysis
python run.py "Full performance audit: identify issues and recommend solutions"
```

### Using Makefile

```bash
# Setup (first time)
make setup

# Run with query
make run QUERY="Analyze ROAS drop in last 7 days"

# Run tests
make test

# Lint code
make lint

# Create sample dataset
make sample-data

# Clean outputs
make clean
```

## 📤 Outputs

### 1. Markdown Report (`reports/report.md`)

Human-readable analysis including:
- Executive summary
- Key findings
- Detailed hypotheses with confidence scores
- Creative recommendations
- Data summary

### 2. Insights JSON (`reports/insights.json`)

Structured insights including:
```json
{
  "query": "Original query",
  "hypotheses": [
    {
      "hypothesis_id": "H1",
      "title": "Creative Fatigue in Video Ads",
      "description": "...",
      "confidence": 0.85,
      "supporting_evidence": ["..."],
      "validation_status": "confirmed"
    }
  ],
  "evaluation": {...}
}
```

### 3. Creatives JSON (`reports/creatives.json`)

Creative recommendations including:
```json
{
  "recommendations": [
    {
      "campaign_name": "Men ComfortMax Launch",
      "current_issue": "Low CTR (0.012)",
      "creative_variations": [
        {
          "variant_id": "V1",
          "creative_type": "Video",
          "headline": "...",
          "message": "...",
          "cta": "...",
          "rationale": "...",
          "expected_improvement": "CTR: +25%"
        }
      ]
    }
  ]
}
```

### 4. Execution Logs (`logs/execution_*.json`)

Structured trace of agent execution:
```json
[
  {
    "timestamp": "2025-01-15T10:30:00",
    "agent": "planner",
    "event": "start",
    "data": {...}
  }
]
```

## 🔍 Observability

The system includes built-in observability:

1. **Structured Logging**: JSON logs track each agent's execution
2. **Timestamps**: All events timestamped
3. **Error Tracking**: Exceptions logged with full context
4. **Performance Metrics**: Track token usage and execution time

Optional Langfuse integration available (see config).

## ✅ Validation

The Evaluator Agent validates hypotheses using:

1. **Quantitative Evidence**: Statistical measures from data
2. **Confidence Scoring**: 0.0-1.0 scale with thresholds
3. **Effect Magnitude**: Classify changes as large/medium/small
4. **Sample Size**: Ensure statistical validity
5. **Contradiction Detection**: Flag conflicting evidence

**Confidence Thresholds**:
- 0.8-1.0: Strong evidence ✅
- 0.6-0.79: Moderate evidence ⚠️
- <0.6: Rejected ❌

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test
pytest tests/test_evaluator.py -v
```

## 🎯 Design Choices & Tradeoffs

### 1. Prompt Strategy
- **Choice**: Separate .md files for each agent prompt
- **Rationale**: Easier to version, iterate, and maintain
- **Tradeoff**: Slightly more I/O overhead vs. inline prompts

### 2. Validation Layer
- **Choice**: Dedicated Evaluator agent
- **Rationale**: Ensures quality control, prevents hallucinated insights
- **Tradeoff**: Additional LLM call, but critical for reliability

### 3. Data Summarization
- **Choice**: Summarize data before passing to LLM
- **Rationale**: Token efficiency, focus on relevant patterns
- **Tradeoff**: Potential loss of granular details

### 4. JSON Outputs
- **Choice**: Structured JSON for insights/creatives
- **Rationale**: Machine-readable, enables downstream automation
- **Tradeoff**: Less human-friendly than pure markdown

### 5. No Short-term Memory
- **Choice**: Stateless execution (no memory between runs)
- **Rationale**: Simplicity, reproducibility
- **Future**: Can add memory by storing insights.json and loading in context

## 🚧 Reproducibility

Ensured through:
- ✅ Pinned dependency versions
- ✅ Random seed configuration
- ✅ Deterministic data processing
- ✅ Full execution logs
- ✅ Config-driven thresholds

## 📋 Checklist Completion

- [x] Repo name format: `kasparro-agentic-fb-analyst-bruuu`
- [x] README with quick start + exact commands
- [x] Config exists (thresholds, seeds)
- [x] Agents separated with clear I/O schema
- [x] Prompts stored as .md files
- [x] reports/: report.md, insights.json, creatives.json
- [x] logs/ with JSON traces
- [x] tests/: evaluator tests
- [x] Makefile for automation
- [x] .gitignore for cleanliness

## 📝 Release

**Version**: v1.0.0  
**Status**: Complete ✅

To create release:
```bash
git tag -a v1.0 -m "Initial release"
git push origin v1.0
```

## 🤝 Self-Review

### Architecture Decisions

1. **Multi-Agent Design**: Chose specialized agents over monolithic prompt for better modularity and debugging
2. **Planner-First**: Query decomposition helps handle complex, multi-faceted questions
3. **Data-Driven Creative**: Grounded recommendations in actual top-performing messages
4. **Validation Critical Path**: Made evaluator mandatory to maintain output quality

### What Went Well

- Clean separation of concerns
- Structured prompts with clear reasoning frameworks
- Comprehensive test coverage for critical components
- Rich observability via structured logs

### Future Improvements

1. Add short-term memory (store validated insights across runs)
2. Implement parallel agent execution where dependencies allow
3. Add visualization generation (charts/graphs in reports)
4. Support for real-time API data fetching
5. A/B test result tracking integration

## 📞 Support

For issues or questions:
1. Check logs in `logs/execution_*.json`
2. Verify config in `config/config.yaml`
3. Ensure ANTHROPIC_API_KEY is set
4. Review agent prompts in `prompts/`

## 📄 License

This is a technical assessment project for Kasparro.

---

**Built with**: Python 3.10+ | Claude Sonnet 4 | Anthropic API  
**Author**: Bruuu  
**Date**: November 2025
