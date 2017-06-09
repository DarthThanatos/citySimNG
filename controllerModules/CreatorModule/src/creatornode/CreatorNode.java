//* Init class responsible for creating new games with given parameters. Will be implemented in future. */ 

package creatornode;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

import org.json.JSONArray;
import org.json.JSONObject;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.SocketNode;
import dependencies.graph.monter.BuildingsMonter;
import dependencies.graph.monter.DwellersMonter;
import dependencies.graph.monter.ResourcesMonter;

public class CreatorNode extends SocketNode{
	
	public CreatorNode(DispatchCenter dispatchCenter, String nodeName) {
		super(dispatchCenter, nodeName);
		System.out.println("Created Creator Node");
		createDefaultDependencies();
	}

	private static JSONArray retrieveArrayFromObj(JSONObject obj){
		JSONArray resArray = new JSONArray();
		Set<String> names = obj.keySet(); 
		for (String name : names){
			resArray.put(obj.getJSONObject(name));
		}
		return resArray;
	}
	
	
	private void createDefaultDependencies(){

		try {
			BufferedReader br = new BufferedReader(new FileReader(new File("resources\\dependencies\\new_stronghold.dep")));
			String dependenciesString = "", line;
			while( (line = br.readLine()) != null ){
				dependenciesString += line + "\n";
			}
			br.close();
			String textureOneName = "Grass3.jpg";
			String textureTwoName = "Grass2.png";
			
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
			
			HashMap<String, DependenciesRepresenter> representers = null;
			try{
				 representers = (HashMap<String, DependenciesRepresenter>) dispatchCenter.getDispatchData("LoaderModule", "DependenciesRepresenters");
			}
			catch(Exception e){
				representers = new HashMap<>();	
				dispatchCenter.putDispatchData("LoaderModule", "DependenciesRepresenters", representers);
			}
			representers.put(dependenciesSetName, dr);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e1) {
			e1.printStackTrace();
		}
	}
	
	@Override
	public String parseCommand(String command, JSONObject args) {
		JSONObject envelope = new JSONObject();
		envelope.put("To", "Creator");
		if(command.equals("Parse")){
			JSONObject responseArgs = new JSONObject();
			responseArgs.put("UUID", args.getString("UUID"));
			envelope.put("Operation", "ParseConfirm");
			envelope.put("Args", responseArgs);
			
			String textureOneName = args.getString("Texture One");
			String textureTwoName = args.getString("Texture Two");
			JSONObject dependencies = args.getJSONObject("Dependencies");
			System.out.println("Creator node received following dependencies package:\n" + dependencies);
			JSONArray resources = dependencies.getJSONArray("Resources");
			JSONArray buildings = dependencies.getJSONArray("Buildings");
			JSONArray dwellers = dependencies.getJSONArray("Dwellers");
			String dependenciesSetName = args.getString("DependenciesSetName");
			DependenciesRepresenter dr = new DependenciesRepresenter();
			ResourcesMonter rm = new ResourcesMonter(resources, dr);
			BuildingsMonter bm = new BuildingsMonter(buildings, dr);
			DwellersMonter dm = new DwellersMonter(dwellers, dr);
			dr.setTextureAt(0, textureOneName);
			dr.setTextureAt(1, textureTwoName);
			//dr now contains all necessary data; let's pass it to dispatchCenter
			HashMap<String, DependenciesRepresenter> representers = null;
			try{
				 representers = (HashMap<String, DependenciesRepresenter>) dispatchCenter.getDispatchData("LoaderModule", "DependenciesRepresenters");
			}
			catch(Exception e){
				//e.printStackTrace();
				representers = new HashMap<>();	
				dispatchCenter.putDispatchData("LoaderModule", "DependenciesRepresenters", representers);
			}
			representers.put(dependenciesSetName, dr);
			
		}
		return envelope.toString();
	}

	@Override
	public void atStart() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void atExit() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void atUnload() {
		// TODO Auto-generated method stub
		
	}

}
