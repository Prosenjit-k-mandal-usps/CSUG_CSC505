import logging
from datetime import datetime

# Configure logging to file 'phts.log' with timestamp, level, and message
logging.basicConfig(
    filename='phts.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def log_and_print(message):
    """
    Log a message at INFO level and print it to the console.
    """
    logging.info(message)
    print(message)

class PotholeReport:
    """
    Represents a citizen's pothole report.
    """
    def __init__(self, report_id, address, size, location, district):
        self.report_id = report_id
        self.address = address
        self.size = size        # 1-10 severity scale
        self.location = location  # e.g., 'curb', 'middle'
        self.district = district
        self.priority = self._determine_priority()
        self.timestamp = datetime.now()
        log_and_print(f"PotholeReport created: {self}")

    def _determine_priority(self):
        # Simple mapping: higher size means higher priority
        if self.size >= 8:
            return 'High'
        elif self.size >= 4:
            return 'Medium'
        else:
            return 'Low'

    def __repr__(self):
        return (f"PotholeReport(id={self.report_id}, address='{self.address}', "
                f"size={self.size}, loc='{self.location}', dist='{self.district}', "
                f"priority='{self.priority}')")

class WorkOrder:
    """
    Represents a repair work order associated with a PotholeReport.
    """
    def __init__(self, report, crew_id, crew_size, equipment):
        self.report = report
        self.crew_id = crew_id
        self.crew_size = crew_size
        self.equipment = equipment  # List of equipment names
        self.hours = 0.0
        self.material_used = 0.0  # in kg
        self.status = 'Not Started'
        self.cost = 0.0
        log_and_print(f"WorkOrder created for report {report.report_id}")

    def log_repair(self, hours, material, rate_per_hour=50, cost_per_kg=2):
        """
        Update work order with repair details and recompute cost.
        """
        self.hours += hours
        self.material_used += material
        labor_cost = hours * self.crew_size * rate_per_hour
        material_cost = material * cost_per_kg
        self.cost = labor_cost + material_cost
        self.status = 'In Progress'
        log_and_print(
            f"WorkOrder {self.report.report_id}: logged {hours}h, {material}kg, cost={self.cost:.2f}"
        )

    def complete_repair(self):
        """
        Mark work order as completed.
        """
        self.status = 'Repaired'
        log_and_print(f"WorkOrder {self.report.report_id} completed. Total cost: {self.cost:.2f}")

class DamageClaim:
    """
    Represents a citizen's damage claim related to a specific pothole.
    """
    def __init__(self, report, claimant_name, claimant_address, phone, damage_type, amount):
        self.report = report
        self.name = claimant_name
        self.address = claimant_address
        self.phone = phone
        self.damage_type = damage_type
        self.amount = amount
        self.claim_id = f"C{report.report_id}-{int(datetime.now().timestamp())}"
        log_and_print(f"DamageClaim created: {self}")

    def __repr__(self):
        return (f"DamageClaim(id={self.claim_id}, report={self.report.report_id}, "
                f"name='{self.name}', amount=${self.amount:.2f})")

class PHTRS:
    """
    Core system to track reports, work orders, and claims.
    """
    def __init__(self):
        self.reports = {}
        self.work_orders = {}
        self.claims = {}
        self.next_report_id = 1
        log_and_print("PHTRS system initialized.")

    def report_pothole(self, address, size, location, district):
        report = PotholeReport(self.next_report_id, address, size, location, district)
        self.reports[self.next_report_id] = report
        self.next_report_id += 1
        return report

    def assign_work_order(self, report_id, crew_id, crew_size, equipment):
        report = self.reports.get(report_id)
        if not report:
            log_and_print(f"Error: Report {report_id} not found.")
            return None
        order = WorkOrder(report, crew_id, crew_size, equipment)
        self.work_orders[report_id] = order
        return order

    def log_repair_details(self, report_id, hours, material):
        order = self.work_orders.get(report_id)
        if order:
            order.log_repair(hours, material)
        else:
            log_and_print(f"Error: WorkOrder for report {report_id} not found.")

    def complete_repair(self, report_id):
        order = self.work_orders.get(report_id)
        if order:
            order.complete_repair()
        else:
            log_and_print(f"Error: WorkOrder for report {report_id} not found.")

    def submit_damage_claim(self, report_id, name, address, phone, damage_type, amount):
        report = self.reports.get(report_id)
        if not report:
            log_and_print(f"Error: Report {report_id} not found.")
            return None
        claim = DamageClaim(report, name, address, phone, damage_type, amount)
        self.claims[claim.claim_id] = claim
        return claim

# Example Usage
if __name__ == "__main__":
    system = PHTRS()

    # Citizen reports a pothole
    r1 = system.report_pothole("123 Main St", size=7, location="curb", district="North")

    # Dispatcher assigns a work order
    wo = system.assign_work_order(r1.report_id, crew_id=42, crew_size=3, equipment=["Truck", "Shovel"])

    # Crew logs repair progress
    system.log_repair_details(r1.report_id, hours=2.5, material=50)
    system.complete_repair(r1.report_id)

    # Citizen submits damage claim
    claim = system.submit_damage_claim(r1.report_id, "Jane Doe", "456 Oak Ave", "555-1234", "Flat tire", amount=100.00)

    log_and_print("Final Data: Reports, Work Orders, Claims stored in memory.")