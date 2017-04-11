package exchange;

import javax.swing.*;
import java.awt.*;
import java.util.*;

/** For testing purposes */

public class MyStockTest extends JFrame implements Runnable {

	private static final long serialVersionUID = 1L;
	Stock[] market = { new Stock("Food", 14.57),
			new Stock("Water", 17.44),
			new Stock("Wood", 16.44),
			new Stock("Iron", 7.21),
			new Stock("Gold", 27.40) };
	boolean monitor;
	Random rg = new Random();
	Thread runner;

	public MyStockTest() {
		// Not meant to be shown as a real frame
		super("Thread only version . . .");
		runner = new Thread(this);
		runner.start();
	}

	public MyStockTest(boolean monitorOn) {
		super("Stock Market Monitor");
		setSize(400, 100);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		monitor = monitorOn;

		getContentPane().add(new JLabel("Trading is active.  " + "Close this window to close the market."),
				BorderLayout.CENTER);
		runner = new Thread(this);
		runner.start();
	}

	public void run() {
		while (true) {
			int whichStock = Math.abs(rg.nextInt()) % market.length;
			double delta = rg.nextDouble() - 0.4;
			market[whichStock].update(delta);
			if (monitor) {
				market[whichStock].print();
			}
			try {
				Thread.sleep(1000);
			} catch (InterruptedException ie) {
			}
		}
	}

	public Stock getQuote(int index) {
		return market[index];
	}

	// This method returns the list of all the symbols in the market table
	public String[] getSymbols() {
		String[] symbols = new String[market.length];
		for (int i = 0; i < market.length; i++) {
			symbols[i] = market[i].symbol;
		}
		return symbols;
	}

	public static void main(String args[]) {
		MyStockTest myMarket = new MyStockTest(true);
		myMarket.setVisible(true);
	}
}
