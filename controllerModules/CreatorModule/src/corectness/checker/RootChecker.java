package corectness.checker;

import org.json.JSONArray;
import org.json.JSONObject;

public class RootChecker {
	
	JSONObject dependencies;
	ResourcesChecker resourcesChecker;
	BuildingsChecker buildingsChecker;
	DwellersChecker dwellersChecker;
	
	public RootChecker(JSONObject dependencies){
		this.dependencies = dependencies;
		
		JSONArray resources = dependencies.getJSONArray("Resources");
		JSONArray buildings = dependencies.getJSONArray("Buildings");
		JSONArray dwellers = dependencies.getJSONArray("Dwellers");
	}
	
	public void checkCorrectness(){
		
	}
}
