package exchange;

import javafx.beans.property.*;

public class Resource {

    private SimpleStringProperty name;
    private SimpleStringProperty priceString;
    private SimpleIntegerProperty quantity;
    private SimpleIntegerProperty playerQuantity;
    private double price;

    Resource(String name, double price, int quantity) {
        super();
        this.name = new SimpleStringProperty(name);
        this.priceString = new SimpleStringProperty(String.format("%.2f", price));
        this.quantity = new SimpleIntegerProperty(quantity);
        this.playerQuantity = new SimpleIntegerProperty(0);
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

    public Integer getQuantity() {
        return quantity.get();
    }

    public void setQuantity(Integer quantity) {
        this.quantity.set(quantity);
    }

    public Integer getPlayerQuantity() {
        return playerQuantity.get();
    }

    public void setPlayerQuantity(Integer playerQuantity) {
        this.playerQuantity.set(playerQuantity);
    }

}
