package ranking;

public class User {
	private final String name;
	private double money;
	private int nrOfGames;
	
	public User(String name, double money, int nrOfGames){
		this.name = name;
		this.money = money;
		this.nrOfGames = nrOfGames;
	}

	public String getName() {
		return name;
	}

	public double getMoney() {
		return money;
	}

	public void setMoney(double money) {
		this.money = money;
	}

	public int getNrOfGames() {
		return nrOfGames;
	}

	public void setNrOfGames(int nrOfGames) {
		this.nrOfGames = nrOfGames;
	}

}
