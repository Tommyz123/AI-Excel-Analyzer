"""
Cost Controller Module
Tracks and limits API usage to control costs
"""

import json
import os
from datetime import datetime
from typing import Tuple, Dict
from config import Config


class CostController:
    """
    API cost controller
    Tracks usage and enforces limits
    """
    
    def __init__(self, 
                 max_daily_calls: int = None,
                 max_weekly_calls: int = None,
                 usage_file: str = ".api_usage.json"):
        """
        Initialize cost controller
        
        Args:
            max_daily_calls: Maximum API calls per day
            max_weekly_calls: Maximum API calls per week
            usage_file: File to store usage data
        """
        self.max_daily_calls = max_daily_calls or Config.MAX_DAILY_API_CALLS
        self.max_weekly_calls = max_weekly_calls or Config.MAX_WEEKLY_API_CALLS
        self.usage_file = usage_file
    
    def _load_usage(self) -> Dict:
        """Load usage data from file"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
            except:
                return {"daily": {}, "weekly": {}}
        return {"daily": {}, "weekly": {}}
    
    def _save_usage(self, usage: Dict):
        """Save usage data to file"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(usage, f)
        except:
            pass  # Fail silently
    
    def can_make_call(self) -> Tuple[bool, str]:
        """
        Check if API call can be made
        
        Returns:
            Tuple[bool, str]: (can_call, message)
        """
        usage = self._load_usage()
        today = datetime.now().strftime("%Y-%m-%d")
        week = datetime.now().strftime("%Y-W%W")
        
        daily_count = usage["daily"].get(today, 0)
        weekly_count = usage["weekly"].get(week, 0)
        
        if daily_count >= self.max_daily_calls:
            return False, f"Daily limit reached ({self.max_daily_calls} calls). Resets tomorrow."
        
        if weekly_count >= self.max_weekly_calls:
            return False, f"Weekly limit reached ({self.max_weekly_calls} calls). Resets next week."
        
        return True, "OK"
    
    def record_call(self):
        """Record an API call"""
        usage = self._load_usage()
        today = datetime.now().strftime("%Y-%m-%d")
        week = datetime.now().strftime("%Y-W%W")
        
        usage["daily"][today] = usage["daily"].get(today, 0) + 1
        usage["weekly"][week] = usage["weekly"].get(week, 0) + 1
        
        self._save_usage(usage)
    
    def get_usage_stats(self) -> Dict:
        """
        Get current usage statistics
        
        Returns:
            Dict: Usage statistics
        """
        usage = self._load_usage()
        today = datetime.now().strftime("%Y-%m-%d")
        week = datetime.now().strftime("%Y-W%W")
        
        daily_count = usage["daily"].get(today, 0)
        weekly_count = usage["weekly"].get(week, 0)
        
        # Estimate cost (GPT-3.5-turbo: ~$0.001 per query)
        estimated_cost_week = weekly_count * 0.001
        estimated_cost_month = estimated_cost_week * 4
        
        return {
            "daily_calls": daily_count,
            "weekly_calls": weekly_count,
            "daily_remaining": max(0, self.max_daily_calls - daily_count),
            "weekly_remaining": max(0, self.max_weekly_calls - weekly_count),
            "estimated_cost_week": estimated_cost_week,
            "estimated_cost_month": estimated_cost_month,
            "daily_limit": self.max_daily_calls,
            "weekly_limit": self.max_weekly_calls
        }
    
    def reset_daily(self):
        """Reset daily counter (for testing)"""
        usage = self._load_usage()
        today = datetime.now().strftime("%Y-%m-%d")
        if today in usage["daily"]:
            del usage["daily"][today]
        self._save_usage(usage)
    
    def reset_weekly(self):
        """Reset weekly counter (for testing)"""
        usage = self._load_usage()
        week = datetime.now().strftime("%Y-W%W")
        if week in usage["weekly"]:
            del usage["weekly"][week]
        self._save_usage(usage)
