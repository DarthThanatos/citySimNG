package mapnode;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.json.JSONObject.*;
import org.json.JSONObject;
import controlnode.SocketStreamSender;

public class Resources {
	private List<String> resources = new ArrayList<String>(Arrays.asList("wood", "rock", "gold"));
	private Map<String, Integer> incomes = new HashMap<String, Integer>();
	private Map<String, Integer> actualValues = new HashMap<String, Integer>();
	private SocketStreamSender sender;
	
	public Resources(SocketStreamSender sender){
		actualValues.put("wood", 0);
		actualValues.put("rock", 0);
		actualValues.put("gold", 0);
	
		incomes.put("wood", 3);
		incomes.put("rock", 2);
		incomes.put("gold", 10);
		
		this.sender = sender;
	}
	
	public void updateResources(){
		Map<String, String> actualValuseAndIncomes = new HashMap<String, String>();
		String sign = " +";
		for(String resource : resources){
			actualValues.put(resource, actualValues.get(resource) + incomes.get(resource));
			if(actualValues.get(resource) < 0)
				actualValues.put(resource, 0);
			if(incomes.get(resource) < 0)
				sign = " ";
			actualValuseAndIncomes.put(resource, actualValues.get(resource) + 
					sign + incomes.get(resource));
		}
		JSONObject json = new JSONObject(actualValuseAndIncomes);
		sender.setStream("Map@" + json);
		synchronized(sender){
			sender.notify();
		} 
	}
	
	public Map<String, Integer> getActualValues(){
		return this.actualValues;
	}
	
	public Map<String, Integer> getIncomes(){
		return this.incomes;
	}
	
	public List<String> getResources(){
		return this.resources;
	}
	
	
	public void setActualValues(Map<String, Integer> actualValues){
		this.actualValues = actualValues;
	}
	
	public void setIncomes(Map<String, Integer> incomes){
		this.incomes = incomes;
	}
	
	
}
