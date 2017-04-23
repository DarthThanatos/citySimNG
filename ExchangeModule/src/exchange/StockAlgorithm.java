package exchange;

import java.util.*;

public class StockAlgorithm {

	private Random rand = new Random();

	public void simulate(Stock stock) {
		while (stock.isWorking()) {
			int whichResource = Math.abs(rand.nextInt()) % stock.getResources().size();
			double delta = rand.nextDouble() - 0.4;
			double oldPrice = stock.getResources().get(whichResource).getPrice();
			stock.getResources().get(whichResource).update(delta);
			try {
				Thread.sleep(1000);
			} 
			catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
}
