package exchange;

import javax.swing.table.*;
import java.util.List;
import javax.swing.*;

@SuppressWarnings("serial")
public class StockTableModel extends AbstractTableModel {

	String[] columnNames = { "Name", "Price" };
	List<Resource> stock;


	public StockTableModel(List<Resource> stock) {
		this.stock = stock;
	}

	public int getRowCount() {
		return stock.size();
	}

	public int getColumnCount() {
		return columnNames.length;
	}

	public String getColumnName(int columnIndex) {
		return columnNames[columnIndex];
	}

	public Object getValueAt(int rowIndex, int columnIndex) {
		switch (columnIndex) {
		case 0:
			return stock.get(rowIndex).getName();
		case 1:
			return String.format("%.2f", stock.get(rowIndex).getPrice());
		}
		throw new IllegalArgumentException("Bad cell (" + rowIndex + ", " + columnIndex + ")");
	}
}