package exchange;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

/** Main exchange class */

public class Stock {

	public Stock(String string, double d) {
		this.symbol = string;
		this.price = d;
	}

	private String symbol;
	private double price;
	private double delta;
	private String lastUpdate;
	private DateFormat date;

	public String getSymbol() {
		return symbol;
	}

	public void setSymbol(String symbol) {
		this.symbol = symbol;
	}

	public double getPrice() {
		return price;
	}

	public void setPrice(double price) {
		this.price = price;
	}

	public double getDelta() {
		return delta;
	}

	public void setDelta(double delta) {
		this.delta = delta;
	}

	public String getLastUpdate() {
		return lastUpdate;
	}

	public void setLastUpdate(String lastUpdate) {
		this.lastUpdate = lastUpdate;
	}

	public DateFormat getDate() {
		return date;
	}

	public void setDate(DateFormat date) {
		this.date = date;
	}

	public void print() {
		System.out.println(this);
	}

	public void update(double delta2) {
		this.delta = delta2;
		this.price = this.price + this.price  * delta2;
		date = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
		Date todaysDate = new Date();
		lastUpdate = date.format(todaysDate);
	}

	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("").append(symbol).append(": price = ").append(price).append(", delta = ")
				.append(delta).append(", lastUpdate = ").append(lastUpdate);
		return builder.toString();
	}
}
