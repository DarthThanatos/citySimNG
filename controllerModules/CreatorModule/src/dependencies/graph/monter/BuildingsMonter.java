package dependencies.graph.monter;

import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import constants.CreatorConsts;

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
		String relativeTexturesPath = CreatorConsts.RELATIVE_TEXTURES_PATH;
		for (int i = 0; i < buildingGraphDesc.length(); i++){
			JSONObject buildingDesc = (JSONObject)buildingGraphDesc.get(i);
			Building building = new Building();
			String buildingName = buildingDesc.getString(CreatorConsts.BUILDING_NAME);
			building.setName(buildingName);
			buildingsNames.add(buildingName);
			building.setTexturePath(relativeTexturesPath + buildingDesc.getString(CreatorConsts.TEXTURE_PATH));
			HashMap<String, Integer> consumes = new HashMap<>();
			HashMap<String, Integer> produces = new HashMap<>();
			HashMap<String, Integer> costs = new HashMap<>();
			JSONObject producedResources = buildingDesc.getJSONObject(CreatorConsts.PRODUCES);
			JSONObject consumedResources = buildingDesc.getJSONObject(CreatorConsts.CONSUMES);
			JSONObject costsDesc = buildingDesc.getJSONObject(CreatorConsts.COST_IN_RESOURCES);
			for (String resourceName : resourcesNames){
				costs.put(resourceName, 0);
				produces.put(resourceName, 0);
				consumes.put(resourceName, 0);
			}

			Iterator<?> costsDescKeys = costsDesc.keys();
			while(costsDescKeys.hasNext()){
				String requiredResource = (String)costsDescKeys.next();
				int costInResource = costsDesc.getInt(requiredResource);
				costs.put(requiredResource,costInResource);
			}
			Iterator<?> producedResourcesKeys = producedResources.keys();
			while(producedResourcesKeys.hasNext()){
				String producedResource = (String) producedResourcesKeys.next();
				int produceRate = producedResources.getInt(producedResource);
				produces.put(producedResource, produceRate);
			}
			Iterator<?> consumedResourcesKeys = consumedResources.keys();
			while(consumedResourcesKeys.hasNext()){
				String consumedResource = (String) consumedResourcesKeys.next();
				int consumeRate = consumedResources.getInt(consumedResource);
				consumes.put(consumedResource, consumeRate);
			}	
			building.setResourcesCost(costs);
			building.setConsumes(consumes);
			building.setProduces(produces);
			allBuildings.add(building);
		}
		dr.putModuleData(CreatorConsts.ALL_BUILDINGS, allBuildings);
		dr.setBuildingsNames(buildingsNames);
	}
	
	public ArrayList<Building> getBuildingsList(){
		return allBuildings;
	}
}
