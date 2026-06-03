"""Word-level text comparison"""

import time
from typing import List
from difflib import SequenceMatcher
from src.comparators.base import BaseComparator, ComparisonResult, Mismatch
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WordComparator(BaseComparator):
    """Compare text at word level"""

    def __init__(self, context_lines: int = 2):
        """Initialize word comparator"""
        super().__init__()
        self.context_lines = context_lines

    def compare(
        self,
        source_text: str,
        target_text: str,
        source_file: str = "source.txt",
        target_file: str = "target.txt",
    ) -> ComparisonResult:
        """Compare two texts at word level"""
        start_time = time.time()
        mismatches = []

        try:
            source_lines = source_text.split("\n")
            target_lines = target_text.split("\n")

            for line_num, (src_line, tgt_line) in enumerate(
                zip(source_lines, target_lines), 1
            ):
                if src_line != tgt_line:
                    line_mismatches = self._compare_line_words(
                        src_line, tgt_line, line_num
                    )
                    mismatches.extend(line_mismatches)

            if len(source_lines) != len(target_lines):
                mismatches.extend(
                    self._compare_line_counts(
                        source_lines, target_lines, len(source_lines)
                    )
                )

            total_mismatches = len(mismatches)
            word_mismatches = len(
                [m for m in mismatches if m.mismatch_type == "word_mismatch"]
            )
            missing_words = len(
                [m for m in mismatches if m.mismatch_type == "missing_word"]
            )
            extra_words = len(
                [m for m in mismatches if m.mismatch_type == "extra_word"]
            )

            similarity = self.calculate_similarity(source_text, target_text)
            comparison_time = time.time() - start_time

            logger.info(f"Word comparison complete: {total_mismatches} mismatches")

            return ComparisonResult(
                source_file=source_file,
                target_file=target_file,
                mismatches=mismatches,
                total_mismatches=total_mismatches,
                word_mismatches=word_mismatches,
                missing_words=missing_words,
                extra_words=extra_words,
                similarity_score=similarity,
                comparison_time=comparison_time,
                success=True,
            )

        except Exception as e:
            logger.error(f"Error comparing text: {str(e)}")
            return ComparisonResult(
                source_file=source_file,
                target_file=target_file,
                mismatches=[],
                success=False,
                error=f"Comparison failed: {str(e)}",
            )

    def _compare_line_words(
        self, source_line: str, target_line: str, line_num: int
    ) -> List[Mismatch]:
        """Compare words in a single line"""
        mismatches = []
        src_words = source_line.split()
        tgt_words = target_line.split()

        matcher = SequenceMatcher(None, src_words, tgt_words)
        matching_blocks = matcher.get_matching_blocks()

        src_pos = 0
        tgt_pos = 0

        for block in matching_blocks:
            if src_pos < block.a or tgt_pos < block.b:
                mismatches.extend(
                    self._find_word_differences(
                        src_words[src_pos : block.a],
                        tgt_words[tgt_pos : block.b],
                        line_num,
                        src_pos,
                    )
                )

            src_pos = block.a + block.size
            tgt_pos = block.b + block.size

        return mismatches

    def _find_word_differences(
        self,
        src_words: List[str],
        tgt_words: List[str],
        line_num: int,
        position: int,
    ) -> List[Mismatch]:
        """Find differences between word lists"""
        mismatches = []
        max_len = max(len(src_words), len(tgt_words))

        for i in range(max_len):
            if i < len(src_words) and i < len(tgt_words):
                if src_words[i] != tgt_words[i]:
                    mismatches.append(
                        Mismatch(
                            mismatch_type="word_mismatch",
                            line=line_num,
                            position=position + i,
                            expected=src_words[i],
                            actual=tgt_words[i],
                            severity="medium",
                        )
                    )
            elif i >= len(tgt_words):
                mismatches.append(
                    Mismatch(
                        mismatch_type="missing_word",
                        line=line_num,
                        position=position + i,
                        expected=src_words[i],
                        actual="",
                        severity="high",
                    )
                )
            else:
                mismatches.append(
                    Mismatch(
                        mismatch_type="extra_word",
                        line=line_num,
                        position=position + i,
                        expected="",
                        actual=tgt_words[i],
                        severity="medium",
                    )
                )

        return mismatches

    def _compare_line_counts(
        self, src_lines: List[str], tgt_lines: List[str], src_count: int
    ) -> List[Mismatch]:
        """Compare number of lines"""
        mismatches = []
        tgt_count = len(tgt_lines)

        if src_count > tgt_count:
            for i in range(tgt_count, src_count):
                mismatches.append(
                    Mismatch(
                        mismatch_type="missing_line",
                        line=i + 1,
                        expected=src_lines[i],
                        actual="",
                        severity="high",
                    )
                )
        elif tgt_count > src_count:
            for i in range(src_count, tgt_count):
                mismatches.append(
                    Mismatch(
                        mismatch_type="extra_line",
                        line=i + 1,
                        expected="",
                        actual=tgt_lines[i],
                        severity="medium",
                    )
                )

        return mismatches
