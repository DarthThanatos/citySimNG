package dependencies.graph.monter;

import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONObject;

import mapnode.Building;
import model.DependenciesRepresenter;

public class BuildingsMonter {
	private ArrayList<Building> allBuildings;
	public BuildingsMonter(JSONArray buildingGraphDesc, DependenciesRepresenter dr){
		allBuildings = new ArrayList<Building>();
		List<String> buildingsNames = new ArrayList<String>();
		List<String> resourcesNames = dr.getResourcesNames();
		String relativeTexturesPath = "resources\\Textures\\";
		for (int i = 0; i < buildingGraphDesc.length(); i++){
			JSONObject buildingDesc = (JSONObject)buildingGraphDesc.get(i);
			Building building = new Building();
			String buildingName = buildingDesc.getString("Building\nName");
			building.setName(buildingName);
			buildingsNames.add(buildingName);
			building.setTexturePath(relativeTexturesPath + buildingDesc.getString("Texture path"));
			HashMap<String, Integer> consumes = new HashMap<>();
			HashMap<String, Integer> produces = new HashMap<>();
			HashMap<String, Integer> costs = new HashMap<>();
			String[] producedResources = buildingDesc.getString("Produces").split(" ");
			String[] consumedResources = buildingDesc.getString("Consumes").split(" ");
			String[] produceRates = buildingDesc.getString("Produce Rate").split(" ");
			String[] consumeRates = buildingDesc.getString("Consume Rate").split(" ");
			String[] costsDesc = buildingDesc.getString("Cost\nin\nresources").split(" ");
			for (String resourceName : resourcesNames){
				costs.put(resourceName, 0);
				produces.put(resourceName, 0);
				consumes.put(resourceName, 0);
			}
			for (String costDesc : costsDesc){
				String requiredResource = costDesc.split(":")[0];
				int costInResource = Integer.parseInt(costDesc.split(":")[1]);
				costs.put(requiredResource,costInResource);
			}
			for (int j = 0; j < producedResources.length; j++){
				int produceRate = Integer.parseInt(produceRates[j]);
				produces.put(producedResources[j], produceRate);
			}
			for (int j = 0; j < consumedResources.length; j++){
				int consumeRate = Integer.parseInt(consumeRates[j]);
				consumes.put(consumedResources[j], consumeRate);
			}	
			building.setResourcesCost(costs);
			building.setConsumes(consumes);
			building.setProduces(produces);
			allBuildings.add(building);
		}
		dr.putModuleData("allBuildings", allBuildings);
		dr.setBuildingsNames(buildingsNames);
	}
	
	public ArrayList<Building> getBuildingsList(){
		return allBuildings;
	}
}
