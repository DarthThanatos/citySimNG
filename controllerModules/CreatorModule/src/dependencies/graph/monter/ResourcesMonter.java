package dependencies.graph.monter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import corectness.checker.CyclesChecker;
import org.json.JSONArray;
import org.json.JSONObject;

import constants.Consts;
import corectness.checker.CheckException;
import entities.Resource;
import graph.ResourceNode;
import model.DependenciesRepresenter;

public class ResourcesMonter extends GraphMonter{
	
	private JSONArray resourceGraphDesc;
	private HashMap<String, ResourceNode> resourceVertices;
	private DependenciesRepresenter dr;
	
	public ResourcesMonter(List<Resource> resources, DependenciesRepresenter dr){
		this.dr = dr;
		resourceGraphDesc = listToJSONArray(resources);
		resourceVertices = new HashMap<>();
		HashMap <String, Integer> incomes = new HashMap<>();
		List<String> resourcesNames = new ArrayList<String>();
		for(Resource resource : resources){
			String resourceName = resource.getName();
			resourcesNames.add(resourceName);
			incomes.put(resourceName, resource.getStartingIncome());
			ResourceNode resourceNode = new ResourceNode(resource);
			resourceVertices.put(resourceName, resourceNode);
		}
		
		dr.putModuleData(Consts.RESOURCES_LIST, resources);
		dr.putModuleData(Consts.RESOURCES_NAMES, resourcesNames);
		dr.putModuleData(Consts.INCOMES, incomes);
		dr.setResourcesNames(resourcesNames);
	}
	

	private JSONArray listToJSONArray(List<Resource> resources){
		JSONArray entities = new JSONArray();
		for(int i = 0; i < resources.size(); i++){
			JSONObject entity = new JSONObject()
				.put(Consts.RESOURCE_NAME, resources.get(i).getName())
				.put(Consts.PREDECESSOR, resources.get(i).getPredecessor())
				.put(Consts.SUCCESSOR, resources.get(i).getSuccessor());
			entities.put(i, entity);
		}
		return entities;
	}


	public HashMap<String, ResourceNode> getResourceVertices() {
		return resourceVertices;
	}

	public ResourcesMonter(JSONArray resourceGraphDesc, DependenciesRepresenter dr){
		this.resourceGraphDesc = resourceGraphDesc;
		this.dr = dr;
		resourceVertices = new HashMap<>();
		String relativeTexturesPath = Consts.RELATIVE_TEXTURES_PATH;
		ArrayList<String> resourcesNames = new ArrayList<String>();
		ArrayList<Resource> resourcesList = new ArrayList<Resource>();
		HashMap <String, Integer> incomes = new HashMap<>();
		for (int i = 0; i < resourceGraphDesc.length(); i++){
			JSONObject resourceJSONRepresentation = (JSONObject)resourceGraphDesc.get(i);
			String resourceName = resourceJSONRepresentation.getString(Consts.RESOURCE_NAME);
			String description = resourceJSONRepresentation.getString(Consts.DESCRIPTION);
			String texturePath = relativeTexturesPath + resourceJSONRepresentation.getString(Consts.TEXTURE_PATH);
			String predecessor = resourceJSONRepresentation.getString(Consts.PREDECESSOR);
			String successor = resourceJSONRepresentation.getString(Consts.SUCCESSOR);
			int startIncome = Integer.parseInt(resourceJSONRepresentation.getString(Consts.START_INCOME));
			Resource resource = new Resource(resourceName, predecessor, successor, texturePath, description);
			resourcesNames.add(resourceName);
			resourcesList.add(resource);
			incomes.put(resourceName, startIncome);
			ResourceNode resourceNode = new ResourceNode(resource);
			resourceVertices.put(resourceName, resourceNode);
		}
		dr.putModuleData(Consts.RESOURCES_LIST, resourcesList);
		dr.putModuleData(Consts.RESOURCES_NAMES, resourcesNames);
		dr.putModuleData(Consts.INCOMES, incomes);
		dr.setResourcesNames(resourcesNames);
		dr.getGraphsHolder().setResourceVertices(resourceVertices);
	}
	
	public void mountDependenciesGraph() throws CheckException{
		new CyclesChecker(resourceGraphDesc, Consts.RESOURCE_NAME).check();
		mountGraph(resourceVertices);
		dr.getGraphsHolder().setResourcesGraphs(rootsList);
		dr.getGraphsHolder().setResourceVertices(resourceVertices);
		
	}
}
