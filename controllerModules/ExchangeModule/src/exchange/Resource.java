package exchange;

public class Resource {

    private String name;
    private int stockQuantity;
    private int playerQuantity;
    private double price;

    public Resource(String name, double price, int stockQuantity) {
        super();
        this.name = name;
        this.stockQuantity = stockQuantity;
        this.playerQuantity = 0;
        this.price = price;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getStockQuantity() {
        return this.stockQuantity;
    }

    public void setStockQuantity(int stockQuantity) {
        this.stockQuantity = stockQuantity;
    }

    public int getPlayerQuantity() {
        return this.playerQuantity;
    }

    public void setPlayerQuantity(int playerQuantity) {
        this.playerQuantity = playerQuantity;
    }

    public Double getPrice() {
        return this.price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public String getPriceString() {
        return String.format("%.2f", price);
    }

    public double getQuantityPriceRatio() {
        return this.stockQuantity / this.price;
    }

}
