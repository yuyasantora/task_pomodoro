from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PySide6.QtCore import Qt
from ..analysis.analyzer import FocusAnalyzer
from ..analysis.suggestions import SuggestionGenerator
from ..core.session import SessionData
from typing import List


class AnalysisDialog(QDialog):
    def __init__(self, sessions: List[SessionData], parent=None):
        super().__init__(parent)
        self.sessions = sessions
        self.setWindowTitle("Focus Analysis")
        self.setMinimumSize(500, 400)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)

        if len(self.sessions) < 5:
            self.text_view.setPlainText("Not enough data for analysis.\n\nComplete at least 5 sessions to see insights.")
        else:
            analysis_text = self._generate_analysis()
            self.text_view.setPlainText(analysis_text)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)

        layout.addWidget(self.text_view)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def _generate_analysis(self) -> str:
        analyzer = FocusAnalyzer(self.sessions)
        suggestion_gen = SuggestionGenerator(analyzer)

        insights = suggestion_gen.generate_insights()
        recommendations = suggestion_gen.generate_recommendations()

        text = "=== FOCUS ANALYSIS ===\n\n"
        text += f"Total sessions analyzed: {len(self.sessions)}\n"
        text += f"Work sessions: {len(analyzer.work_sessions)}\n\n"

        text += "--- Key Insights ---\n"
        for insight in insights:
            text += f"• {insight}\n"

        text += "\n--- Recommendations ---\n"
        for rec in recommendations:
            text += f"• {rec}\n"

        return text
