package exchange;

import java.util.*;

import javax.swing.JOptionPane;

import model.DependenciesRepresenter;

public class Stock {

	private List<Resource> resources = new ArrayList<>();
	private RepresenterMock player;
	private DependenciesRepresenter dependenciesRepresenter;
	private String[] names;
	private boolean working;
	Random random;

	public Stock() {
		random = new Random();
		this.setWorking(true);
	}

	public void setDependenciesRepresenter(DependenciesRepresenter dependenciesRepresenter){
		this.dependenciesRepresenter = dependenciesRepresenter;
	}

	public DependenciesRepresenter getDependenciesRepresenter(){
		return dependenciesRepresenter;
	}

	public List<Resource> getResources() {
		return resources;
	}

	public boolean isWorking() {
		return working;
	}

	public void setWorking(boolean working) {
		if(working == true) {
			System.out.println("Stock is working");
		}
		else {
			System.out.println("Stock is stopped");
		}
		this.working = working;
	}

	public void init(List<String> resourcesNames) {
		names = new String[resourcesNames.size()];
		int i = 0;
		for (String name : resourcesNames) {
			double initPrice = random.nextDouble() * 10;
			resources.add(new Resource(name, initPrice));
			names[i] = name;
			i++;
		}
	}

	public String[] getNames() {
		return names;
	}

	public void setPlayer(RepresenterMock player) {
		this.player = player;
	}

	public Resource getResource(String name) {
		for (Resource resource : resources) {
			if (resource.getName().equals(name)) {
				return resource;
			}
		}
		return null;
	}

	public void stockOperation(String resourceName, double amount, String operation) {
		if (operation.startsWith("buy")) {
			if (player.getMoney() > amount * getResource(resourceName).getPrice()) {
				double currentResources = player.getPlayerResources().get(resourceName);
				player.getPlayerResources().put(resourceName, currentResources + amount);
				player.setMoney(player.getMoney() - amount * getResource(resourceName).getPrice());
				JOptionPane.showMessageDialog(null, "You bought " + resourceName + ", and now you have "
						+ player.getPlayerResources().get(resourceName)+" units", "", JOptionPane.WARNING_MESSAGE);
			} else {
				JOptionPane.showMessageDialog(null, "Not enough money", "", JOptionPane.WARNING_MESSAGE);
			}
		} else {
			if (player.getPlayerResources().get(resourceName) > amount) {
				double currentResources = player.getPlayerResources().get(resourceName);
				player.getPlayerResources().put(resourceName, currentResources - amount);
				player.setMoney(player.getMoney() + amount * getResource(resourceName).getPrice());
				JOptionPane.showMessageDialog(null, "You sold " + resourceName + ", and now you have "
						+ player.getMoney()+" gold coins", "", JOptionPane.WARNING_MESSAGE);
			} else {
				JOptionPane.showMessageDialog(null, "Not enough resources", "", JOptionPane.WARNING_MESSAGE);
			}
		}
	}
}
