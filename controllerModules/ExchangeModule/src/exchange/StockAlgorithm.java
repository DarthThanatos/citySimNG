package exchange;

import java.util.Random;

public class StockAlgorithm {

	private Random rand = new Random();

	public void simulate(Stock stock) {
		while (true) {
			if(stock.isWorking()) {
				for(Resource resource: stock.getResources()) {
					double delta = rand.nextDouble() - 0.4;
					resource.update(delta);
				}
			}
			try {
				Thread.sleep(500);
			} catch (InterruptedException ie) {
			}
		}
	}
}

