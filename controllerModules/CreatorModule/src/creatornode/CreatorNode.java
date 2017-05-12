//* Init class responsible for creating new games with given parameters. Will be implemented in future. */ 

package creatornode;
import org.json.JSONArray;
import org.json.JSONObject;

import model.DependenciesRepresenter;
import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.SocketNode;

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
			JSONArray buildings = dependencies.getJSONArray("Buildings");
			JSONArray resources = dependencies.getJSONArray("Resources");
			JSONArray dwellers = dependencies.getJSONArray("Dwellers");
			
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
