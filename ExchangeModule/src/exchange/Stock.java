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

	public String symbol;
	public double price;
	public double delta;
	public String lastUpdate;
	DateFormat date;

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
