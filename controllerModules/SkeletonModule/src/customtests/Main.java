package customtests;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.UUID;

import controlnode.DispatchCenter;

public class Main {

	public static void main(String[] args){
		ArrayList<String> names = new ArrayList<>();
		//DispatchCenter dc = new DispatchCenter(names);
		for (String name : names)System.out.println(name);
		
		JSONObject obj = new JSONObject();
		System.out.println(obj);
		obj.put("UUID", UUID.randomUUID().toString() );
		obj.put("From", "Map");
		obj.put("To", "Menu");
		obj.put("To", "None");
		obj.put("Operation", "MoveTo");
		JSONObject nested = new JSONObject(obj.toString());
		obj.put("recursive", nested);
		System.out.println("Parsed JSON: " + obj.toString());
		
		HashMap<String, Object> map = new HashMap<>();
		List<String> list = new ArrayList<>(Arrays.asList("Robert", "Zenek", "Kinga"));
		map.put("list", list);
		for(String name: (ArrayList<String>)map.get("list")){
			System.out.println(name);
		}
		JSONArray arr = new JSONArray(list);
		JSONArray arr1 = new JSONArray(new ArrayList<String>());
		System.out.println(arr1);
		
		//dc.mainLoop();
	}
}
