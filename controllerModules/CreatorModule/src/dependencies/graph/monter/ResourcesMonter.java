package dependencies.graph.monter;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import javax.print.attribute.HashAttributeSet;

import org.json.JSONArray;
import org.json.JSONObject;

import mapnode.Resource;
import model.DependenciesRepresenter;

public class ResourcesMonter {
	
	public ResourcesMonter(JSONArray resourceGraphDesc, DependenciesRepresenter dr){
		String relativeTexturesPath = "resources\\Textures\\";
		ArrayList<String> resourcesNames = new ArrayList<String>();
		ArrayList<Resource> resourcesList = new ArrayList<Resource>();
		HashMap <String, Integer> incomes = new HashMap<>();
		for (int i = 0; i < resourceGraphDesc.length(); i++){
			JSONObject resourceJSONRepresentation = (JSONObject)resourceGraphDesc.get(i);
			String resourceName = resourceJSONRepresentation.getString("Resource\nName");
			String texturePath = relativeTexturesPath + resourceJSONRepresentation.getString("Texture path");
			String predecessor = resourceJSONRepresentation.getString("Predecessor");
			String successor = resourceJSONRepresentation.getString("Successor");
			int startIncome = Integer.parseInt(resourceJSONRepresentation.getString("Start income"));
			Resource resource = new Resource(resourceName, predecessor, successor, texturePath);
			resourcesNames.add(resourceName);
			resourcesList.add(resource);
			incomes.put(resourceName, startIncome);			
		}
		dr.putModuleData("resourcesList", resourcesList);
		dr.putModuleData("resourcesNames", resourcesNames);
		dr.putModuleData("incomes", incomes);
		dr.setResourcesNames(resourcesNames);
	}
}
