package exchange;
import java.awt.*;
import javax.swing.*;

public class MarketTable extends JFrame {

  public MarketTable() {
    super("Dynamic Data Test");
    setSize(300, 200);
    setDefaultCloseOperation(EXIT_ON_CLOSE);

    MarketDataModel mdm = new MarketDataModel(5);

    mdm.setStocks(new int[] { 0, 1, 2 });

    JTable jt = new JTable(mdm);
    JScrollPane jsp = new JScrollPane(jt);
    getContentPane().add(jsp, BorderLayout.CENTER);
  }

  public static void main(String args[]) {
    MarketTable mt = new MarketTable();
    mt.setVisible(true);
  }
}