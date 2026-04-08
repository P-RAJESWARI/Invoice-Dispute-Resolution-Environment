"""
Invoice Dispute Resolution Environment - Models
Defines Action, Observation, and State dataclasses used by both client and server.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


# ──────────────────────────────────────────────
# ACTION  (what the agent sends to the env)
# ──────────────────────────────────────────────

class DisputeAction(BaseModel):
    """
    The agent chooses a resolution decision and drafts a customer-facing response.

    decision:
        - "full_refund"    : approve 100 % refund
        - "partial_refund" : approve a partial credit (specify amount)
        - "reject"         : reject the dispute with justification
        - "escalate"       : escalate to a human supervisor
        - "request_info"   : ask the customer for more information

    response_text : the message that will be sent back to the customer
    refund_amount : only required when decision == "partial_refund"
    """
    decision: Literal[
        "full_refund",
        "partial_refund",
        "reject",
        "escalate",
        "request_info",
    ]
    response_text: str = Field(
        ...,
        description="Customer-facing message explaining the resolution decision",
    )
    refund_amount: Optional[float] = Field(
        default=None,
        description="Refund amount in USD; required for partial_refund decision",
    )


# ──────────────────────────────────────────────
# OBSERVATION  (what the env returns to the agent)
# ──────────────────────────────────────────────

class DisputeObservation(BaseModel):
    """Feedback the environment sends back after each agent action."""

    step_result: str = Field(
        ...,
        description="Human-readable outcome of the agent's last action",
    )
    reward: float = Field(
        ...,
        description="Reward signal for this step (range -1.0 to +1.0)",
    )
    done: bool = Field(
        ...,
        description="True if the episode has ended",
    )
    feedback: str = Field(
        ...,
        description="Grader feedback explaining why the reward was given",
    )
    customer_reaction: Optional[str] = Field(
        default=None,
        description="Simulated customer reaction to the agent's response (if applicable)",
    )


# ──────────────────────────────────────────────
# STATE  (full environment state, returned by state())
# ──────────────────────────────────────────────

class DisputeState(BaseModel):
    """Complete snapshot of the current episode."""

    # Invoice details
    invoice_id: str
    invoice_amount: float
    invoice_date: str
    line_items: list[dict]          # e.g. [{"item": "Cloud Storage", "amount": 49.99}]

    # Dispute details
    dispute_type: Literal[
        "duplicate_charge",
        "wrong_amount",
        "service_not_received",
        "unauthorized_charge",
        "already_paid",
    ]
    customer_message: str           # The complaint from the customer
    customer_tier: Literal["standard", "premium", "enterprise"]
    customer_history: dict          # e.g. {"total_orders": 12, "disputes_filed": 1, "churn_risk": "low"}

    # Company policy (the rules the agent must follow)
    policy: dict                    # e.g. {"max_auto_refund": 200, "escalate_above": 500}

    # Episode progress
    step_count: int
    max_steps: int
    is_done: bool
    total_reward: float

    # Ground truth (used by grader, NOT shown to agent during episode)
    correct_decision: Optional[str] = Field(
        default=None,
        description="Ground-truth correct decision; revealed only after episode ends",
    )
