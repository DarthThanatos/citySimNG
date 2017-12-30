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
    private final Stock stock;
    private CurrentPricesSender currentPricesSender;


    public Node getParent(){
        return parent;
    }

    public Node getNeighbour(String neighbourHash){
        return neighbors.get(neighbourHash);
    }

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
        Thread stockThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());
        stockThread.start();

        // thread for view modelling
        Thread thread = new Thread(() -> StockView.initStockView(stock, dependenciesRepresenter));
        thread.start();

        currentPricesSender = new CurrentPricesSender(this, dispatchCenter.getEventBus());
    }

    @Override
    public Node nodeLoop() {
        synchronized (stock) {
            StockView.stock.setWorkingStatus(false);
        }
        StockView.show();
        return parent;
    }

    @Override
    public void setParent(String parentName, Node parent) {
        this.parent = parent;
        neighbors.put(parentName, parent);
    }

    public HashMap<String, Integer> getCurrentPrices() {
        return stock.updateAndGetCurrentPrices();
    }

    @Override
    public void addNeighbour(String hashKey, Node neighbor) {
        neighbors.put(hashKey, neighbor);
    }

    @Override
    public void atUnload() {
        currentPricesSender.atUnload();
    }

    public String getNodeName() {
        return nodeName;
    }

}
