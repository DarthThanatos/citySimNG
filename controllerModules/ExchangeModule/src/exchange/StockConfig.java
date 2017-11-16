package exchange;

import javax.swing.filechooser.FileSystemView;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Properties;
import java.util.Set;
import java.util.logging.Logger;

public class StockConfig {

    public static final double PRICE_GROW_FACTOR;
    public static final int QUANTITY_GROW_FACTOR;
    public static final double QUANTITY_PRICE_RATIO_FACTOR;
    public static final int PRICE_UPDATE_SPEED;
    public static final int SPECIAL_EVENT_LENGTH;
    public static final double SPECIAL_EVENT_GROW_FACTOR;
    public static final int SPECIAL_EVENT_CHANCE;
    public static final double DICE_OPERATION_PRICE;
    public static final int DICE_OPERATION_MAX_WIN_QUANTITY;
    public static final int DICE_OPERATION_WIN_CHANCE;

    private static Properties stockProperties;
    private static String basePropertiesPath = FileSystemView.getFileSystemView().getDefaultDirectory().getPath();
    private static Logger logger = Logger.getLogger("StockConfig");
    private static String[] propertiesNames = {"PRICE_GROW_FACTOR_IN_PERCENT",
            "QUANTITY_GROW_FACTOR_APIECE",
            "QUANTITY_PRICE_RATIO_FACTOR",
            "PRICE_UPDATE_SPEED_IN_MILLIS",
            "SPECIAL_EVENT_LENGTH_IN_UPDATES",
            "SPECIAL_EVENT_GROW_FACTOR_IN_PERCENT",
            "SPECIAL_EVENT_CHANCE_IN_PERCENT",
            "DICE_OPERATION_PRICE",
            "DICE_OPERATION_MAX_WIN_QUANTITY_APIECE",
            "DICE_OPERATION_WIN_CHANCE_IN_PERCENT"};
    private static HashMap<String, String> propertiesDefaultValues = new HashMap<>();

    static {
        createDefaultPropertiesMap();
        stockProperties = new Properties();
        try {
            loadPropertiesFile();
            validateAndAmendProperties();
        } catch (IOException e) {
            logger.info("Missing property file, creating new one.");
            try {
                createPropertiesFile();
            } catch (IOException e1) {
                logger.warning("Exception during creation of properties file for stock");
                e1.printStackTrace();
            }
        }

        PRICE_GROW_FACTOR = Double.parseDouble(stockProperties.getProperty(propertiesNames[0]));
        QUANTITY_GROW_FACTOR = Integer.parseInt(stockProperties.getProperty(propertiesNames[1]));
        QUANTITY_PRICE_RATIO_FACTOR = Double.parseDouble(stockProperties.getProperty(propertiesNames[2]));
        PRICE_UPDATE_SPEED = Integer.parseInt(stockProperties.getProperty(propertiesNames[3]));
        SPECIAL_EVENT_LENGTH = Integer.parseInt(stockProperties.getProperty(propertiesNames[4]));
        SPECIAL_EVENT_GROW_FACTOR = Double.parseDouble(stockProperties.getProperty(propertiesNames[5]));
        SPECIAL_EVENT_CHANCE = Integer.parseInt(stockProperties.getProperty(propertiesNames[6]));
        DICE_OPERATION_PRICE = Double.parseDouble(stockProperties.getProperty(propertiesNames[7]));
        DICE_OPERATION_MAX_WIN_QUANTITY = Integer.parseInt(stockProperties.getProperty(propertiesNames[8]));
        DICE_OPERATION_WIN_CHANCE = Integer.parseInt(stockProperties.getProperty(propertiesNames[9]));

    }

    private StockConfig() {

    }

    private static void createDefaultPropertiesMap() {
        propertiesDefaultValues.put(propertiesNames[0], "0.01"); // PRICE_GROW_FACTOR_IN_PERCENT
        propertiesDefaultValues.put(propertiesNames[1], "2");    // QUANTITY_GROW_FACTOR_APIECE
        propertiesDefaultValues.put(propertiesNames[2], "2.5");  // QUANTITY_PRICE_RATIO_FACTOR
        propertiesDefaultValues.put(propertiesNames[3], "1000"); // PRICE_UPDATE_SPEED_IN_MILLIS
        propertiesDefaultValues.put(propertiesNames[4], "3");    // SPECIAL_EVENT_LENGTH_IN_UPDATES
        propertiesDefaultValues.put(propertiesNames[5], "0.10"); // SPECIAL_EVENT_GROW_FACTOR_IN_PERCENT
        propertiesDefaultValues.put(propertiesNames[6], "1");    // SPECIAL_EVENT_CHANCE_IN_PERCENT
        propertiesDefaultValues.put(propertiesNames[7], "10.0"); // DICE_OPERATION_PRICE
        propertiesDefaultValues.put(propertiesNames[8], "50");   // DICE_OPERATION_MAX_WIN_QUANTITY_APIECE
        propertiesDefaultValues.put(propertiesNames[9], "30");   // DICE_OPERATION_WIN_CHANCE_IN_PERCENT

    }

    private static void loadPropertiesFile() throws IOException {
        FileInputStream in = new FileInputStream(basePropertiesPath + "/citySimNG/stock.properties");
        stockProperties.load(in);
        in.close();
    }

    private static void createPropertiesFile() throws IOException {
        setDefaultStockProperties();
        if (!Files.exists(Paths.get(basePropertiesPath + "/citySimNG"))) {
            Files.createDirectory(Paths.get(basePropertiesPath + "/citySimNG"));
        }
        FileOutputStream out = new FileOutputStream(basePropertiesPath + "/citySimNG/stock.properties");
        stockProperties.store(out, "This is a configuration file for stock.");
        out.close();
    }

    private static void setDefaultStockProperties() {
        Set<String> propertiesKeySet = propertiesDefaultValues.keySet();
        for (String propertyName : propertiesKeySet) {
            stockProperties.put(propertyName, propertiesDefaultValues.get(propertyName));
        }
    }

    private static void validateAndAmendProperties() {
        for (String name : propertiesNames) {
            try {
                //noinspection ResultOfMethodCallIgnored
                Double.parseDouble(stockProperties.getProperty(name));
            } catch (NumberFormatException e) {
                logger.warning("Property " + name + " has wrong format, default value is loaded.");
                stockProperties.put(name, propertiesDefaultValues.get(name));
            } catch (NullPointerException e) {
                logger.warning("Property " + name + " is missing, default value is loaded.");
                stockProperties.put(name, propertiesDefaultValues.get(name));
            }
        }
    }
}
