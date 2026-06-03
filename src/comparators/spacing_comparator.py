"""Whitespace and spacing comparison"""

import time
from typing import List
from src.comparators.base import BaseComparator, ComparisonResult, Mismatch
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SpacingComparator(BaseComparator):
    """Compare whitespace and spacing differences"""

    def compare(
        self,
        source_text: str,
        target_text: str,
        source_file: str = "source.txt",
        target_file: str = "target.txt",
    ) -> ComparisonResult:
        """Compare spacing and whitespace differences"""
        start_time = time.time()
        mismatches = []

        try:
            source_lines = source_text.split("\n")
            target_lines = target_text.split("\n")

            for line_num, (src_line, tgt_line) in enumerate(
                zip(source_lines, target_lines), 1
            ):
                if self._get_words(src_line) == self._get_words(tgt_line):
                    if src_line != tgt_line:
                        mismatches.append(
                            Mismatch(
                                mismatch_type="spacing_mismatch",
                                line=line_num,
                                expected=src_line,
                                actual=tgt_line,
                                severity="low",
                                additional_info={
                                    "expected_spaces": src_line.count(" "),
                                    "actual_spaces": tgt_line.count(" "),
                                },
                            )
                        )

            source_line_endings = self._detect_line_endings(source_text)
            target_line_endings = self._detect_line_endings(target_text)

            if source_line_endings != target_line_endings:
                mismatches.append(
                    Mismatch(
                        mismatch_type="line_ending_mismatch",
                        expected=source_line_endings,
                        actual=target_line_endings,
                        severity="low",
                    )
                )

            src_tabs = source_text.count("\t")
            tgt_tabs = target_text.count("\t")

            if src_tabs != tgt_tabs:
                mismatches.append(
                    Mismatch(
                        mismatch_type="tab_mismatch",
                        expected=f"Tabs: {src_tabs}",
                        actual=f"Tabs: {tgt_tabs}",
                        severity="low",
                    )
                )

            comparison_time = time.time() - start_time
            logger.info(f"Spacing comparison complete: {len(mismatches)} mismatches")

            return ComparisonResult(
                source_file=source_file,
                target_file=target_file,
                mismatches=mismatches,
                total_mismatches=len(mismatches),
                spacing_mismatches=len(mismatches),
                similarity_score=self.calculate_similarity(source_text, target_text),
                comparison_time=comparison_time,
                success=True,
            )

        except Exception as e:
            logger.error(f"Error comparing spacing: {str(e)}")
            return ComparisonResult(
                source_file=source_file,
                target_file=target_file,
                mismatches=[],
                success=False,
                error=f"Spacing comparison failed: {str(e)}",
            )

    @staticmethod
    def _get_words(text: str) -> List[str]:
        """Extract words from text, ignoring spacing"""
        return text.split()

    @staticmethod
    def _detect_line_endings(text: str) -> str:
        """Detect the line ending type used in text"""
        crlf_count = text.count("\r\n")
        lf_count = text.count("\n") - crlf_count
        cr_count = text.count("\r") - crlf_count

        if crlf_count > 0 and lf_count == 0 and cr_count == 0:
            return "CRLF"
        elif lf_count > 0 and crlf_count == 0 and cr_count == 0:
            return "LF"
        elif cr_count > 0 and crlf_count == 0 and lf_count == 0:
            return "CR"
        elif (crlf_count + lf_count + cr_count) > 0:
            return "MIXED"
        return "NONE"
