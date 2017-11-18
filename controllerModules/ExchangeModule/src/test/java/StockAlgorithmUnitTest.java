import exchange.Stock;
import exchange.StockAlgorithm;
import exchange.StockConfig;
import model.DependenciesRepresenter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.LinkedList;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class StockAlgorithmUnitTest {

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

        StockConfig.setPropertyValue("PRICE_UPDATE_SPEED", "100");
    }

    @Test
    public void testPriceChangeWhenNotWorking() {
        // given
        Stock stock = new Stock();
        Thread stockAlgorithmThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.setWorkingStatus(true);
        stockAlgorithmThread.start();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        stock.setWorkingStatus(false);
        double priceBefore = stock.getResource(RESOURCE_1).getPrice();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        double priceAfter = stock.getResource(RESOURCE_1).getPrice();

        assertEquals(priceBefore, priceAfter, 0.0);
    }

    @Test
    public void testPriceChangeWhenWorking() {
        // given
        Stock stock = new Stock();
        Thread stockAlgorithmThread = new Thread(() -> new StockAlgorithm(stock).simulateStock());

        // when
        stock.setDependenciesRepresenter(dependenciesRepresenter);
        stock.init();
        stock.setWorkingStatus(true);
        stockAlgorithmThread.start();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        double priceBefore = stock.getResource(RESOURCE_1).getPrice();
        try {
            Thread.sleep(StockConfig.PRICE_UPDATE_SPEED + 100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        double priceAfter = stock.getResource(RESOURCE_1).getPrice();

        assertNotEquals(priceBefore, priceAfter);
    }

    @After
    public void cleanUp() {
        StockConfig.loadProperties();
    }
}
