package exchangenode;

import java.util.*;
import controlnode.Node;
import exchange.*;
import model.DependenciesRepresenter;

// this class is only for testing purposes
public class Test {

	public static void main(String[] args) {

		List<String> resourcesNames = new ArrayList<String>();
		Map<String, Integer> stockPile = new HashMap<>();
		resourcesNames.add("gold");
		stockPile.put("gold", 100);
		resourcesNames.add("silver");
		stockPile.put("silver", 100);
		resourcesNames.add("copper");
		stockPile.put("copper", 100);

		DependenciesRepresenter dependenciesRepresenter = new DependenciesRepresenter();
		dependenciesRepresenter.setResourcesNames(resourcesNames);
		dependenciesRepresenter.setMoney(1000);
		dependenciesRepresenter.setStockPile(stockPile);

		Stock stock = new Stock();
		stock.setDependenciesRepresenter(dependenciesRepresenter);
		stock.init();

		Thread stockAlgorithmThread = new Thread(() -> {
			new StockAlgorithm().simulateStock(stock);
		});
		stockAlgorithmThread.start();

		StockView.setStock(stock);
		Thread stockTableThread = new Thread(() -> StockView.initStockView());
		stockTableThread.start();

		Scanner input = new Scanner(System.in);
		String command = "hi";
		try {
			Thread.sleep(400);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		while (!command.startsWith("exit")) {
			stock.setWorkingStatus(false);
			System.out.println("Showing stock");
			StockView.show();
			command = input.nextLine();
		}

		input.close();
	}

}