package creatornode;

import java.util.ArrayList;



import java.util.HashMap;

import model.DependenciesRepresenter;
import monter.LoaderMonter;

import org.json.JSONArray;
import org.json.JSONObject;

import controlnode.DispatchCenter;
import controlnode.Node;
import controlnode.SocketNode;

public class LoaderNode extends SocketNode{

	public LoaderNode(DispatchCenter dispatchCenter, String nodeName) {
		super(dispatchCenter, nodeName);
		// TODO Auto-generated constructor stub
	}

	@Override
	public String parseCommand(String command, JSONObject args) {
		JSONObject envelope = new JSONObject();
		envelope.put("To", "Loader");
		if(command.equals("Select")){
			String chosenSet = args.getString("SetChosen");
			System.out.println(nodeName + ": got string selection: " + chosenSet);
			String operationId = args.getString("UUID");
			JSONObject ackArgs = new JSONObject();
			ackArgs.put("UUID",operationId);
			envelope.put("Operation", "SelectConfirm");
			envelope.put("Args", ackArgs);
			//assuming that at least atStart() method initialized empty hashmap; no exception expected
			HashMap<String, DependenciesRepresenter> representers = (HashMap<String, DependenciesRepresenter>) dispatchCenter.getDispatchData("LoaderModule", "DependenciesRepresenters");
			DependenciesRepresenter dr = representers.get(chosenSet);
			
			//dynamically mount new set of rules
			LoaderMonter monter = new LoaderMonter("resources\\injectFiles\\loaderInject.txt", new String[]{}, dispatchCenter, dr);
			Node menu = monter.mount(new ArrayList<String>());
			menu.setParent(nodeName, this);
			neighbors = new HashMap<>();
			neighbors.put(menu.getNodeName(),menu);
			neighbors.put(parent.getNodeName(),parent);
		}
		return envelope.toString();
	}

	@Override
	public void atStart() {

		HashMap<String, DependenciesRepresenter> representers = null;
		try{
			representers = (HashMap<String, DependenciesRepresenter>) dispatchCenter.getDispatchData("LoaderModule", "DependenciesRepresenters");
		}
		catch(Exception e){
			representers = new HashMap<String, DependenciesRepresenter>();
			dispatchCenter.putDispatchData("LoaderModule", "DependenciesRepresenters", representers);
		}
		JSONArray dependenciesNames = new JSONArray(representers.keySet());		
		JSONObject envelope = new JSONObject();
		envelope.put("To", "Loader");
		envelope.put("Operation", "Init");
		JSONObject args = new JSONObject();
		args.put("DependenciesNames", dependenciesNames);
		envelope.put("Args", args);
		sender.pushStreamAndWaitForResponse(envelope);
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
