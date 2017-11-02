package model;

import constants.CreatorConfig;
import graph.GraphsHolder;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

//* Primary class for all inheritance modules */ 
public class DependenciesRepresenter {
	
	private List<String> buildingsNames;
	private List<String> resourcesNames;
	private List<String> dwellersNames;
	private HashMap<String, Object> dependencies;
	private double money;
	private Map<String, Integer> stockPile;
	private String[] texturesNames = {CreatorConfig.TEXTURE_ONE_DEFAULT_NAME, CreatorConfig.TEXTURE_TWO_DEFAULT_NAME};
	private GraphsHolder graphsHolder;
	private String mp3 = CreatorConfig.MP3_DEFAULT_NAME;
	private String panelTexture = CreatorConfig.PANEL_TEXURE_DEFAULT_NAME;

	public void setMp3(String mp3){
		this.mp3 = mp3;
	}

	public String getMp3(){
		return mp3;
	}

	public String getPanelTexture() {
		return panelTexture;
	}

	public void setPanelTexture(String panelTexture) {
		this.panelTexture = panelTexture;
	}

	public DependenciesRepresenter(){
		dependencies = new HashMap<>();
		graphsHolder = new GraphsHolder();
	}
	

	public GraphsHolder getGraphsHolder(){
		return graphsHolder;
	}
	
	public String getTextureAt(int index){
		if (index < 0 || index >= 2) return "DefaultBuilding.jpg";
		return texturesNames[index];
	}

	public void setTextureAt(int index, String textureName){
		texturesNames[index] = textureName;
	}

	public Map<String,Integer> getStockPile(){
		return stockPile;
	}
	
	public void setStockPile(Map<String, Integer> actualValues){
		this.stockPile = actualValues;
	}
	
	public void setMoney(double money){
		this.money = money;
	}
	
	public double getMoney(){
		return money;
	}
	
	public void setBuildingsNames(List<String> buildingsNames){
		this.buildingsNames = buildingsNames;
	}
	
	public void setResourcesNames(List<String> resourcesNames){
		this.resourcesNames = resourcesNames;
	}
	
	public void setDwellersNames(List<String> dwellersNames){
		this.dwellersNames = dwellersNames;
	}
	
	public List<String> getBuildingsNames(){
		return buildingsNames;
	}

	public List<String> getResourcesNames(){
		return resourcesNames;
	}
	
	public List<String> getDwellersNames(){
		return dwellersNames;
	}
	
	public void putModuleData(String dataName, Object data){
		dependencies.put(dataName, data);
	}
	
	public Object getModuleData(String dataName){
		return dependencies.get(dataName);
	}
	
}
