package model;
import org.json.*;

import java.util.*;

//* Management class for Model */
public  class ModelKeeper {

	private HashMap<String, Model> models;
	
	
	
	public Model fetchData(String key){
		return models.get(key);
	}
	
	public void buildDataFromJSON(){
		JSONObject obj = new JSONObject(" .... ");
		String pageName = obj.getJSONObject("pageInfo").getString("pageName");

		JSONArray arr = obj.getJSONArray("posts");
		for (int i = 0; i < arr.length(); i++)
		{
		    String post_id = arr.getJSONObject(i).getString("post_id");

		}
	}
	
}
