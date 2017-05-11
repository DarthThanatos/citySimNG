package exchange;

import java.util.*;

public class RepresenterMock {
	private double money;
	private HashMap<String, Double> playerResources = new HashMap<>();

	public RepresenterMock(List<String> resources) {
		for(String res: resources) {
			playerResources.put(res, 1000.0);
		}
		this.money = 10000;
	}

	public double getMoney() {
		return money;
	}

	public void setMoney(double money) {
		this.money = money;
	}

	public HashMap<String, Double> getPlayerResources() {
		return playerResources;
	}

	public void setPlayerResources(HashMap<String, Double> playerResources) {
		this.playerResources = playerResources;
	}
}
