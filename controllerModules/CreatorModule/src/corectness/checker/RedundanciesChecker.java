package corectness.checker;

import java.util.List;

import org.json.JSONArray;

public class RedundanciesChecker implements CorrectnessChecker{
	
	protected JSONArray entities;
	private List<String> uniqueNames;
	protected String key;
	
	public RedundanciesChecker(JSONArray entities, String key){
		this.entities = entities;
		this.key = key;
	}
	
	@Override
	public void check() throws CheckException {
		for (int i = 0; i < entities.length(); i++){
			String itemName = entities.getJSONObject(i).getString(key);
			if (uniqueNames.contains(itemName)){
				String errorMsg = "Duplicate items for name " + itemName;
				throw new CheckException(errorMsg);
			}
			uniqueNames.add(itemName);
		}
	}
}
