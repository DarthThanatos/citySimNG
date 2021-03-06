package exchange;

import java.util.Random;

import static exchange.StockConfig.*;

public class StockAlgorithm {

    private Stock stock;
    private int bullMarketTurnsLeft;
    private int bearMarketTurnsLeft;
    private Random random;

    public StockAlgorithm(Stock stock) {
        this.stock = stock;
        random = new Random();
        bullMarketTurnsLeft = 0;
        bearMarketTurnsLeft = 0;
    }

    public void simulateStock() {

        //noinspection InfiniteLoopStatement
        while (true) {

            drawForSpecialEvent();

            if (stock.getWorkingStatus()) {
                calculateAndUpdateResources();
                checkForBearMarket();
                checkForBullMarket();
            }
            try {
                Thread.sleep(PRICE_UPDATE_SPEED);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
    }

    private void calculateAndUpdateResources() {
        for (Resource resource : stock.getStockResources()) {
            double delta = calculateResourceDelta(resource);
            updateResourcePrice(resource, delta);
        }
    }

    private void updateResourcePrice(Resource resource, double delta) {
        double newPrice = resource.getPrice() + resource.getPrice() * delta;
        resource.setPrice(newPrice);
        resource.setStockQuantity(resource.getStockQuantity() + random.nextInt(QUANTITY_GROW_FACTOR));
        stock.updatePriceHistory(newPrice, resource.getName());
    }

    private double calculateResourceDelta(Resource resource) {

        double averageQuantityPriceRatio = stock.getAverageQuantityPriceRatio();
        double averageQuantity = stock.getAverageQuantity();
        double averagePrice = stock.getAveragePrice();

        double delta = (random.nextDouble() - 0.50) % PRICE_GROW_FACTOR;

        if (resource.getQuantityPriceRatio() > QUANTITY_PRICE_RATIO_FACTOR * averageQuantityPriceRatio) {
            // too big quantity or too small price
            if (resource.getStockQuantity() > averageQuantity * QUANTITY_PRICE_RATIO_FACTOR) {
                resource.setStockQuantity(resource.getStockQuantity() - 2 * QUANTITY_GROW_FACTOR);
            }
            if (resource.getPrice() < averagePrice / QUANTITY_PRICE_RATIO_FACTOR) {
                delta = delta + 2 * PRICE_GROW_FACTOR;
            }
        } else if (resource.getQuantityPriceRatio() < averageQuantityPriceRatio / QUANTITY_PRICE_RATIO_FACTOR) {
            // too small quantity or too big price
            if (resource.getStockQuantity() < averageQuantity / QUANTITY_PRICE_RATIO_FACTOR) {
                resource.setStockQuantity(resource.getStockQuantity() + 2 * QUANTITY_GROW_FACTOR);
            }
            if (resource.getPrice() > averagePrice * QUANTITY_PRICE_RATIO_FACTOR) {
                delta = delta - 2 * PRICE_GROW_FACTOR;
            }
        }
        return delta;

    }

    private void drawForSpecialEvent() {
        if (bullMarketTurnsLeft == 0 && bearMarketTurnsLeft == 0) {
            int randomNumber = random.nextInt(100) + 1;
            if (randomNumber <= SPECIAL_EVENT_CHANCE) {
                if (randomNumber % 2 == 0) {
                    bearMarketTurnsLeft = SPECIAL_EVENT_LENGTH;
                } else {
                    bullMarketTurnsLeft = SPECIAL_EVENT_LENGTH;
                }
            }
        }
    }

    private void checkForBearMarket() {
        if (bearMarketTurnsLeft > 0) {
            bearMarketTurnsLeft--;
            for (Resource resource : stock.getStockResources()) {
                updateResourcePrice(resource, -SPECIAL_EVENT_GROW_FACTOR);
            }
        }
    }

    private void checkForBullMarket() {
        if (bullMarketTurnsLeft > 0) {
            bullMarketTurnsLeft--;
            for (Resource resource : stock.getStockResources()) {
                updateResourcePrice(resource, SPECIAL_EVENT_GROW_FACTOR);
            }
        }
    }
}
