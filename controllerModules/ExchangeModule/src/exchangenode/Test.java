package exchangenode;

import java.util.*;
import controlnode.Node;
import exchange.*;

// this class is only for testing purposes
public class Test {

	public static void main(String[] args) {

		List<String> resourcesNames = new ArrayList<String>();
		resourcesNames.add("gold");
		resourcesNames.add("silver");
		resourcesNames.add("copper");

		RepresenterMock player = new RepresenterMock(resourcesNames);

		Stock stock = new Stock();
		stock.init(resourcesNames);
		stock.setPlayer(player);

		Thread stockAlgorithmThread = new Thread( () -> { new StockAlgorithm().simulate(stock); } );
		stockAlgorithmThread.start();

        StockTable.stock = stock;
        Thread stockTableThread = new Thread( () -> StockTable.show() );
        stockTableThread.start();

        Scanner input = new Scanner(System.in);
        String command = "hi";
        try {
			Thread.sleep(400);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

        while(!command.startsWith("exit")) {
        	stock.setWorking(false);
        	System.out.println("Showing stock");
        	StockTable.again();
        	command = input.nextLine();
        }

        input.close();

	}

}
