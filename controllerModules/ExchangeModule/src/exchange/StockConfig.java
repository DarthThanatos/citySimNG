package exchange;

import java.io.*;
import java.util.HashMap;
import java.util.Properties;
import java.util.Set;
import java.util.logging.Logger;

class StockConfig {

    static final double PRICE_GROW_FACTOR;
    static final int QUANTITY_GROW_FACTOR;
    static final double QUANTITY_PRICE_RATIO_FACTOR;
    static final int PRICE_UPDATE_SPEED;
    static final int SPECIAL_EVENT_LENGTH;
    static final double SPECIAL_EVENT_GROW_FACTOR;
    static final int SPECIAL_EVENT_CHANCE;
    static final double DICE_OPERATION_PRICE;
    static final int DICE_OPERATION_MAX_WIN_QUANTITY;
    static final int DICE_OPERATION_WIN_CHANCE;

    private static Properties stockProperties;
    private static String stockPropertiesFileName = "controllerModules/ExchangeModule/resources/stock.properties";
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
                logger.warning("Exception during creation of properties file for stock.");
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

    private static void createDefaultPropertiesMap() {
        propertiesDefaultValues.put(propertiesNames[0], "0.01");
        propertiesDefaultValues.put(propertiesNames[1], "2");
        propertiesDefaultValues.put(propertiesNames[2], "2.5");
        propertiesDefaultValues.put(propertiesNames[3], "2000");
        propertiesDefaultValues.put(propertiesNames[4], "5");
        propertiesDefaultValues.put(propertiesNames[5], "0.05");
        propertiesDefaultValues.put(propertiesNames[6], "5");
        propertiesDefaultValues.put(propertiesNames[7], "10.0");
        propertiesDefaultValues.put(propertiesNames[8], "50");
        propertiesDefaultValues.put(propertiesNames[9], "30");

    }

    private static void loadPropertiesFile() throws IOException {
        FileInputStream in = new FileInputStream(stockPropertiesFileName);
        stockProperties.load(in);
        in.close();
    }

    private static void createPropertiesFile() throws IOException {
        setDefaultStockProperties();
        FileOutputStream out = new FileOutputStream(stockPropertiesFileName);
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