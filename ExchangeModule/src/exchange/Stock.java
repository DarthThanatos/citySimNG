package exchange;
public class Stock {

public Stock(String string, double d) {
        this.symbol = string;
        this.price = d;
    }

    public String symbol;
    public double price;
    public double delta;
    public String lastUpdate;

    public void print() {
        System.out.println(this);
    }

    public void update(double delta2) {
        this.delta = delta2;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder.append("Stock [symbol=").append(symbol).append(", price=").append(price).append(", delta=").append(delta).append(", lastUpdate=")
                .append(lastUpdate).append("]");
        return builder.toString();
    }
}