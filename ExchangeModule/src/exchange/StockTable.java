package exchange;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.util.Arrays;
import java.util.List;
import javax.swing.*;
import javax.swing.table.TableColumn;

public class StockTable extends JFrame {

	private static final long serialVersionUID = 1L;

	public StockTable(Stock stock) {
		super("Stock Data");
		setSize(300, 210);
		setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
	//	setDefaultCloseOperation(EXIT_ON_CLOSE);
		Dimension dim = Toolkit.getDefaultToolkit().getScreenSize();
		this.setLocation(dim.width/2-this.getSize().width/2, dim.height/2-this.getSize().height/2);
		Font font = new Font("Verdana", Font.BOLD, 20);
		this.setFont(font);

		JFrame me = this;
		WindowListener exitListener = new WindowAdapter() {

		    @Override
		    public void windowClosing(WindowEvent e) {
		    	me.setAlwaysOnTop(false);
		        int confirm = JOptionPane.showOptionDialog(
		             null, "Are you sure to close stock?",
		             "Closing confirmation", JOptionPane.YES_NO_OPTION,
		             JOptionPane.QUESTION_MESSAGE, null, null, null);
		        if (confirm == 0) {
		        	setVisible(false);
		            stock.setWorking(true);
		        }
		    	me.setAlwaysOnTop(false);
		    }
		};
		this.addWindowListener(exitListener);

		StockTableModel stockModel = new StockTableModel(stock.getResources());
		JTable table = new JTable(stockModel);

		table.setFont(font);
		table.setRowHeight(30);
		TableColumn col0 = table.getColumnModel().getColumn(0);
		col0.setPreferredWidth(125);
		TableColumn col1 = table.getColumnModel().getColumn(1);
		col1.setPreferredWidth(125);

		JPanel panel = new JPanel();
		panel.setPreferredSize(new Dimension(300, 130));
		panel.add(table.getTableHeader(), BorderLayout.NORTH);
		panel.add(table, BorderLayout.CENTER);
		getContentPane().add(panel, BorderLayout.PAGE_START);

		JComboBox<String> resourceList = new JComboBox<String>(stock.getNames());
		JTextField textField = new JTextField("0");

		JPanel buttons = new JPanel();
		Button sellButton = new Button("SELL");
		sellButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String resourceName = (String)resourceList.getSelectedItem();
				double amount =  Double.parseDouble(textField.getText());
				me.setAlwaysOnTop(false);
				stock.stockOperation(resourceName, amount, "sell");
				me.setAlwaysOnTop(true);
			}
		} );

		Button buyButton = new Button("BUY");
		buyButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String resourceName = (String)resourceList.getSelectedItem();
				double amount =  Double.parseDouble(textField.getText());
				me.setAlwaysOnTop(false);
				stock.stockOperation(resourceName, amount, "buy");
				me.setAlwaysOnTop(true);
			}
		} );

		Button exitButton = new Button("EXIT");
		exitButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
		    	me.setAlwaysOnTop(false);
		        setVisible(false);
		        stock.setWorking(true);
		    	me.setAlwaysOnTop(false);
			}
		} );

		buttons.add(sellButton);
		buttons.add(buyButton);
		buttons.add(exitButton);
		getContentPane().add(resourceList, BorderLayout.LINE_START);
		getContentPane().add(textField, BorderLayout.CENTER);
		getContentPane().add(buttons, BorderLayout.LINE_END);
		this.setAlwaysOnTop(true);

	}
}
