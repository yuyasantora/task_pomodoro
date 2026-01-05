from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
from ..core.session import SessionData


class FocusAnalyzer:
    def __init__(self, sessions: List[SessionData]):
        self.sessions = sessions
        self.work_sessions = [s for s in sessions if s.session_type == "work"]

    def analyze_time_of_day(self) -> Dict:
        hour_stats = defaultdict(lambda: {"total": 0, "completed": 0, "skipped": 0})

        for session in self.work_sessions:
            hour = session.start_time.hour
            hour_stats[hour]["total"] += 1
            if session.was_completed:
                hour_stats[hour]["completed"] += 1
            elif session.was_skipped:
                hour_stats[hour]["skipped"] += 1

        completion_rates = {}
        for hour, stats in hour_stats.items():
            if stats["total"] > 0:
                completion_rates[hour] = stats["completed"] / stats["total"]

        return {
            "hour_stats": dict(hour_stats),
            "completion_rates": completion_rates,
            "best_hour": max(completion_rates.items(), key=lambda x: x[1])[0] if completion_rates else None
        }

    def analyze_duration_patterns(self) -> Dict:
        if not self.work_sessions:
            return {"average_duration": 0, "completion_rate_by_duration": {}}

        durations = [s.actual_duration for s in self.work_sessions]
        avg_duration = statistics.mean(durations) if durations else 0

        duration_buckets = defaultdict(lambda: {"total": 0, "completed": 0})
        for session in self.work_sessions:
            bucket = (session.planned_duration // 300) * 300
            duration_buckets[bucket]["total"] += 1
            if session.was_completed:
                duration_buckets[bucket]["completed"] += 1

        completion_by_duration = {}
        for duration, stats in duration_buckets.items():
            if stats["total"] > 0:
                completion_by_duration[duration] = stats["completed"] / stats["total"]

        return {
            "average_duration": avg_duration,
            "completion_rate_by_duration": completion_by_duration
        }

    def calculate_completion_rate(self) -> float:
        if not self.work_sessions:
            return 0.0

        completed = sum(1 for s in self.work_sessions if s.was_completed)
        return completed / len(self.work_sessions)

    def analyze_weekly_pattern(self) -> Dict:
        weekday_stats = defaultdict(lambda: {"total": 0, "completed": 0})

        for session in self.work_sessions:
            weekday = session.start_time.weekday()
            weekday_stats[weekday]["total"] += 1
            if session.was_completed:
                weekday_stats[weekday]["completed"] += 1

        completion_by_weekday = {}
        for day, stats in weekday_stats.items():
            if stats["total"] > 0:
                completion_by_weekday[day] = stats["completed"] / stats["total"]

        return {
            "weekday_stats": dict(weekday_stats),
            "completion_by_weekday": completion_by_weekday
        }

    def analyze_pause_patterns(self) -> Dict:
        if not self.work_sessions:
            return {"average_pauses": 0, "pause_impact": 0}

        pauses = [s.pause_count for s in self.work_sessions]
        avg_pauses = statistics.mean(pauses) if pauses else 0

        paused_sessions = [s for s in self.work_sessions if s.pause_count > 0]
        no_pause_sessions = [s for s in self.work_sessions if s.pause_count == 0]

        paused_completion = sum(1 for s in paused_sessions if s.was_completed) / len(paused_sessions) if paused_sessions else 0
        no_pause_completion = sum(1 for s in no_pause_sessions if s.was_completed) / len(no_pause_sessions) if no_pause_sessions else 0

        return {
            "average_pauses": avg_pauses,
            "paused_completion_rate": paused_completion,
            "no_pause_completion_rate": no_pause_completion,
            "pause_impact": no_pause_completion - paused_completion
        }
