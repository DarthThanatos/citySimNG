import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Set;

import model.DependenciesRepresenter;

import org.json.JSONArray;
import org.json.JSONObject;
import dependencies.graph.monter.BuildingsMonter;
import dependencies.graph.monter.DwellersMonter;
import dependencies.graph.monter.ResourcesMonter;


public class Main {
	
	private static JSONArray retrieveArrayFromObj(JSONObject obj){
		JSONArray resArray = new JSONArray();
		Set<String> names = obj.keySet(); 
		for (String name : names){
			resArray.put(obj.getJSONObject(name));
		}
		return resArray;
	}
	
	private static void createDefaultDependencies(){
		try {
			BufferedReader br = new BufferedReader(new FileReader(new File("..\\..\\resources\\dependencies\\new_stronghold.dep")));
			String dependenciesString = "", line;
			while( (line = br.readLine()) != null ){
				dependenciesString += line + "\n";
			}
			br.close();
			String textureOneName = "resources\\Textures\\Grass2.png";
			String textureTwoName = "resources\\Textures\\Grass3.jpg";
			
			JSONObject dependencies = new JSONObject(dependenciesString);
			System.out.println("Creator node received following dependencies package:\n" + dependencies);
			
			JSONArray resources = retrieveArrayFromObj(dependencies.getJSONObject("Resources"));		
			JSONArray buildings = retrieveArrayFromObj(dependencies.getJSONObject("Buildings"));
			JSONArray dwellers = retrieveArrayFromObj(dependencies.getJSONObject("Dwellers"));
			String dependenciesSetName = "Default Set";
			
			DependenciesRepresenter dr = new DependenciesRepresenter();
			ResourcesMonter rm = new ResourcesMonter(resources, dr);
			BuildingsMonter bm = new BuildingsMonter(buildings, dr);
			DwellersMonter dm = new DwellersMonter(dwellers, dr);
			dr.setTextureAt(0, textureOneName);
			dr.setTextureAt(1, textureTwoName);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e1) {
			e1.printStackTrace();
		}
	}
	
	public static void main(String [] args){
		createDefaultDependencies();
	}
}
