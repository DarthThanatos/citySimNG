package exchangenode;

import java.util.*;

import model.DependenciesRepresenter;
import controlnode.Node;
import exchange.RepresenterMock;
import exchange.Stock;
import exchange.StockAlgorithm;
import exchange.StockTable;

public class ExchangeNode implements Node{

	private Node parent;
	private HashMap<String, Node> neighbors;
	
	public ExchangeNode(DependenciesRepresenter dr){
		System.out.println("Created Exchange Node");
		neighbors = new HashMap<String, Node>();
	}
	
	
	
	@Override
	public Node nodeLoop() {		
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
		return null;
	}



	@Override
	public void setParent(String parentName, Node parent) {
		// TODO Auto-generated method stub
		this.parent = parent;
	}



	@Override
	public void addNeighbour(String hashKey, Node neighbor) {
		// TODO Auto-generated method stub
		neighbors.put(hashKey, neighbor);
	}
}
