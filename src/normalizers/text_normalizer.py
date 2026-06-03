"""Text normalization and cleanup utilities"""

import re
from dataclasses import dataclass
from src.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class NormalizationConfig:
    """Configuration for text normalization"""
    lowercase: bool = False
    strip_whitespace: bool = True
    remove_extra_spaces: bool = False
    normalize_line_endings: bool = True
    remove_special_chars: bool = False
    remove_punctuation: bool = False
    remove_urls: bool = False
    remove_emails: bool = False


class TextNormalizer:
    """Normalize and clean text for comparison"""

    def __init__(self, config: NormalizationConfig = None):
        """Initialize normalizer with configuration"""
        self.config = config or NormalizationConfig()
        self.logger = get_logger(self.__class__.__name__)

    def normalize(self, text: str) -> str:
        """Apply all normalization steps"""
        if not text:
            return text

        if self.config.normalize_line_endings:
            text = self._normalize_line_endings(text)

        if self.config.lowercase:
            text = text.lower()

        if self.config.remove_urls:
            text = self._remove_urls(text)

        if self.config.remove_emails:
            text = self._remove_emails(text)

        if self.config.remove_punctuation:
            text = self._remove_punctuation(text)

        if self.config.remove_extra_spaces:
            text = self._remove_extra_spaces(text)

        if self.config.strip_whitespace:
            text = text.strip()

        return text

    @staticmethod
    def _normalize_line_endings(text: str) -> str:
        """Normalize line endings to newline"""
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
        return text

    @staticmethod
    def _remove_urls(text: str) -> str:
        """Remove URLs from text"""
        url_pattern = r'https?://\S+|www\.\S+'
        return re.sub(url_pattern, '', text)

    @staticmethod
    def _remove_emails(text: str) -> str:
        """Remove email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.sub(email_pattern, '', text)

    @staticmethod
    def _remove_punctuation(text: str) -> str:
        """Remove punctuation from text"""
        return re.sub(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', '', text)

    @staticmethod
    def _remove_extra_spaces(text: str) -> str:
        """Remove extra spaces"""
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        return text

    @staticmethod
    def split_into_lines(text: str) -> list:
        """Split text into lines"""
        return text.split('\n')

    @staticmethod
    def split_into_words(text: str) -> list:
        """Split text into words"""
        return text.split()

    @staticmethod
    def get_whitespace_info(text: str) -> dict:
        """Get whitespace information"""
        return {
            "total_chars": len(text),
            "spaces": text.count(" "),
            "tabs": text.count("\t"),
            "newlines": text.count("\n"),
        }
