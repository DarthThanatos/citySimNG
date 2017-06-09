package corectness.checker;

import org.json.JSONArray;
import constants.CreatorConsts;

public class ResourcesChecker extends CyclesChecker{
	
	JSONArray resources;
	
	public ResourcesChecker(JSONArray resources){
		super(resources, CreatorConsts.RESOURCE_NAME);
		this.resources = resources;
	}

	@Override
	public void check() {
		
	}
}
