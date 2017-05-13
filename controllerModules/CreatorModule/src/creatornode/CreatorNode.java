//* Init class responsible for creating new games with given parameters. Will be implemented in future. */ 

package creatornode;
import java.util.HashMap;
import java.util.List;

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
