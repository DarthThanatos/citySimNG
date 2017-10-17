package exchange;

import javafx.collections.ObservableList;
import javafx.geometry.Rectangle2D;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.PieChart;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.KeyCombination;
import javafx.scene.text.Font;
import javafx.stage.Screen;
import javafx.stage.Stage;

@SuppressWarnings("unchecked")
class StockViewUtils {

    private static Rectangle2D primaryScreenBounds;

    static {
        primaryScreenBounds = Screen.getPrimary().getVisualBounds();
    }

    static void setStageSettings(Stage stage) {
        stage.setAlwaysOnTop(true);
        stage.setFullScreen(true);
        stage.setResizable(true);
        stage.setFullScreenExitKeyCombination(KeyCombination.NO_MATCH);
    }

    static Label createMoneyLabel() {
        Label moneyLabel = new Label();
        moneyLabel.setFont(new Font("Arial", 20));
        moneyLabel.setPrefSize(primaryScreenBounds.getWidth() * 0.18, primaryScreenBounds.getHeight() * 0.04);
        moneyLabel.setLayoutX(primaryScreenBounds.getWidth() * 0.68);
        moneyLabel.setLayoutY(primaryScreenBounds.getHeight() * 0.77);
        return moneyLabel;
    }

    static Label createResourceTableLabel() {
        Label resourceTableLabel = new Label("Resource table detailed info:");
        resourceTableLabel.setFont(new Font("Arial", 20));
        resourceTableLabel.setPrefSize(primaryScreenBounds.getWidth() * 0.18, primaryScreenBounds.getHeight() * 0.04);
        resourceTableLabel.setLayoutX(primaryScreenBounds.getWidth() * 0.05);
        resourceTableLabel.setLayoutY(primaryScreenBounds.getHeight() * 0.60);
        return resourceTableLabel;
    }

    static Label createResourceComboBoxLabel() {
        Label resourceComboBoxLabel = new Label("Choose resource type:");
        resourceComboBoxLabel.setFont(new Font("Arial", 20));
        resourceComboBoxLabel.setPrefSize(primaryScreenBounds.getWidth() * 0.17,
                primaryScreenBounds.getHeight() * 0.04);
        resourceComboBoxLabel.setLayoutX(primaryScreenBounds.getWidth() * 0.30);
        resourceComboBoxLabel.setLayoutY(primaryScreenBounds.getHeight() * 0.77);
        return resourceComboBoxLabel;
    }

    static Label createResourceAmountLabel() {
        Label resourceAmountLabel = new Label("Enter resource quantity:");
        resourceAmountLabel.setFont(new Font("Arial", 20));
        resourceAmountLabel.setPrefSize(primaryScreenBounds.getWidth() * 0.17, primaryScreenBounds.getHeight() * 0.04);
        resourceAmountLabel.setLayoutX(primaryScreenBounds.getWidth() * 0.30);
        resourceAmountLabel.setLayoutY(primaryScreenBounds.getHeight() * 0.83);
        return resourceAmountLabel;
    }

    static Label createBuyLabel() {
        Label buyLabel = new Label("Buy chosen resources: ");
        buyLabel.setFont(new Font("Arial", 20));
        buyLabel.setPrefSize(primaryScreenBounds.getWidth() * 0.17, primaryScreenBounds.getHeight() * 0.04);
        buyLabel.setLayoutX(primaryScreenBounds.getWidth() * 0.30);
        buyLabel.setLayoutY(primaryScreenBounds.getHeight() * 0.88);
        return buyLabel;
    }

    static Label createSellLabel() {
        Label sellLabel = new Label("Sell chosen resources: ");
        sellLabel.setFont(new Font("Arial", 20));
        sellLabel.setPrefSize(primaryScreenBounds.getWidth() * 0.17, primaryScreenBounds.getHeight() * 0.04);
        sellLabel.setLayoutX(primaryScreenBounds.getWidth() * 0.30);
        sellLabel.setLayoutY(primaryScreenBounds.getHeight() * 0.93);
        return sellLabel;
    }

    static Label createDiceLabel() {
        Label diceLabel = new Label("Take part in a lottery:");
        diceLabel.setFont(new Font("Arial", 20));
        diceLabel.setPrefSize(primaryScreenBounds.getWidth() * 0.14, primaryScreenBounds.getHeight() * 0.04);
        diceLabel.setLayoutX(primaryScreenBounds.getWidth() * 0.68);
        diceLabel.setLayoutY(primaryScreenBounds.getHeight() * 0.82);
        return diceLabel;
    }

    static Label createExitLabel() {
        Label exitLabel = new Label("Leave stock:");
        exitLabel.setFont(new Font("Arial", 20));
        exitLabel.setPrefSize(primaryScreenBounds.getWidth() * 0.14, primaryScreenBounds.getHeight() * 0.04);
        exitLabel.setLayoutX(primaryScreenBounds.getWidth() * 0.68);
        exitLabel.setLayoutY(primaryScreenBounds.getHeight() * 0.87);
        return exitLabel;
    }

    static TableView<Resource> createResourceTable() {
        TableView<Resource> resourceTable = createEmptyResourceTable();
        TableColumn<Resource, String> resourceNames = createResourceTableColumn("Name", "name");
        TableColumn<Resource, String> resourcePrice = createResourceTableColumn("Price", "priceString");
        TableColumn<Resource, String> resourceQuantity = createResourceTableColumn("In stock", "stockQuantityString");
        TableColumn<Resource, String> playerResourceQuantity = createResourceTableColumn("Possessed", "playerQuantityString");
        resourceTable.getColumns().addAll(resourceNames, resourcePrice, resourceQuantity, playerResourceQuantity);
        return resourceTable;
    }

    static LineChart<String, Number> createLineChart() {
        CategoryAxis xAxis = new CategoryAxis();
        NumberAxis yAxis = new NumberAxis();
        xAxis.setLabel("Turn");
        yAxis.setLabel("Price");

        LineChart<String, Number> lineChart = new LineChart<>(xAxis, yAxis);
        lineChart.setTitle("Stock Monitoring");
        lineChart.setLayoutX(primaryScreenBounds.getWidth() * 0.30);
        lineChart.setLayoutY(primaryScreenBounds.getHeight() * 0.05);
        lineChart.setPrefSize(primaryScreenBounds.getWidth() * 0.6, primaryScreenBounds.getHeight() * 0.7);
        lineChart.setStyle("-fx-background-color: rgba(0, 168, 255, 0.05);");
        return lineChart;
    }

    static PieChart createPieChart(ObservableList<PieChart.Data> pieChartData) {
        PieChart pieChart = new PieChart(pieChartData);
        pieChart.setTitle("Stock resources chart");
        pieChart.setLayoutX(primaryScreenBounds.getWidth() * 0.02);
        pieChart.setLayoutY(primaryScreenBounds.getHeight() * 0.05);
        pieChart.setPrefSize(primaryScreenBounds.getWidth() * 0.25, primaryScreenBounds.getHeight() * 0.40);
        return pieChart;
    }

    static ComboBox<String> createResourceComboBox() {
        ComboBox<String> resourceComboBox = new ComboBox<>();
        resourceComboBox.getSelectionModel().selectFirst();
        resourceComboBox.setPrefSize(primaryScreenBounds.getWidth() * 0.10, primaryScreenBounds.getHeight() * 0.04);
        resourceComboBox.setLayoutX(primaryScreenBounds.getWidth() * 0.48);
        resourceComboBox.setLayoutY(primaryScreenBounds.getHeight() * 0.77);
        return resourceComboBox;
    }

    static TextField createResourceAmountField() {
        TextField resourceAmountField = new TextField();
        resourceAmountField.setPromptText("resource quantity");
        resourceAmountField.setPrefColumnCount(10);
        resourceAmountField.setPrefSize(primaryScreenBounds.getWidth() * 0.10, primaryScreenBounds.getHeight() * 0.04);
        resourceAmountField.setLayoutX(primaryScreenBounds.getWidth() * 0.48);
        resourceAmountField.setLayoutY(primaryScreenBounds.getHeight() * 0.83);
        return resourceAmountField;
    }

    static Button createBuyButton() {
        Button buyButton = new Button("BUY");
        buyButton.setPrefSize(primaryScreenBounds.getWidth() * 0.10, primaryScreenBounds.getHeight() * 0.04);
        buyButton.setLayoutX(primaryScreenBounds.getWidth() * 0.48);
        buyButton.setLayoutY(primaryScreenBounds.getHeight() * 0.88);
        return buyButton;
    }

    static Button createSellButton() {
        Button sellButton = new Button("SELL");
        sellButton.setPrefSize(primaryScreenBounds.getWidth() * 0.10, primaryScreenBounds.getHeight() * 0.04);
        sellButton.setLayoutX(primaryScreenBounds.getWidth() * 0.48);
        sellButton.setLayoutY(primaryScreenBounds.getHeight() * 0.93);
        return sellButton;
    }

    static Button createDiceButton() {
        Button diceButton = new Button("ROLL THE DICE");
        diceButton.setPrefSize(primaryScreenBounds.getWidth() * 0.10, primaryScreenBounds.getHeight() * 0.04);
        diceButton.setLayoutX(primaryScreenBounds.getWidth() * 0.82);
        diceButton.setLayoutY(primaryScreenBounds.getHeight() * 0.82);
        return diceButton;
    }

    static Button createExitButton() {
        Button exitButton = new Button("Exit");
        exitButton.setPrefSize(primaryScreenBounds.getWidth() * 0.10, primaryScreenBounds.getHeight() * 0.04);
        exitButton.setLayoutX(primaryScreenBounds.getWidth() * 0.82);
        exitButton.setLayoutY(primaryScreenBounds.getHeight() * 0.87);
        return exitButton;
    }

    static void showAlertMessage(String message, Stage stage) {
        Alert alert;
        if (message.startsWith("ERROR")) {
            alert = new Alert(Alert.AlertType.ERROR);
        } else if (message.startsWith("WARNING")) {
            alert = new Alert(Alert.AlertType.WARNING);
        } else {
            alert = new Alert(Alert.AlertType.INFORMATION);
        }
        // alert.initStyle(StageStyle.UNDECORATED);
        alert.initOwner(stage);
        alert.setTitle("Info");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.show();
    }

    static private TableView<Resource> createEmptyResourceTable() {
        TableView<Resource> resourceTable = new TableView<>();
        resourceTable.setEditable(false);
        resourceTable.setFixedCellSize(primaryScreenBounds.getHeight() * 0.04);
        resourceTable.setMaxHeight((primaryScreenBounds.getHeight() * 0.04) * 6.8);
        resourceTable.setLayoutX(primaryScreenBounds.getWidth() * 0.05);
        resourceTable.setLayoutY(primaryScreenBounds.getHeight() * 0.65);
        return resourceTable;
    }

    static private TableColumn<Resource, String> createResourceTableColumn(String columnName, String propertName) {
        TableColumn<Resource, String> resourceColumn = new TableColumn<>(columnName);
        resourceColumn.setMinWidth(primaryScreenBounds.getWidth() * 0.05);
        resourceColumn.setCellValueFactory(new PropertyValueFactory<>(propertName));
        return resourceColumn;
    }
}
