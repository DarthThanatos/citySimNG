import exchange.Stock;
import model.DependenciesRepresenter;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.*;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class StockUnitTest {

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
    }

    @Test
    public void testStockCreation() {
        // given
        Stock stock = new Stock();

        // then
        assertTrue(stock.getWorkingStatus());
    }

    @Test
    public void testStockInit() {
        // given
        Stock stock = new Stock();

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.setWorkingStatus(false);
        stock.init();

        // then
        assertNotNull(stock.getDependenciesRepresenter());
        assertNotNull(stock.getStockResources());
        assertNotNull(stock.getStockResourcesNames());
        assertNotNull(stock.getPriceHistory());
        assertFalse(stock.getWorkingStatus());
        verify(dependenciesRepresenter, times(1)).getResourcesNames();
    }

    @Test
    public void testGetResource() {
        // given
        Stock stock = new Stock();

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();

        // then
        assertNotNull(stock.getResource(RESOURCE_1));
        assertNotNull(stock.getResource(RESOURCE_2));
    }

    @Test
    public void testGetAverageQuantityPriceRatio() {
        // given
        Stock stock = new Stock();

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();

        // then
        double ratio = stock.getAverageQuantityPriceRatio();
        assertEquals(ratio, 1.0, 10.0);
        assertTrue(ratio > 0);
    }

    @Test
    public void testUpdatePriceHistory() {
        // given
        Stock stock = new Stock();

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.updatePriceHistory(3.14, RESOURCE_1);
        stock.updatePriceHistory(2.71, RESOURCE_2);

        // then
        assertEquals(stock.getPriceHistory().get(RESOURCE_1)[Stock.priceHistoryRange - 2], 0.0, 0.0);
        assertEquals(stock.getPriceHistory().get(RESOURCE_2)[Stock.priceHistoryRange - 2], 0.0, 0.0);
        assertEquals(stock.getPriceHistory().get(RESOURCE_1)[Stock.priceHistoryRange - 1], 3.14, 0.001);
        assertEquals(stock.getPriceHistory().get(RESOURCE_2)[Stock.priceHistoryRange - 1], 2.71, 0.001);
    }

    @Test
    public void testUpdatePlayerResource() {
        // given
        Stock stock = new Stock();

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        Map<String, Integer> stockPile = new HashMap<>();
        stockPile.put(RESOURCE_1, 50);
        stockPile.put(RESOURCE_2, 30);
        when(dependenciesRepresenter.getStockPile()).thenReturn(stockPile);
        stock.updatePlayerResource();

        // then
        assertEquals(stock.getStockResources().get(0).getPlayerQuantity(), 50);
        assertEquals(stock.getStockResources().get(1).getPlayerQuantity(), 30);
        verify(dependenciesRepresenter, times(2)).getStockPile();
    }

    @Test
    public void testBuyOperation() {
        // given
        Stock stock = new Stock();

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        Map<String, Integer> stockPile = new HashMap<>();
        stockPile.put(RESOURCE_1, 15);
        stockPile.put(RESOURCE_2, 10);
        when(dependenciesRepresenter.getStockPile()).thenReturn(stockPile);
        when(dependenciesRepresenter.getMoney()).thenReturn(Double.valueOf(10000));
        stock.updatePlayerResource();

        String response1 = stock.buyOperation(RESOURCE_1, "1");
        String response2 = stock.buyOperation(RESOURCE_2, "100");
        when(dependenciesRepresenter.getMoney()).thenReturn(Double.valueOf(1));
        String response3 = stock.buyOperation(RESOURCE_2, "1");

        // then
        assertEquals("You bought 1 of Gold, and now have 16 Gold and 10000.00 money", response1);
        assertEquals("WARNING - not enough resources in stock", response2);
        assertEquals("WARNING - you don't have enough money", response3);
    }

    @Test
    public void testSellOperation() {
        // given
        Stock stock = new Stock();

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        Map<String, Integer> stockPile = new HashMap<>();
        stockPile.put(RESOURCE_1, 15);
        stockPile.put(RESOURCE_2, 10);
        when(dependenciesRepresenter.getStockPile()).thenReturn(stockPile);
        when(dependenciesRepresenter.getMoney()).thenReturn(Double.valueOf(10000));
        stock.updatePlayerResource();

        String response1 = stock.sellOperation(RESOURCE_1, "1");
        String response2 = stock.sellOperation(RESOURCE_2, "100");

        // then
        assertEquals("You sold 1 of Gold, and now have 14 Gold and 10000.00 money", response1);
        assertEquals("WARNING - you don't have enough resources to sell", response2);
    }

    @Test
    public void testDiceOperation() {
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

        when(dependenciesRepresenter.getMoney()).thenReturn(Double.valueOf(1000));
        String response1 = stock.diceOperation();

        when(dependenciesRepresenter.getMoney()).thenReturn(Double.valueOf(0));
        String response2 = stock.diceOperation();

        // then
        assertTrue(response1.contains("You won"));
        assertTrue(response2.contains("WARNING - you need"));
    }

    @Test
    public void testUpdateAndGetCurrentPrices() {
        // given
        Stock stock = new Stock();

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        Map<String, Integer> currentPrices = stock.updateAndGetCurrentPrices();

        // then
        assertNotNull(currentPrices);
        assertEquals(currentPrices.size(), 2);
        assertEquals(currentPrices.get(RESOURCE_1), 10, 10);
        assertEquals(currentPrices.get(RESOURCE_2), 10, 10);
    }
}
