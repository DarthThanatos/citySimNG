import exchange.Stock;
import exchange.StockAlgorithm;
import exchange.StockConfig;
import model.DependenciesRepresenter;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class IntegrationTests {

    private static final String RESOURCE_1 = "Gold";
    private static final String RESOURCE_2 = "Silver";

    @Mock
    private DependenciesRepresenter dependenciesRepresenter;

    @Before
    public void initialize() {
        dependenciesRepresenter = mock(DependenciesRepresenter.class);

        List<String> resourcesNames = new LinkedList<>();
        resourcesNames.add(RESOURCE_1);
        resourcesNames.add(RESOURCE_2);
        when(dependenciesRepresenter.getResourcesNames()).thenReturn(resourcesNames);

        StockConfig.setPropertyValue("PRICE_UPDATE_SPEED", "10");
    }

    @Test
    public void testSpecialEventTest() {
        // given
        StockConfig.setPropertyValue("SPECIAL_EVENT_CHANCE", "100");
        StockConfig.setPropertyValue("SPECIAL_EVENT_LENGTH", "3");
        StockConfig.setPropertyValue("SPECIAL_EVENT_GROW_FACTOR", "1.0");
        Stock stock = new Stock();
        Thread stockAlgorithmThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.setWorkingStatus(true);
        double priceBefore = stock.getResource(RESOURCE_1).getPrice();
        stockAlgorithmThread.start();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 20);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // then
        double priceAfter = stock.getResource(RESOURCE_1).getPrice();
        double factor = priceAfter / priceBefore;
        assertTrue("factor = " + factor, factor > 1.5 || factor < 0.15);
    }

    @Test
    public void priceGrowFactorTest() {
        // given
        StockConfig.setPropertyValue("PRICE_GROW_FACTOR", "0.5");
        Stock stock = new Stock();
        Thread stockAlgorithmThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.setWorkingStatus(true);
        double priceBefore = stock.getResource(RESOURCE_1).getPrice();
        stockAlgorithmThread.start();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 20);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // then
        double priceAfter = stock.getResource(RESOURCE_1).getPrice();
        double factor = priceAfter / priceBefore;
        assertTrue("factor = " + factor, factor > 0.5 || factor < 1.5);
    }

    @Test
    public void quantityGrowFactorTest() {
        // given
        StockConfig.setPropertyValue("QUANTITY_GROW_FACTOR", "5");
        Stock stock = new Stock();
        Thread stockAlgorithmThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.setWorkingStatus(true);
        int quantityBefore = stock.getResource(RESOURCE_1).getStockQuantity();
        stockAlgorithmThread.start();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 20);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // then
        int quantityAfter = stock.getResource(RESOURCE_1).getStockQuantity();
        assertNotEquals(quantityBefore, quantityAfter);
    }

    @Test
    public void diceTest() {
        // given
        Stock stock = new Stock();

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        Map<String, Integer> stockPile = new HashMap<>();
        stockPile.put(RESOURCE_1, 15);
        stockPile.put(RESOURCE_2, 10);
        when(dependenciesRepresenter.getStockPile()).thenReturn(stockPile);
        stock.updatePlayerResource();

        StockConfig.setPropertyValue("DICE_OPERATION_WIN_CHANCE", "100");
        when(dependenciesRepresenter.getMoney()).thenReturn(Double.valueOf(1000));
        String response1 = stock.diceOperation();

        StockConfig.setPropertyValue("DICE_OPERATION_WIN_CHANCE", "0");
        when(dependenciesRepresenter.getMoney()).thenReturn(Double.valueOf(1000));
        String response2 = stock.diceOperation();

        // then
        assertTrue(response1.contains("You won"));
        assertTrue(response2.contains("You won nothing, and now have"));
    }

    @Test
    public void tooBigQuantityResourceTest() {
        // given
        StockConfig.setPropertyValue("QUANTITY_PRICE_RATIO_FACTOR", "1.5");
        Stock stock = new Stock();
        Thread stockAlgorithmThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.getResource(RESOURCE_1).setStockQuantity(99);
        stock.getResource(RESOURCE_2).setStockQuantity(1);
        int quantityBefore = stock.getResource(RESOURCE_1).getStockQuantity();
        stock.setWorkingStatus(true);
        stockAlgorithmThread.start();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // then
        int quantityAfter = stock.getResource(RESOURCE_1).getStockQuantity();
        assertTrue(quantityAfter < quantityBefore);
    }

    @Test
    public void tooSmallPriceResourceTest() {
        // given
        StockConfig.setPropertyValue("QUANTITY_PRICE_RATIO_FACTOR", "1.5");
        Stock stock = new Stock();
        Thread stockAlgorithmThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.getResource(RESOURCE_1).setPrice(99.0);
        stock.getResource(RESOURCE_2).setPrice(1.0);
        double priceBefore = stock.getResource(RESOURCE_2).getPrice();
        stock.setWorkingStatus(true);
        stockAlgorithmThread.start();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        double priceAfter = stock.getResource(RESOURCE_2).getPrice();

        // then
        assertTrue(priceBefore < priceAfter);
    }

    @Test
    public void tooSmallQuantityResourceTest() {
        // given
        StockConfig.setPropertyValue("QUANTITY_PRICE_RATIO_FACTOR", "1.5");
        Stock stock = new Stock();
        Thread stockAlgorithmThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.getResource(RESOURCE_1).setStockQuantity(99);
        stock.getResource(RESOURCE_2).setStockQuantity(1);
        int quantityBefore = stock.getResource(RESOURCE_2).getStockQuantity();
        stock.setWorkingStatus(true);
        stockAlgorithmThread.start();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // then
        int quantityAfter = stock.getResource(RESOURCE_2).getStockQuantity();
        assertTrue(quantityAfter > quantityBefore);
    }

    @Test
    public void tooBigPriceResourceTest() {
        // given
        StockConfig.setPropertyValue("QUANTITY_PRICE_RATIO_FACTOR", "1.5");
        Stock stock = new Stock();
        Thread stockAlgorithmThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.getResource(RESOURCE_1).setPrice(99.0);
        stock.getResource(RESOURCE_2).setPrice(1.0);
        double priceBefore = stock.getResource(RESOURCE_1).getPrice();
        stock.setWorkingStatus(true);
        stockAlgorithmThread.start();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        double priceAfter = stock.getResource(RESOURCE_1).getPrice();

        // then
        assertTrue(priceBefore > priceAfter);
    }

    @After
    public void setDefaults() {
        StockConfig.setPropertyValue("SPECIAL_EVENT_CHANCE", "0");
        StockConfig.setPropertyValue("PRICE_GROW_FACTOR", "0.1");
        StockConfig.setPropertyValue("SPECIAL_EVENT_LENGTH", "3");
        StockConfig.setPropertyValue("SPECIAL_EVENT_GROW_FACTOR", "0.1");
        StockConfig.setPropertyValue("QUANTITY_GROW_FACTOR", "2");
        StockConfig.setPropertyValue("DICE_OPERATION_WIN_CHANCE", "30");
    }

    @AfterClass
    public static void cleanUp() {
        StockConfig.loadProperties();
    }
}
