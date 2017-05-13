package exchangenode;

import java.util.*;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;
import exchange.RepresenterMock;
import exchange.Stock;
import exchange.StockAlgorithm;
import exchange.StockTable;

public class ExchangeNode implements Node{

	private Node parent;
	private HashMap<String, Node> neighbors;
	private DependenciesRepresenter dr;
	private DispatchCenter dispatchCenter;
	private String nodeName;
	StockTable stockTable;
	Stock stock;

	public ExchangeNode(DependenciesRepresenter dr, DispatchCenter dispatchCenter, String nodeName){
		System.out.println("Created Exchange Node");
		neighbors = new HashMap<String, Node>();
		this.nodeName = nodeName;
		this.dr = dr;
		this.dispatchCenter = dispatchCenter;
		List<String> resourcesNames = dr.getResourcesNames();
		/*
		List<String> resourcesNames = new ArrayList<String>();
		resourcesNames.add("gold");
		resourcesNames.add("silver");
		resourcesNames.add("copper");*/
		stock = new Stock();
		stock.init(resourcesNames);
		RepresenterMock player = new RepresenterMock(resourcesNames);
		stockTable = new StockTable(stock);
		stock.setPlayer(player);
		stock.setDependenciesRepresenter(dr);
		// this thread simulates stock's price changes in the background
		Runnable stockThread = new Runnable() {
			public void run() {
				new StockAlgorithm().simulate(stock);
			}
		};
		new Thread(stockThread).start();
	}

	@Override
	public Node nodeLoop() {
		stock.setWorking(false);
 		stockTable.setVisible(true);
		return parent;
	}

	@Override
	public void setParent(String parentName, Node parent) {
		this.parent = parent;
		neighbors.put(parentName, parent);
	}

	@Override
	public void addNeighbour(String hashKey, Node neighbor) {
		neighbors.put(hashKey, neighbor);
	}

	@Override
	public void atUnload() {
		// TODO Auto-generated method stub
		
	}
	
	public String getNodeName(){
		return nodeName;
	}

}
