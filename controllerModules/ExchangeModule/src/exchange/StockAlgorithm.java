package exchange;

import java.util.Random;

public class StockAlgorithm {

    private static final double priceGrowFactor = 0.01;
    private static final int quantityGrowFactor = 2;
    private static final double quantityPriceRatioFactor = 2.5;
    private static final int priceUpdateSpeed = 3000;
    private static final int bearMarketLength = 10;
    private static final int bullMarketLength = 10;
    private static final double bearMarketGrowFactor = -0.01;
    private static final double bullMarketGrowFactor = 0.01;
    private static final int specialEventChance = 10;

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
                Thread.sleep(priceUpdateSpeed);
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
        resource.setStockQuantity(resource.getStockQuantity() + random.nextInt(quantityGrowFactor));
        stock.updatePriceHistory(newPrice, resource.getName());
    }

    private double calculateResourceDelta(Resource resource) {

        double averageQuantityPriceRatio = stock.getAverageQuantityPriceRatio();
        double delta = (random.nextDouble() - 0.50) % priceGrowFactor;

        if (resource.getQuantityPriceRatio() > quantityPriceRatioFactor * averageQuantityPriceRatio) {
            delta = delta + priceGrowFactor;
        } else if (resource.getQuantityPriceRatio() < averageQuantityPriceRatio / quantityPriceRatioFactor) {
            delta = delta - priceGrowFactor;
        }
        return delta;

    }

    private void drawForSpecialEvent() {
        if (bullMarketTurnsLeft == 0 && bearMarketTurnsLeft == 0) {
            int randomNumber = random.nextInt(100) + 1;
            if (randomNumber <= specialEventChance) {
                if (randomNumber % 2 == 0) {
                    System.out.println("Entering bear market");
                    bearMarketTurnsLeft = bearMarketLength;
                } else {
                    System.out.println("Entering bull market");
                    bullMarketTurnsLeft = bullMarketLength;
                }
            }
        }
    }

    private void checkForBearMarket() {
        if (bearMarketTurnsLeft > 0) {
            bearMarketTurnsLeft--;
            for (Resource resource : stock.getStockResources()) {
                updateResourcePrice(resource, bearMarketGrowFactor);
            }
        }
    }

    private void checkForBullMarket() {
        if (bullMarketTurnsLeft > 0) {
            bullMarketTurnsLeft--;
            for (Resource resource : stock.getStockResources()) {
                updateResourcePrice(resource, bullMarketGrowFactor);
            }
        }
    }
}
