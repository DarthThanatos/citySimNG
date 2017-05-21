package exchange;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Rectangle2D;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.KeyCombination;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.stage.Screen;
import javafx.stage.Stage;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.stage.Stage;

public class StockTable extends Application {

    public static Stage stage;
    public static Stock stock;
    static TableView<Resource> table;
    static ObservableList<Resource> data;
    static LineChart<String,Number> lineChart;

    @SuppressWarnings({ "unchecked", "rawtypes" })
	@Override
    public void start(Stage primaryStage) {

    	Rectangle2D primaryScreenBounds = Screen.getPrimary().getVisualBounds();

    	// stage settings
        Platform.setImplicitExit(false);
        stage = primaryStage;
        stage.setAlwaysOnTop(true);
        stage.setFullScreen(true);
        stage.setResizable(true);
        stage.setFullScreenExitKeyCombination(KeyCombination.NO_MATCH);

        // title settings
        final Label label = new Label("Stock");
        label.setFont(new Font("Arial", 30));

        // table settings
        table = new TableView<Resource>();
        table.setEditable(false);
        table.setLayoutX(primaryScreenBounds.getWidth() * 0.05);
        table.setLayoutY(primaryScreenBounds.getHeight() * 0.09);

        TableColumn resourceNames = new TableColumn("Name");
        resourceNames.setMinWidth(110);
        resourceNames.setCellValueFactory(
                new PropertyValueFactory<Resource, String>("name"));

        TableColumn resourcePrice = new TableColumn("Price");
        resourcePrice.setMinWidth(110);
        resourcePrice.setCellValueFactory(
                new PropertyValueFactory<Resource, String>("priceString"));

        TableColumn resoureQuantity = new TableColumn("Quantity");
        resoureQuantity.setMinWidth(110);
        resoureQuantity.setCellValueFactory(
                new PropertyValueFactory<Resource, Integer>("quantity"));

        data = FXCollections.observableArrayList(stock.getResources());
        table.setItems(data);
        table.getColumns().addAll(resourceNames, resourcePrice, resoureQuantity);

        // axis settings
        final CategoryAxis xAxis = new CategoryAxis();
        final NumberAxis yAxis = new NumberAxis();
        xAxis.setLabel("Turn");

        // chart settings
        lineChart = new LineChart<String,Number>(xAxis,yAxis);
        lineChart.setTitle("Stock Monitoring");
        lineChart.setLayoutX(primaryScreenBounds.getWidth() * 0.25);
        lineChart.setLayoutY(primaryScreenBounds.getHeight() * 0.05);
        lineChart.setPrefSize(primaryScreenBounds.getWidth() * 0.6, primaryScreenBounds.getHeight() * 0.7);

        Button exitButton = new Button("Exit");
        exitButton.setOnAction(new EventHandler<ActionEvent>() {
            public void handle(ActionEvent event) {
                stage.hide();
                stock.setWorking(true);
            }
        });
        exitButton.setPrefSize(100, 50);
        exitButton.setLayoutX(primaryScreenBounds.getWidth() * 0.45);
        exitButton.setLayoutY(primaryScreenBounds.getHeight() * 0.9);

        Scene scene = new Scene(new Group());
        ((Group) scene.getRoot()).getChildren().addAll(table, lineChart, exitButton);

        stage.setScene(scene);
        stage.hide();
    }

    public static void show() {
        launch();
    }

    @SuppressWarnings({ "rawtypes", "unchecked" })
	private static void updateChart() {
        for(Resource resource: stock.getResources()) {
        	XYChart.Series series = new XYChart.Series();
        	series.setName(resource.getName());
        	double[] prices = resource.getPriceHistory();
        	for(int i = 0; i < Resource.priceHistoryRange; i++) {
        		series.getData().add(new XYChart.Data(String.valueOf(Resource.priceHistoryRange - i - 1), prices[i]));
        	}
        	lineChart.getData().add(series);
        }
    }

    public static void again() {
        Platform.runLater(() -> {
        	lineChart.getData().clear();
        	updateChart();
        	table.getColumns().get(0).setVisible(false);
        	table.getColumns().get(0).setVisible(true);
        	stage.show();
        });
    }

}