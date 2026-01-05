from typing import List
from .analyzer import FocusAnalyzer


class SuggestionGenerator:
    def __init__(self, analyzer: FocusAnalyzer):
        self.analyzer = analyzer

    def generate_insights(self) -> List[str]:
        insights = []

        completion_rate = self.analyzer.calculate_completion_rate()
        insights.append(f"Overall completion rate: {completion_rate * 100:.1f}%")

        time_analysis = self.analyzer.analyze_time_of_day()
        if time_analysis["best_hour"] is not None:
            best_hour = time_analysis["best_hour"]
            best_rate = time_analysis["completion_rates"][best_hour] * 100
            insights.append(f"Your focus is strongest at {best_hour}:00 ({best_rate:.1f}% completion)")

        pause_analysis = self.analyzer.analyze_pause_patterns()
        if pause_analysis["pause_impact"] > 0.1:
            insights.append(f"Sessions without pauses have {pause_analysis['pause_impact'] * 100:.1f}% higher completion rate")
        elif pause_analysis["pause_impact"] < -0.1:
            insights.append("Taking breaks during sessions may help maintain focus")

        weekly_analysis = self.analyzer.analyze_weekly_pattern()
        if weekly_analysis["completion_by_weekday"]:
            weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            best_day = max(weekly_analysis["completion_by_weekday"].items(), key=lambda x: x[1])
            worst_day = min(weekly_analysis["completion_by_weekday"].items(), key=lambda x: x[1])

            insights.append(f"Best day: {weekday_names[best_day[0]]} ({best_day[1] * 100:.1f}% completion)")
            insights.append(f"Most challenging day: {weekday_names[worst_day[0]]} ({worst_day[1] * 100:.1f}% completion)")

        duration_analysis = self.analyzer.analyze_duration_patterns()
        if duration_analysis["average_duration"] > 0:
            avg_minutes = duration_analysis["average_duration"] / 60
            insights.append(f"Average session duration: {avg_minutes:.1f} minutes")

        return insights

    def generate_recommendations(self) -> List[str]:
        recommendations = []

        completion_rate = self.analyzer.calculate_completion_rate()

        if completion_rate < 0.5:
            recommendations.append("Try shorter work sessions to improve completion rate")

        time_analysis = self.analyzer.analyze_time_of_day()
        if time_analysis["best_hour"] is not None:
            best_hour = time_analysis["best_hour"]
            recommendations.append(f"Schedule important tasks around {best_hour}:00 for maximum focus")

        pause_analysis = self.analyzer.analyze_pause_patterns()
        if pause_analysis["average_pauses"] > 2:
            recommendations.append("High pause frequency detected. Consider removing distractions")

        if pause_analysis["pause_impact"] > 0.2:
            recommendations.append("Minimize interruptions - your uninterrupted sessions are much more successful")

        return recommendations
