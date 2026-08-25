from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class StageResult:
    stage_name: str
    status: str
    records_processed: int = 0
    records_rejected: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: str = ""
