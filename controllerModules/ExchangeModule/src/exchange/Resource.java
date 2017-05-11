package exchange;

public class Resource {

	public static final double defaultPrice = 100.0;

	private String name;
	private double price;
	private double oldprice;
	private double quantity;

	Resource() {
		super();
	}

	Resource(String name) {
		super();
		this.name = name;
		this.price = defaultPrice;
	}

	Resource(String name, double price) {
		super();
		this.name = name;
		this.price = price;
	}

	public Resource(String name, double price, double quantity) {
		super();
		this.name = name;
		this.price = price;
		this.quantity = quantity;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public double getPrice() {
		return price;
	}

	public void setPrice(double price) {
		this.price = price;
	}

	public double getQuantity() {
		return quantity;
	}

	public void setQuantity(double quantity) {
		this.quantity = quantity;
	}

	public void update(double delta) {
		this.oldprice = this.price;
		this.price = this.price + this.price * delta;
		// printChange();
	}

	// method for debugging purposes
	public void printChange() {
		System.out.println(this.name+": old price = "+this.oldprice+", new price = "+this.price);
	}

	@Override
	public String toString() {
		return "Resource [name=" + name + ", price=" + price + ", quantityToBuy="+ quantity + "]";
	}

}
