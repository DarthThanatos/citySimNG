package dependencies.graph.monter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.json.JSONArray;

import mapnode.Building;

public class BuildingsMonter {
	
	public BuildingsMonter(JSONArray buildingGraphDesc){
		ArrayList<Building> allBuildings = new ArrayList<Building>();
		Building b1 = new Building();
		b1.setName("house");
		b1.setTexturePath("Building1.png");
		Map a = new HashMap();
		a.put("rock", 2);
		a.put("wood", 10);
		a.put("gold", 0);
		b1.setResourcesCost(a);
		Map a2 = new HashMap();
		a2.put("rock", 1);
		a2.put("wood", 3);
		a2.put("gold", 0);
		b1.setProduces(a2);
		Map a3 = new HashMap();
		a3.put("gold", 3);
		a3.put("rock", 0);
		a3.put("wood", 0);
		b1.setConsumes(a3);
		
		Building b2 = new Building();
		b2.setName("shed");
		b2.setTexturePath("Building.png");
		Map b = new HashMap();
		b.put("wood", 15);
		b.put("rock", 0);
		b.put("gold", 0);
		b2.setResourcesCost(b);
		Map bm2 = new HashMap();
		bm2.put("rock", 1);
		bm2.put("wood", 3);
		bm2.put("gold", 0);
		b2.setProduces(bm2);
		Map bm3 = new HashMap();
		bm3.put("gold", 3);
		bm3.put("rock", 0);
		bm3.put("wood", 0);
		b2.setConsumes(bm3);
		
		Building b3 = new Building();
		b3.setName("windmill");
		b3.setTexturePath("Building3.png");
		Map c = new HashMap();
		c.put("wood", 15);
		c.put("rock", 2);
		c.put("gold", 0);
		b3.setResourcesCost(c);
		Map c2 = new HashMap();
		c2.put("rock", 1);
		c2.put("wood", 0);
		c2.put("gold", 3);
		b3.setProduces(c2);
		Map c3 = new HashMap();
		c3.put("wood", 3);
		c3.put("gold", 0);
		c3.put("rock", 0);
		b3.setConsumes(c3);
		
		allBuildings.add(b1);
		allBuildings.add(b2);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b3);
		allBuildings.add(b1);
		allBuildings.add(b2);
	}
}
