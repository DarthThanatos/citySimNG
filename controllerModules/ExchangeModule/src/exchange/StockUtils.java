package exchange;

import model.DependenciesRepresenter;

import java.util.*;

import static exchange.StockConfig.*;

class StockUtils {

    private static Random random = new Random();

    static String buyOperation(Resource resource, String stringQuantity, DependenciesRepresenter dependenciesRepresenter) {

        int quantity;
        try {
            quantity = Integer.parseInt(stringQuantity);
        } catch (Exception e) {
            return "ERROR - you entered wrong value, integer number is expected";
        }

        if (quantity * resource.getPrice() > dependenciesRepresenter.getMoney()) {
            return "WARNING - you don't have enough money";
        } else if (quantity > resource.getStockQuantity()) {
            return "WARNING - not enough resources in stock";
        } else {
            dependenciesRepresenter.setMoney(dependenciesRepresenter.getMoney() - quantity * resource.getPrice());
            dependenciesRepresenter.getStockPile().put(resource.getName(),
                    dependenciesRepresenter.getStockPile().get(resource.getName()) + quantity);
            resource.setStockQuantity(resource.getStockQuantity() - quantity);
            resource.setPlayerQuantity(dependenciesRepresenter.getStockPile().get(resource.getName()));
            return "You bought " + stringQuantity + " of " + resource.getName() + ", and now have "
                    + dependenciesRepresenter.getStockPile().get(resource.getName()) + " " + resource.getName()
                    + " and " + String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
        }
    }

    static String sellOperation(Resource resource, String stringQuantity, DependenciesRepresenter dependenciesRepresenter) {

        int quantity;
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
            resource.setStockQuantity(resource.getStockQuantity() + quantity);
            resource.setPlayerQuantity(dependenciesRepresenter.getStockPile().get(resource.getName()));
            return "You sold " + stringQuantity + " of " + resource.getName() + ", and now have "
                    + dependenciesRepresenter.getStockPile().get(resource.getName()) + " " + resource.getName()
                    + " and " + String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
        }
    }

    static String diceOperation(DependenciesRepresenter dependenciesRepresenter, List<Resource> resources) {
        if (DICE_OPERATION_PRICE > dependenciesRepresenter.getMoney()) {
            return "WARNING - you need 10 money to roll the dice, you have "
                    + String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
        } else {
            if (random.nextInt(100) + 1 >= DICE_OPERATION_WIN_CHANCE) {
                dependenciesRepresenter.setMoney(dependenciesRepresenter.getMoney() - DICE_OPERATION_PRICE);
                return "You won nothing, and now have " + String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
            }
            Resource resource = resources.get(random.nextInt(resources.size()));
            int wonQuantity = 1 + random.nextInt(DICE_OPERATION_MAX_WIN_QUANTITY);
            dependenciesRepresenter.getStockPile().put(resource.getName(),
                    dependenciesRepresenter.getStockPile().get(resource.getName()) + wonQuantity);
            dependenciesRepresenter.setMoney(dependenciesRepresenter.getMoney() - DICE_OPERATION_PRICE);
            resource.setPlayerQuantity(dependenciesRepresenter.getStockPile().get(resource.getName()));
            return "You won " + wonQuantity + " of " + resource.getName() + ", and now have "
                    + dependenciesRepresenter.getStockPile().get(resource.getName()) + " " + resource.getName()
                    + " and " + String.format("%.2f", dependenciesRepresenter.getMoney()) + " money";
        }
    }

    static void updateCurrentPrices(Map<String, Double> currentPrices, List<Resource> stockResources) {
        if (currentPrices.isEmpty()) {
            for (Resource resource : stockResources) {
                currentPrices.put(resource.getName(), resource.getPrice());
            }
        } else {
            for (Resource resource : stockResources) {
                double currentPrice = resource.getPrice().intValue();
                if (currentPrices.get(resource.getName()) > currentPrice) {
                    currentPrice = -currentPrice;
                }
                currentPrices.put(resource.getName(), currentPrice);
            }
        }
    }

    static HashMap<String, Integer> getIntMapFromDouble(Map<String, Double> currentPrices) {
        HashMap<String, Integer> currentPricesInt = new HashMap<>();
        for (String resourceName : currentPrices.keySet()) {
            currentPricesInt.put(resourceName, currentPrices.get(resourceName).intValue());
        }
        return currentPricesInt;
    }
}
