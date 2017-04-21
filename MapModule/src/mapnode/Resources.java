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
		while(true){
			for(String resource : resources){
				actualValues.put(resource, actualValues.get(resource) + incomes.get(resource));
			}
			JSONObject json = new JSONObject(actualValues);
			System.out.println(json);
			synchronized(sender){
			sender.setStream("Map@" + json);
			sender.notify();
			}
			try{
				Thread.sleep(3000);
			}catch(InterruptedException ie){
				// TODO
			}
		}
	}
}
