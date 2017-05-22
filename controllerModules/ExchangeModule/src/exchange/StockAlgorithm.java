package exchange;

import java.util.Random;

public class StockAlgorithm {

	private Random random = new Random();

	public void simulateStock(Stock stock) {
		while (true) {
			if (stock.getWorkingStatus()) {
				for (Resource resource : stock.getResources()) {
					double delta = random.nextDouble() - 0.45;
					double newPrice = resource.getPrice() + resource.getPrice() * delta;
					resource.setPrice(newPrice);
					resource.setQuantity(resource.getQuantity() + 3);
					stock.updatePriceHistory(newPrice, resource.getName());
				}
			}
			try {
				Thread.sleep(500);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
}
