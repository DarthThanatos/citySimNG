package exchangenode;

import java.util.*;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;
import exchange.*;

public class ExchangeNode implements Node {

    private Node parent;
    private HashMap<String, Node> neighbors = new HashMap<>();
    private DispatchCenter dispatchCenter;
    private String nodeName;
    private Stock stock;

    public ExchangeNode(DependenciesRepresenter dependenciesRepresenter, DispatchCenter dispatchCenter,
                        String nodeName) {

        // app logic settings
        this.nodeName = nodeName;
        this.dispatchCenter = dispatchCenter;

        // exchange module init
        stock = new Stock();
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();

        // thread for price algorithm
        Thread stockThread = new Thread(() -> new StockAlgorithm().simulateStock(stock));
        stockThread.start();

        // thread for view modelling
        Thread thread = new Thread(() -> StockView.initStockView(stock, dependenciesRepresenter));
        thread.start();
    }

    @Override
    public Node nodeLoop() {
        StockView.stock.setWorkingStatus(false);
        StockView.show();
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
        System.out.println("At unload Exchange");
    }

    public String getNodeName() {
        return nodeName;
    }

}
