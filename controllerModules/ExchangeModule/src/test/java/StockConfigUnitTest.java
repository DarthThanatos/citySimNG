import exchange.StockConfig;
import org.junit.Test;

import javax.swing.filechooser.FileSystemView;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static exchange.StockConfig.*;
import static org.junit.Assert.*;

public class StockConfigUnitTest {

    private static final String stockPropertiesPath = FileSystemView.getFileSystemView().getDefaultDirectory().getPath() + "/citySimNG/stock.properties";

    @Test
    public void testConfigCreation() {
        // given
        Path path = Paths.get(stockPropertiesPath);

        // then
        assertTrue(Files.exists(path));
    }

    @Test
    public void testExistenceOfProperties() {
        assertNotEquals(0, PRICE_GROW_FACTOR);
        assertNotEquals(0, QUANTITY_GROW_FACTOR);
        assertNotEquals(0, QUANTITY_PRICE_RATIO_FACTOR);
        assertNotEquals(0, PRICE_UPDATE_SPEED);
        assertNotEquals(0, SPECIAL_EVENT_LENGTH);
        assertNotEquals(0, SPECIAL_EVENT_GROW_FACTOR);
        assertNotEquals(0, SPECIAL_EVENT_CHANCE);
        assertNotEquals(0, DICE_OPERATION_PRICE);
        assertNotEquals(0, DICE_OPERATION_MAX_WIN_QUANTITY);
        assertNotEquals(0, DICE_OPERATION_WIN_CHANCE);
    }

    @Test
    public void testSettingValues() {
        // given
        String[] propertiesNames = {"PRICE_GROW_FACTOR",
                "QUANTITY_GROW_FACTOR",
                "QUANTITY_PRICE_RATIO_FACTOR",
                "PRICE_UPDATE_SPEED",
                "SPECIAL_EVENT_LENGTH",
                "SPECIAL_EVENT_GROW_FACTOR",
                "SPECIAL_EVENT_CHANCE",
                "DICE_OPERATION_PRICE",
                "DICE_OPERATION_MAX_WIN_QUANTITY",
                "DICE_OPERATION_WIN_CHANCE"};

        // when
        for (String name : propertiesNames) {
            StockConfig.setPropertyValue(name, "12345");
        }

        // then
        assertEquals(12345.0, PRICE_GROW_FACTOR, 0.0);
        assertEquals(12345, QUANTITY_GROW_FACTOR);
        assertEquals(12345.0, QUANTITY_PRICE_RATIO_FACTOR, 0.0);
        assertEquals(12345, PRICE_UPDATE_SPEED);
        assertEquals(12345, SPECIAL_EVENT_LENGTH);
        assertEquals(12345.0, SPECIAL_EVENT_GROW_FACTOR, 0.0);
        assertEquals(12345, SPECIAL_EVENT_CHANCE);
        assertEquals(12345.0, DICE_OPERATION_PRICE, 0.0);
        assertEquals(12345, DICE_OPERATION_MAX_WIN_QUANTITY);
        assertEquals(12345, DICE_OPERATION_WIN_CHANCE);

        StockConfig.loadProperties();
    }
}
