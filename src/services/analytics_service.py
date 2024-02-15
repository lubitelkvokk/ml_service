from src.repositories.TransactionRepository import transaction_repository
import matplotlib.pyplot as plt

class AnalyticsService:
    async def plot_total_credits_by_date(self):
        data = await transaction_repository.get_data_by_data()
        dates, total_credits = zip(*data)
        plt.figure(figsize=(10, 6))
        plt.plot(dates, total_credits, marker='o')
        plt.title("Total Credits by Date")
        plt.xlabel("Date")
        plt.ylabel("Total Credits")
        plt.grid(True)
        plt.show()

analytics_service = AnalyticsService()