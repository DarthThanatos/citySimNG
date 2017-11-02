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
    private CurrentPricesSender currentPricesSender;

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

        currentPricesSender = new CurrentPricesSender(this, dispatchCenter.getEventBus());
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

    public HashMap<String, Integer> getCurrentPrices(){
        //TODO, actual prices and synchronized block
        return new HashMap<String, Integer>() {
            {
                put("Oil",3);
                put("Gold", -5);
                put("Wood", -2);
                put("Stone", -6);
                put("Bread", 7);
                put("Crop", 5);
                put("Oil1",3);
                put("Gold1", -5);
                put("Woo1d", -2);
                put("Sto1ne", -6);
                put("Bre1ad", 7);
                put("Cro1p", 5);
                put("Oi21l",3);
                put("G122old", -5);
                put("Wo21od", -2);
                put("St2one", -6);
                put("Br2ead", 7);
                put("C2rop", 5);
                put("O3il",3);
                put("Go3ld", -5);
                put("W33ood", -2);
                put("St3one", -6);
                put("Br3ead", 7);
                put("Cr3op", 5);
                put("O4il",3);
                put("Go4ld", -5);
                put("W4ood", -2);
                put("St4one", -6);
                put("Br4ead", 7);
                put("Cr5op", 5);
                put("Oi5l",3);
                put("G5old", -5);
                put("Wo5od", -2);
                put("Sto5ne", -6);
                put("Bre5ad", 7);
                put("Cr5op", 5);
                put("Oi6l",3);
                put("Go6ld", -5);
                put("Wo6od", -2);
                put("S6tone", -6);
                put("B6read", 7);
                put("Cr6op", 5);
                put("O7il",3);
                put("G7old", -5);
                put("Woo7d", -2);
                put("St7one", -6);
                put("Bre7ad", 7);
                put("Cr7op", 5);

            }
        };
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
