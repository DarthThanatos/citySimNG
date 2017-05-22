package exchange;

import javafx.beans.property.*;

public class Resource {

	public static final double defaultPrice = 100.0;
	public static final int defaultQuantity = 100;
	private SimpleStringProperty name;
	private SimpleStringProperty priceString;
	private SimpleIntegerProperty quantity;
	private double price;

	Resource() {
		super();
	}

	Resource(String name) {
		super();
		this.name = new SimpleStringProperty(name);
		this.priceString = new SimpleStringProperty(String.format("%.2f", defaultPrice));
		this.quantity = new SimpleIntegerProperty(defaultQuantity);
		this.price = defaultPrice;
	}

	Resource(String name, double price) {
		super();
		this.name = new SimpleStringProperty(name);
		this.priceString = new SimpleStringProperty(String.format("%.2f", defaultPrice));
		this.quantity = new SimpleIntegerProperty(defaultQuantity);
		this.price = price;
	}

	Resource(String name, double price, int quantity) {
		super();
		this.name = new SimpleStringProperty(name);
		this.priceString = new SimpleStringProperty(String.format("%.2f", defaultPrice));
		this.quantity = new SimpleIntegerProperty(quantity);
		this.price = price;
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
		this.priceString.set(String.format("%.2f", price));
	}

	public String getPriceString() {
		return priceString.get();
	}

	public void setPriceString(String priceString) {
		this.priceString.set(priceString);
	}

	public Integer getQuantity() {
		return quantity.get();
	}

	public void setQuantity(Integer quantity) {
		this.quantity.set(quantity);
	}

}
