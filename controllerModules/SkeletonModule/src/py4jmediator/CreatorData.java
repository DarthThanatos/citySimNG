package py4jmediator;

import java.io.Serializable;
import java.util.List;
import java.util.stream.Stream;

import constants.Consts;
import entities.Building;
import entities.Dweller;
import entities.Resource;

public class CreatorData {

	private String textureOne;
	private String textureTwo;
	private String dependenciesSetName;
	private List<Building> buildings;
	private List<Resource> resources;
	private List<Dweller> dwellers;
	
	
	public String getTextureOne() {
		return textureOne;
	}
	public void setTextureOne(String textureOne) {
		this.textureOne = textureOne;
	}
	public String getTextureTwo() {
		return textureTwo;
	}
	public void setTextureTwo(String textureTwo) {
		this.textureTwo = textureTwo;
	}
	public String getDependenciesSetName() {
		return dependenciesSetName;
	}
	public void setDependenciesSetName(String dependenciesSetName) {
		this.dependenciesSetName = dependenciesSetName;
	}
	public List<Building> getBuildings() {
		return buildings;
	}
	public void setBuildings(List<Building> buildings) {
		this.buildings = buildings;
	}
	public List<Resource> getResources() {
		return resources;
	}
	public void setResources(List<Resource> resources) {
		this.resources = resources;
	}
	public List<Dweller> getDwellers() {
		return dwellers;
	}
	public void setDwellers(List<Dweller> dwellers) {
		this.dwellers = dwellers;
	}
	
	@Override 
	public String toString(){
		return "Dependencies set name: " + dependenciesSetName + "\n"
				+ "Texture One: " + textureOne + "\n"
				+ "Texture two: " + textureTwo + "\n"
				+ "Buildings: " + concatenateBuildings();
	}
	
	private String concatenateBuildings(){
		return buildings.size() == 0 ? "" : buildings.stream().map(Object::toString).reduce((b1, b2) -> b1 + b2).get(); 
	}
	
	private String concatenateDwellers(){
		return dwellers.size() == 0 ? "" : dwellers.stream().map(Object::toString).reduce((d1, d2) -> d1 + d2).get(); 
	}
	
	private String concatenateResources(){
		return resources.size() == 0 ? "" : resources.stream().map(Object::toString).reduce((r1, r2) -> r1 + r2).get();
		
	}
}
