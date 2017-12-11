package exchange;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.PieChart;
import javafx.scene.chart.PieChart.Data;
import javafx.scene.chart.XYChart;
import model.DependenciesRepresenter;

import java.io.File;

public class StockView extends Application {

    private static Stage stage;
    public static Stock stock = null;
    private static TableView<Resource> resourceTable;
    private static LineChart<String, Number> lineChart;
    private static ObservableList<PieChart.Data> pieChartData = FXCollections.observableArrayList();
    private static Label moneyLabel;
    private static ComboBox<String> resourceComboBox;

    @Override
    public void start(Stage primaryStage) {

        Platform.setImplicitExit(false);
        stage = primaryStage;
        StockViewUtils.setStageSettings(stage);

        moneyLabel = StockViewUtils.createMoneyLabel();

        resourceTable = StockViewUtils.createResourceTable();
        setResourceTable();

        lineChart = StockViewUtils.createLineChart();

        PieChart pieChart = StockViewUtils.createPieChart(pieChartData);
        setPieChartData();

        resourceComboBox = StockViewUtils.createResourceComboBox();
        setResourceComboBox();

        TextField resourceAmountField = StockViewUtils.createResourceAmountField();

        Button buyButton = StockViewUtils.createBuyButton();
        buyButton.setOnAction(event -> {
            String message = stock.buyOperation(resourceComboBox.getValue(), resourceAmountField.getText());
            performAction(message);
        });

        Button sellButton = StockViewUtils.createSellButton();
        sellButton.setOnAction(event -> {
            String message = stock.sellOperation(resourceComboBox.getValue(), resourceAmountField.getText());
            performAction(message);
        });

        Button diceButton = StockViewUtils.createDiceButton();
        diceButton.setOnAction(event -> {
            String message = stock.diceOperation();
            performAction(message);
        });

        Button exitButton = StockViewUtils.createExitButton();
        exitButton.setOnAction(event -> {
            stage.hide();
            stock.setWorkingStatus(true);
        });

        Scene scene = new Scene(new Group(), Color.AZURE);
        ((Group) scene.getRoot()).getChildren().addAll(
                StockViewUtils.createResourceTableLabel(),
                StockViewUtils.createResourceComboBoxLabel(),
                StockViewUtils.createResourceAmountLabel(),
                StockViewUtils.createBuyLabel(),
                StockViewUtils.createSellLabel(),
                StockViewUtils.createDiceLabel(),
                StockViewUtils.createExitLabel(),
                moneyLabel,
                buyButton, sellButton, diceButton, exitButton,
                resourceTable, lineChart, resourceAmountField, resourceComboBox,
                pieChart);

        File f = new File("resources/TextFiles/stock_view_styles.css");
        scene.getStylesheets().add("file:///" + f.getAbsolutePath().replace("\\", "/"));
        lineChart.applyCss();

        stage.setScene(scene);
        stage.hide();
    }

    public static void initStockView(Stock stock, DependenciesRepresenter dependenciesRepresenter) {
        Stock tmpStock = StockView.stock;
        StockView.stock = stock;
        try {
            launch();
        } catch (Exception ex) {
            StockView.stock = tmpStock;
            StockView.stock.setDependenciesRepresenter(dependenciesRepresenter);
            StockView.stock.init();
            setResourceTable();
            setPieChartData();
            setResourceComboBox();
        }
    }

    private static void performAction(String message) {
        updatePieChart();
        updateMoneyLabel();
        resourceTable.refresh();
        StockViewUtils.showAlertMessage(message, stage);
    }

    public static void show() {
        Platform.runLater(() -> {
            updateLineChart();
            updatePieChart();
            stock.updatePlayerResource();
            resourceTable.refresh();
            updateMoneyLabel();
            stage.show();
        });
    }

    private static void updateLineChart() {
        lineChart.getData().clear();
        for (Resource resource : stock.getStockResources()) {
            XYChart.Series<String, Number> series = new XYChart.Series<>();
            series.setName(resource.getName());
            Double[] pricesHistory = stock.getPriceHistory().get(resource.getName());
            for (int i = 0; i < Stock.priceHistoryRange; i++) {
                series.getData().add(new XYChart.Data<>(String.valueOf(Stock.priceHistoryRange - i - 1), pricesHistory[i]));
            }
            lineChart.getData().add(series);
        }
    }

    private static void updatePieChart() {
        for (Data data : pieChartData) {
            data.setPieValue(stock.getResource(data.getName()).getStockQuantity());
        }
    }

    private static void updateMoneyLabel() {
        moneyLabel.setText("You have " + String.format("%.2f", stock.getDependenciesRepresenter().getMoney()) + " money.");
    }

    private static void setResourceTable() {
        ObservableList<Resource> lineChartData = FXCollections.observableArrayList(stock.getStockResources());
        resourceTable.getItems().removeAll();
        resourceTable.setItems(lineChartData);
    }

    private static void setPieChartData() {
        pieChartData.removeAll();
        pieChartData.clear();
        for (Resource resource : stock.getStockResources()) {
            pieChartData.add(new PieChart.Data(resource.getName(), resource.getStockQuantity()));
        }
    }

    private static void setResourceComboBox() {
        resourceComboBox.getItems().removeAll();
        resourceComboBox.getItems().clear();
        resourceComboBox.getItems().addAll(stock.getStockResourcesNames());
        resourceComboBox.getSelectionModel().selectFirst();
    }

}