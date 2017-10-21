package exchange;

import java.util.Random;

public class StockAlgorithm {

    private Random random = new Random();

    public void simulateStock(Stock stock) {
        while (true) {
            if (stock.getWorkingStatus()) {
                int averageQuantity = stock.getAverageResourceQuantity();
                double averagePrice = stock.getAverageResourcePrice();
                for (Resource resource : stock.getStockResources()) {
                    double delta = (random.nextDouble() - 0.50) % 0.10;

                    if (averageQuantity > resource.getStockQuantity() * 2) {
                        delta = delta + (random.nextDouble() % 0.05);
                    } else if (averageQuantity < resource.getStockQuantity() / 2) {
                        delta = delta - (random.nextDouble() % 0.05);
                    }

                    if (averagePrice > resource.getPrice() * 2) {
                        delta = delta + (random.nextDouble() % 0.05);
                    } else if (averagePrice < resource.getPrice() / 2) {
                        delta = delta - (random.nextDouble() % 0.05);
                    }

                    double newPrice = resource.getPrice() + resource.getPrice() * delta;
                    resource.setPrice(newPrice);
                    resource.setStockQuantity(resource.getStockQuantity() + random.nextInt(2));
                    stock.updatePriceHistory(newPrice, resource.getName());
                }
            }
            try {
                Thread.sleep(300);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
