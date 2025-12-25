from .types import Proposal
from .utils import utc_now_iso

def maybe_generate_proposal(latest, proposals, next_id):
    if latest["overall_risk"] < 65:
        return None

    return Proposal(
        id=next_id,
        created_ts=utc_now_iso(),
        title="Reduce speed and reassess operating profile",
        rationale=f"Base risk {latest['overall_risk']:.1f}%",
        status="PENDING",
        snapshot={
            "tick": latest["tick"],
            "overall_risk": latest["overall_risk"],
        },
    )
