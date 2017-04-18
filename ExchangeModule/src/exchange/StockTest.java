package exchange;

import java.util.*;

public class StockTest {

	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
		String line = "";
		List<String> resourcesNames = new ArrayList<>();
		resourcesNames.add("gold");
		resourcesNames.add("silver");
		resourcesNames.add("copper");
		Stock stock = new Stock();
		stock.init(resourcesNames);

		Runnable stockThread = new Runnable() {
			public void run() {
				new StockAlgorithm().simulate(stock);
			}
		};

		RepresenterMock player = new RepresenterMock(resourcesNames);
		new Thread(stockThread).start();
		StockTable stockTable = new StockTable(stock);
		while(!line.startsWith("exit")) {
			System.out.println("Type 'stack' to open stack module");
			line = input.nextLine();
			if(line.startsWith("stack")) {
				stock.setWorking(false);
				stock.setPlayer(player);
		 		stockTable.setVisible(true);
			}
		}
		input.close();
	}
}
