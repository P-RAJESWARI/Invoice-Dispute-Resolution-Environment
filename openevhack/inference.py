"""
Invoice Dispute Resolution Environment - Baseline Inference Script
Evaluates OpenAI models against the environment with proper grading.
Requirements:
- OpenAI API key via OPENAI_API_KEY environment variable
- HuggingFace token via HF_TOKEN environment variable (optional)
Usage:
    python inference.py
    python inference.py --model gpt-4
    python inference.py --difficulty easy
"""

import os
import sys
import json
import argparse
import requests
from typing import Dict, List, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI imports
try:
    from openai import OpenAI
except ImportError:
    print("❌ OpenAI package not found. Install with: pip install openai")
    sys.exit(1)


class InvoiceDisputeAgent:
    """Agent that uses OpenAI-compatible API to resolve disputes."""
    
    def __init__(self, api_url: str = "http://localhost:7860", model: str = None):
        """
        Initialize agent with OpenAI-compatible client.
        
        Args:
            api_url: Base URL for the environment API
            model: Model name (uses env vars for API config)
            
        Environment variables (injected by judges or set locally):
            - API_KEY: API key for the LLM provider
            - API_BASE_URL: Base URL for the LLM provider (e.g., https://router.huggingface.co/v1)
            - MODEL_NAME: Model name to use
        """
        self.api_url = api_url
        
        # Get configuration from environment variables (injected by judges)
        api_key = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
        api_base_url = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
        model_name = os.getenv("MODEL_NAME", model or "gpt-3.5-turbo")
        
        self.model = model_name
        
        # Initialize OpenAI-compatible client
        # This works with ANY provider (OpenAI, HuggingFace, etc.)
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base_url
        )
        
        # Track statistics
        self.episodes_completed = 0
        self.total_reward = 0.0
        self.episode_rewards = []
        self.decision_counts = {}
        
    def reset_environment(self, difficulty: str) -> Dict:
        """Reset environment and get initial observation."""
        try:
            response = requests.post(
                f"{self.api_url}/reset",
                json={"difficulty": difficulty},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error resetting environment: {e}")
            raise
    
    def get_state(self) -> Dict:
        """Get current environment state."""
        try:
            response = requests.get(f"{self.api_url}/state", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error getting state: {e}")
            raise
    
    def submit_action(self, action: Dict) -> Dict:
        """Submit action to environment and get observation."""
        try:
            response = requests.post(
                f"{self.api_url}/step",
                json=action,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error submitting action: {e}")
            raise
    
    def generate_decision(self, state: Dict) -> Tuple[str, str, float]:
        """
        Use OpenAI API to generate decision.
        
        Args:
            state: Current environment state
            
        Returns:
            Tuple of (decision, response_text, refund_amount)
        """
        # Build context prompt
        prompt = f"""You are an expert customer service manager handling billing disputes.
INVOICE DETAILS:
- Invoice ID: {state['invoice_id']}
- Amount: ${state['invoice_amount']:.2f}
- Date: {state['invoice_date']}
- Type: {state['dispute_type'].replace('_', ' ').title()}
CUSTOMER INFORMATION:
- Tier: {state['customer_tier'].upper()}
- Total Orders: {state['customer_history']['total_orders']}
- Prior Disputes: {state['customer_history']['disputes_filed']}
- Churn Risk: {state['customer_history']['churn_risk'].upper()}
COMPANY POLICY:
- Max Auto-Refund: ${state['policy']['max_auto_refund']:.2f}
- Escalate Above: ${state['policy']['escalate_above']:.2f}
- Response SLA: {state['policy']['response_sla_hours']} hours
CUSTOMER COMPLAINT:
{state['customer_message']}
LINE ITEMS:
{json.dumps(state['line_items'], indent=2)}
Based on the evidence, company policy, and customer history, decide on ONE of these actions:
1. full_refund - Approve 100% refund
2. partial_refund - Approve partial refund (specify amount)
3. reject - Deny the dispute
4. escalate - Escalate to human supervisor
5. request_info - Ask customer for more information
Respond in JSON format:
{{
    "decision": "<one of the 5 options>",
    "reasoning": "<brief explanation>",
    "refund_amount": <number or null>
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a customer service expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse response
            content = response.choices[0].message.content
            decision_data = json.loads(content)
            
            decision = decision_data.get("decision", "request_info")
            reasoning = decision_data.get("reasoning", "")
            refund_amount = decision_data.get("refund_amount")
            
            # Generate professional response text
            response_prompt = f"""Write a brief, professional customer service response to this dispute.
Decision: {decision}
Reasoning: {reasoning}
Max length: 100 words
Keep it empathetic and professional."""
            
            response_text_obj = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": response_prompt}],
                temperature=0.5,
                max_tokens=100
            )
            
            response_text = response_text_obj.choices[0].message.content
            
            return decision, response_text, refund_amount
        
        except Exception as e:
            print(f"⚠️  Error generating decision: {e}")
            # Fallback to request_info
            return "request_info", "We need more information to resolve this dispute.", None
    
    def run_episode(self, difficulty: str = "medium") -> Dict:
        """
        Run a single episode with OpenEnv-compliant structured logging.
        Ensures:
        - No crashes
        - Proper stdout format
        - Score strictly in (0,1)
        """
    
        try:
            # ✅ START BLOCK
            print(f"[START] task=invoice-dispute difficulty={difficulty}", flush=True)
    
            obs = self.reset_environment(difficulty)
    
            episode_reward = 0.0
            steps = 0
            max_steps = 10
    
            while not obs.get("done", False) and steps < max_steps:
                steps += 1
    
                try:
                    # Get state
                    state = self.get_state()
    
                    # Generate decision
                    decision, response_text, refund_amount = self.generate_decision(state)
    
                    action = {
                        "decision": decision,
                        "response_text": response_text,
                        "refund_amount": refund_amount
                    }
    
                    # Step environment
                    obs = self.submit_action(action)
    
                    reward = obs.get("reward", 0.0)
                    episode_reward += reward
    
                    # ✅ STEP BLOCK
                    print(f"[STEP] step={steps} reward={reward}", flush=True)
    
                except Exception:
                    # Fail-safe per step (no crash)
                    print(f"[STEP] step={steps} reward=0.0", flush=True)
                    continue
    
            # ✅ Normalize + clamp score to (0, 1)
            final_score = (episode_reward + 1) / 2  # map [-1,1] → [0,1]
            final_score = max(0.01, min(0.99, final_score))
    
            # ✅ END BLOCK
            print(
                f"[END] task=invoice-dispute score={final_score} steps={steps}",
                flush=True
            )
    
            return {
                "difficulty": difficulty,
                "reward": episode_reward,
                "steps": steps,
                "completed": True
            }
    
        except Exception as e:
            # ✅ GLOBAL FAIL-SAFE (prevents evaluator crash)
            print(f"[END] task=invoice-dispute score=0.01 steps=0", flush=True)
    
            return {
                "difficulty": difficulty,
                "reward": 0.0,
                "steps": 0,
                "completed": False,
                "error": str(e)
            }
        
    def evaluate(self, difficulties: List[str] = None, episodes_per_difficulty: int = 3):
        """
        Run full evaluation across difficulties.
        
        Args:
            difficulties: List of difficulties to evaluate
            episodes_per_difficulty: Number of episodes per difficulty
        """
        if difficulties is None:
            difficulties = ["easy", "medium", "hard"]
        
        results = {
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
            "results_by_difficulty": {},
            "summary": {}
        }
        
        for difficulty in difficulties:
            print(f"\n{'='*60}")
            print(f"EVALUATING {difficulty.upper()} DIFFICULTY")
            print(f"{'='*60}")
            
            difficulty_rewards = []
            difficulty_steps = []
            
            for episode in range(episodes_per_difficulty):
                try:
                    print(f"\nEpisode {episode + 1}/{episodes_per_difficulty}")
                    episode_result = self.run_episode(difficulty)
                    difficulty_rewards.append(episode_result["reward"])
                    difficulty_steps.append(episode_result["steps"])
                except Exception as e:
                    print(f"⚠️  Error in episode: {e}")
                    continue
            
            # Calculate statistics
            if difficulty_rewards:
                avg_reward = sum(difficulty_rewards) / len(difficulty_rewards)
                max_reward = max(difficulty_rewards)
                min_reward = min(difficulty_rewards)
                avg_steps = sum(difficulty_steps) / len(difficulty_steps)
                
                results["results_by_difficulty"][difficulty] = {
                    "episodes": len(difficulty_rewards),
                    "average_reward": avg_reward,
                    "max_reward": max_reward,
                    "min_reward": min_reward,
                    "average_steps": avg_steps,
                    "all_rewards": difficulty_rewards
                }
        
        # Overall summary
        if self.episode_rewards:
            results["summary"] = {
                "total_episodes": len(self.episode_rewards),
                "overall_average_reward": sum(self.episode_rewards) / len(self.episode_rewards),
                "total_reward": sum(self.episode_rewards)
            }
        
        return results
    
    def print_results(self, results: Dict):
        """Pretty print evaluation results."""
        print(f"\n{'='*60}")
        print("📊 EVALUATION RESULTS")
        print(f"{'='*60}\n")
        
        print(f"Model: {results['model']}")
        print(f"Timestamp: {results['timestamp']}\n")
        
        for difficulty, stats in results["results_by_difficulty"].items():
            print(f"\n{difficulty.upper()}:")
            print(f"  Episodes: {stats['episodes']}")
            print(f"  Average Reward: {stats['average_reward']:.4f}")
            print(f"  Max Reward: {stats['max_reward']:.4f}")
            print(f"  Min Reward: {stats['min_reward']:.4f}")
            print(f"  Average Steps: {stats['average_steps']:.2f}")
        
        if "summary" in results:
            print(f"\n{'─'*60}")
            print(f"OVERALL:")
            print(f"  Total Episodes: {results['summary']['total_episodes']}")
            print(f"  Overall Average Reward: {results['summary']['overall_average_reward']:.4f}")
            print(f"  Total Reward: {results['summary']['total_reward']:.4f}")
        
        print(f"\n{'='*60}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Evaluate agents on Invoice Dispute Resolution environment"
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
        help="Model to use (default: env var MODEL_NAME or gpt-3.5-turbo)"
    )
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard", "all"],
        default="all",
        help="Difficulty level to evaluate"
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=3,
        help="Episodes per difficulty (default: 3)"
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:7860",
        help="Base URL for environment API"
    )
    parser.add_argument(
        "--output",
        help="Output file for results (JSON)"
    )
    
    args = parser.parse_args()
    
    # Check required environment variables
    api_key = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
    api_base_url = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    
    if not api_key:
        print("⚠️  API_KEY or OPENAI_API_KEY environment variable not set")
        print("\nFor local development, use free options:")
        print("  1. HuggingFace: export API_KEY='hf_...'")
        print("     export API_BASE_URL='https://router.huggingface.co/v1'")
        print("     export MODEL_NAME='Qwen/Qwen2.5-72B-Instruct'")
        print("\n  2. OpenAI: export API_KEY='sk-...'")
        print("     export API_BASE_URL='https://api.openai.com/v1'")
        print("\nDuring evaluation, judges will inject API_KEY and API_BASE_URL")
        print("Continuing with available configuration...")
    
    # Create agent
    print(f"🤖 Initializing agent with model: {args.model}")
    print(f"   API Base URL: {api_base_url}")
    agent = InvoiceDisputeAgent(api_url=args.api_url, model=args.model)
    
    # Determine difficulties to evaluate
    difficulties = ["easy", "medium", "hard"] if args.difficulty == "all" else [args.difficulty]
    
    # Run evaluation
    try:
        results = agent.evaluate(
            difficulties=difficulties,
            episodes_per_difficulty=args.episodes
        )
        
        # Print results
        agent.print_results(results)
        
        # Save results if requested
        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            print(f"✅ Results saved to {args.output}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Evaluation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n⚠️  Evaluation note: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
