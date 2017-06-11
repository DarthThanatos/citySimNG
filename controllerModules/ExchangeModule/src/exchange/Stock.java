package exchange;

import java.util.*;

import model.DependenciesRepresenter;

public class Stock {

    public static final int priceHistoryRange = 15;
    private DependenciesRepresenter dependenciesRepresenter;
    private List<Resource> resources = new ArrayList<>();
    private List<String> resourcesNames;
    private boolean workingStatus;
    private Map<String, Double[]> priceHistory = new HashMap<>();
    private Random random;

    public Stock() {
        random = new Random();
        this.setWorkingStatus(true);
    }

    public void setDependenciesRepresenter(DependenciesRepresenter dependenciesRepresenter) {
        this.dependenciesRepresenter = dependenciesRepresenter;
    }

    public DependenciesRepresenter getDependenciesRepresenter() {
        return dependenciesRepresenter;
    }

    public List<Resource> getResources() {
        return resources;
    }

    public List<String> getResourcesNames() {
        return resourcesNames;
    }

    public boolean getWorkingStatus() {
        return workingStatus;
    }

    public void setWorkingStatus(boolean working) {
        if (working) {
            System.out.println("Stock is working");
        } else {
            System.out.println("Stock is stopped");
        }
        this.workingStatus = working;
    }

    public Map<String, Double[]> getPriceHistory() {
        return priceHistory;
    }

    public void init() {
        this.resourcesNames = dependenciesRepresenter.getResourcesNames();
        for (String resourceName : this.resourcesNames) {
            resources.add(new Resource(resourceName, (random.nextDouble() + 1) * 10, random.nextInt(10)));
            Double[] history;
            history = new Double[priceHistoryRange];
            for (int i = 0; i < priceHistoryRange; i++) {
                history[i] = 0d;
            }
            priceHistory.put(resourceName, history);
        }
    }

    public Resource getResource(String name) {
        for (Resource resource : resources) {
            if (resource.getName().equals(name)) {
                return resource;
            }
        }
        return null;
    }

    public int getAverageResourceQuantity() {
        int averageQuantity = 0;
        for (Resource resource : resources) {
            averageQuantity = averageQuantity + resource.getQuantity();
        }
        return averageQuantity / resources.size();
    }

    public double getAverageResourcePrice() {
        double averagePrice = 0;
        for (Resource resource : resources) {
            averagePrice = averagePrice + resource.getPrice();
        }
        return averagePrice / resources.size();
    }

    public void updatePriceHistory(double newPrice, String resourceName) {
        Double[] historyTable = priceHistory.get(resourceName);
        System.arraycopy(historyTable, 1, historyTable, 0, priceHistoryRange - 1);
        historyTable[priceHistoryRange - 1] = newPrice;
    }

    public void updatePlayerResource() {
        for(Resource resource: resources) {
            resource.setPlayerQuantity(dependenciesRepresenter.getStockPile().get(resource.getName()));
        }

    }

    public void resetStock() {
        for(Resource resource: resources) {
            double newPrice = (random.nextDouble() + 1) * 10;
            resource.setPrice(newPrice);
            resource.setQuantity(0);
            Double[] historyTable = priceHistory.get(resource.getName());
            for(int i = 0; i < historyTable.length - 2; i++) {
                historyTable[i] = 0d;
            }
            historyTable[historyTable.length - 1] = newPrice;
        }
    }

    public String buyOperation(String resourceName, String stringQuantity) {
        int quantity;
        Resource resource = getResource(resourceName);

        try {
            quantity = Integer.parseInt(stringQuantity);
        } catch (Exception e) {
            return "ERROR - you entered wrong value, integer number is expected";
        }

        if (quantity * resource.getPrice() > dependenciesRepresenter.getMoney()) {
            return "WARNING - you don't have enough money";
        } else if (quantity > resource.getQuantity()) {
            return "WARNING - not enough resources in stock";
        } else {
            dependenciesRepresenter.setMoney(dependenciesRepresenter.getMoney() - quantity * resource.getPrice());
            dependenciesRepresenter.getStockPile().put(resource.getName(),
                    dependenciesRepresenter.getStockPile().get(resource.getName()) + quantity);
            resource.setQuantity(resource.getQuantity() - quantity);
            resource.setPlayerQuantity(dependenciesRepresenter.getStockPile().get(resourceName));
            return "You successfully bought " + stringQuantity + " of " + resource.getName() + ", and now have "
                    + dependenciesRepresenter.getStockPile().get(resource.getName()) + " " + resource.getName()
                    + " and " + String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
        }
    }

    public String sellOperation(String resourceName, String stringQuantity) {
        int quantity;
        Resource resource = getResource(resourceName);

        try {
            quantity = Integer.parseInt(stringQuantity);
        } catch (Exception e) {
            return "ERROR - you entered wrong value, integer number is expected";
        }

        if (quantity > dependenciesRepresenter.getStockPile().get(resource.getName())) {
            return "WARNING - you don't have enough resources to sell";
        } else {
            dependenciesRepresenter.setMoney(dependenciesRepresenter.getMoney() + quantity * resource.getPrice());
            dependenciesRepresenter.getStockPile().put(resource.getName(),
                    dependenciesRepresenter.getStockPile().get(resource.getName()) - quantity);
            resource.setQuantity(resource.getQuantity() + quantity);
            resource.setPlayerQuantity(dependenciesRepresenter.getStockPile().get(resourceName));
            return "You successfully sold " + stringQuantity + " of " + resource.getName() + ", and now have "
                    + dependenciesRepresenter.getStockPile().get(resource.getName()) + " " + resource.getName()
                    + " and " + String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
        }
    }

    public String diceOperation() {
        if (10 > dependenciesRepresenter.getMoney()) {
            return "WARNING - you need 10 money to roll the dice, you have "
                    + String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
        } else {
            if (random.nextInt(10) % 2 == 0) {
                dependenciesRepresenter.setMoney(dependenciesRepresenter.getMoney() - 10);
                return "You won nothing, and now have "+ String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
            }
            Resource resource = resources.get(random.nextInt(resources.size() - 1));
            int wonQuantity = (int) (random.nextInt(200) / resource.getPrice());
            dependenciesRepresenter.getStockPile().put(resource.getName(),
                    dependenciesRepresenter.getStockPile().get(resource.getName()) + wonQuantity);
            dependenciesRepresenter.setMoney(dependenciesRepresenter.getMoney() - 10);
            resource.setPlayerQuantity(dependenciesRepresenter.getStockPile().get(resource.getName()));
            return "You won " + wonQuantity + " of " + resource.getName() + ", and now have "
                    + dependenciesRepresenter.getStockPile().get(resource.getName()) + " " + resource.getName()
                    + " and " + String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
        }
    }
}
