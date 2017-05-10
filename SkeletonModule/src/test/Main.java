package test;

import java.util.ArrayList;

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
		
		//dc.mainLoop();
	}
}
