package exchange;

import java.util.Random;
import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;

public class Resource {

	public static final double defaultPrice = 100.0;
	public static final int defaultQuantity = 100;
	public static final int priceHistoryRange = 15;
	private SimpleStringProperty name;
	private SimpleStringProperty priceString;
	private SimpleIntegerProperty quantity;
	private double price;
	private double[] priceHistory;
	private Random random = new Random();

	Resource() {
		super();
	}

	Resource(String name) {
		super();
		this.name = new SimpleStringProperty(name);
		this.priceString = new SimpleStringProperty(String.format("%.2f", defaultPrice));
		this.quantity = new SimpleIntegerProperty(defaultQuantity);
		this.price = defaultPrice;
		priceHistory = new double[priceHistoryRange];
		for (int i = 0; i < priceHistoryRange; i++) {
			priceHistory[i] = new Double(0);
		}
	}

	Resource(String name, double price) {
		super();
		this.name = new SimpleStringProperty(name);
		this.priceString = new SimpleStringProperty(String.format("%.2f", defaultPrice));
		this.quantity = new SimpleIntegerProperty(defaultQuantity);
		this.price = price;
		priceHistory = new double[priceHistoryRange];
		for (int i = 0; i < priceHistoryRange; i++) {
			priceHistory[i] = new Double(0);
		}
	}

	Resource(String name, double price, int quantity) {
		super();
		this.name = new SimpleStringProperty(name);
		this.priceString = new SimpleStringProperty(String.format("%.2f", defaultPrice));
		this.quantity = new SimpleIntegerProperty(quantity);
		this.price = price;
		priceHistory = new double[priceHistoryRange];
		for (int i = 0; i < priceHistoryRange; i++) {
			priceHistory[i] = new Double(0);
		}
	}

	public String getName() {
		return this.name.get();
	}

	public void setName(String name) {
		this.name.set(name);
	}

	public double getPrice() {
		return this.price;
	}

	public void setPrice(double price) {
		this.price = price;
	}

	public String getPriceString() {
		return priceString.get();
	}

	public void setPriceString(String priceString) {
		this.priceString.set(priceString);
	}

	public double[] getPriceHistory() {
		return priceHistory;
	}

	public Integer getQuantity() {
		return quantity.get();
	}

	public void setQuantity(Integer quantity) {
		this.quantity.set(quantity);
	}

	public void update(double delta) {
		for (int i = 0; i < priceHistoryRange - 1; i++) {
			priceHistory[i] = priceHistory[i + 1];
		}
		this.price = this.price + this.price * delta;
		priceHistory[priceHistoryRange - 1] = this.price;
		this.priceString.set(String.format("%.2f", this.price));
		this.quantity.set(this.quantity.get() + 5);
	}

}
