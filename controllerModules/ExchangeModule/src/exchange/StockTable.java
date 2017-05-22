package exchange;

import java.util.*;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.geometry.Rectangle2D;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Dialog;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.KeyCombination;
import javafx.scene.layout.Background;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.Modality;
import javafx.stage.Screen;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.PieChart;
import javafx.scene.chart.PieChart.Data;
import javafx.scene.chart.XYChart;

public class StockTable extends Application {

	private static Stage stage;
	public static Stock stock;
	private static TableView<Resource> table;
	private static ObservableList<Resource> lineChartData;
	private static LineChart<String, Number> lineChart;
	private static PieChart pieChart;
	private static ObservableList<PieChart.Data> pieChartData;

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

		// resources table settings
		table = new TableView<Resource>();
		table.setEditable(false);
		table.setMaxHeight(260);
		table.setLayoutX(primaryScreenBounds.getWidth() * 0.05);
		table.setLayoutY(primaryScreenBounds.getHeight() * 0.60);

		TableColumn resourceNames = new TableColumn("Name");
		resourceNames.setMinWidth(110);
		resourceNames.setCellValueFactory(new PropertyValueFactory<Resource, String>("name"));

		TableColumn resourcePrice = new TableColumn("Price");
		resourcePrice.setMinWidth(110);
		resourcePrice.setCellValueFactory(new PropertyValueFactory<Resource, String>("priceString"));

		TableColumn resoureQuantity = new TableColumn("Quantity");
		resoureQuantity.setMinWidth(110);
		resoureQuantity.setCellValueFactory(new PropertyValueFactory<Resource, Integer>("quantity"));

		lineChartData = FXCollections.observableArrayList(stock.getResources());
		table.setItems(lineChartData);
		table.getColumns().addAll(resourceNames, resourcePrice, resoureQuantity);

		// axis settings
		final CategoryAxis xAxis = new CategoryAxis();
		final NumberAxis yAxis = new NumberAxis();
		xAxis.setLabel("Turn");

		// linechart settings
		lineChart = new LineChart<String, Number>(xAxis, yAxis);
		lineChart.setTitle("Stock Monitoring");
		lineChart.setLayoutX(primaryScreenBounds.getWidth() * 0.30);
		lineChart.setLayoutY(primaryScreenBounds.getHeight() * 0.05);
		lineChart.setPrefSize(primaryScreenBounds.getWidth() * 0.6, primaryScreenBounds.getHeight() * 0.7);
		lineChart.setStyle("-fx-background-color: rgba(0, 168, 255, 0.05);");

		// piechart settings
		pieChartData = FXCollections.observableArrayList();
		for (Resource resource : stock.getResources()) {
			pieChartData.add(new PieChart.Data(resource.getName(), resource.getQuantity()));
		}
		pieChart = new PieChart(pieChartData);
		pieChart.setTitle("In stock");
		pieChart.setLayoutX(primaryScreenBounds.getWidth() * 0.005);
		pieChart.setLayoutY(primaryScreenBounds.getHeight() * 0.01);

		// combo box for resource choosing
		final ComboBox resourceComboBox = new ComboBox();
		resourceComboBox.getItems().addAll(stock.getResourcesNames());
		resourceComboBox.getSelectionModel().selectFirst();
		resourceComboBox.setLayoutX(primaryScreenBounds.getWidth() * 0.30);
		resourceComboBox.setLayoutY(primaryScreenBounds.getHeight() * 0.80);

		// text field settings
		final TextField resourceAmount = new TextField();
		resourceAmount.setPromptText("Enter resource amount");
		resourceAmount.setPrefColumnCount(10);
		resourceAmount.setPrefSize(200, 30);
		resourceAmount.setLayoutX(primaryScreenBounds.getWidth() * 0.30);
		resourceAmount.setLayoutY(primaryScreenBounds.getHeight() * 0.88);

		// buy button settings
		Button buyButton = new Button("BUY");
		buyButton.setOnAction(new EventHandler<ActionEvent>() {
			public void handle(ActionEvent event) {
				String message = stock.buyOperation((String) resourceComboBox.getValue(), resourceAmount.getText());
				updatePieChart();
				table.getColumns().get(0).setVisible(false);
				table.getColumns().get(0).setVisible(true);
				showAlert(message);
			}
		});
		buyButton.setPrefSize(100, 50);
		buyButton.setLayoutX(primaryScreenBounds.getWidth() * 0.45);
		buyButton.setLayoutY(primaryScreenBounds.getHeight() * 0.80);

		// sell button settings
		Button sellButton = new Button("SELL");
		sellButton.setOnAction(new EventHandler<ActionEvent>() {
			public void handle(ActionEvent event) {
				String message = stock.sellOperation((String) resourceComboBox.getValue(), resourceAmount.getText());
				updatePieChart();
				table.getColumns().get(0).setVisible(false);
				table.getColumns().get(0).setVisible(true);
				showAlert(message);
			}
		});
		sellButton.setPrefSize(100, 50);
		sellButton.setLayoutX(primaryScreenBounds.getWidth() * 0.52);
		sellButton.setLayoutY(primaryScreenBounds.getHeight() * 0.80);

		// dice button settings
		Button diceButton = new Button("ROLL THE DICE");
		diceButton.setOnAction(new EventHandler<ActionEvent>() {
			public void handle(ActionEvent event) {
				String message = stock.diceOperation();
				showAlert(message);
			}
		});
		diceButton.setPrefSize(235, 50);
		diceButton.setLayoutX(primaryScreenBounds.getWidth() * 0.45);
		diceButton.setLayoutY(primaryScreenBounds.getHeight() * 0.88);

		// exit button settings
		Button exitButton = new Button("Exit");
		exitButton.setOnAction(new EventHandler<ActionEvent>() {
			public void handle(ActionEvent event) {
				stage.hide();
				stock.setWorkingStatus(true);
			}
		});
		exitButton.setPrefSize(150, 70);
		exitButton.setLayoutX(primaryScreenBounds.getWidth() * 0.85);
		exitButton.setLayoutY(primaryScreenBounds.getHeight() * 0.90);

		// main scene settings
		Scene scene = new Scene(new Group());
		((Group) scene.getRoot()).getChildren().addAll(table, lineChart, exitButton, resourceAmount, resourceComboBox,
				buyButton, sellButton, diceButton, pieChart);

		stage.setScene(scene);
		stage.hide();
	}

	public static void show() {
		launch();
	}

	@SuppressWarnings({ "rawtypes", "unchecked" })
	private static void updateChart() {
		lineChart.getData().clear();
		for (Resource resource : stock.getResources()) {
			XYChart.Series series = new XYChart.Series();
			series.setName(resource.getName());
			Double[] prices = stock.getPriceHistory().get(resource.getName());
			for (int i = 0; i < Stock.priceHistoryRange; i++) {
				series.getData().add(new XYChart.Data(String.valueOf(Stock.priceHistoryRange - i - 1), prices[i]));
			}
			lineChart.getData().add(series);
		}
	}

	private static void updatePieChart() {
		for (Data data : pieChartData) {
			data.setPieValue(stock.getResource(data.getName()).getQuantity());
		}
	}

	public static void showAlert(String message) {
		Alert alert;
		if (message.startsWith("ERROR")) {
			alert = new Alert(AlertType.ERROR);
		} else if (message.startsWith("WARNING")) {
			alert = new Alert(AlertType.WARNING);
		} else {
			alert = new Alert(AlertType.INFORMATION);
		}
		//alert.initStyle(StageStyle.UNDECORATED);
		alert.initOwner(stage);
		alert.setTitle("Info");
		alert.setHeaderText(null);
		alert.setContentText(message);
		alert.show();
	}

	public static void again() {
		Platform.runLater(() -> {
			updateChart();
			table.getColumns().get(0).setVisible(false);
			table.getColumns().get(0).setVisible(true);
			stage.show();
		});
	}

}