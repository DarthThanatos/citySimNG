package exchange;

import javafx.beans.property.*;

public class Resource {

    private SimpleStringProperty name;
    private SimpleStringProperty priceString;
    private SimpleIntegerProperty quantity;
    private double price;

    Resource(String name, double price, int quantity) {
        super();
        this.name = new SimpleStringProperty(name);
        this.priceString = new SimpleStringProperty(String.format("%.2f", price));
        this.quantity = new SimpleIntegerProperty(quantity);
        this.price = price;
    }

    public String getName() {
        return this.name.get();
    }

    public double getPrice() {
        return this.price;
    }

    void setPrice(double price) {
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
