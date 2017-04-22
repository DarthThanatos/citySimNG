package mapnode;

import java.util.List;
import java.util.Map;

public class Building {
	private int sizeX;
	private int sizeY;
	private String texture;
	private String name;
	private Map<String, Integer> resourcesCost;
	
	public int getSizeX() {
		return sizeX;
	}
	
	public void setSizeX(int sizeX) {
		this.sizeX = sizeX;
	}
	
	public String getTexture() {
		return texture;
	}
	
	public void setTexture(String texture) {
		this.texture = texture;
	}
	
	public int getSizeY() {
		return sizeY;
	}
	
	public void setSizeY(int sizeY) {
		this.sizeY = sizeY;
	}
	
	public String getName() {
		return name;
	}
	
	public void setName(String name) {
		this.name = name;
	}

	public Map<String, Integer> getResourcesCost() {
		return resourcesCost;
	}

	public void setResourcesCost(Map<String, Integer> resourcesCost) {
		this.resourcesCost = resourcesCost;
	}
	
}
