package exchange;
import javax.swing.table.*;
import javax.swing.*;

public class MarketDataModel extends AbstractTableModel
implements Runnable {

  Thread runner;
  MyStockTest market;
  int delay;

  public MarketDataModel(int initialDelay) {
    market = new MyStockTest();
    delay = initialDelay * 1000;
    Thread runner = new Thread(this);
    runner.start();
  }

  Stock[] stocks = new Stock[0];
  int[] stockIndices = new int[0];
  String[] headers = {"Symbol", "Price", "Change", "Last updated"};

  public int getRowCount() { return stocks.length; }
  public int getColumnCount() { return headers.length; }

  public String getColumnName(int c) { return headers[c]; }

  public Object getValueAt(int r, int c) {
    switch(c) {
    case 0:
      return stocks[r].symbol;
    case 1:
      return new Double(stocks[r].price);
    case 2:
      return new Double(stocks[r].delta);
    case 3:
      return stocks[r].lastUpdate;
    }
    throw new IllegalArgumentException("Bad cell (" + r + ", " + c +")");
  }

  public void setDelay(int seconds) { delay = seconds * 1000; }
  public void setStocks(int[] indices) {
    stockIndices = indices;
    updateStocks();
    fireTableDataChanged();
  }

  public void updateStocks() {
    stocks = new Stock[stockIndices.length];
    for (int i = 0; i < stocks.length; i++) {
      stocks[i] = market.getQuote(stockIndices[i]);
    }
  }

  public void run() {
    while(true) {

      updateStocks();


      fireTableRowsUpdated(0, stocks.length - 1);
      try { Thread.sleep(delay); }
      catch(InterruptedException ie) {}
    }
  }
}