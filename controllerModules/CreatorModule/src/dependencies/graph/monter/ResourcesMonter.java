package dependencies.graph.monter;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import javax.print.attribute.HashAttributeSet;

import org.json.JSONArray;
import org.json.JSONObject;

import constants.CreatorConsts;
import mapnode.Resource;
import model.DependenciesRepresenter;

public class ResourcesMonter {
	
	public ResourcesMonter(JSONArray resourceGraphDesc, DependenciesRepresenter dr){
		String relativeTexturesPath = CreatorConsts.RELATIVE_TEXTURES_PATH;
		ArrayList<String> resourcesNames = new ArrayList<String>();
		ArrayList<Resource> resourcesList = new ArrayList<Resource>();
		HashMap <String, Integer> incomes = new HashMap<>();
		for (int i = 0; i < resourceGraphDesc.length(); i++){
			JSONObject resourceJSONRepresentation = (JSONObject)resourceGraphDesc.get(i);
			String resourceName = resourceJSONRepresentation.getString(CreatorConsts.RESOURCE_NAME);
			String texturePath = relativeTexturesPath + resourceJSONRepresentation.getString(CreatorConsts.TEXTURE_PATH);
			String predecessor = resourceJSONRepresentation.getString(CreatorConsts.PREDECESSOR);
			String successor = resourceJSONRepresentation.getString(CreatorConsts.SUCCESSOR);
			int startIncome = Integer.parseInt(resourceJSONRepresentation.getString(CreatorConsts.START_INCOME));
			Resource resource = new Resource(resourceName, predecessor, successor, texturePath);
			resourcesNames.add(resourceName);
			resourcesList.add(resource);
			incomes.put(resourceName, startIncome);			
		}
		dr.putModuleData(CreatorConsts.RESOURCES_LIST, resourcesList);
		dr.putModuleData(CreatorConsts.RESOURCES_NAMES, resourcesNames);
		dr.putModuleData(CreatorConsts.INCOMES, incomes);
		dr.setResourcesNames(resourcesNames);
	}
}
