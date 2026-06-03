"""Base comparator class"""

from abc import ABC, abstractmethod
from typing import Dict, List
from dataclasses import dataclass, field
from src.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Mismatch:
    """Represents a single text mismatch"""
    mismatch_type: str
    page: int = 0
    line: int = 0
    position: int = 0
    expected: str = ""
    actual: str = ""
    context_expected: str = ""
    context_actual: str = ""
    severity: str = "medium"
    additional_info: Dict = field(default_factory=dict)


@dataclass
class ComparisonResult:
    """Result of text comparison"""
    source_file: str
    target_file: str
    mismatches: List[Mismatch]
    total_mismatches: int = 0
    word_mismatches: int = 0
    spacing_mismatches: int = 0
    structural_mismatches: int = 0
    missing_words: int = 0
    extra_words: int = 0
    similarity_score: float = 0.0
    comparison_time: float = 0.0
    success: bool = True
    error: str = ""


class BaseComparator(ABC):
    """Abstract base class for text comparators"""

    def __init__(self):
        """Initialize base comparator"""
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def compare(
        self,
        source_text: str,
        target_text: str,
        source_file: str = "source.txt",
        target_file: str = "target.txt",
    ) -> ComparisonResult:
        """Compare two texts"""
        pass

    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calculate similarity score between two texts (0-1)"""
        from difflib import SequenceMatcher

        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0

        matcher = SequenceMatcher(None, text1, text2)
        return matcher.ratio()
