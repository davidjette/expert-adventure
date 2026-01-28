"""
VCMatch Copy Improvement Script
Reads the draft copy and runs it through OpenAI to generate refined version.
"""

import os
from pathlib import Path

# Load .env from project directory
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from openai import OpenAI

SYSTEM_PROMPT = """You are a conversion copywriter specializing in B2B SaaS and startup tools. You're revising website copy for VCMatch, an AI-powered platform that matches founders with the right investors.

### Context
VCMatch is a two-sided marketplace:
- **Primary users:** Founders seeking investment
- **Value proposition:** Upload your pitch deck → AI analyzes it → Get matched with investors who fit your stage, sector, and needs
- **Key features:** 2,200+ indexed VCs, investor profiles, warm intro paths, portfolio fit analysis, stage/thesis matching

### Current Problem
The existing copy has an adversarial, anti-VC tone ("the game is rigged," "VCs aren't your friends," "fighting back"). While this resonates emotionally with frustrated founders, it:
- Could alienate VC partners the platform needs for warm intros
- Feels paranoid rather than confident
- Positions the product as reactive rather than empowering
- May not appeal to first-time founders who haven't been burned yet

### Your Task
Revise the copy to:

1. **Keep the founder-first energy** — Founders should still feel like this tool is built FOR them, by people who understand their struggles

2. **Reframe from "fighting VCs" to "working smarter"** — The problem isn't that VCs are evil; it's that the matching process is inefficient for everyone. Wrong-fit pitches waste everyone's time.

3. **Emphasize empowerment over victimhood** — Instead of "you're being exploited," try "you deserve better tools to control your fundraise"

4. **Highlight mutual benefit** — Good matches help VCs too. They want to find great companies. The current system just makes it hard.

5. **Keep it punchy and direct** — Don't sanitize it into bland corporate speak. Founders respond to real talk, not marketing fluff.

6. **Preserve the stats and social proof** — The numbers (2,200+ VCs, 850+ matches, $2.3B raised) build credibility

### Tone Guidelines
- **Yes:** Confident, direct, founder-focused, efficient, smart, no-BS
- **No:** Adversarial, paranoid, victimizing, accusatory toward VCs
- **Think:** "Work smarter, not harder" vs. "Fight the system"

### Output Format
Return the revised copy in the same markdown structure as the input, with each section clearly labeled. After each major section, add a brief [RATIONALE] note explaining the key changes."""


def load_copy_draft():
    draft_path = Path(__file__).parent / "COPY-DRAFT.md"
    with open(draft_path, "r", encoding="utf-8") as f:
        return f.read()


def improve_copy(draft: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your-key-here":
        raise ValueError("Please add your OpenAI API key to .env file")

    client = OpenAI(api_key=api_key)

    print("Sending copy to OpenAI for revision...")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Please revise the following website copy:\n\n{draft}"}
        ],
        temperature=0.7,
        max_tokens=4000
    )

    return response.choices[0].message.content


def main():
    print("=" * 60)
    print("VCMatch Copy Improvement Script")
    print("=" * 60)

    # Load the draft
    print("\nLoading COPY-DRAFT.md...")
    draft = load_copy_draft()

    # Run through OpenAI
    revised = improve_copy(draft)

    # Save the result
    output_path = Path(__file__).parent / "COPY-DRAFT-V2.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# VCMatch Website Copy - Revised Draft V2\n\n")
        f.write("*Generated via OpenAI GPT-4o with tone refinement prompt*\n\n")
        f.write("---\n\n")
        f.write(revised)

    print(f"\nRevised copy saved to: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
