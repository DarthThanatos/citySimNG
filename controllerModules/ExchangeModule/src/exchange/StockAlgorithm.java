package exchange;

import java.util.Random;

public class StockAlgorithm {

	private Random random = new Random();

	public void simulateStock(Stock stock) {
		while (true) {
			if (stock.getWorkingStatus()) {
				int averageQuantity = stock.getAverageResourceQuantity();
				for (Resource resource : stock.getResources()) {
					double delta;
					if (resource.getQuantity() > averageQuantity * 2) {
						delta = (random.nextDouble() - 1) % 0.10;
					} else if (resource.getQuantity() * 2 < averageQuantity) {
						delta = random.nextDouble() % 0.10;
					} else {
						delta = (random.nextDouble() - 0.50) % 0.10;
					}
					double newPrice = resource.getPrice() + resource.getPrice() * delta;
					resource.setPrice(newPrice);
					resource.setQuantity(resource.getQuantity() + random.nextInt(3));
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
