
class HuntReportData:
    def __init__(self):
        self.success = 0
        self.fail = 0
        self.fail_roll = 0
        self.no_prey = 0
        self.no_prey_at_all = 0

    def __str__(self):
        return "success: {} fail: {} fail_roll: {} no_prey: {} no_prey_at_all: {}".format(self.success, self.fail, self.fail_roll, self.no_prey, self.no_prey_at_all)

    def __repr__(self):
        return self.__str__()

class HuntReport:
    def __init__(self):
        self.hunt_report = {}
    
    def add_success(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].success += 1
    
    def add_fail(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].fail += 1

    def add_fail_roll(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].fail_roll += 1

    def add_no_prey(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].no_prey += 1
    
    def add_no_prey_at_all(self, role):
        if role not in self.hunt_report:
            self.hunt_report[role] = HuntReportData()
        self.hunt_report[role].no_prey_at_all += 1

    def __str__(self):
        return str(self.hunt_report)

    def __repr__(self):
        return self.__str__()
