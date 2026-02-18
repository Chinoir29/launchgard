"""
ARCHI-Ω v1.2 - Command Line Interface

Simple CLI for running the ARCHI-Ω framework.
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import Dict, Any

from .pipeline.stages import Pipeline, ProjectContext
from .epistemic.foundation import OriginTag, ProofLevel, TestabilityLevel, Claim


def load_user_input(input_file: Path) -> ProjectContext:
    """Load user input from YAML or markdown file"""
    context = ProjectContext()
    
    if input_file.suffix in ['.yaml', '.yml']:
        with open(input_file, 'r') as f:
            data = yaml.safe_load(f)
            
        # Map YAML fields to context
        context.goal = data.get('GOAL', '')
        context.deliverable = data.get('DELIVERABLE', '')
        context.users_load = data.get('USERS_LOAD', {})
        context.sla_slo = data.get('SLA_SLO', {})
        context.data = data.get('DATA', {})
        context.constraints = data.get('CONSTRAINTS', {})
        context.integrations = data.get('INTEGRATIONS', [])
        context.ops = data.get('OPS', {})
        context.security = data.get('SECURITY', {})
        context.ai_ml = data.get('AI_ML')
        context.done_criteria = data.get('DONE', {})
    
    return context


def load_config(config_file: Path) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    return {
        "mode": config.get('mode', 'MAXCAP'),
        "budget": config.get('budget', 'long'),
        "evidence": config.get('evidence', 'mid'),
        "divergence": config.get('divergence', 'mid'),
        "auto_gov": config.get('auto_gov', True),
        "auto_tools": config.get('auto_tools', True),
        "pcx": config.get('pcx', True),
        "nest": config.get('nest', True)
    }


def format_deliverable_markdown(deliverable: Dict[str, Any]) -> str:
    """Format deliverable as markdown"""
    lines = [
        "# ARCHI-Ω v1.2 - Deliverable",
        "",
        "## 0) FACTS [USER]",
        ""
    ]
    
    for fact in deliverable.get('facts', []):
        lines.append(f"- {fact}")
    
    lines.extend([
        "",
        "## 1) OPEN QUESTIONS",
        ""
    ])
    
    for question in deliverable.get('open_questions', []):
        lines.append(f"- {question}")
    
    lines.extend([
        "",
        "## 2) ASSUMPTIONS [HYP]",
        ""
    ])
    
    for assumption in deliverable.get('assumptions', []):
        lines.append(f"- {assumption}")
    
    lines.extend([
        "",
        "## 3) OPTIONS",
        ""
    ])
    
    for option in deliverable.get('options', []):
        lines.append(f"### {option.get('name', 'Unknown')}")
        lines.append(f"**Total Score:** {option.get('total_score', 0)}")
        lines.append("")
    
    lines.extend([
        "",
        "## 4) RECOMMENDATION",
        ""
    ])
    
    rec = deliverable.get('recommendation')
    if rec:
        lines.append(f"**Recommended Option:** {rec.get('name', 'Unknown')}")
        lines.append(f"**Score:** {rec.get('total_score', 0)}")
    else:
        lines.append("No recommendation available")
    
    lines.extend([
        "",
        "## 11) CLAIM LEDGER",
        "",
        deliverable.get('claim_ledger', 'No claims recorded'),
        "",
        "## 12) TERMINATION",
        "",
        f"**TERM:** {deliverable.get('termination', 'UNKNOWN')}",
        ""
    ])
    
    return "\n".join(lines)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="ARCHI-Ω v1.2 - Architectural Framework CLI"
    )
    
    parser.add_argument(
        'input',
        type=Path,
        help='Input file (YAML or markdown) with user requirements'
    )
    
    parser.add_argument(
        '-c', '--config',
        type=Path,
        default=Path('archi-omega-config.yaml'),
        help='Configuration file (default: archi-omega-config.yaml)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file for deliverable (default: stdout)'
    )
    
    parser.add_argument(
        '--format',
        choices=['markdown', 'yaml', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='ARCHI-Ω v1.2'
    )
    
    args = parser.parse_args()
    
    # Load input
    if not args.input.exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1
    
    try:
        context = load_user_input(args.input)
    except Exception as e:
        print(f"Error loading input: {e}", file=sys.stderr)
        return 1
    
    # Load config
    config = {}
    if args.config.exists():
        try:
            config = load_config(args.config)
        except Exception as e:
            print(f"Warning: Could not load config: {e}", file=sys.stderr)
            print("Using default configuration", file=sys.stderr)
    
    # Run pipeline
    print("Executing ARCHI-Ω pipeline...", file=sys.stderr)
    pipeline = Pipeline(config)
    
    try:
        deliverable = pipeline.execute(context)
    except Exception as e:
        print(f"Error executing pipeline: {e}", file=sys.stderr)
        return 1
    
    # Format output
    if args.format == 'markdown':
        output = format_deliverable_markdown(deliverable)
    elif args.format == 'yaml':
        output = yaml.dump(deliverable, default_flow_style=False)
    else:  # json
        import json
        output = json.dumps(deliverable, indent=2, default=str)
    
    # Write output
    if args.output:
        args.output.write_text(output)
        print(f"Deliverable written to {args.output}", file=sys.stderr)
    else:
        print(output)
    
    print(f"\nTermination: {deliverable.get('termination', 'UNKNOWN')}", file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
