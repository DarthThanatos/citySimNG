package exchange;

import java.util.*;

import model.DependenciesRepresenter;

public class Stock {

    static final int priceHistoryRange = 15;
    private DependenciesRepresenter dependenciesRepresenter;
    private List<Resource> stockResources;
    private List<String> stockResourcesNames;
    private boolean workingStatus;
    private Map<String, Double[]> priceHistory;
    private Random random;

    public Stock() {
        random = new Random();
        this.setWorkingStatus(true);
    }

    public void setDependenciesRepresenter(DependenciesRepresenter dependenciesRepresenter) {
        this.dependenciesRepresenter = dependenciesRepresenter;
    }

    DependenciesRepresenter getDependenciesRepresenter() {
        return dependenciesRepresenter;
    }

    List<Resource> getStockResources() {
        return stockResources;
    }

    List<String> getStockResourcesNames() {
        return stockResourcesNames;
    }

    boolean getWorkingStatus() {
        return workingStatus;
    }

    public void setWorkingStatus(boolean working) {
        this.workingStatus = working;
    }

    Map<String, Double[]> getPriceHistory() {
        return priceHistory;
    }

    public void init() {
        this.stockResourcesNames = dependenciesRepresenter.getResourcesNames();
        stockResources = new ArrayList<>();
        priceHistory = new HashMap<>();
        for (String resourceName : this.stockResourcesNames) {
            stockResources.add(new Resource(resourceName, (random.nextDouble() + 1) * 10, random.nextInt(10)));
            Double[] history;
            history = new Double[priceHistoryRange];
            for (int i = 0; i < priceHistoryRange; i++) {
                history[i] = 0d;
            }
            priceHistory.put(resourceName, history);
        }
    }

    Resource getResource(String name) {
        for (Resource resource : stockResources) {
            if (resource.getName().equals(name)) {
                return resource;
            }
        }
        return null;
    }

    double getAverageQuantityPriceRatio() {
        double ratio = 0.0;
        for (Resource resource : stockResources) {
            ratio = resource.getStockQuantity() / resource.getPrice();
        }
        return ratio / stockResources.size();
    }

    void updatePriceHistory(double newPrice, String resourceName) {
        Double[] historyTable = priceHistory.get(resourceName);
        System.arraycopy(historyTable, 1, historyTable, 0, priceHistoryRange - 1);
        historyTable[priceHistoryRange - 1] = newPrice;
    }

    void updatePlayerResource() {
        for (Resource resource : stockResources) {
            resource.setPlayerQuantity(dependenciesRepresenter.getStockPile().get(resource.getName()));
        }

    }

    String buyOperation(String resourceName, String stringQuantity) {
        Resource resource = getResource(resourceName);
        return StockUtils.buyOperation(resource, stringQuantity, dependenciesRepresenter);
    }

    String sellOperation(String resourceName, String stringQuantity) {
        Resource resource = getResource(resourceName);
        return StockUtils.sellOperation(resource, stringQuantity, dependenciesRepresenter);
    }

    String diceOperation() {
        return StockUtils.diceOperation(dependenciesRepresenter, stockResources);
    }
}
