package exchange;

@SuppressWarnings("unused")
public class Resource {

    private String name;
    private int stockQuantity;
    private int playerQuantity;
    private double price;

    Resource(String name, double price, int stockQuantity) {
        super();
        this.name = name;
        this.stockQuantity = stockQuantity;
        this.playerQuantity = 0;
        this.price = price;
    }

    @SuppressWarnings("WeakerAccess")
    public String getName() {
        return this.name;
    }

    void setName(String name) {
        this.name = name;
    }

    double getPrice() {
        return this.price;
    }

    void setPrice(double price) {
        this.price = price;
    }

    int getStockQuantity() {
        return this.stockQuantity;
    }

    void setStockQuantity(int stockQuantity) {
        this.stockQuantity = stockQuantity;
    }

    int getPlayerQuantity() {
        return this.playerQuantity;
    }

    void setPlayerQuantity(int playerQuantity) {
        this.playerQuantity = playerQuantity;
    }

    // these three methods are implicitly used by resourceTable in StockView class
    public String getPriceString() {
        return String.format("%.2f", price);
    }

    public String getStockQuantityString() {
        return String.valueOf(stockQuantity);
    }

    public String getPlayerQuantityString() {
        return String.valueOf(playerQuantity);
    }

}
