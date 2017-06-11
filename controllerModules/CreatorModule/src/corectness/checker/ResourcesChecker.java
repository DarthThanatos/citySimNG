package corectness.checker;

import graph.ResourceNode;

import java.util.HashMap;

import org.json.JSONArray;

import constants.Consts;

public class ResourcesChecker extends CyclesChecker{

	HashMap<String, ResourceNode> resourceVertices;
	
	public ResourcesChecker(JSONArray resources, HashMap<String, ResourceNode> resourceVertices){
		super(resources, Consts.RESOURCE_NAME);
		this.resourceVertices = resourceVertices;
	}

}
