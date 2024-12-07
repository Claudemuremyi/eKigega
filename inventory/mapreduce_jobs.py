from mrjob.job import MRJob
from mrjob.step import MRStep

class InventoryAnalysisJob(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer)
        ]

    def mapper(self, _, line):
        # Split the CSV line and extract relevant data
        fields = line.split(',')
        if len(fields) >= 5:  # Ensure we have enough fields
            product_name = fields[1]
            stock_quantity = int(fields[3])
            yield (product_name, stock_quantity)

    def reducer(self, key, values):
        total_stock = sum(values)
        yield (key, total_stock)

if __name__ == '__main__':
    InventoryAnalysisJob.run()