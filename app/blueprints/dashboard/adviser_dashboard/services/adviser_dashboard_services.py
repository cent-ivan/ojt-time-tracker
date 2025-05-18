class AdviserDashboardServices:
    @staticmethod
    def compute_total_hours(timesheet) -> int:
        total = 0
        for time in timesheet:
            total += time['hours_worked']

        return total
    
    @staticmethod
    def compute_remaining_days(remaining_hours:int) -> int:
        return (remaining_hours // 8)