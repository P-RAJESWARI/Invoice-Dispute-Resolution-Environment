"""
Invoice Dispute Resolution Environment — Core Logic
Implements reset(), step(), and state() for the OpenEnv framework.

An AI agent receives a billing dispute scenario and must:
  1. Analyse the invoice, customer complaint, and company policy
  2. Choose the correct resolution (full refund, partial refund, reject, escalate, request_info)
  3. Draft a professional, policy-compliant customer response

DIFFICULTY LEVELS (3 Tasks):
  EASY       → Obvious disputes (duplicate charges, clear service failures)
  MEDIUM     → Ambiguous cases (wrong amount, customer history needed)
  HARD       → Complex cases (unauthorized charges, policy edge cases)

Reward is shaped by:
  - Correctness of the decision          (+0.5)
  - Policy compliance                    (+0.2)
  - Response quality (tone & clarity)    (+0.2)
  - Efficiency (fewer steps = bonus)     (+0.1)
  - Wrong decisions                      (-0.3)
  - Policy violations                    (-0.2)
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import Optional, Literal

from models import DisputeAction, DisputeObservation, DisputeState


# ─────────────────────────────────────────────────────────────
# TASK DEFINITIONS - 3 difficulty levels
# ─────────────────────────────────────────────────────────────

# EASY: Obvious, clear-cut disputes
EASY_SCENARIOS = [
    {
        "dispute_type": "duplicate_charge",
        "invoice_amount": 99.99,
        "line_items": [
            {"item": "Pro Plan Subscription", "amount": 99.99},
            {"item": "Pro Plan Subscription", "amount": 99.99},
        ],
        "customer_message": (
            "I was charged twice for my Pro Plan this month. "
            "Please refund the duplicate charge of $99.99."
        ),
        "correct_decision": "full_refund",
        "expected_refund": 99.99,
        "difficulty": "easy",
    },
    {
        "dispute_type": "service_not_received",
        "invoice_amount": 59.99,
        "line_items": [
            {"item": "Premium Support (Monthly)", "amount": 59.99},
        ],
        "customer_message": (
            "I was billed for Premium Support but nobody responded to my tickets. "
            "This service was never provided."
        ),
        "correct_decision": "full_refund",
        "expected_refund": 59.99,
        "difficulty": "easy",
    },
]

# MEDIUM: Requires understanding customer history and policy
MEDIUM_SCENARIOS = [
    {
        "dispute_type": "wrong_amount",
        "invoice_amount": 249.99,
        "line_items": [
            {"item": "Enterprise Storage (500 GB)", "amount": 149.99},
            {"item": "API Add-on", "amount": 100.00},
        ],
        "customer_message": (
            "My invoice shows $249.99 but I was quoted $199.99 during sign-up. "
            "I have the email confirmation. This is incorrect billing."
        ),
        "correct_decision": "partial_refund",
        "expected_refund": 50.00,
        "difficulty": "medium",
    },
    {
        "dispute_type": "sla_breach",
        "invoice_amount": 199.99,
        "line_items": [
            {"item": "SLA Support Plan", "amount": 199.99},
        ],
        "customer_message": (
            "Your SLA guarantees 4-hour response time. I submitted a critical issue "
            "and got no response for 48 hours. This is a breach of contract."
        ),
        "correct_decision": "partial_refund",
        "expected_refund": 100.00,
        "difficulty": "medium",
    },
]

# HARD: Complex, ambiguous, requires policy knowledge
HARD_SCENARIOS = [
    {
        "dispute_type": "unauthorized_charge",
        "invoice_amount": 399.99,
        "line_items": [
            {"item": "Enterprise Upgrade", "amount": 399.99},
        ],
        "customer_message": (
            "I never authorised an upgrade to Enterprise. Someone on my team must "
            "have done this by mistake. Please reverse this charge."
        ),
        "correct_decision": "escalate",
        "expected_refund": None,
        "difficulty": "hard",
    },
    {
        "dispute_type": "policy_ambiguity",
        "invoice_amount": 1299.00,
        "line_items": [
            {"item": "Annual Enterprise Plan", "amount": 1299.00},
        ],
        "customer_message": (
            "Your pricing page showed $99/month for Enterprise, which is $1188/year. "
            "You charged $1299. Is this a mistake or a different plan?"
        ),
        "correct_decision": "escalate",
        "expected_refund": None,
        "difficulty": "hard",
    },
]

ALL_SCENARIOS = {
    "easy": EASY_SCENARIOS,
    "medium": MEDIUM_SCENARIOS,
    "hard": HARD_SCENARIOS,
}

CUSTOMER_TIERS = ["standard", "premium", "enterprise"]

POLICIES = {
    "standard":   {"max_auto_refund": 100, "escalate_above": 300, "response_sla_hours": 48},
    "premium":    {"max_auto_refund": 250, "escalate_above": 500, "response_sla_hours": 24},
    "enterprise": {"max_auto_refund": 500, "escalate_above": 1000, "response_sla_hours": 4},
}


# ─────────────────────────────────────────────────────────────
# ENVIRONMENT CLASS
# ─────────────────────────────────────────────────────────────

class InvoiceDisputeEnv:
    """
    OpenEnv-compatible Invoice Dispute Resolution Environment.
    Supports 3 difficulty levels: easy, medium, hard.
    """

    MAX_STEPS = 3

    def __init__(self, difficulty: Literal["easy", "medium", "hard"] = "medium"):
        self.difficulty = difficulty
        self._state: Optional[DisputeState] = None
        self._scenario = None

    # ── reset ─────────────────────────────────────────────────
    def reset(self) -> DisputeObservation:
        """Start a new dispute episode with a scenario from the selected difficulty."""
        scenario = random.choice(ALL_SCENARIOS[self.difficulty])
        tier = random.choice(CUSTOMER_TIERS)
        policy = POLICIES[tier]

        invoice_date = (datetime.today() - timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")

        self._state = DisputeState(
            invoice_id=f"INV-{uuid.uuid4().hex[:8].upper()}",
            invoice_amount=scenario["invoice_amount"],
            invoice_date=invoice_date,
            line_items=scenario["line_items"],
            dispute_type=scenario["dispute_type"],
            customer_message=scenario["customer_message"],
            customer_tier=tier,
            customer_history={
                "total_orders": random.randint(1, 50),
                "disputes_filed": random.randint(0, 3),
                "churn_risk": random.choice(["low", "medium", "high"]),
            },
            policy=policy,
            step_count=0,
            max_steps=self.MAX_STEPS,
            is_done=False,
            total_reward=0.0,
            correct_decision=scenario["correct_decision"],
        )

        self._scenario = scenario

        return DisputeObservation(
            step_result="New dispute received. Analyse the invoice and customer complaint, then resolve.",
            reward=0.0,
            done=False,
            feedback="Episode started. No action taken yet.",
            customer_reaction=None,
        )

    # ── step ──────────────────────────────────────────────────
    def step(self, action: DisputeAction) -> DisputeObservation:
        """Process the agent's resolution decision and return reward + feedback."""
        if self._state is None:
            raise RuntimeError("Call reset() before step().")
        if self._state.is_done:
            raise RuntimeError("Episode already finished. Call reset() to start a new one.")

        self._state.step_count += 1
        reward = 0.0
        feedback_parts = []

        correct = self._scenario["correct_decision"]
        expected_refund = self._scenario.get("expected_refund")
        policy = self._state.policy

        # ── Decision correctness ───────────────────────────────
        if action.decision == correct:
            reward += 0.5
            feedback_parts.append("✅ Correct decision.")
        else:
            reward -= 0.3
            feedback_parts.append(f"❌ Wrong (expected {correct}, got {action.decision}).")

        # ── Policy compliance ──────────────────────────────────
        policy_ok = True
        if action.decision == "full_refund":
            if self._state.invoice_amount > policy["max_auto_refund"]:
                reward -= 0.2
                feedback_parts.append(
                    f"⚠️ Refund ${self._state.invoice_amount} exceeds limit ${policy['max_auto_refund']}."
                )
                policy_ok = False

        if action.decision == "partial_refund":
            if action.refund_amount is None:
                reward -= 0.1
                feedback_parts.append("⚠️ partial_refund chosen but refund_amount missing.")
                policy_ok = False
            elif expected_refund and abs(action.refund_amount - expected_refund) < 10:
                reward += 0.1
                feedback_parts.append(f"✅ Refund ${action.refund_amount} within range.")

        if action.decision == "escalate" and self._state.invoice_amount < policy["escalate_above"]:
            reward -= 0.1
            feedback_parts.append(f"⚠️ Escalation unnecessary (${self._state.invoice_amount} < ${policy['escalate_above']}).")
            policy_ok = False

        if policy_ok and action.decision == correct:
            reward += 0.2
            feedback_parts.append("✅ Policy compliant.")

        # ── Response quality ───────────────────────────────────
        response_score = self._grade_response(action.response_text, action.decision)
        reward += response_score * 0.2
        if response_score >= 0.8:
            feedback_parts.append("✅ Professional response.")
        elif response_score >= 0.5:
            feedback_parts.append("ℹ️ Response acceptable but could be better.")
        else:
            feedback_parts.append("❌ Response too brief or unprofessional.")

        # ── Efficiency bonus ───────────────────────────────────
        if self._state.step_count == 1 and action.decision == correct:
            reward += 0.1
            feedback_parts.append("🚀 Efficiency bonus (1-step resolution).")

        # ── Termination ────────────────────────────────────────
        done = False
        if action.decision in ("full_refund", "partial_refund", "reject", "escalate"):
            done = True
        elif self._state.step_count >= self._state.max_steps:
            done = True
            reward -= 0.2
            feedback_parts.append("⏰ Max steps exceeded.")

        reward = max(-1.0, min(1.0, reward))

        self._state.is_done = done
        self._state.total_reward += reward

        if done:
            self._state.correct_decision = correct
            feedback_parts.append(f"\n📋 Ground truth: {correct}")

        customer_reaction = self._simulate_customer_reaction(action.decision, reward)

        return DisputeObservation(
            step_result=f"Step {self._state.step_count}: {action.decision}",
            reward=round(reward, 4),
            done=done,
            feedback=" | ".join(feedback_parts),
            customer_reaction=customer_reaction,
        )

    # ── state ─────────────────────────────────────────────────
    @property
    def state(self) -> DisputeState:
        if self._state is None:
            raise RuntimeError("Call reset() first.")
        return self._state

    # ── helpers ───────────────────────────────────────────────
    def _grade_response(self, text: str, decision: str) -> float:
        if not text or len(text) < 20:
            return 0.0
        score = 0.5
        text_lower = text.lower()
        empathy = ["apologise", "sorry", "understand", "inconvenience", "appreciate"]
        if any(w in text_lower for w in empathy):
            score += 0.15
        action_words = ["refund", "credit", "escalate", "investigate", "resolve"]
        if any(w in text_lower for w in action_words):
            score += 0.15
        if text == text.upper():
            score -= 0.2
        if len(text) > 60:
            score += 0.1
        if len(text) > 150:
            score += 0.1
        return min(1.0, max(0.0, score))

    def _simulate_customer_reaction(self, decision: str, reward: float) -> str:
        if reward >= 0.6:
            return "Thank you! I appreciate the quick resolution."
        elif reward >= 0.2:
            return "OK, I understand. Let's proceed."
        else:
            return "I'm disappointed with this response."
