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
}
