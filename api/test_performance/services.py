from .models import TestPerformance


class TestPerformanceService:
    model = TestPerformance

    def insert_one(self, data):
        self.model.collection.insert_one(data)


test_performance_service = TestPerformanceService()
