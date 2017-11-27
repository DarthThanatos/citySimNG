import exchange.Resource;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class ResourceUnitTest {

    @Test
    public void testResourceCreation() {
        // given
        Resource resource = new Resource("Gold", 20.0, 9);

        // then
        assertEquals(resource.getName(), "Gold");
        assertEquals(resource.getStockQuantity(), 9);
        assertEquals(resource.getPrice(), 20.0, 0.0);
        assertEquals(resource.getPlayerQuantity(), 0);
    }

    @Test
    public void testResourceSetters() {
        // given
        Resource resource = new Resource("", 0.0, 0);

        // when
        resource.setName("Gold");
        resource.setStockQuantity(10);
        resource.setPlayerQuantity(10);
        resource.setPrice(10.0);

        // then
        assertEquals(resource.getName(), "Gold");
        assertEquals(resource.getStockQuantity(), 10);
        assertEquals(resource.getPrice(), 10.0, 0.0);
        assertEquals(resource.getPlayerQuantity(), 10);
    }

    @Test
    public void testResourceUtils() {
        // given
        Resource resource = new Resource("Gold", 3.1234, 10);

        // when
        String priceString = resource.getPriceString();
        double quantityPriceRatio = resource.getQuantityPriceRatio();

        // then
        String floatStr = "3%s12";
        assert(priceString.equals(String.format(floatStr, ".")) || priceString.equals(String.format(floatStr, ",")));
        assertEquals(quantityPriceRatio, 3.20163, 0.00001);
    }
}