package dependencies.graph.monter;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import javax.print.attribute.HashAttributeSet;

import org.json.JSONArray;
import org.json.JSONObject;

import constants.Consts;
import corectness.checker.CheckException;
import corectness.checker.ResourcesChecker;
import entities.Resource;
import graph.ResourceNode;
import model.DependenciesRepresenter;

public class ResourcesMonter extends GraphMonter{
	
	private JSONArray resourceGraphDesc;
	private HashMap<String, ResourceNode> resourceVertices;
	private DependenciesRepresenter dr;
	
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
			String texturePath = relativeTexturesPath + resourceJSONRepresentation.getString(Consts.TEXTURE_PATH);
			String predecessor = resourceJSONRepresentation.getString(Consts.PREDECESSOR);
			String successor = resourceJSONRepresentation.getString(Consts.SUCCESSOR);
			int startIncome = Integer.parseInt(resourceJSONRepresentation.getString(Consts.START_INCOME));
			Resource resource = new Resource(resourceName, predecessor, successor, texturePath);
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
		ResourcesChecker resourcesChecker = new ResourcesChecker(resourceGraphDesc, resourceVertices);
		resourcesChecker.check();
		System.out.println("Resources: ");
		mountGraph(resourceVertices);
		dr.getGraphsHolder().setResourcesGraphs(rootsList);
		dr.getGraphsHolder().setResourceVertices(resourceVertices);
		
	}
}
