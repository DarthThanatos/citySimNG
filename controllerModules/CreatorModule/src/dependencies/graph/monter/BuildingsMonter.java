package dependencies.graph.monter;

import corectness.checker.CyclesChecker;
import entities.Building;
import graph.BuildingNode;

import java.util.*;

import constants.Consts;
import corectness.checker.BuildingsChecker;
import corectness.checker.CheckException;

import graph.DwellerNode;
import graph.ResourceNode;
import org.json.JSONArray;
import org.json.JSONObject;

import model.DependenciesRepresenter;

public class BuildingsMonter extends GraphMonter{
	
	private ArrayList<Building> allBuildings;
	private JSONArray buildingsGraphDesc;
	private HashMap<String, BuildingNode> buildingVertices; 
	private DependenciesRepresenter dr;
	
	public BuildingsMonter(List<Building> buildings, DependenciesRepresenter dr){
		this.dr = dr;
		allBuildings = new ArrayList<Building>(buildings);
		buildingVertices = new HashMap<>();
		dr.putModuleData(Consts.ALL_BUILDINGS, buildings);
		
		List<String> buildingsNames = new ArrayList<>();
		for(Building building : buildings){
			String buildingName = building.getName();
			buildingsNames.add(buildingName);
			BuildingNode buildingNode = new BuildingNode(building);
			buildingVertices.put(buildingName, buildingNode);
			
		}
		dr.setBuildingsNames(buildingsNames);
		buildingsGraphDesc = listToJSONArray(buildings);
	}
	

	private JSONArray listToJSONArray(List<Building> buildings){
		JSONArray entities = new JSONArray();
		for(int i = 0; i < buildings.size(); i++){
			JSONObject entity = new JSONObject()
				.put(Consts.BUILDING_NAME, buildings.get(i).getName())
				.put(Consts.PREDECESSOR, buildings.get(i).getPredecessor())
				.put(Consts.SUCCESSOR, buildings.get(i).getSuccessor());
			entities.put(i, entity);
		}
		return entities;
	}
	
	public BuildingsMonter(JSONArray buildingGraphDesc, DependenciesRepresenter dr){
		this.buildingsGraphDesc = buildingGraphDesc;
		this.dr = dr;
		allBuildings = new ArrayList<Building>();
		buildingVertices = new HashMap<>();
		List<String> buildingsNames = new ArrayList<String>();
		List<String> resourcesNames = dr.getResourcesNames();
		String relativeTexturesPath = Consts.RELATIVE_TEXTURES_PATH;
		for (int i = 0; i < buildingGraphDesc.length(); i++){
			JSONObject buildingDesc = (JSONObject)buildingGraphDesc.get(i);
			Building building = new Building();
			String buildingName = buildingDesc.getString(Consts.BUILDING_NAME);
			building.setName(buildingName);
			buildingsNames.add(buildingName);
			building.setTexturePath(relativeTexturesPath + buildingDesc.getString(Consts.TEXTURE_PATH));
			building.setType(buildingDesc.getString(Consts.TYPE));
			building.setDwellersName(buildingDesc.getString(Consts.DWELLER_NAME));
			building.setDwellersAmount(buildingDesc.getInt(Consts.DWELLERS_AMOUNT));

			String predeccessor = buildingDesc.getString(Consts.PREDECESSOR);
			String successor = buildingDesc.getString(Consts.SUCCESSOR);
			building.setPredecessor(predeccessor);
			building.setSuccessor(successor);
			
			HashMap<String, Integer> consumes = new HashMap<>();
			HashMap<String, Integer> produces = new HashMap<>();
			HashMap<String, Integer> costs = new HashMap<>();
			JSONObject producedResources = buildingDesc.getJSONObject(Consts.PRODUCES);
			JSONObject consumedResources = buildingDesc.getJSONObject(Consts.CONSUMES);
			JSONObject costsDesc = buildingDesc.getJSONObject(Consts.COST_IN_RESOURCES);
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
			BuildingNode buildingNode = new BuildingNode(building);
			buildingVertices.put(buildingName, buildingNode);
		}
		dr.putModuleData(Consts.ALL_BUILDINGS, allBuildings);
		dr.setBuildingsNames(buildingsNames);
	}
	
	public ArrayList<Building> getBuildingsList(){
		return allBuildings;
	}
	
	public void mountDependenciesGraph() throws CheckException{
		new CyclesChecker(buildingsGraphDesc, Consts.BUILDING_NAME).check();
		mountGraph(buildingVertices);
		dr.getGraphsHolder().setBuildingsGraphs(rootsList);
		dr.getGraphsHolder().setBuildingsVertices(buildingVertices);
		new BuildingsChecker(dr).check();
	}
}
