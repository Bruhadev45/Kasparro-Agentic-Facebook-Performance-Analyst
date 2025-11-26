#!/usr/bin/env python3
"""
Kasparro Agentic Facebook Performance Analyst
Main entry point for running the multi-agent system.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from dotenv import load_dotenv
from utils.config_loader import load_config, validate_config
from orchestrator.orchestrator import AgentOrchestrator


def main():
    """Main execution function."""
    # Load environment variables
    load_dotenv()

    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment")
        print("Please set it in .env file or export it:")
        print("  export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)

    # Get query from command line or interactive input
    if len(sys.argv) < 2:
        # Interactive mode
        print("🚀 Kasparro Agentic FB Analyst")
        print("=" * 70)
        print("\nExample queries:")
        print("  • Analyze ROAS drop in last 7 days")
        print("  • Which campaigns have low CTR?")
        print("  • Identify creative fatigue")
        print("  • Compare Facebook vs Instagram performance")
        print("=" * 70)

        try:
            query = input("\n💬 Enter your query: ").strip()
            if not query:
                print("❌ Error: Query cannot be empty")
                sys.exit(1)
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Exiting...")
            sys.exit(0)
    else:
        # Command-line argument mode
        query = sys.argv[1]
    
    # Load and validate config
    try:
        config = load_config()
        validate_config(config)
    except Exception as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    
    print(f"🚀 Starting Kasparro Agentic FB Analyst")
    print(f"📊 Query: {query}")
    print(f"⚙️  Model: {config['llm']['model']}")
    print(f"📈 Confidence threshold: {config['thresholds']['confidence_min']}")
    print("-" * 70)
    
    # Initialize and run orchestrator
    try:
        orchestrator = AgentOrchestrator(config, api_key)
        result = orchestrator.run(query)
        
        print("\n" + "=" * 70)
        print("✅ Analysis complete!")
        print("=" * 70)
        print(f"\n📄 Reports generated:")
        print(f"   - reports/report.md")
        print(f"   - reports/insights.json")
        print(f"   - reports/creatives.json")
        print(f"\n📋 Logs saved:")
        print(f"   - logs/execution_*.json")
        print("\n" + "-" * 70)
        
        # Print summary
        print("\n📊 Summary:")
        print(f"   Hypotheses generated: {len(result['insights'].get('hypotheses', []))}")
        print(f"   Validated insights: {result['evaluation'].get('validated_count', 0)}")
        print(f"   Creative recommendations: {result['creatives'].get('total_recommendations', 0)}")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
